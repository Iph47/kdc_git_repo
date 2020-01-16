# -*- coding: utf-8 -*-

import __builtin__
import datetime
import sys
import time
import pickle

import requests

import koding
import xbmcaddon
import xbmcgui
import xbmcplugin
from ..plugin import Plugin
from language import get_string as _
from resources.lib.util.context import get_context_items
from resources.lib.util.url import get_addon_url, replace_url, xbmc
from resources.lib.util.xml import JenItem

__builtin__.BOB_BASE_DOMAIN = "178.32.217.111"
ADDON = xbmcaddon.Addon()
addon_name = xbmcaddon.Addon().getAddonInfo('name')


class bones(Plugin):
    name = "bones"

    def process_item(self, item_xml):
        item = JenItem(item_xml)
        enable_gifs = xbmcaddon.Addon().getSetting('enable_gifs') == "true"
        if item.item_string.startswith("<dir>"):
            title = item["name"]
            if title == "":
                title = item["title"]
            try:
                title = xbmcaddon.Addon().getLocalizedString(int(title))
            except ValueError:
                pass
            if item["link"] == "sport_acesoplisting":
                mode = "sport_acesoplisting"
                is_playable = False
                link = ""
            elif "sport_nhl_games" in item["link"]:
                game_date = item["link"].replace("sport_nhl_games(", "")[:-1]
                if "sport" in game_date:
                    game_date = ""
                mode = "sport_nhl_games"
                is_playable = False
                link = game_date + "a"
            elif "nhl_home_away(" in item["link"]:
                fargs = item["link"].replace("nhl_home_away(",
                                             "")[:-1].split(",")
                mode = "nhl_home_away"
                link = ",".join(fargs)
                is_playable = False
            elif item["link"].startswith("sport_hockeyrecaps"):
                page = item["link"].strip()[18:]
                if page == "":
                    page = "1a"
                mode = "get_hockey_recaps"
                is_playable = False
                link = page
            elif "sport_nfl_games" in item["link"]:
                fargs = item["link"].replace("sport_nfl_games(", "")[:-1]
                if "sport" in fargs:
                    fargs = ""
                else:
                    fargs = fargs.split(",")
                    if len(fargs) != 2:
                        fargs = ""
                mode = "sport_nfl_games"
                is_playable = False
                link = fargs
            elif "sport_nfl_get_game(" in item["link"]:
                farg = item["link"].replace("sport_nfl_get_game(", "")[:-1]
                mode = "get_nfl_game"
                link = farg
            elif "sport_condensed_nfl_games" in item["link"]:
                fargs = item["link"].replace("sport_condensed_nfl_games(",
                                             "")[:-1]
                if "sport" in fargs:
                    fargs = ""
                else:
                    fargs = fargs.split(",")
                    if len(fargs) != 2:
                        fargs = ""
                mode = "sport_condensed_nfl_games"
                is_playable = False
                link = fargs
            elif "sport_condensed_nfl_get_game(" in item["link"]:
                farg = item["link"].replace("sport_condensed_nfl_get_game(",
                                            "")[:-1]
                mode = "sport_condensed_nfl_get_game"
                is_playable = False
                link = farg

            # filter out "unreleased"
            if title == "" or " /title" in title or "/ title" in title:
                return

            context = get_context_items(item)

            content = item["content"]
            if content == "boxset":
                content = "set"
            if content != '':
                self.content = content
            imdb = item["imdb"]
            season = item["season"] or '0'
            episode = item["episode"] or '0'
            year = item["year"] or '0'
            fanart = None
            if enable_gifs:
                fan_url = item.get("animated_fanart", "")
                if fan_url and fan_url != "0":
                    fanart = replace_url(fan_url)
            if not fanart:
                fanart = replace_url(item.get("fanart", ""), replace_gif=False)
            thumbnail = None
            if enable_gifs:
                thumb_url = item.get("animated_thumbnail", "")
                if thumb_url and thumb_url != "0":
                    thumbnail = replace_url(thumb_url)
            if not thumbnail:
                thumbnail = replace_url(
                    item.get("thumbnail", ""), replace_gif=False)

            premiered = item.get("premiered", "")
            if premiered:
                try:
                    today_tt = datetime.date.today().timetuple()
                    premiered_tt = time.strptime(premiered, "%Y-%m-%d")
                    if today_tt < premiered_tt:
                        title = "[COLORyellow]" + title + "[/COLOR]"
                except Exception, e:
                    koding.dolog("wrong premiered format: " + repr(e))
                    pass
            try:
                result_item = {
                    'label': title,
                    'icon': thumbnail,
                    'fanart': fanart,
                    'mode': mode,
                    'url': link,
                    'folder': not is_playable,
                    'imdb': imdb,
                    'content': content,
                    'season': season,
                    'episode': episode,
                    'info': {},
                    'year': year,
                    'context': context,
                    "summary": item.get("summary", None)
                }
            except:
                return
            if fanart:
                result_item["properties"] = {'fanart_image': fanart}
                result_item['fanart_small'] = fanart

            if content in ['movie', 'episode']:
                # only add watched data for applicable items
                result_item['info']['watched'] = 0
            return result_item

    def get_xml(self, url):
        url = self.replace_url(url)
        xml = self.get_cached(url)
        return xml

    def get_xml_uncached(self, url):
        url = self.replace_url(url)
        xml = self.get_cached(url, cached=False)
        return xml

    def clear_cache(self):
        import xbmcgui
        dialog = xbmcgui.Dialog()
        if dialog.yesno(addon_name, _("Clear XML cache?")):
            koding.Remove_Table("xml_cache")

    def first_run_wizard(self):
        import xbmcgui
        addon = xbmcaddon.Addon()
        dialog = xbmcgui.Dialog()
        addon_name = xbmcaddon.Addon().getAddonInfo('name')
        addon.setSetting("first_run", "false")
        if not dialog.yesno(addon_name, _("Run Setup Wizard?")):
            return
        if dialog.yesno(
                addon_name,
                "choose movie metadata provider",
                nolabel=_("TMDB"),
                yeslabel=_("TRAKT")):
            addon.setSetting("movie_metadata_provider", "Trakt")
        else:
            addon.setSetting("movie_metadata_provider", "TMDB")

        if dialog.yesno(
                addon_name,
                _("choose tv metadata provider"),
                nolabel=_("TVDB"),
                yeslabel=_("TRAKT")):
            addon.setSetting("tv_metadata_provider", "Trakt")
        else:
            addon.setSetting("tv_metadata_provider", "TVDB")

        if dialog.yesno(
                addon_name,
                _("choose Selector type"),
                nolabel=_("HD/SD"),
                yeslabel=_("Link Selector")):
            addon.setSetting("use_link_dialog", "true")
        else:
            default_links = [_("BOTH"), _("HD"), _("SD")]
            selected = dialog.select(_("choose default link"), default_links)
            if selected != -1:
                addon.setSetting("default_link", default_links[selected])

        themes = [
            "DEFAULT", "CARS", "COLOURFUL", "KIDS", "MOVIES", "SPACE",
            "GIF LIFE", "GIF NATURE", "USER"
        ]
        selected = dialog.select(_("choose theme"), themes)
        if selected != -1:
            addon.setSetting("theme", themes[selected])

        if dialog.yesno(addon_name,
                        _("Enable GIF support?\n"),
                        _("May cause issues on lower end devices")):
            addon.setSetting("enable_gifs", "true")
        else:
            addon.setSetting("enable_gifs", "false")

        return True

    def get_theme_list(self):
        base_url = "http://www.norestrictions.club/norestrictions.club"
        base_theme_url = base_url + "/reloaded/themes/"
        theme_list = {
            'cars': [
                base_theme_url + "cars/cars1.jpg",
                base_theme_url + "cars/cars2.jpg",
                base_theme_url + "cars/cars3.jpg",
                base_theme_url + "cars/cars4.jpg",
                base_theme_url + "cars/cars5.jpg",
                base_theme_url + "cars/cars6.jpg",
                base_theme_url + "cars/cars7.jpg",
                base_theme_url + "cars/cars8.jpg",
                base_theme_url + "cars/cars9.jpg",
                base_theme_url + "cars/cars10.jpg",
            ],
            'colourful': [
                base_theme_url + "colourful/colourful1.jpg",
                base_theme_url + "colourful/colourful2.jpg",
                base_theme_url + "colourful/colourful3.jpg",
                base_theme_url + "colourful/colourful4.jpg",
                base_theme_url + "colourful/colourful5.jpg",
                base_theme_url + "colourful/colourful6.jpg",
                base_theme_url + "colourful/colourful7.jpg",
                base_theme_url + "colourful/colourful8.jpg",
            ],
            'kids': [
                base_theme_url + "kids/kids1.jpg",
                base_theme_url + "kids/kids2.jpg",
                base_theme_url + "kids/kids3.jpg",
                base_theme_url + "kids/kids4.jpg",
                base_theme_url + "kids/kids5.jpg",
                base_theme_url + "kids/kids6.jpg",
            ],
            'movies': [
                base_theme_url + "movies/movies1.jpg",
                base_theme_url + "movies/movies2.jpg",
                base_theme_url + "movies/movies3.jpg",
                base_theme_url + "movies/movies4.jpg",
                base_theme_url + "movies/movies5.jpg",
                base_theme_url + "movies/movies6.jpg",
                base_theme_url + "movies/movies7.jpg",
                base_theme_url + "movies/movies8.jpg",
                base_theme_url + "movies/movies9.jpg",
                base_theme_url + "movies/movies10.jpg",
                base_theme_url + "movies/movies11.jpg",
                base_theme_url + "movies/movies12.jpg",
            ],
            'space': [
                base_theme_url + "space/space1.jpg",
                base_theme_url + "space/space2.jpg",
                base_theme_url + "space/space3.jpg",
                base_theme_url + "space/space4.jpg",
                base_theme_url + "space/space5.jpg",
                base_theme_url + "space/space6.jpg",
                base_theme_url + "space/space7.jpg",
            ],
            'gif life': [
                base_theme_url + "giflife/city.gif",
                base_theme_url + "giflife/evUPmG6%20-%20Imgur.gif",
                base_theme_url + "giflife/night%20lights.gif",
                base_theme_url + "giflife/spinning%20wool.gif",
            ],
            'gif nature': [
                base_theme_url + "gifnature/falls.gif",
                base_theme_url + "gifnature/iceland.gif",
                base_theme_url + "gifnature/korea%20garden.gif",
                base_theme_url + "gifnature/sky%20waves.gif",
            ],
        }
        return theme_list

    def display_list(self, items, content_type):
        if content_type == "seasons":
            context_items = []
            if ADDON.getSetting("settings_context") == "true":
                context_items.append(
                    (_("Settings"),
                     "RunPlugin({0})".format(get_addon_url("Settings"))))
            url = []
            for item in items:
                url.append(item["url"])
            koding.Add_Dir(
                name=_("All Episodes"),
                url=pickle.dumps(url),
                mode="all_episodes",
                folder=True,
                icon=ADDON.getAddonInfo("icon"),
                fanart=ADDON.getAddonInfo("fanart"),
                context_items=context_items,
                content_type="video")

        for item in items:
            context_items = []
            if ADDON.getSetting("settings_context") == "true":
                context_items.append(
                    (_("Settings"),
                     "RunPlugin({0})".format(get_addon_url("Settings"))))
            context_items.extend(item["context"])
            koding.Add_Dir(
                name=item["label"],
                url=item["url"],
                mode=item["mode"],
                folder=item["folder"],
                icon=item["icon"],
                fanart=item["fanart"],
                context_items=context_items,
                content_type="video",
                info_labels=item["info"],
                set_property=item.get("properties", {}),
                set_art={"poster": item["icon"]})
        xbmcplugin.setContent(int(sys.argv[1]), content_type)
        return True

    def replace_url(self, url):
        if 'norestrictions.noobsandnerds.com' in url and 'norestrictions.club/norestrictions.club' not in url:
            url = url.replace('norestrictions.noobsandnerds.com',
                              __builtin__.BOB_BASE_DOMAIN)
        elif 'www.norestrictions.club' in url and 'www.norestrictions.club/norestrictions.club' not in url and 'norestrictions.club/norestrictions.club' not in url:
            url = url.replace('www.norestrictions.club',
                              __builtin__.BOB_BASE_DOMAIN)
        elif 'www.norestrictions.club/norestrictions.club' in url:
            url = url.replace('www.norestrictions.club/norestrictions.club',
                              __builtin__.BOB_BASE_DOMAIN)
        elif 'norestrictions.club' in url and 'norestrictions.club/norestrictions.club' not in url:
            url = url.replace('norestrictions.club',
                              __builtin__.BOB_BASE_DOMAIN)
        elif 'norestrictions.club/norestrictions.club' in url:
            url = url.replace('norestrictions.club/norestrictions.club',
                              __builtin__.BOB_BASE_DOMAIN)
        return url

    def get_link_message(self, *args):
        messages = [
            {
                'HD': 'Hensley',
                'SD': 'Guerrero'
            },
            {
                'HD': 'Land',
                'SD': 'Slam'
            },
            {
                'HD': 'RAD',
                'SD': 'Sketchy'
            },
            {
                'HD': 'Great! Worth the wait',
                'SD': 'Good Enough. I just want to watch'
            },
            {
                'HD': 'BluRay Quality',
                'SD': 'VHS Quality'
            },
            {
                'HD': 'Voddy ',
                'SD': 'Budweiser'
            },
            {
                'HD': 'I must see this film in the highest quality',
                'SD': 'Flick probably sucks so lets just get it over'
            },
            {
                'HD': 'Looks like a Maserati',
                'SD': ' Looks like a Ford Focus'
            },
            {
                'HD': 'Supermodel Quality',
                'SD': ' Looks like Grandma Thelma'

            },
        ]

        if xbmcaddon.Addon().getSetting('enable_offensive') == 'true':
            messages.extend([
                {
                    'HD': 'Kicks Ass!!',
                    'SD': 'Gets ass kicked repeatedly'
                },
                {
                    'HD': 'Fucking Rocks!!',
                    'SD': 'Fucking Wanker!!'
                },
            ])
        return messages

    def get_searching_message(self, preset):
        messages = [
            'Yapple Dapple',
			'They dont call him commander fun for nothing',
			'Welcome to the Blue Tile Lounge',
			'We just went to Wallows',
			'Turn off the camera',
			'Thats a pump Sir',
			'Maps to the skaters homes',
			'Animal Chin Have you seen him',
			'Ever do a tail drop guys',
			'Weak ollies are a worldwide problem',
            'This is a high ollie zone',
            'Where is Rodney',
            'He cracked his head on a frontside',
            'One more trick and then we re outta here',
            'Matt Who Matt Who Matt Hensley have you seen him',
            'Its like you re not skating anymore you re just flying around',
            'Skaters Only',
            'And comb your hair',
            'Dont fall through the tunnel in the ramp What Never mind',
            'Pink Motel where skaters check in and then pass out',
            'We are eating when Im skating I put my skate shows on',
            'Look for the ramp between two junkyards',
            'McTwist and shout',
            'Welcome to the Blue Tile Lounge',
            'Skate and Create',
            'Skate and Destroy',
            'Skateboarding Is Not a Crime',
			'Put your nose rail up in the air',
            'You re doin the skateboard shuffle',
            'Livi locals',
            'Mick at Quarterback',
			'Mick at MBC',
			'So who wants to go to Andys',
            'No way he got his own milk carton',
            'Yeah Matt',
            'Do a Bunsen over the Junsen',
            'I especially like the flip of the board!',
            'im eighteen, hes eighteen, everybodys eighteen',
            'The teams not that hot either',
            'Sal Barbier, swamp rat, super good',
            'I dont understand the vibes about skating rocks',
            'Dont look back you re not going that way',
            'Dont take life too seriously',
            'You really got to stop pushing mongo',
            'Then she asked me if I love skateboarding more than HER pmsl',
            'I wont quit skating until I am physically unable',
            'You dont quit skating because you get old You get old because you quit skating',
        ]

        if xbmcaddon.Addon().getSetting('enable_offensive') == "true":
            messages.extend([
                'Go Fuck Yourself',
                'Fucking street league',
                'Fuck YES',
                'Ya Fucking Numpty',
				'FUCK KODI THE COMMUNITY IT SUX',
				'FUCK, SHIT, PRICK, WANK',
				'You CHEAP Skate, GO to the Cinema',
            ])

        if preset == "search":
            messages.extend(['bones is popping in Blu Ray Disc'])
        elif preset == "searchsd":
            messages.extend([
                'bones rummaging through her vhs collection',
            ])

        return messages

    def get_cached(self, url, cached=True):
        if not url.startswith("http"):
            return
        if __builtin__.BOB_BASE_DOMAIN not in url and "norestrictions" not in url:
            return requests.get(url).content
        xml_cache_spec = {
            "columns": {
                "url": "TEXT",
                "xml": "TEXT",
                "cache_time": "TEXT",
                "created": "TEXT"
            },
            "constraints": {
                "unique": "url"
            }
        }
        koding.Create_Table("xml_cache", xml_cache_spec)
        if not cached:
            koding.dolog("uncached requested")
            response = requests.get(url, verify=False)
            xml = response.content
            response.close()
        else:
            match = koding.Get_From_Table("xml_cache", {"url": url})
            if match:
                koding.dolog("match: " + repr(match))
                match = match[0]
                created_time = float(match["created"])
                cache_time = int(match["cache_time"])
                koding.dolog("expire time: " + repr(created_time + cache_time))
                koding.dolog("created_time: " + repr(created_time))
                koding.dolog("now: " + repr(time.mktime(time.gmtime())))
                if time.mktime(time.gmtime()) <= created_time + cache_time:
                    koding.dolog("loading from cache, cache time not reached")
                    return pickle.loads(match["xml"])
                else:
                    try:
                        response = requests.get(url, verify=False, timeout=10)
                        changed = response.headers["Last-Modified"]
                        changed_struct = time.strptime(
                            changed, "%a, %d %b %Y %H:%M:%S GMT")
                        epoch_changed = int(time.mktime(changed_struct))
                        if epoch_changed < created_time:
                            koding.dolog(
                                "loading from cache, list not changed")
                            #xml = pickle.loads(match["xml"])
                            xml = response.content
                            response.close()
                        else:
                            koding.dolog("refreshing content")
                            xml = response.content
                            response.close()
                    except Exception as e:
                        koding.dolog("cache error: " + repr(e))
                        return pickle.loads(match["xml"])
            else:
                koding.dolog("initial load")
                response = requests.get(url, verify=False)
                xml = response.content
                response.close()
        if not xml:
            xbmcgui.Dialog().notification(
                ADDON.getAddonInfo("name"),
                "Server under high load, try again")
            return ""
        info = JenItem(xml.split('<item>')[0].split('<dir>')[0])
        cache_time = int(info.get("cache", 21600))
        koding.dolog("cache_time: " + repr(cache_time))
        created_time = time.mktime(time.gmtime())
        try:
            koding.Remove_From_Table("xml_cache", {
                "url": url,
            })
        except Exception, e:
            koding.dolog("Database error: " + repr(e))
        koding.Add_To_Table("xml_cache", {
            "url": url,
            "xml": pickle.dumps(xml).replace("\"", "'"),
            "cache_time": cache_time,
            "created": created_time
        })
        return xml
