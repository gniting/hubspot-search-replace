Global search and replace for HubSpot blog posts
------------------------------------------------

HubSpot does not provide for a global search and replace for its blog so it becomes a real pain
if you need to make mass updates.

This simple python script attempts to fix the lack of a global search/replace by doing the following:

0. for given blog id, get a list of all posts
0. pull down the components of each post
0. do the search/replace across all relevant components (title, url, body, rss body, etc.)
0. push updated components back to HubSpot through their API

Fair Warning(s):

0. This is not elegant code by any means. I needed something quick and I am not a
developer. Any recommendations to make this more efficient are welcome!
0. This script was built and tested on MacOS. If you're using another system, your
mileage may vary.

Usage
-----
0. Make sure Python 2.7.x is installed on your system.
0. Open up the file and change the following variables:
   - `api_key`
   - `blog_id`
   - `string_to_replace`
   - `replacement_string`
0. Run the script in a terminal that supports colors and utf-8 characters

Dependencies
------------
1. Requires that the Python `requests` package is installed
