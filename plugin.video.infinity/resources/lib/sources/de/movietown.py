# -*- coding: UTF-8 -*-

"""
    Infinity Add-on (C) 2019 (ka)
    Credits to Placenta and Covenant; our thanks go to their creators

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
# Addon id: plugin.video.Infinity
# Addon Provider: Infinity

import re
import urllib
import urlparse
import cfscrape

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser
from resources.lib.modules import source_faultlog
from resources.lib.modules import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['movietown.org']
        self.base_link = 'https://movietown.org'
        self.search_link = '/search?q=%s'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.__search([localtitle] + source_utils.aliases_to_array(aliases), year, False)
            if not url and title != localtitle: url = self.__search([title] + source_utils.aliases_to_array(aliases), year, False)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = self.__search([localtvshowtitle] + source_utils.aliases_to_array(aliases), year, True)
            if not url and tvshowtitle != localtvshowtitle: url = self.__search([tvshowtitle] + source_utils.aliases_to_array(aliases), year, True)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            s = '/seasons/%s/episodes/%s' % (season, episode)

            url = url.rstrip('/')
            url = url + s
            url = urlparse.urljoin(self.base_link, url)

            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if not url:
                return sources
            url = urlparse.urljoin(self.base_link, url)
            result = self.scraper.get(url).content

            r = result
            r = dom_parser.parse_dom(r, 'table', attrs={'class': 'table table-striped links-table'})
            r = dom_parser.parse_dom(r, 'tbody')
            r = dom_parser.parse_dom(r, 'tr')

            q = -1
            for i in r:
                q = q + 1
                x = dom_parser.parse_dom(i, 'td', attrs={'class': 'name'}, req='data-bind')

                if len(x) == 0:
                    continue

                quality = dom_parser.parse_dom(r[q], 'td')
                quality = quality[1].content
                quality, info = source_utils.get_release_quality(quality)

                hoster = re.search("(?<=>).*$", x[0][1])
                hoster = hoster.group().lower()

                link = re.search("http(.*?)(?=')", x[0][0]['data-bind'])
                link = link.group()

                valid, hoster = source_utils.is_host_valid(hoster, hostDict)
                if valid:
                    sources.append({'source': hoster, 'quality': quality, 'language': 'de', 'url': link, 'direct': False, 'debridonly': False})

            if len(sources) == 0:
                raise Exception()
            return sources
        except:
            source_faultlog.logFault(__name__,source_faultlog.tagScrape, url)
            return sources

    def resolve(self, url):
        return url

    def __search(self, titles, year, isSerieSearch):
        try:
            query = self.search_link % (urllib.quote_plus(cleantitle.query(titles[0])))
            query = urlparse.urljoin(self.base_link, query)
            t = [cleantitle.get(i) for i in set(titles) if i]

            sHtmlContent = self.scraper.get(query).content
            id = 'movies'
            if isSerieSearch: id = 'series'
            pattern = 'id="%s">(.*?)</div' % id
            r = re.findall(pattern, sHtmlContent, flags=re.DOTALL)
            r = dom_parser.parse_dom(r, 'figcaption')

            links = []
            for i in r:
                title = client.replaceHTMLCodes(i[0]['title'])
                title = cleantitle.get(title)
                if title in t:
                    x = dom_parser.parse_dom(i, 'a', req='href')
                    link= source_utils.strip_domain(x[0][0]['href'])
                    links.append(link)
                else:
                    for j in t:
                        if j in cleantitle.get(title):
                            x = dom_parser.parse_dom(i, 'a', req='href')
                            link = source_utils.strip_domain(x[0][0]['href'])
                            links.append(link)

            # Mehrfach z.B. https://movietown.org/search?q=Der+K%C3%B6nig+der+L%C3%B6wen
            # vorgesehen für Abgleich mit "year"
            if len(links) == 1:
                return links[0]
            if len(links) > 1:
                from resources.lib.modules import workers
                import Queue
                que = Queue.Queue()
                threads = []
                for i in links:
                    threads.append(workers.Thread(self.chk_year, i, year, que))
                [i.start() for i in threads]
                [i.join() for i in threads]
                result = que.get()
                if len(result) > 0:
                    return result
            return

        except:
            try:
                source_faultlog.logFault(__name__, source_faultlog.tagSearch, titles[0])
            except:
                return
            return

    def chk_year(self, url, year, que):
        query = urlparse.urljoin(self.base_link, url)
        sHtmlContent = self.scraper.get(query).content
        r = dom_parser.parse_dom(sHtmlContent, 'div', attrs={'class': 'row details-panel'})
        r = dom_parser.parse_dom(r[0].content, 'ul', attrs={'class': 'list-unstyled'})
        r = dom_parser.parse_dom(r, 'span')
        if year in r[0].content:
            que.put(url)
