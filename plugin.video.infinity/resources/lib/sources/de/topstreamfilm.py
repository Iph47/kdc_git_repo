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

import re
import urllib
import urlparse
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser
from resources.lib.modules import source_faultlog
from resources.lib.modules.handler.requestHandler import cRequestHandler


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['topstreamfilm.com']
        self.base_link = 'https://topstreamfilm.com'
        self.search_link = '/?s=%s'
        self.episode_link = '/episode/%s-staffel-%s-episode-%s/'
        self.get_link = '?trembed=%s&%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            titles = [localtitle] + source_utils.aliases_to_array(aliases)
            url = self.__search(titles, year)
            if not url and title != localtitle: url = self.__search([title] + source_utils.aliases_to_array(aliases), year)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = self.__search([localtvshowtitle] + source_utils.aliases_to_array(aliases), year)
            if not url and tvshowtitle != localtvshowtitle: url = self.__search([tvshowtitle] + source_utils.aliases_to_array(aliases), year)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            url = url.replace("/", "")
            url = self.episode_link % (url, season, episode)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if not url:
                return sources
            oRequest = cRequestHandler(urlparse.urljoin(self.base_link, url))
            oRequest.removeBreakLines(False)
            oRequest.removeNewLines(False)
            moviecontent = oRequest.request()
            searchResult = dom_parser.parse_dom(moviecontent, 'div', attrs={'class': 'TPlayer'})

            results = re.findall(r'src=".*?;(.*?)"', searchResult[0].content, flags=re.DOTALL)
            opt = re.findall(r'id="Opt(\d)"', searchResult[0].content, flags=re.DOTALL)

            for i in range(0, len(opt)):
                r = self.get_link % (i, results[0])
                oRequest = cRequestHandler(urlparse.urljoin(self.base_link, r))
                oRequest.addHeaderEntry('Referer', urlparse.urljoin(self.base_link, url))
                oRequest.addHeaderEntry('Upgrade-Insecure-Requests', '1')
                oRequest.removeBreakLines(False)
                oRequest.removeNewLines(False)
                hostcontent = oRequest.request()
                searchResult = dom_parser.parse_dom(hostcontent, 'div', attrs={'class': 'Video'})
                links = re.findall(r'src="(.*?)"', searchResult[0].content, flags=re.DOTALL)
                link = links[0]
                valid, hoster = source_utils.is_host_valid(link, hostDict)
                if not valid: continue
                sources.append(
                        {'source': hoster, 'quality': '720p', 'language': 'de', 'url': link, 'direct': False,
                         'debridonly': False, 'checkquality': False})

            return sources

        except:
            source_faultlog.logFault(__name__, source_faultlog.tagScrape)
            return sources

    def resolve(self, url):
        return url

    def __search(self, titles, year):
        try:
            query = self.search_link % (urllib.quote_plus(cleantitle.query(titles[0])))
            query = urlparse.urljoin(self.base_link, query)

            titles = [cleantitle.get(i) for i in set(titles) if i]

            oRequest = cRequestHandler(query)
            oRequest.addHeaderEntry('Referer', self.base_link)
            oRequest.addHeaderEntry('Upgrade-Insecure-Requests', '1')
            oRequest.removeBreakLines(False)
            oRequest.removeNewLines(False)
            searchResult = oRequest.request()

            results = dom_parser.parse_dom(searchResult, 'section')
            if results:
                results = re.findall(r'href="(.*?)".*?Title">(.*?)<(.*?)<\/span', results[0].content, flags=re.DOTALL)
                url = None
                for x in range(0, len(results)):
                    title = cleantitle.get(results[x][1])
                    if any(i in title for i in titles) and year in results[x][2]:
                        url = source_utils.strip_domain(results[x][0])
                        return url

                if url == None:  # ohne year - es gibt nicht bei alle Einträge "year"
                    for x in range(0, len(results)):
                        title = cleantitle.get(results[x][1])
                        if any(i in title for i in titles):
                            url = source_utils.strip_domain(results[x][0])
                            return url
            return
        except:
            try:
                source_faultlog.logFault(__name__, source_faultlog.tagSearch, titles[0])
            except:
                return
            return
