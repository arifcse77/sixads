# How to Run Project
* Clone repository
* Install mysql server
* Install mysql client
* Install requirements.txt
* Make migration
* Run server

# Feature
* Scrapes channel videos with tags and stats and save video stats data (Task-1 and Task-2)
    * Endpoint = http://localhost:8000/youtube/
    * You can add this endpoint at crontab with 10 mins interval
    * if video stats is changed from API then we are updating stats data at database

# Tutorial Reference
* https://developers.google.com/youtube/v3/getting-started
* https://www.googleapis.com/youtube/v3/search?key=AIzaSyAcuYO6-UOTS5QN-c1HO6xhcecwKO_1bSM&channelId=UC_x5XG1OV2P6uZZ5FSM9Ttw&part=snippet,id&order=date&maxResults=20
* https://pypi.org/project/python-youtube/
* https://stackoverflow.com/questions/18953499/youtube-api-to-fetch-all-videos-on-a-channel
