import requests
from django.http import JsonResponse
from .service import Service

youtube_api_v3 = "https://www.googleapis.com/youtube/v3/"
api_key = "AIzaSyAcuYO6-UOTS5QN-c1HO6xhcecwKO_1bSM" # TODO api key will be in outside of git file.
channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"

service = Service(youtube_api_v3=youtube_api_v3, api_key=api_key, channel_id=channel_id)


def index(request):
    # We can add this endpoint at crontab with 10 mins interval for track video stats
    service.youtube_video_process()
    return JsonResponse({"message": "Youtube API processing is successfully completed"})


# TODO API method can be using django rest framework
def api(request):
    tag_name = request.GET.get("tag_name") # TODO Processing parameters can be using django forms
    video_performance = request.GET.get("video_performance") # TODO Processing parameters can be using django forms
    videos = service.video_report(tag_name=tag_name, video_performance=video_performance)
    return JsonResponse({"videos": videos})


def channels(request):
    channel_list = {}
    api_url = "{youtube_api_v3}channels?part=snippet,contentDetails,statistics&forUsername=jambrose42&key={api_key}".format(youtube_api_v3=youtube_api_v3, api_key=api_key)
    channel_list_response = requests.get(api_url, timeout=60)
    if channel_list_response.status_code == 200:
        channel_list = channel_list_response.json()

    return JsonResponse(channel_list)
