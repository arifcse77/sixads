from django.http import JsonResponse

from .service import Service

youtube_api_v3 = "https://www.googleapis.com/youtube/v3/"
api_key = "AIzaSyAcuYO6-UOTS5QN-c1HO6xhcecwKO_1bSM" # TODO api key will be in outside of git file.
channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"

service = Service(youtube_api_v3=youtube_api_v3, api_key=api_key, channel_id=channel_id)


def index(request):
    service.youtube_video_process()
    return JsonResponse({"message": "Youtube API processing is successfully completed"})

