# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2018 RACC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import unicode_literals, absolute_import

import sys
from xbmcgui import ListItem
from kodi_six import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from routing import Plugin

import os
import io
import time
import json
import requests
import datetime
from datetime import timedelta
from itertools import chain
from base64 import b64decode
from future.moves.urllib.parse import urlencode

from resources.lib.rbtv_config_backendless import rbtvConfig
from resources.lib.rbtv_channels import rbtvChannels


addon = xbmcaddon.Addon()
plugin = Plugin()
s = requests.Session()
plugin.name = addon.getAddonInfo("name")
user_agent = "Dalvik/2.1.0 (Linux; U; Android 5.1.1; AFTT Build/LVY48F)"
USER_DATA_DIR = xbmc.translatePath(addon.getAddonInfo("profile"))
if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)
implemented = ["0", "38", "21", "48"]

app_config_file = os.path.join(USER_DATA_DIR, "config32.json")
channel_list_file = os.path.join(USER_DATA_DIR, "channels32.json")

data_time = int(addon.getSetting("data_time32") or "0")
cache_time = int(addon.getSetting("cache_time") or "0")
user_id = addon.getSetting("user_id32")


current_time = int(time.time())
if current_time - data_time > cache_time * 60 * 60:
    try:
        new_config = rbtvConfig()
        app_config = new_config.get_data()
        with io.open(app_config_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(app_config, indent=2, sort_keys=True, ensure_ascii=False))
    except:
        with io.open(app_config_file, "r", encoding="utf-8") as f:
            app_config = json.loads(f.read())
    try:
        new_channels = rbtvChannels(app_config, user_id)
        channel_list = new_channels.get_channel_list()
        addon.setSetting("user_id32", new_channels.user)
        with io.open(channel_list_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(channel_list, indent=2, sort_keys=True, ensure_ascii=False))
    except:
        with io.open(channel_list_file, "r", encoding="utf-8") as f:
            channel_list = json.loads(f.read())

    addon.setSetting("data_time32", str(int(time.time())))
else:
    try:
        with io.open(app_config_file, "r", encoding="utf-8") as f:
            app_config = json.loads(f.read())
    except IOError:
        app_config = ""
    try:
        with io.open(channel_list_file, "r", encoding="utf-8") as f:
            channel_list = json.loads(f.read())
    except IOError:
        channel_list = ""


def fix_auth_date(auth):
    now = datetime.datetime.utcnow()
    _in = list(auth)
    _in.pop(len(_in) + 2 - 3 - int(str(now.year)[:2]))
    _in.pop(len(_in) + 3 - 4 - int(str(now.year)[2:]))
    # java January = 0
    _in.pop(len(_in) + 4 - 5 - (now.month - 1 + 1 + 10))
    _in.pop(len(_in) + 5 - 6 - now.day)
    return "".join(_in)


def get_auth_token_38():
    wms_url = b64decode(app_config.get("YmVsZ2lfMzgw")[1:])
    auth = b64decode(app_config.get("Z2Vsb29mc2JyaWVm")[1:])
    mod_value = int(b64decode(app_config.get("TW9vbl9oaWsx")[1:]))
    modified = lambda value: "".join(chain(*zip(str(int(time.time()) ^ value), "0123456789")))
    fix_auth = lambda auth: "".join([auth[:-59], auth[-58:-52], auth[-51:-43], auth[-42:-34], auth[-33:]])
    req = requests.Request(
        "GET",
        wms_url,
        headers={
            "User-Agent": user_agent,
            "Accept-Encoding": "gzip",
            "Modified": modified(mod_value),
            "Authorization": auth,
        },
    )
    prq = req.prepare()
    r = s.send(prq)
    return fix_auth(r.text)


def get_auth_token_21():
    wms_url = b64decode(app_config.get("Y2FsYWFtb19pa3Mw")[1:])
    auth = b64decode(app_config.get("WXJfd3lmX3luX2JhaXMw")[1:])
    mod_value = int(b64decode(app_config.get("TW9vbl9oaWsx")[1:]))
    modified = lambda value: "".join(chain(*zip(str(int(time.time()) ^ value), "0123456789")))
    req = requests.Request(
        "GET",
        wms_url,
        headers={
            "User-Agent": user_agent,
            "Accept-Encoding": "gzip",
            "Modified": modified(mod_value),
            "Authorization": auth,
        },
    )
    prq = req.prepare()
    r = s.send(prq)
    return r.text


def get_auth_token_48():
    wms_url = b64decode(app_config.get("Ym9ya3lsd3VyXzQ4")[1:])
    auth = b64decode(app_config.get("dGVydHRleWFj")[1:])
    mod_value = int(b64decode(app_config.get("TW9vbl9oaWsx")[1:]))
    modified = lambda value: "".join(chain(*zip(str(int(time.time()) ^ value), "0123456789")))
    req = requests.Request(
        "GET",
        wms_url,
        headers={
            "User-Agent": user_agent,
            "Accept-Encoding": "gzip",
            "Modified": modified(mod_value),
            "Authorization": auth,
        },
    )
    prq = req.prepare()
    r = s.send(prq)
    return fix_auth_date(r.text)


@plugin.route("/")
def root():
    categories = channel_list.get("categories_list")
    list_items = []
    for c in categories:
        li = ListItem(c.get("cat_name"))
        url = plugin.url_for(list_channels, cat=c.get("cat_id"))
        list_items.append((url, li, True))

    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_FULLPATH)
    xbmcplugin.addDirectoryItems(plugin.handle, list_items)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route("/list_channels/<cat>")
def list_channels(cat=None):
    list_items = []
    for channel in channel_list.get("eY2hhbm5lbHNfbGlzdA=="):
        if channel.get("cat_id") == cat:
            if (
                len(
                    [
                        stream
                        for stream in channel.get("Qc3RyZWFtX2xpc3Q=")
                        if b64decode(stream.get("AdG9rZW4=")[:-1]) in implemented
                    ]
                )
                == 0
            ):
                continue

            title = b64decode(channel.get("ZY19uYW1l")[:-1])
            icon = b64decode(channel.get("abG9nb191cmw=")[1:])
            image = "{0}|{1}".format(icon, urlencode({"User-Agent": user_agent}))
            c_id = channel.get("rY19pZA==")

            li = ListItem(title)
            li.setProperty("IsPlayable", "true")
            li.setInfo(type="Video", infoLabels={"Title": title, "mediatype": "video"})
            li.setArt({"thumb": image, "icon": image})
            try:
                li.setContentLookup(False)
            except AttributeError:
                pass
            url = plugin.url_for(play, c_id=c_id)
            list_items.append((url, li, False))

    xbmcplugin.addDirectoryItems(plugin.handle, list_items)
    xbmcplugin.setContent(plugin.handle, "videos")
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route("/play/<c_id>/play.pvr")
def play(c_id):
    for channel in channel_list.get("eY2hhbm5lbHNfbGlzdA=="):
        if channel.get("rY19pZA==") == c_id:
            selected_channel = channel
            break

    # stream_list = selected_channel.get("Qc3RyZWFtX2xpc3Q=")
    stream_list = [
        stream
        for stream in selected_channel.get("Qc3RyZWFtX2xpc3Q=")
        if b64decode(stream.get("AdG9rZW4=")[:-1]) in implemented
    ]
    if len(stream_list) > 1:
        select_list = []
        for stream in stream_list:
            select_list.append(b64decode(stream.get("Bc3RyZWFtX3VybA==")[1:]))

        dialog = xbmcgui.Dialog()
        ret = dialog.select("Choose Stream", select_list)
        selected_stream = stream_list[ret]
    else:
        selected_stream = stream_list[0]

    if "AdG9rZW4=" in selected_stream:
        if b64decode(selected_stream.get("AdG9rZW4=")[:-1]) == "38":
            media_url = b64decode(selected_stream.get("Bc3RyZWFtX3VybA==")[1:]) + get_auth_token_38()
        elif b64decode(selected_stream.get("AdG9rZW4=")[:-1]) == "21":
            media_url = b64decode(selected_stream.get("Bc3RyZWFtX3VybA==")[1:]) + get_auth_token_21()
        elif b64decode(selected_stream.get("AdG9rZW4=")[:-1]) == "48":
            media_url = b64decode(selected_stream.get("Bc3RyZWFtX3VybA==")[1:]) + get_auth_token_48()
        elif b64decode(selected_stream.get("AdG9rZW4=")[:-1]) == "0":
            media_url = b64decode(selected_stream.get("Bc3RyZWFtX3VybA==")[1:])
    else:
        media_url = b64decode(selected_stream.get("Bc3RyZWFtX3VybA==")[1:])

    media_headers = {"User-Agent": user_agent}

    title = b64decode(selected_channel.get("ZY19uYW1l")[:-1])
    icon = b64decode(selected_channel.get("abG9nb191cmw=")[1:])
    image = "{0}|{1}".format(icon, urlencode({"User-Agent": user_agent}))

    if "playlist.m3u8" in media_url:
        if addon.getSetting("inputstream") == "true":
            li = ListItem(title, path=media_url)
            li.setArt({"thumb": image, "icon": image})
            li.setMimeType("application/vnd.apple.mpegurl")
            li.setProperty("inputstreamaddon", "inputstream.adaptive")
            li.setProperty("inputstream.adaptive.manifest_type", "hls")
            li.setProperty("inputstream.adaptive.stream_headers", urlencode(media_headers))
        else:
            li = ListItem(title, path="{0}|{1}".format(media_url, urlencode(media_headers)))
            li.setArt({"thumb": image, "icon": image})
            li.setMimeType("application/vnd.apple.mpegurl")
    else:
        li = ListItem(title, path="{0}|{1}".format(media_url, urlencode(media_headers)))
        li.setArt({"thumb": image, "icon": image})
    try:
        li.setContentLookup(False)
    except AttributeError:
        pass

    xbmcplugin.setResolvedUrl(plugin.handle, True, li)


if __name__ == "__main__":
    plugin.run(sys.argv)
