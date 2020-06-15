# -*- coding: UTF-8 -*-

"""
    Infinity Add-on (C) 2019
    Credits to Lastship, Placenta and Covenant; our thanks go to their creators

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Addon Name: Infinity
# Addon id: plugin.video.infinity
# Addon Provider: Infinity

import base64
import requests
import json

from resources.lib.modules import source_utils
from resources.lib.modules import cache


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['']
        self.base_link = base64.b64decode('aHR0cHM6Ly92amFja3Nvbi5pbmZvLw==')
        self.search_link = '/movie-search?key=%s'
        self.get_link = '/movie/getlink/%s/%s'
        self.session = requests.Session()
        self.vavoo_auth = self._auth()

    def _auth(self):
        vavoo_auth_token = self.session.post("https://www.vavoo.tv/api/box/guest",
                                     data={'reason': 'check/missing'})

        token = vavoo_auth_token.json()['response']['token']

        data = {'service_version': '1.2.26', 'reason': 'check', 'meta_system': 'Windows', 'platform': 'win32',
                'token': token, 'version': '2.2', 'branch': 'addonv22', 'apk_package': 'unknown',
                'meta_version': '6.1.7601', 'meta_platform': 'Windows-7-6.1.7601-SP1', 'recovery_version': '1.1.7',
                'processor': 'Intel64 Family 6 Model 42 Stepping 7, GenuineIntel'}

        vavoo_auth = self.session.post("https://www.vavoo.tv/api/box/ping2", data=data)

        vavoo_auth = json.dumps(vavoo_auth.content)

        vavoo_auth = base64.b64encode(vavoo_auth)

        return vavoo_auth

    def movie(self, imdb, title, localtitle, aliases, year):
        try:

            content1 = cache.get(self.session.get, 24, self.base_link + "all?type=movie&query=" + title).json()
            # content = cache.get(self.session.get,0,self.base_link + "all?type=movie&query=" + title + "&vavoo_auth=" + self.vavoo_auth).json()

            d = {}
            for data in content1:
                d[data["imdb"]] = data["id"]

            for key, value in d.iteritems():
                if key == imdb:
                    jid = str(value)

            content = cache.get(self.session.get, 24,
                                self.base_link + "get?locale=de&hosters=!rapidgator.net,!tata.to,!hdfilme.tv,!1fichier.com,!share-online.biz,!uploadrocket.net,!oboom.com,!rockfile.eu,!kinoger.com,!uptobox.com&resolutions=all&language=de&id=" + jid).json()
            # content=cache.get(self.session.get,0,self.base_link + "get?locale=de&hosters=!tata.to,!hdfilme.tv,!1fichier.com,!share-online.biz,!uploadrocket.net,!oboom.com,!rockfile.eu,!kinoger.com,!uptobox.com&resolutions=hd&language=de&id=" + jid + "&vavoo_auth=" + self.vavoo_auth).json()

            array = content['get']['links']

            linklist = dict()
            for idx, word in enumerate(array):
                link = self.base_link + "link?hoster=" + (word['hoster']) + "&language=de&resolution=" + word[
                    'resolution'] + "&id=" + jid + "&parts=1" + "&quality=" + str(
                    word['quality']) + "&subtitles=" + "&vavoo_auth=" + self.vavoo_auth
                # link=self.base_link+"link?hoster="+(word['hoster'])+"&language=de&resolution=hd&id="+jid+"&parts=1"+"&quality="+str(word['quality'])+"&subtitles="+"&season="+season+"&episode="+episode
                linklist[link] = word['resolution']

            urllist = dict()

            for items, quality in linklist.iteritems():

                response = requests.Session().get(items)

                try:
                    content = response.json()

                    dict1 = content['parts']
                    link = dict1['1']

                    urllist[link] = quality

                except:
                    print "print exception"

            url = urllist

            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        return tvshowtitle

    def episode(self, tvshowtitle, imdb, tvdb, title, premiered, season, episode):
        try:
            content1 = cache.get(self.session.get, 24, self.base_link + "all?type=serie&query=" + tvshowtitle).json()

            d = {}
            for data in content1:
                d[data["imdb"]] = data["id"]
                d[data["title"]] = data["id"]
            jids = []
            for key, value in d.iteritems():
                if key == imdb:
                    if str(value) not in jids: jids.append(str(value))
                if key == tvshowtitle:
                    if str(value) not in jids: jids.append(str(value))

            # content=self.session.get(self.base_link + "get?locale=de&hosters=!rapidgator.net,!tata.to,!hdfilme.tv,!1fichier.com,!share-online.biz,!uploadrocket.net,!oboom.com,!rockfile.eu,!kinoger.com,!uptobox.com&resolutions=all&language=de&id=" + jid + "&season=" + season + "&episode=" + episode) #.json()
            url ={}
            for jid in jids:
                content = self.session.get(
                    self.base_link + "get?locale=de&hosters=!rapidgator.net,!filmpalast.to,!hdfilme.tv,!kinoger.com,!flashx.tv,!tata.to,!1fichier.com,!share-online.biz,!uploadrocket.net,!oboom.com,!rockfile.eu,!uptobox.com&resolutions=all&language=de&id=" + jid + "&season=" + season + "&episode=" + episode)
                content = content.json()
                array = content['get']['links']

                linklist = dict()
                for idx, word in enumerate(array):
                    # enable resolution to retrieve all possible links, however quality checkmissing
                    link = self.base_link + "link?hoster=" + (word['hoster']) + "&language=de&resolution=" + word[
                        'resolution'] + "&id=" + jid + "&parts=1" + "&quality=" + str(word[
                                                                                          'quality']) + "&subtitles=" + "&season=" + season + "&episode=" + episode + "&vavoo_auth=" + self.vavoo_auth
                    # link=self.base_link+"link?hoster="+(word['hoster'])+"&language=de&resolution=hd&id="+jid+"&parts=1"+"&quality="+str(word['quality'])+"&subtitles="+"&season="+season+"&episode="+episode
                    linklist[link] = word['resolution']

                urllist = dict()
                for items, quality in linklist.iteritems():
                    try:
                        response = requests.Session().get(items)
                        result = response.json()
                        dict1 = result['parts']
                        link = dict1['1']
                        urllist[link] = quality
                    except:
                        print "print vavoo exception"

                url.update(urllist)

            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if not url:
                return sources

            for items, quality in url.iteritems():
                if "original" in quality.lower():
                    quality = "SD"
                elif "sd" in quality.lower():
                    quality = "SD"
                elif "hd" in quality.lower():
                    quality = "720p"
                else:
                    quality = "720p"

                if 'thevideo' in items or 'filmpalast' in items:
                    continue  # first edit urlresover "vevio.py"
                    # items = self.session.get(items).url #u'https://vev.red/embed/9jo17zzg7oex'
                    # mediaId = items.split('/')[-1]

                if "clip" in items:
                    sources.append(
                        {'source': "clipboard.cc", 'quality': quality, 'language': 'de', 'url': items, 'direct': True,
                         'debridonly': False})
                    continue

                valid, host = source_utils.is_host_valid(items, hostDict)
                if not valid: continue

                sources.append({'source': host, 'quality': quality, 'language': 'de', 'url': items, 'direct': False,
                                'debridonly': False, 'checkquality': True})

            return sources
        except:
            return sources

    def resolve(self, url):
        if 'clipboard' in url:
            host = 'clipboard.cc'
            userAgent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
            headers_dict = {'User-Agent': userAgent, 'Host': host}
            r = requests.get(url, allow_redirects=False, headers=headers_dict)
            if 300 <= r.status_code <= 400:
                url = r.headers['Location']
        return url
