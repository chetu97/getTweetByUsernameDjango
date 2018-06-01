# from django.shortcuts import render
# import tweepy
from django.views.decorators.csrf import csrf_exempt
from pprint import pprint
from django.http.response import HttpResponse
import twitter
import json
from firebase import firebase
import datetime


@csrf_exempt
def index(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        username = received_json_data['username']
        username = '@' + username
        consumer_key = 'uJy8yd1jHRKWNJEY7JHU5CY6b'
        consumer_secret = '5s2ByeTyzdEBOICcMFogmujA4uJWZU9vaNlKV2O8hR36JEoR6t'
        access_token = '2904942878-8m8c0nAMA3f4z9jUnimq8DOv0Wx0ENeCeJ6CCkY'
        access_token_secret = 'fbFkinImXZoHtkVvXE50SpciyWuhQurH2qFIttgPpvoAU'
        api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token,
                          access_token_secret=access_token_secret)
        # print(api.VerifyCredentials())
        statuses = api.GetUserTimeline(screen_name=username, count=1)
        # pprint(statuses)
        # pprint([s.Text for s in statuses])
        # pprint([s.Text for s in statuses])
        var = ([s.text for s in statuses])
        response_data = {}
        if var != "":
            var = list(var)
            var = var.pop(0)
            var = str(var)
            firebase1 = firebase.FirebaseApplication('https://simpletwitterapp.firebaseio.com/', None)
            now = datetime.datetime.now()
            result = firebase1.post('/', {"tweet": var, "date": now.strftime("%Y-%m-%d %H:%M"), "username": username})
            if result != None:
                response_data['success'] = '1'
                response_data['data'] = var
                response_data['extra_comment'] = 'Tweet Stored'
            else:
                response_data['success'] = '0'
                response_data['extra_comment'] = 'Error'
        else:
            response_data['success'] = '0'
            response_data['extra_comment'] = 'Error'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
