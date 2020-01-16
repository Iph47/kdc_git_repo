#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmcgui,xbmcaddon,xbmcplugin,re,os,sys,urllib
import resources.lib.feedparser as feedparser
addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path').decode('utf-8')
def addDir(name,url,mode,iconimage):
    u=sys.argv[0]+'?url='+str(url)+'&mode='+str(mode)+'&name='+str(name)
    liz=xbmcgui.ListItem(name,iconImage='DefaultFolder.png',thumbnailImage=iconimage)
    liz.setInfo( type='Video',infoLabels={'Title':name } )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
epg = []
def get_epg(rss_url):
    feed = feedparser.parse(rss_url)
    for i in range(0,len(feed['entries'])):
        titel = feed['entries'][i].title
        try:
            time= re.search('(([0-1][0-9])|([2][0-3])):([0-5][0-9]) - (([0-1][0-9])|([2][0-3])):([0-5][0-9])', feed['entries'][i].description)
            epg.append({'title':titel.replace(':','*')+'*'+time.group(0)})
        except:
            epg.append({'title':titel})
def epg_list(epg_array):
    liste = []
    if len(epg) > 0:
        for line in epg:
            line = line['title']
            try:
                sender = '[COLOR red]'+line.split('*')[0]+'[/COLOR]'
                titel = '[COLOR green]'+line.split('*')[1]+'[/COLOR]'
                time = '[COLOR red]'+line.split('*')[2]+'[/COLOR]'
                liste.append(sender+' '+titel+' '+time)
            except:
                sender = '[COLOR red]'+line.split('|')[0]+'[/COLOR]'
                time = '[COLOR green]'+line.split('|')[1]+'[/COLOR]'
                titel = '[COLOR red]'+line.split('|')[2]+'[/COLOR]'
                liste.append(sender+' '+time+' '+titel)
    return liste
def list_dir():
    for epg_info in epg_list(epg):
        addDir(unicode(epg_info).encode("utf-8"),'',4,os.path.join(addon_path,'icon.png'))
    xbmc.executebuiltin('Container.SetViewMode(51)')
if not sys.argv[2] == '' and '?mode=' in sys.argv[2] and '&name=' in sys.argv[2]:
    tv_mode = int(sys.argv[2].split('?mode=')[1].split('&name=')[0])
    if tv_mode == 1:
        get_epg('http://www.texxas.de/tv/hauptsenderJetzt.xml')
        get_epg('http://www.texxas.de/tv/spartensenderJetzt.xml')
        get_epg('http://www.texxas.de/tv/regionalsenderJetzt.xml')
        get_epg('http://www.texxas.de/tv/skyJetzt.xml')	
        get_epg('http://www.texxas.de/tv/kabeldigitalhomeJetzt.xml')
        get_epg('http://www.texxas.de/tv/digitalsenderJetzt.xml')
        get_epg('http://www.texxas.de/tv/nachrichtensenderJetzt.xml')
        get_epg('http://www.texxas.de/tv/oesterreichJetzt.xml')
        get_epg('http://www.texxas.de/tv/schweizJetzt.xml')
        list_dir()
    elif tv_mode == 2:
        get_epg('http://www.texxas.de/tv/hauptsender.xml')
        get_epg('http://www.texxas.de/tv/spartensender.xml')
        get_epg('http://www.texxas.de/tv/regionalsender.xml')
        get_epg('http://www.texxas.de/tv/sky.xml')	
        get_epg('http://www.texxas.de/tv/kabeldigitalhome.xml')
        get_epg('http://www.texxas.de/tv/digitalsender.xml')
        get_epg('http://www.texxas.de/tv/nachrichtensender.xml')
        get_epg('http://www.texxas.de/tv/oesterreich.xml')
        get_epg('http://www.texxas.de/tv/schweiz.xml')
        list_dir()
    elif tv_mode == 3:
        keyboard = xbmc.Keyboard('','TV GUIDE SCHLAGWORT SUCHE')
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():		
            get_epg(str('http://www.texxas.de/searchXml/'+keyboard.getText().decode("iso-8859-1", "ignore").encode('utf8').strip()+'_tv.xml'))
            list_dir()
        else:
            sys.exit(0)
    elif tv_mode == 4:
        sys.exit(0)
else:
    addDir('TV JETZT','',1,os.path.join(addon_path,'folder.png'))
    addDir('TV PROGRAMM 20:15','',2,os.path.join(addon_path,'folder.png'))
    addDir('SUCHE NACH TV SENDUNG ( SCHLAGWORT )','',3,os.path.join(addon_path,'folder.png'))
    xbmc.executebuiltin('Container.SetViewMode(100)')
xbmcplugin.endOfDirectory(int(sys.argv[1]))

