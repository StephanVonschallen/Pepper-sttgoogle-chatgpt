import time
import os

import urllib2
import json


'''
Visit https://developers.google.com/oauthplayground and generate a Access Token, which is valid of 1h
Give
'''

def wait_until_new_response(form_id, access_token):
    handler = urllib2.HTTPHandler()
    opener = urllib2.build_opener(handler)

    url = "https://forms.googleapis.com/v1/forms/%s/responses" % form_id
    print(url)
    request = urllib2.Request(url)
    request.get_method = lambda: "GET"
    request.add_header("Content-Type", 'application/json')
    request.add_header("Authorization", "Bearer %s" % access_token)

    response = opener.open(request)
    current_form_responses = json.loads(response.read())

    while True:
        time.sleep(1)
        print("waiting")
        response = opener.open(request)
        new_form_responses = json.loads(response.read())
        if len(current_form_responses["responses"]) < len(new_form_responses["responses"]):
            print("new response")
            return current_form_responses["responses"][-1]

def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    new_response = wait_until_new_response("1tuRmxHBZAVR8Mcg0Mk71MXjhSW_kEX9peNo4hfQfJCI", api_key)
    print(new_response)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
