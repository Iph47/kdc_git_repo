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

import urlparse

from resources.lib.modules import cache
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import dom_parser
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['kinox.one']
        self.base_link = 'http://kinox.one/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.__search([localtitle] + source_utils.aliases_to_array(aliases))
            if not url and title != localtitle: url = self.__search([title] + source_utils.aliases_to_array(aliases))
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        if not url:
            return sources

        url = urlparse.urljoin(self.base_link, url)

        sources.append({'source': 'CDN', 'quality': 'HD', 'language': 'de', 'url': url, 'direct': True, 'debridonly': False})

        return sources

    def resolve(self, url):
        cookie = client.request(self.base_link, post={'login_name': 'lastship', 'login_password': 'lastship', 'login': 'submit'}, output='cookie')

        content = client.request(url, cookie=cookie)
        link = dom_parser.parse_dom(content, 'div', attrs={'class': 'dlevideoplayer'})
        link = dom_parser.parse_dom(link, 'li')[0].attrs['data-url']
        return link

    def __search(self, titles):
        try:
            t = [cleantitle.get(i) for i in set(titles) if i]

            for title in titles:
                params = {
                    'do': 'search',
                    'subaction': 'search',
                    'story': cleantitle.getsearch(title)
                }

                result = cache.get(client.request, 6, self.base_link, post=params, headers={'Upgrade-Insecure-Requests': 1})

                links = dom_parser.parse_dom(result, 'div', attrs={'id': 'dle-content'})
                links = dom_parser.parse_dom(links, 'a')
                links = [(i.attrs['href'], dom_parser.parse_dom(i, 'div', attrs={'class': 'tiitle'})[0].content) for i in links]
                links = [i[0] for i in links if cleantitle.get(i[1]) in t]

                if len(links) == 0:
                    raise Exception()
                return source_utils.strip_domain(links[0])
            return
        except:
            cache.clearFunc(client.request, self.base_link, post=params, headers={'Upgrade-Insecure-Requests': 1})
            pass
