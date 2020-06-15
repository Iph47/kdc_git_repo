# -*- coding: UTF-8 -*-

import urlparse
import re
import urllib
import difflib


try:
    from providerModules.LastShip import cache
    from providerModules.LastShip import cleantitle
    from providerModules.LastShip import dom_parser
    from providerModules.LastShip import source_utils
    from resources.lib.modules.handler.requestHandler import cRequestHandler
    from resources.lib.modules.gdrive import Drive

except:
    from resources.lib.modules import cache
    from resources.lib.modules import cleantitle
    from resources.lib.modules import dom_parser
    from resources.lib.modules import source_utils
    from resources.lib.modules.handler.requestHandler import cRequestHandler
    from resources.lib.modules.gdrive import Drive

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']

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
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'localtvshowtitle': localtvshowtitle, 'aliases': aliases, 'year': year}
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
        sources = url
        return sources

    def resolve(self, url):
        return url

    def __search(self, titles, year, season='0', episode='0'):
        Drivelist = Drive().list_accounts()
        for i in Drivelist:
            DriveContent = Drive().list_folder(driveid=i,path='/')

        index={'4k Filme':'', 'Serien': '', 'Filme':'', 'Serien_bad':''}
        
        for i in range(0,len(DriveContent)):
            if DriveContent[i]['name'] == 'Filme (NUR 2160p & 1080p)':
                index['4k Filme'] = i
            elif DriveContent[i]['name'] == 'Serien (NUR 2160p & 1080 & 720p)':
                index['Serien'] = i
            elif DriveContent[i]['name'] == 'Filme (schlechtere Qualität)':
                index['Filme'] = i
            elif DriveContent[i]['name'] == 'Serien (schlechtere Qualität)':
                index['Serien_bad'] = i

        streams = []
        if season == '0':
            Filme = Drive().list_folder(driveid=DriveContent[index['Filme']]['parent'], item_driveid=DriveContent[index['Filme']]['parent'],item_id=DriveContent[index['Filme']]['id'])
            for i in Filme:
                stream = {'gdrivetitle' : '', 'ratio' : '', 'parent' : '', 'id': ''}
                localtitle = cleantitle.query(titles[0])
                gdrivetitle = cleantitle.query(i['name'])
                ratio=difflib.SequenceMatcher(None, localtitle, gdrivetitle).ratio() 
                stream['gdrivetitle'] = gdrivetitle
                stream['ratio'] = ratio      
                stream['parent'] = i['parent']
                stream['id'] = i['id']
                stream['driveid'] = DriveContent[index['Filme']]['parent']
                if float(ratio) > float(0.5):
                    streams.append(stream)
            Filme = Drive().list_folder(driveid=DriveContent[index['4k Filme']]['parent'], item_driveid=DriveContent[index['4k Filme']]['parent'],item_id=DriveContent[index['4k Filme']]['id'])
            for i in Filme:
                stream = {'gdrivetitle' : '', 'ratio' : '', 'parent' : '', 'id': '', 'driveid': ''}
                localtitle = cleantitle.query(titles[0])
                gdrivetitle = cleantitle.query(i['name'])
                ratio=difflib.SequenceMatcher(None, localtitle, gdrivetitle).ratio() 
                stream['gdrivetitle'] = gdrivetitle
                stream['ratio'] = ratio      
                stream['parent'] = i['parent']
                stream['id'] = i['id']
                stream['driveid'] = DriveContent[index['4k Filme']]['parent']
                if float(ratio) > float(0.5):
                    streams.append(stream)
            streams = sorted(streams, key = lambda i: i['ratio'])
            x = len(streams) - 1
            stream_file = Drive().list_folder(driveid=streams[x]['driveid'], item_driveid=streams[x]['parent'],item_id=streams[x]['id'])


            stream_file = sorted(stream_file, key=lambda i: i['video']['width'])
            x = len(stream_file)
            for i in stream_file:
                if i['video']:
                    sources = []
                    file = Drive().get_item_play_url(driveid=streams[0]['driveid'], item_driveid=streams[0]['parent'], item_id=i['id'])
                    url = file['download_info']['url']
                    if file['video']['width'] >= 3840:
                        sources.append({'source': 'googledrive', 'quality': '4K', 'language': 'de', 'url': url, 'direct': True,
                                        'debridonly': False})
                    elif file['video']['height'] >= 1080:
                        sources.append(
                            {'source': 'googledrive', 'quality': '1080p', 'language': 'de', 'url': url, 'direct': True,
                             'debridonly': False})
                    elif file['video']['height'] >= 720:
                        sources.append(
                            {'source': 'googledrive', 'quality': '720p', 'language': 'de', 'url': url, 'direct': True,
                             'debridonly': False})
                    else:
                        sources.append({'source': 'googledrive', 'quality': 'SD', 'language': 'de', 'url': url, 'direct': True,
                                        'debridonly': False})

                    return sources
                else: return


#######################################################################################


        else:
            Serien = Drive().list_folder(driveid=DriveContent[index['Serien']]['parent'], item_driveid=DriveContent[index['Serien']]['parent'], item_id=DriveContent[index['Serien']]['id'])
            for i in Serien:
                stream = {'gdrivetitle': '', 'ratio': '', 'parent': '', 'id': '', 'driveid': ''}
                localtitle = cleantitle.query(titles[0])
                gdrivetitle = cleantitle.query(i['name'])
                ratio = difflib.SequenceMatcher(None, localtitle, gdrivetitle).ratio()
                stream['gdrivetitle'] = gdrivetitle
                stream['ratio'] = ratio
                stream['parent'] = i['parent']
                stream['id'] = i['id']
                stream['driveid'] = DriveContent[index['Serien']]['parent']
                if float(ratio) > float(0.2):
                    streams.append(stream)

            Serien = Drive().list_folder(driveid=DriveContent[index['Serien_bad']]['parent'], item_driveid=DriveContent[index['Serien_bad']]['parent'], item_id=DriveContent[index['Serien_bad']]['id'])
            for i in Serien:
                stream = {'gdrivetitle': '', 'ratio': '', 'parent': '', 'id': '', 'driveid': ''}
                localtitle = cleantitle.query(titles[0])
                gdrivetitle = cleantitle.query(i['name'])
                ratio = difflib.SequenceMatcher(None, localtitle, gdrivetitle).ratio()
                stream['gdrivetitle'] = gdrivetitle
                stream['ratio'] = ratio
                stream['parent'] = i['parent']
                stream['id'] = i['id']
                stream['driveid'] = DriveContent[index['Serien_bad']]['parent']
                if float(ratio) > float(0.2):
                    streams.append(stream)

            streams = sorted(streams, key=lambda i: i['ratio'])
            x = len(streams) -1
            stream_Seasons = Drive().list_folder(driveid=streams[x]['driveid'], item_driveid=streams[x]['parent'], item_id=streams[x]['id'])

            if int(season) < 10:
                season = 'S0' + str(season)
            else:
                season = 'S' + str(season)

            for i in stream_Seasons:
                if season in i['name']:
                    stream = {'Season': '', 'parent': '', 'id': '', 'driveid': ''}
                    stream['Season'] = i['name']
                    stream['parent'] = i['parent']
                    stream['id'] = i['id']
                    stream['driveid'] = DriveContent[index['Serien']]['parent']
                    break

            stream_Episodes = Drive().list_folder(driveid=stream['driveid'], item_driveid=stream['parent'], item_id=stream['id'])

            if int(episode) < 10:
                episode = 'E0' + str(episode)
            else:
                episode = 'E' + str(episode)

            for i in stream_Episodes:
                if episode in i['name']:
                    stream = i
                    stream['driveid'] = DriveContent[index['Serien']]['parent']
                    break

            sources = []
            file = Drive().get_item_play_url(driveid=stream['driveid'], item_driveid=stream['parent'], item_id=stream['id'])
            url = file['download_info']['url']
            if file['video']['width'] >= 3840:
                sources.append({'source': 'googledrive', 'quality': '4K', 'language': 'de', 'url': url, 'direct': True,
                                'debridonly': False})
            elif file['video']['height'] >= 1080:
                sources.append(
                    {'source': 'googledrive', 'quality': '1080p', 'language': 'de', 'url': url, 'direct': True,
                     'debridonly': False})
            elif file['video']['height'] >= 720:
                sources.append(
                    {'source': 'googledrive', 'quality': '720p', 'language': 'de', 'url': url, 'direct': True,
                     'debridonly': False})
            else:
                sources.append({'source': 'googledrive', 'quality': 'SD', 'language': 'de', 'url': url, 'direct': True,
                                'debridonly': False})

            return sources

        return
