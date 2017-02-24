#!/usr/local/bin/python

import json
import requests
import os
import pastel
from requests.exceptions import ConnectionError

# --- Alter the variables below to fit your needs

# your Hubspot API key
api_key                   = ""
# The numberic ID of the blog
blog_id                   = ""
# If you want/need to pass any additional HubSpot blog post API params
api_params                = "&state=PUBLISHED&limit=500&content_group_id="
# Switch to true if you want a local copy of the downloaded post JSON
# before it is updated
save_local                = False
# These should be obvious. The code will look for the EXACT string
string_to_replace         = ""
replacement_string        = ""
# --- Should not have to make any changes beyond this point

hubspot_blog_api_base_url = "https://api.hubapi.com/content/api/v2/blog-posts?hapikey="
counter                   = 0

# Pick up all the blog posts from the API
api_response = requests.get(hubspot_blog_api_base_url + api_key + api_params + blog_id)
blog_data = api_response.json()

class bcolors:
    HEADER    = '\033[95m'
    BLUE      = '\033[94m'
    GRAY      = '\033[1;30m'
    GREEN     = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'

def update_post(payload, post_id):
    put_url = "https://api.hubapi.com/content/api/v2/blog-posts/" + \
        post_id + "?hapikey=" + api_key
    print bcolors.WARNING + "Payload Details:\n" + bcolors.GRAY + "Length: " + str(len(payload))
    print "URL: " + put_url + "\nContent: " + payload + bcolors.ENDC
    hold_the_door = raw_input(
        bcolors.WARNING + "\nMake the change (enter to continue or ctrl-d to abort)?" + bcolors.ENDC)
    put_request = requests.put(put_url, data=payload)
    if put_request.status_code != 200:
        print bcolors.FAIL + "POST Status code: " + str(put_request.status_code) + bcolors.ENDC
        print bcolors.FAIL + "POST response content: " + put_request.content + bcolors.ENDC
    return;

def save_post(payload):
    '''
    The untouched downloaded JSON content will be saved into a file with post_id as its name.
    This file will be placed in a folder called "originals". The folder will be created if it
    does not exist.
    '''
    if not os.path.exists('originals'):
        os.makedirs('originals')
    with open('originals/' + str(payload['analytics_page_id']) + '.json', 'w') as outfile:
        json.dump(payload, outfile)
    return;

try:
    api_response = requests.get(hubspot_blog_api_base_url + api_key + api_params + blog_id)
    blog_data = api_response.json()
    for post in blog_data['objects']:
        counter += 1
        print bcolors.HEADER + "Picking up post " + str(counter) + " of a total of " + str(len(blog_data['objects'])) + " with id " + post['analytics_page_id'] + bcolors.ENDC
        print bcolors.HEADER + "Post title: " + post['html_title'] + bcolors.ENDC
        print bcolors.HEADER + "Post URL: " + post['url'] + bcolors.ENDC
        for key in post.items():
            if (key[0] != "published_url" and key[0] != "url" and key[0] != "slug"):
                if type(key[1]) == unicode and string_to_replace in key[1]:
                    corrected_data = {}
                    print bcolors.BOLD + "\nFound string in item: " + key[0] + bcolors.ENDC
                    json_to_string = str(key[1].encode('utf-8', 'replace'))
                    json_to_string = json_to_string.replace(string_to_replace, replacement_string)
                    corrected_data[key[0]] = json_to_string
                    print bcolors.BLUE + "Original content:\n" + key[1] + bcolors.ENDC
                    print bcolors.GREEN + "Updated content:\n" + json_to_string + bcolors.ENDC
                    if save_local is True:
                        save_post(post)
                    update_post(json.dumps(corrected_data), post['analytics_page_id'])

        if 'corrected_data' not in locals():
            print bcolors.FAIL + "\nFound nothing to update in this post...\n" + bcolors.ENDC

        proceed = raw_input(
            bcolors.WARNING + "\nContinue to the next post (enter to continue or ctrl-d to abort)?" + bcolors.ENDC)
        os.system('clear')
except requests.exceptions.RequestException as e:
    print (pastel.colorize('<fg=yellow;bg=red;options=bold>Connection error while making API call to HubSpot! ' + e + ' Aborted.</>\n'))
    sys.exit(1)
