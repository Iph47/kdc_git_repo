# -*- coding: UTF-8 -*-

import urlparse
import re
import urllib
import difflib
import xbmcaddon
import xbmcvfs
import os

try:
    from providerModules.LastShip import cache
    from providerModules.LastShip import cleantitle
    from providerModules.LastShip import dom_parser
    from providerModules.LastShip import source_utils
    from resources.lib.modules.handler.requestHandler import cRequestHandler

except:
    from resources.lib.modules import cache
    from resources.lib.modules import cleantitle
    from resources.lib.modules import dom_parser
    from resources.lib.modules import source_utils
    from resources.lib.modules.handler.requestHandler import cRequestHandler


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.Addon = xbmcaddon.Addon()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            titles = [localtitle] + source_utils.aliases_to_array(aliases)
            url = self.__search(titles, year)
            if not url and title != localtitle: url = self.__search([title] + source_utils.aliases_to_array(aliases),
                                                                    year)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'localtvshowtitle': localtvshowtitle,
                   'aliases': aliases, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            tvshowtitle = data['tvshowtitle']
            aliases = source_utils.aliases_to_array(eval(data['aliases']))
            aliases.append(data['localtvshowtitle'])
            url = self.__search([tvshowtitle] + aliases, data['year'], season, episode)
            if not url: return
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        url, filename = url
        quality = source_utils.get_release_quality(filename)
        sources.append({'source': 'local', 'quality': quality[0], 'language': 'de', 'url': url, 'direct': True, 'debridonly': False, 'local': True})
        return sources

    def resolve(self, url):
        return url

    def __search(self, titles, year, season='0', episode='0'):
        if season == '0':
            path = self.Addon.getSetting('privatefolder.path')
            path = os.path.join(path, "Filme")

            dirs, files = xbmcvfs.listdir(path)
            filme = []
            for i in files:
                film = {'titel': '', 'ratio': '', 'foldername':''}
                localtitle = cleantitle.query(titles[0])
                filmname = cleantitle.query(i)
                ratio = difflib.SequenceMatcher(None, localtitle, filmname).ratio()
                film['titel'] = localtitle
                film['ratio'] = ratio
                film['filename'] = i
                if float(ratio) > float(0.4):
                    filme.append(film)

            filme = sorted(filme, key=lambda i: i['ratio'])
            url = os.path.join(path, filme[len(filme) - 1]['filename'])
            return url
        else:
            path = self.Addon.getSetting('privatefolder.path')
            path = os.path.join(path, "Serien")

            dirs, files = xbmcvfs.listdir(path)
            serien = []
            for i in dirs:
                serie = {'titel': '', 'ratio': '', 'foldername':''}
                localtitle = cleantitle.query(titles[0])
                foldername = cleantitle.query(i)
                ratio = difflib.SequenceMatcher(None, localtitle, foldername).ratio()
                serie['titel'] = localtitle
                serie['ratio'] = ratio
                serie['foldername'] = i
                if float(ratio) > float(0.4):
                    serien.append(serie)

            serien = sorted(serien, key=lambda i: i['ratio'])
            path = os.path.join(path, serien[len(serien) - 1]['foldername'])
            if int(season) < 10:
                season = 'S0' + str(season)
            else:
                season = 'S' + str(season)

            path = os.path.join(path, season)
            dirs, files = xbmcvfs.listdir(path)

            if int(episode) < 10:
                episode = 'E0' + str(episode)
            else:
                episode = 'E' + str(episode)

            for i in files:
                if episode in i:
                    filename = i
                    break

            url = [os.path.join(path, i), i]
            return url

        return
