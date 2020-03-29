from datetime import datetime

import requests

from .models import (Channel, Video, Stats, VideoTag, Tag)

now = datetime.now()


class Service:

    def __init__(self, youtube_api_v3=None, api_key=None, channel_id=None):
        self.youtube_api_v3 = youtube_api_v3
        self.api_key = api_key
        self.channel_id = channel_id

    def youtube_video_process(self):
        channel_video_list = self.get_channel_video_list()
        if channel_video_list.status_code == 200:
            channel_video_list_json = channel_video_list.json()
            channel = self.save_channel_data(channel_video_list_json)
            video_id_list = self.save_video_data(channel_video_list_json, channel)

            for video_id in video_id_list:
                video_details = self.video_details(video_id)
                if video_details.status_code == 200:
                    video_details_json = video_details.json()
                    self.update_video_stats(video_details_json, video_id)

    def get_channel_video_list(self):
        channel_video_list_api = "{youtube_api_v3}search?key={api_key}&channelId={channel_id}&part=snippet,id&order=date&maxResults=20".format(
            youtube_api_v3=self.youtube_api_v3,
            api_key=self.api_key,
            channel_id=self.channel_id
        )
        channel_video_list = requests.get(channel_video_list_api, timeout=60)
        return channel_video_list

    def save_channel_data(self, channel_video_list_json):
        data = channel_video_list_json.get("items")[0]
        channel_title = data.get("snippet").get("channelTitle")

        channel = Channel.objects.filter(youtube_channel_id=self.channel_id).first()
        if not channel:
            channel = Channel(youtube_channel_id=self.channel_id, channel_title=channel_title)
            channel.save()

        return channel

    @staticmethod
    def save_video_data(channel_video_list_json, channel):
        video_list = []
        video_id_list = []
        for data in channel_video_list_json.get("items"):
            youtube_video_id = data.get("id").get("videoId")
            title = data.get("snippet").get("title")
            published_at = data.get("snippet").get("publishedAt")

            video_exists = Video.objects.filter(youtube_video_id=youtube_video_id).exists()
            if not video_exists:
                video = Video(youtube_video_id=youtube_video_id, title=title, published_at=published_at,
                              channel=channel)
                video_list.append(video)

            video_id_list.append(youtube_video_id)

        if video_list:
            Video.objects.bulk_create(video_list)

        return video_id_list

    def video_details(self, video_id):
        video_details_api = "{youtube_api_v3}videos?id={video_id}&key={api_key}&part=snippet,contentDetails,statistics,status".format(
            youtube_api_v3=self.youtube_api_v3,
            video_id=video_id,
            api_key=self.api_key
        )
        video_details = requests.get(video_details_api, timeout=60)
        return video_details

    def update_video_stats(self, video_details_json, video_id):
        item = video_details_json.get("items")[0]
        tags = item.get("snippet").get("tags")
        view_count = item.get("statistics").get("viewCount")
        like_count = item.get("statistics").get("likeCount")
        dislike_count = item.get("statistics").get("dislikeCount")
        favorite_count = item.get("statistics").get("favoriteCount")
        comment_count = item.get("statistics").get("commentCount")

        video = Video.objects.filter(youtube_video_id=video_id).first()
        if video:
            video.view_count = view_count
            video.like_count = like_count
            video.dislike_count = dislike_count
            video.favorite_count = favorite_count
            video.comment_count = comment_count
            video.save()

            stats_exists = Stats.objects.filter(video=video, view_count=view_count, like_count=like_count,
                                                dislike_count=dislike_count, favorite_count=favorite_count,
                                                comment_count=comment_count).first()
            if not stats_exists:
                stats = Stats(video=video, view_count=view_count, like_count=like_count,
                              dislike_count=dislike_count, favorite_count=favorite_count,
                              comment_count=comment_count,
                              track_time=now)
                stats.save()

            self.save_tag(tags, video)

    @staticmethod
    def save_tag(tags, video):
        for tag_name in tags:
            tag = Tag.objects.filter(tag_name=tag_name).first()
            if not tag:
                tag = Tag(tag_name=tag_name)
                tag.save()

            video_tag_exists = VideoTag.objects.filter(video=video, tag=tag).exists()
            if not video_tag_exists:
                video_tag = VideoTag(video=video, tag=tag)
                video_tag.save()
