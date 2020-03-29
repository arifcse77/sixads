from django.db import models


class Tag(models.Model):
    tag_name = models.CharField(unique=True, max_length=255)


class Channel(models.Model):
    youtube_channel_id = models.CharField(unique=True, max_length=255)
    channel_title = models.CharField(max_length=255)


class Video(models.Model):
    youtube_video_id = models.CharField(max_length=200, unique=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    published_at = models.DateTimeField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    favorite_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)


class VideoTag(models.Model):
    class Meta:
        unique_together = (('video', 'tag'),)

    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class Stats(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    comment_count = models.IntegerField()
    like_count = models.IntegerField()
    dislike_count = models.IntegerField()
    favorite_count = models.IntegerField()
    view_count = models.IntegerField()
    track_time = models.DateTimeField()
