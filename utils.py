#!/usr/bin/python3
import os
import re
import json
import requests
import database
import constants
from pathlib import Path
from urllib.parse import urlparse, parse_qs, urlencode

def execute_os(file_name, movie_path):
    os.system("/bin/rm -f /var/media/Video/Movies/Random_Movie/*")
    os.symlink(movie_path, "/var/media/Video/Movies/Random_Movie/" + file_name, target_is_directory=False)

def reset():
    os.system("/usr/sbin/minidlnad -r")

def fix_name(name):
    dname = re.sub("\.[^.]*$", "", name)
    sname = re.sub("[^0-9a-zA-Z]+", " ", dname)
    return sname

def pictures(movie_name):
    info = {}
    host = constants.google_host
    url = constants.google_url
    cache = parse_qs(urlparse(url).query)
    cache["q"] = movie_name
    cache["key"] = constants.google_key
    cache["cx"] = constants.google_context
    try:
        request = urlencode(cache)
        r = requests.get(host + request)
        images = json.loads(r.text)
        info["image_link"] = images["items"][0]["pagemap"]["cse_thumbnail"][0]["src"]
        info["snippet"] = images["items"][0]["snippet"]
        info["name"] = movie_name
    except KeyError:
        info["image_link"] = constants.broken
        info["snippet"] = constants.broken_text
        info["name"] = movie_name
    return info

def get_movie():
    movie_path = database.finder()
    file_name = Path(movie_path).name
    execute_os(file_name, movie_path)
    name = fix_name(file_name)
    info = pictures(name)
    info["link"] = "/static/Movie/" + file_name
    info["type"] = file_name[-3:]
    print(info["link"])
    reset()
    return info