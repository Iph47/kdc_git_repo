import os,xbmc
import xbmcplugin
import kodi
from BeautifulSoup import BeautifulSoup
import urllib2
import urllib
import webbrowser
import resolveurl as urlresolver
import xbmcgui
import xbmcplugin
import sys
import os
import shutil
import requests
addon_id   = 'script.module.7of9-pirateslife4me'
addon_id2   = 'script.module.7of9-pirateslife4me/'

# https://proxyofthepiratebay.com/
# https://proxyofthepiratebay.com/

icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+ '/icon.png'))
fanart     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+ '/fanart.jpg'))
logfile    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+ '/log.txt'))
plugin_path=xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+"/"))


hectoricon = icon

header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0"}

from resources.root import android

def home():
    addDir('[B][COLOR dodgerblue]***** Welcome To "A Pirates Life For Me" *****[/COLOR][/B]','url','',icon,fanart,'')
    addDir('[B][COLOR dodgerblue]***** Optimized For Real-Debrid/Torrents *****[/COLOR][/B]','url','',icon,fanart,'')
    addDir('[B][COLOR dodgerblue]You Need A Real-Debrid Account,[/COLOR][/B]','url','',icon,fanart,'') 
    addDir('[B][COLOR dodgerblue]Torrents Sent To Real-Debrid  NOT Your Device,[/COLOR][/B]','','',icon,fanart,'')
    addDir('[B][COLOR dodgerblue]Personal IP Will Never Connect T The Torrent Network.[/COLOR][/B]','url','',icon,fanart,'')
    addDir('[B][COLOR gold]Authorize Premium Server: [/COLOR][COLOR white]Real-Debrid[/COLOR][/B]','url',6673,icon,fanart,'')
    addDir('[B][COLOR dodgerblue]*** Trending Top Movies and TV Shows - Last 48 Hours***[/COLOR][/B]','url','',icon,fanart,'')		
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Trending Movies[/COLOR][/B]','https://eztv.io/search/',2003,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Trending HD Movies[/COLOR][/B]','https://eztv.io/search/',20031,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Trending 3D Movies[/COLOR][/B]','https://eztv.io/search/',20034,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Trending 4K Movies[/COLOR][/B]','https://eztv.io/search/',20032,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Trending TV Shows[/COLOR][/B]','https://eztv.io/search/',20035,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Trending HD TV Shows[/COLOR][/B]','https://eztv.io/search/',20036,icon,fanart,'')
    addDir('','url','',icon,fanart,'')	
    addDir('[B][COLOR goldenrod]*** Under Construction ***[/COLOR][/B]','url','',icon,fanart,'')
    addDir('[B][COLOR dodgerblue]*** Top Movies By Resolution And Year ***[/COLOR][/B]','url','',icon,fanart,'')		
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]720p Year Of 2019 to 1999 - 1 Page Each[/COLOR][/B]','url',6674,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]1080p Year Of 2019 to 1999 - 1 Page Each[/COLOR][/B]','url',10806674,icon,fanart,'')	
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]4K Year Of 2019 to 1999 - 1 Page Each[/COLOR][/B]','url',21606674,icon,fanart,'')
    addDir('[B][COLOR goldenrod]*** Under Construction ***[/COLOR][/B]','url','',icon,fanart,'')
    addDir('','url','',icon,fanart,'')
    addDir('[B][COLOR dodgerblue]*** Top Movie Streams - 720p, And 1080p - Mixed Years - 20 Pages***[/COLOR][/B]','url','',icon,fanart,'')	
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]720p, 1080p Mixed Years - 20 Pages[/COLOR][/B]','url',6669,icon,fanart,'')	
    addDir('','url','',icon,fanart,'')
    addDir('[B][COLOR dodgerblue]*** Movie Servers Direct Links - Needs Updating ***[/COLOR][/B]','url','',icon,fanart,'')	
    addDir('[B][COLOR gold]Movie Direct Links: [/COLOR][COLOR white]Free Servers[/COLOR][/B]','url',6671,icon,fanart,'')
    addDir('[B][COLOR dodgerblue]*** Exdoux Forks Real-Debrid or Free Links ***[/COLOR][/B]','url','',icon,fanart,'')	
    addDir('[B][COLOR gold]The USS Defiant - Select Link: [/COLOR][COLOR white]Free Servers and Real-Debrid[/COLOR][/B]','url',6670,icon,fanart,'')
    addDir('[B][COLOR gold]Greased Lightning - Auto Play Link: [/COLOR][COLOR white]Free Servers and Real-Debrid[/COLOR][/B]','url',66704444,icon,fanart,'')
    addDir('[B][COLOR dodgerblue]*** Media Search ***[/COLOR][/B]','url','',icon,fanart,'')
    addDir('[B][COLOR gold]Search Movies and TV Shows: [/COLOR][COLOR white]Free Servers and Real-Debrid[/COLOR][/B]','url',6672,icon,fanart,'')
    addDir('','url','',icon,fanart,'')
    addDir('[B][COLOR lime]This addon searches Torrents and websites [/COLOR][/B]','url','',icon,fanart,'')
    addDir('[B][COLOR lime]For Content, Please Use at your own risk![/COLOR][/B]','','',icon,fanart,'')
    addDir('','url','',icon,fanart,'')
    addDir('','url','',icon,fanart,'')
    addDir('[B][COLOR dodgerblue]***** Warning Porn XXX Gateway *****[/COLOR][/B]','url','',icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Grown-Up Movies[/COLOR][/B]','url',6675,icon,fanart,'')
    addDir('[B][COLOR dodgerblue]********* Please Come Again *********[/COLOR][/B]','url','',icon,fanart,'')
	
def LiveMenu():#
    addDir('[B][COLOR gold]Pirate: [/COLOR][COLOR white]IPTV[/COLOR][/B]','url',2000,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate: [/COLOR][COLOR white]IPTV UK Geo Locked[/COLOR][/B] (BBCi)','url',1000,icon,fanart,'')
	
def LiveMenu1():#
    addDir('[B][COLOR dodgerblue]*********** Torrent Movies ************[/COLOR][/B]','url','',icon,fanart,'')
    addDir('[B][COLOR white]If A List Is Empty, Please Try Again[/COLOR][/B]','','',icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Trending Popular Movies[/COLOR][/B]','https://eztv.io/search/',2003,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Trending HD Movies[/COLOR][/B]','https://eztv.io/search/',20031,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Search - For Movies[/COLOR][/B]','https://thepiratebay.vip/search/',2002,icon,fanart,'')
    addDir('[B][COLOR gold]GlowTorrents: [/COLOR][COLOR white]Search - For Movies[/COLOR][/B]','http://glodls.to/search_results.php?search=',2009,icon,fanart,'')
	
def LiveMenu2():#
    addDir('[B][COLOR dodgerblue]*********** Torrent TV Shows ************[/COLOR][/B]','url','',icon,fanart,'')
    addDir('[B][COLOR white]If A List Is Empty, Please Try Again[/COLOR][/B]','','',icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Trending Popular TV Shows[/COLOR][/B]','https://eztv.io/search/',20035,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Trending HD TV Shows[/COLOR][/B]','https://eztv.io/search/',20036,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Search - For TV Shows[/COLOR][/B]','https://thepiratebay.vip/search/',2002,icon,fanart,'')
    addDir('[B][COLOR gold]EZTV: [/COLOR][COLOR white]Search - For TV Shows[/COLOR][/B]','https://eztv.io/search/',2002,icon,fanart,'')
	
def LiveMenu3():#
    addDir('[B][COLOR dodgerblue]********* Torrent Top Movie Streams - 720p, And 1080p - Mixed Years 20 Pages **********[/COLOR][/B]','url','',icon,fanart,'')
    addDir('[B][COLOR white]If A List Is Empty, Please Try Again[/COLOR][/B]','','',icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Top Movie Streams - Page 1[/COLOR][/B]','https://eztv.io/search/',20153,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Top Movie Streams - Page 2[/COLOR][/B]','https://eztv.io/search/',20154,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Top Movie Streams - Page 3[/COLOR][/B]','https://eztv.io/search/',20155,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Top Movie Streams - Page 4[/COLOR][/B]','https://eztv.io/search/',20156,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Top Movie Streams - Page 5[/COLOR][/B]','https://eztv.io/search/',20157,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Top Movie Streams - Page 6[/COLOR][/B]','https://eztv.io/search/',20158,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Top Movie Streams - Page 7[/COLOR][/B]','https://eztv.io/search/',20159,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Top Movie Streams - Page 8[/COLOR][/B]','https://eztv.io/search/',20160,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Top Movie Streams - Page 9[/COLOR][/B]','https://eztv.io/search/',20161,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Top Movie Streams - Page 10[/COLOR][/B]','https://eztv.io/search/',20162,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Top Movie Streams - Page 11[/COLOR][/B]','https://eztv.io/search/',20163,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Top Movie Streams - Page 12[/COLOR][/B]','https://eztv.io/search/',20164,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Top Movie Streams - Page 13[/COLOR][/B]','https://eztv.io/search/',20165,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Top Movie Streams - Page 14[/COLOR][/B]','https://eztv.io/search/',20166,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Top Movie Streams - Page 15[/COLOR][/B]','https://eztv.io/search/',20167,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Top Movie Streams - Page 16[/COLOR][/B]','https://eztv.io/search/',20168,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Top Movie Streams - Page 17[/COLOR][/B]','https://eztv.io/search/',20169,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Top Movie Streams - Page 18[/COLOR][/B]','https://eztv.io/search/',20170,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Top Movie Streams - Page 19[/COLOR][/B]','https://eztv.io/search/',20171,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Top Movie Streams - Page 20[/COLOR][/B]','https://eztv.io/search/',20172,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Search - For Movies[/COLOR][/B]','https://thepiratebay.vip/search/',2002,icon,fanart,'')
	
def LiveMenu4():#
    addDir('[B][COLOR dodgerblue]*** The USS Defiant - Select Links ***[/COLOR][/B]','url','',icon,fanart,'')
    addDir('[B][COLOR dodgerblue]*** Real-Debrid / Torrent / Free Links ***[/COLOR][/B]','url','',icon,fanart,'')
    addDir('[B][COLOR gold]The USS Defiant: [/COLOR][COLOR white][B]Movies[/COLOR][/B]','url',9002,icon,fanart,'')
    addDir('[B][COLOR gold]The USS Defiant: [/COLOR][COLOR white][B]TV Shows[/COLOR][/B]','url',9003,icon,fanart,'')
    addDir('[B][COLOR gold]The USS Defiant: [/COLOR][COLOR white][B]Search[/COLOR][/B]','url',9000,icon,fanart,'')
    addDir('[B][COLOR gold]The USS Defiant: [/COLOR][COLOR white][B]Settings[/COLOR][/B]','url',9004,icon,fanart,'')
	
def LiveMenu44444():#
    addDir('[B][COLOR dodgerblue]*** Greased Lightning - Auto Play Links ***[/COLOR][/B]','url','',icon,fanart,'')
    addDir('[B][COLOR dodgerblue]*** Real-Debrid / Torrent / Free Links ***[/COLOR][/B]','url','',icon,fanart,'')
    addDir('[B][COLOR gold]Greased Lightning: [/COLOR][COLOR white][B]Movies[/COLOR][/B]','url',90024444,icon,fanart,'')
    addDir('[B][COLOR gold]Greased Lightning: [/COLOR][COLOR white][B]TV Shows[/COLOR][/B]','url',90034444,icon,fanart,'')
    addDir('[B][COLOR gold]Greased Lightning: [/COLOR][COLOR white][B]Search[/COLOR][/B]','url',90004444,icon,fanart,'')
    addDir('[B][COLOR gold]Greased Lightning: [/COLOR][COLOR white][B]Settings[/COLOR][/B]','url',90044444,icon,fanart,'')
	
def LiveMenu5():#
    addDir('[B][COLOR dodgerblue]*** Direct Links, Real-Debrid Not Required ***[/COLOR][/B]','url','',icon,fanart,'')
    addDir('[B][COLOR gold]Dirent: [/COLOR][COLOR white]Movies On Demand[/COLOR][/B] (Direct)','url',2016,icon,fanart,'')
    addDir('[B][COLOR gold]Dirent: [/COLOR][COLOR white]Movies On Demand[/COLOR][/B] (Direct H265 Only)','url',2015,icon,fanart,'')
    addDir('[B][COLOR gold]Dirent: [/COLOR][COLOR white]Movies On Demand[/COLOR][/B] (Direct Pirate List 1)','url',20152,icon,fanart,'')
    addDir('[B][COLOR gold]Dirent: [/COLOR][COLOR white]Movies On Demand - Kung Fu [/COLOR][/B] (Direct)','url',20150,icon,fanart,'')
    addDir('[B][COLOR gold]Dirent: [/COLOR][COLOR white]Movies On Demand - GodZilla [/COLOR][/B] (Direct)','url',20151,icon,fanart,'')	
	
def LiveMenu6():#
    addDir('[B][COLOR dodgerblue]**** Search - For Movies and TV Shows ****[/COLOR][/B]','url','',icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Search[/COLOR][/B]','https://thepiratebay.vip/search/',2002,icon,fanart,'')
    addDir('[B][COLOR gold]GlowTorrents: [/COLOR][COLOR white]Search[/COLOR][/B]','http://glodls.to/search_results.php?search=',2009,icon,fanart,'')
    addDir('[B][COLOR gold]EZTV: [/COLOR][COLOR white]Search[/COLOR][/B]','https://eztv.io/search/',2002,icon,fanart,'')
    addDir('[B][COLOR gold]The USS Defiant : [/COLOR][COLOR white][B]Search[/COLOR][/B]','url',9000,icon,fanart,'')
    addDir('[B][COLOR gold]Greased Lightning: [/COLOR][COLOR white][B]Search[/COLOR][/B]','url',90004444,icon,fanart,'')
	
def LiveMenu7():#
    addDir('[B][COLOR dodgerblue]******* Authorize Premium Servers *******[/COLOR][/B]','url','',icon,fanart,'')
    addDir('[B][COLOR gold]Authorize RD: [/COLOR][COLOR white]Open ResolveURL Settings[/COLOR][/B]','url',5555,icon,fanart,'') 
    addDir('[B][COLOR gold]Click Here to: [/COLOR][COLOR white]Get Real-Debrid[/COLOR][/B]','url',5556,icon,fanart,'')
    #addDir('[B][COLOR gold]Click Here to: [/COLOR][COLOR white]Get Premiumize[/COLOR][/B]','url',5557,icon,fanart,'')
	
def LiveMenu8():#
    addDir('[B][COLOR dodgerblue]********* Torrent HD 720p 2019 - 1999**********[/COLOR][/B]','url','',icon,fanart,'')
    addDir('[B][COLOR white]If A List Is Empty, Please Try Again[/COLOR][/B]','','',icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 720p - 2019 - Page 1[/COLOR][/B]','https://eztv.io/search/',72020153,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 720p - 2019 - Page 2[/COLOR][/B]','https://eztv.io/search/',72020154,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 720p - 2019 - Page 3[/COLOR][/B]','https://eztv.io/search/',72020155,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 720p - 2018 - Page 1[/COLOR][/B]','https://eztv.io/search/',72020156,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 720p - 2018 - Page 2[/COLOR][/B]','https://eztv.io/search/',72020157,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 720p - 2018 - Page 3[/COLOR][/B]','https://eztv.io/search/',72020158,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 720p - 2017 - Page 1[/COLOR][/B]','https://eztv.io/search/',72020159,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 720p - 2017 - Page 2[/COLOR][/B]','https://eztv.io/search/',72020160,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 720p - 2017 - Page 3[/COLOR][/B]','https://eztv.io/search/',72020161,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 720p - 2010[/COLOR][/B]','https://eztv.io/search/',72020162,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 720p - 2009[/COLOR][/B]','https://eztv.io/search/',72020163,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 720p - 2008[/COLOR][/B]','https://eztv.io/search/',72020164,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 720p - 2007[/COLOR][/B]','https://eztv.io/search/',72020165,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 720p - 2006[/COLOR][/B]','https://eztv.io/search/',72020166,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 720p - 2005[/COLOR][/B]','https://eztv.io/search/',72020167,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 720p - 2004[/COLOR][/B]','https://eztv.io/search/',72020168,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 720p - 2003[/COLOR][/B]','https://eztv.io/search/',72020169,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 720p - 2002[/COLOR][/B]','https://eztv.io/search/',72020170,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 720p - 2001[/COLOR][/B]','https://eztv.io/search/',72020171,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 720p - 2000[/COLOR][/B]','https://eztv.io/search/',72020172,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 720p - 1999[/COLOR][/B]','https://eztv.io/search/',72020173,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Search - For Movies[/COLOR][/B]','https://thepiratebay.vip/search/',2002,icon,fanart,'')
	
def LiveMenu10808():#
    addDir('[B][COLOR dodgerblue]********* Torrent HD 1080p 2019 - 1999**********[/COLOR][/B]','url','',icon,fanart,'')
    addDir('[B][COLOR white]If A List Is Empty, Please Try Again[/COLOR][/B]','','',icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 1080p - 2019 - Page 1[/COLOR][/B]','https://eztv.io/search/',108020153,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 1080p - 2019 - Page 2[/COLOR][/B]','https://eztv.io/search/',108020154,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 1080p - 2019 - Page 3[/COLOR][/B]','https://eztv.io/search/',108020155,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 1080p - 2018 - Page 1[/COLOR][/B]','https://eztv.io/search/',108020156,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 1080p - 2018 - Page 2[/COLOR][/B]','https://eztv.io/search/',108020157,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 1080p - 2018 - Page 3[/COLOR][/B]','https://eztv.io/search/',108020158,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 1080p - 2017 - Page 1[/COLOR][/B]','https://eztv.io/search/',108020159,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 1080p - 2017 - Page 2[/COLOR][/B]','https://eztv.io/search/',108020160,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 1080p - 2017 - Page 3[/COLOR][/B]','https://eztv.io/search/',108020161,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 1080p - 2010[/COLOR][/B]','https://eztv.io/search/',108020162,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 1080p - 2009[/COLOR][/B]','https://eztv.io/search/',108020163,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 1080p - 2008[/COLOR][/B]','https://eztv.io/search/',108020164,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 1080p - 2007[/COLOR][/B]','https://eztv.io/search/',108020165,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 1080p - 2006[/COLOR][/B]','https://eztv.io/search/',108020166,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 1080p - 2005[/COLOR][/B]','https://eztv.io/search/',108020167,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 1080p - 2004[/COLOR][/B]','https://eztv.io/search/',108020168,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 1080p - 2003[/COLOR][/B]','https://eztv.io/search/',108020169,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 1080p - 2002[/COLOR][/B]','https://eztv.io/search/',108020170,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 1080p - 2001[/COLOR][/B]','https://eztv.io/search/',108020171,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 1080p - 2000[/COLOR][/B]','https://eztv.io/search/',108020172,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 1080p - 1999[/COLOR][/B]','https://eztv.io/search/',108020173,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Search - For Movies[/COLOR][/B]','https://thepiratebay.vip/search/',2002,icon,fanart,'')
	
def LiveMenu21608():#
    addDir('[B][COLOR dodgerblue]********* Torrent HD 2160p 2019 - 1999**********[/COLOR][/B]','url','',icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 2160p - 2019 - Page 1[/COLOR][/B]','https://eztv.io/search/',216020153,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 2160p - 2019 - Page 2[/COLOR][/B]','https://eztv.io/search/',216020154,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 2160p - 2019 - Page 3[/COLOR][/B]','https://eztv.io/search/',216020155,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 2160p - 2018 - Page 1[/COLOR][/B]','https://eztv.io/search/',216020156,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 2160p - 2018 - Page 2[/COLOR][/B]','https://eztv.io/search/',216020157,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 2160p - 2018 - Page 3[/COLOR][/B]','https://eztv.io/search/',216020158,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 2160p - 2017 - Page 1[/COLOR][/B]','https://eztv.io/search/',216020159,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 2160p - 2017 - Page 2[/COLOR][/B]','https://eztv.io/search/',216020160,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 2160p - 2017 - Page 3[/COLOR][/B]','https://eztv.io/search/',216020161,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 2160p - 2010[/COLOR][/B]','https://eztv.io/search/',216020162,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 2160p - 2009[/COLOR][/B]','https://eztv.io/search/',216020163,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 2160p - 2008[/COLOR][/B]','https://eztv.io/search/',216020164,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 2160p - 2007[/COLOR][/B]','https://eztv.io/search/',216020165,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 2160p - 2006[/COLOR][/B]','https://eztv.io/search/',216020166,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 2160p - 2005[/COLOR][/B]','https://eztv.io/search/',216020167,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 2160p - 2004[/COLOR][/B]','https://eztv.io/search/',216020168,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 2160p - 2003[/COLOR][/B]','https://eztv.io/search/',216020169,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 2160p - 2002[/COLOR][/B]','https://eztv.io/search/',216020170,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 2160p - 2001[/COLOR][/B]','https://eztv.io/search/',216020171,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 2160p - 2000[/COLOR][/B]','https://eztv.io/search/',216020172,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Movies HD 2160p - 1999[/COLOR][/B]','https://eztv.io/search/',216020173,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Search - For Movies[/COLOR][/B]','https://thepiratebay.vip/search/',2002,icon,fanart,'')	
	
def LiveMenu9():#
    addDir('[B][COLOR dodgerblue]****** Warning Porn XXX Below ******[/COLOR][/B]','url','',icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Trending[/COLOR] [COLORred]XXX[/COLOR] [COLOR white]Movies[/COLOR][/B]','https://eztv.io/search/',20030,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Trending HD[/COLOR] [COLORred]XXX[/COLOR] [COLOR white]Movies[/COLOR][/B]','https://eztv.io/search/',20033,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Trending Clips[/COLOR] [COLORred]XXX[/COLOR] [COLOR white]Movies[/COLOR][/B]','https://eztv.io/search/',20038,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate Bay: [/COLOR][COLOR white]Trending Test[/COLOR] [COLORred]XXX[/COLOR] [COLOR white]Movies[/COLOR][/B]','https://eztv.io/search/',20039,icon,fanart,'')
    addDir('[B][COLOR dodgerblue]********* Please Come Again *********[/COLOR][/B]','url','',icon,fanart,'')
	
def play(url,name,pdialogue=None):
        from resources.modules import resolvers
        import xbmcgui
        
        url = url.strip()

        url = resolvers.resolve(url)
        if url == 'False':xbmcgui.Dialog().notification('A','This Link is Down, Try Another')
        if url.endswith('m3u8'):
            from resources.root import iptv
            iptv.listm3u(url)
        else:
                
            liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
            liz.setInfo(type='Video', infoLabels={'Title':name})
            liz.setProperty("IsPlayable","true")
            liz.setPath(url)

            if url.lower().startswith('plugin') and 'youtube' not in  url.lower():
                xbmc.executebuiltin('XBMC.PlayMedia('+url+')') 
                for i in range(8):
                    xbmc.sleep(500) ##sleep for 10 seconds, half each time
                    try:
                        #print 'condi'
                        if xbmc.getCondVisibility("Player.HasMedia") and xbmc.Player().isPlaying():
                            return True
                    except: pass
                print 'returning now'
                return False
            elif url.endswith('.ts'):
                playf4m(url,name)
                from resources.modules import  CustomPlayer
                import time

                player = CustomPlayer.MyXBMCPlayer()
                if (xbmc.Player().isPlaying() == 0):
                    quit()
                try:
                   
                        if player.urlplayed:
                            print 'yes played'
                            return
                        if time.time()-beforestart>4: return False
                    #xbmc.sleep(1000)
                except: pass

                print 'returning now'
                return False
            from resources.modules import  CustomPlayer
            import time

            player = CustomPlayer.MyXBMCPlayer()
            player.pdialogue=pdialogue
            start = time.time() 
            #xbmc.Player().play( liveLink,listitem)
            print 'going to play'
            import time
            beforestart=time.time()
            player.play( url, liz)
            if (xbmc.Player().isPlaying() == 0):
                quit()
            try:
                while player.is_active:
                    xbmc.sleep(400)
                   
                    if player.urlplayed:
                        print 'yes played'
                        return
                    if time.time()-beforestart>4: return False
                    #xbmc.sleep(1000)
            except: pass
            print 'not played',url
            xbmc.Player().stop()
            return
        
        
def playf4m(url, name):
                import urlparse,json
                if not any(i in url for i in ['.f4m', '.ts', '.m3u8']): raise Exception()
                ext = url.split('?')[0].split('&')[0].split('|')[0].rsplit('.')[-1].replace('/', '').lower()
                if not ext: ext = url
                if not ext in ['f4m', 'ts', 'm3u8']: raise Exception()

                params = urlparse.parse_qs(url)

                try: proxy = params['proxy'][0]
                except: proxy = None

                try: proxy_use_chunks = json.loads(params['proxy_for_chunks'][0])
                except: proxy_use_chunks = True

                try: maxbitrate = int(params['maxbitrate'][0])
                except: maxbitrate = 0

                try: simpleDownloader = json.loads(params['simpledownloader'][0])
                except: simpleDownloader = False

                try: auth_string = params['auth'][0]
                except: auth_string = ''


                try:
                   streamtype = params['streamtype'][0]
                except:
                   if ext =='ts': streamtype = 'TSDOWNLOADER'
                   elif ext =='m3u8': streamtype = 'HLS'
                   else: streamtype = 'HDS'

                try: swf = params['swf'][0]
                except: swf = None

                from F4mProxy import f4mProxyHelper
                return f4mProxyHelper().playF4mLink(url, name, proxy, proxy_use_chunks, maxbitrate, simpleDownloader, auth_string, streamtype, False, swf)
        
def log(text):
    file = open(logfile,"w+")
    file.write(str(text))
    
    

        
def regex_from_to(text, from_string, to_string, excluding=True):
    import re,string
    if excluding:
        try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
        except: r = ''
    else:
        try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
        except: r = ''
    return r


def regex_get_all(text, start_with, end_with):
    import re
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r





def addDir(name,url,mode,iconimage,fanart,description):
    import xbmcgui,xbmcplugin,urllib,sys
    u=sys.argv[0]+"?url="+url+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
    liz.setProperty('fanart_image', fanart)
    if mode==87:
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    else:
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok
    xbmcplugin.endOfDirectory


def OPEN_URL(url):
    import requests
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    link = requests.session().get(url, headers=headers, verify=False).text
    link = link.encode('ascii', 'ignore')
    return link

def ServerChecker():
	import requests,base64
	try:
		requests.get(base64.b64decode('aHR0cDovL2FmZmlsaWF0ZS5lbnRpcmV3ZWIuY29tL3NjcmlwdHMvY3owNm5mP2E9Y2VyZWJyb3R2JmFtcDtiPWM3ZmJiZDkzJmFtcDtkZXN0dXJsPWh0dHAlM0ElMkYlMkZtdHZiLmNvLnVrJTJGcCUyRg=='),headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'},verify=False,timeout=4).text
	except:
		pass
		
		
def main_menu2(search):

    kodi.create_item({'mode': ""}, '[COLOR gold]Search Results: [/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks(search)


	
def main_menu4():
    basefolder = "http://avadl.uploadt.com/DL7/Film/X265/"

    kodi.create_item({'mode': ""}, '[COLOR gold]H265 Movies List: [/COLOR]', is_folder=False, is_playable=False)

    GetFolderList("http://avadl.uploadt.com/DL7/Film/X265/")


	
def main_menu5():
    basefolder = "http://avadl.uploadt.com/DL7/Film/"

    kodi.create_item({'mode': ""}, '[COLOR gold]Movies List (some H265): [/COLOR]', is_folder=False, is_playable=False)

    GetFolderList2("http://avadl.uploadt.com/DL7/Film/")


	
def main_menu20150():
    basefolder = "http://aitvn.com/content/kungfu/"

    kodi.create_item({'mode': ""}, '[COLOR gold]Movies List - Kung Fu: [/COLOR]', is_folder=False, is_playable=False)

    GetFolderList3("http://aitvn.com/content/kungfu/")


	
def main_menu20151():
    basefolder = "http://fromv.ir/vip/Movie/Collection/GodZilla/"

    kodi.create_item({'mode': ""}, '[COLOR gold]Movies List - Kung Fu: [/COLOR]', is_folder=False, is_playable=False)

    GetFolderList4("http://fromv.ir/vip/Movie/Collection/GodZilla/")


	
def main_menu20152():
    basefolder = "http://dl2.funsaber.net/movie/97/08/"

    kodi.create_item({'mode': ""}, '[COLOR gold]Movies List - Pirate List 1: [/COLOR]', is_folder=False, is_playable=False)

    GetFolderList5("http://dl2.funsaber.net/movie/97/08/")


	
def main_menu6():
    basefolder = "http://avadl.uploadt.com/DL7/Animation/"

    kodi.create_item({'mode': ""}, '[COLOR gold]Animation: [/COLOR]', is_folder=False, is_playable=False)

    GetFolderList6("http://avadl.uploadt.com/DL7/Animation/")


	
def main_menu7():
    basefolder = "http://avadl.uploadt.com/DL4/Film/"

    kodi.create_item({'mode': ""}, '[COLOR gold]Animation: [/COLOR]', is_folder=False, is_playable=False)

    GetFolderList7("http://avadl.uploadt.com/DL4/Film/")


		
def GetTorLinks(url):
    r = requests.get(url, headers=header)
    plain_text = r.text
    soup = BeautifulSoup(plain_text)
    for link in soup.findAll('a'):
        #xbmc.log( link.get('href') , 2)
        if "magnet" in link.get('href'):
            name = link.get('href').split("&dn=")
            name = name[1].split("&tr=")
            link = link.get('href')
            lable = urllib.unquote(name[0]).decode('utf8')
            make_link(link, link, lable.replace('.', ' ').replace('+', ' ') , link)
            #xbmc.log( link.get('href') , 2)
			
def GetFolderList(url):
    basefolder = "http://avadl.uploadt.com/DL7/Film/X265/"
    lable = "name?"
    r = requests.get(url, headers=header)
    plain_text = r.text
    soup = BeautifulSoup(plain_text)
    for link in soup.findAll('a'):
        #xbmc.log( link.get('href') , 2)
        mlink = link.get('href')
        if ".zip" in mlink:
            continue
        if "/" in mlink:
            continue
        lable = urllib.unquote_plus(link.get('href'))
        make_link2(basefolder+mlink, basefolder+mlink, lable.replace('.', ' ').replace('+', ' ').replace('20%', ' ') , link)
            #xbmc.log( link.get('href') , 2)
			
def GetFolderList2(url):
    basefolder = "http://avadl.uploadt.com/DL7/Film/"
    lable = "name?"
    r = requests.get(url, headers=header)
    plain_text = r.text
    soup = BeautifulSoup(plain_text)
    for link in soup.findAll('a'):
        xbmc.log( link.get('href') , 2)
        mlink = link.get('href')
        if ".zip" in mlink:
            continue
        if "/" in mlink:
            continue
        lable = urllib.unquote_plus(link.get('href'))
        make_link2(basefolder+mlink, basefolder+mlink, lable.replace('.', ' ').replace('+', ' ').replace('20%', ' ') , link)
            #xbmc.log( link.get('href') , 2)
			
def GetFolderList3(url):
    basefolder = "http://aitvn.com/content/kungfu/"
    lable = "name?"
    r = requests.get(url, headers=header)
    plain_text = r.text
    soup = BeautifulSoup(plain_text)
    for link in soup.findAll('a'):
        xbmc.log( link.get('href') , 2)
        mlink = link.get('href')
        if ".zip" in mlink:
            continue
        if "/" in mlink:
            continue
        lable = urllib.unquote_plus(link.get('href'))
        make_link2(basefolder+mlink, basefolder+mlink, lable.replace('.', ' ').replace('+', ' ').replace('20%', ' ') , link)
            #xbmc.log( link.get('href') , 2)
			
def GetFolderList4(url):
    basefolder = "http://fromv.ir/vip/Movie/Collection/GodZilla/"
    lable = "name?"
    r = requests.get(url, headers=header)
    plain_text = r.text
    soup = BeautifulSoup(plain_text)
    for link in soup.findAll('a'):
        xbmc.log( link.get('href') , 2)
        mlink = link.get('href')
        if ".zip" in mlink:
            continue
        if "/" in mlink:
            continue
        lable = urllib.unquote_plus(link.get('href'))
        make_link2(basefolder+mlink, basefolder+mlink, lable.replace('.', ' ').replace('+', ' ').replace('20%', ' ') , link)
            #xbmc.log( link.get('href') , 2)
			
def GetFolderList5(url):
    basefolder = "http://dl2.funsaber.net/movie/97/08/"
    lable = "name?"
    r = requests.get(url, headers=header)
    plain_text = r.text
    soup = BeautifulSoup(plain_text)
    for link in soup.findAll('a'):
        xbmc.log( link.get('href') , 2)
        mlink = link.get('href')
        if ".zip" in mlink:
            continue
        if "/" in mlink:
            continue
        lable = urllib.unquote_plus(link.get('href'))
        make_link2(basefolder+mlink, basefolder+mlink, lable.replace('.', ' ').replace('+', ' ').replace('20%', ' ') , link)
            #xbmc.log( link.get('href') , 2)
			
def GetFolderList6(url):
    basefolder = "http://avadl.uploadt.com/DL4/Film/"
    lable = "name?"
    r = requests.get(url, headers=header)
    plain_text = r.text
    soup = BeautifulSoup(plain_text)
    for link in soup.findAll('a'):
        xbmc.log( link.get('href') , 2)
        mlink = link.get('href')
        if ".zip" in mlink:
            continue
        if "/" in mlink:
            continue
        lable = urllib.unquote_plus(link.get('href'))
        make_link2(basefolder+mlink, basefolder+mlink, lable.replace('.', ' ').replace('+', ' ').replace('20%', ' ') , link)
            #xbmc.log( link.get('href') , 2)
			
def GetFolderList7(url):
    basefolder = "http://avadl.uploadt.com/DL4/Film/"
    lable = "name?"
    r = requests.get(url, headers=header)
    plain_text = r.text
    soup = BeautifulSoup(plain_text)
    for link in soup.findAll('a'):
        xbmc.log( link.get('href') , 2)
        mlink = link.get('href')
        if ".zip" in mlink:
            continue
        if "/" in mlink:
            continue
        lable = urllib.unquote_plus(link.get('href'))
        make_link2(basefolder+mlink, basefolder+mlink, lable.replace('.', ' ').replace('+', ' ').replace('20%', ' ') , link)
            #xbmc.log( link.get('href') , 2)


def main_menu3():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Trending Movies for last 48 hours[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/top/201')



def main_menu30():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top XXX Movies for last 48 hours[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/top/501')



def main_menu31():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top HD Movies for last 48 hours[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/top/207')



def main_menu32():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top 4K UHD Movies[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/uhd/0/99/0')



def main_menu33():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top HD XXX Movies for last 48 hours[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/top/505')



def main_menu34():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top 3D Movies for last 48 hours[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/top/209')



def main_menu35():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Trending TV Shows for last 48 hours[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/top/205')



def main_menu36():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top HD TV Shows for last 48 hours[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/top/208')



def main_menu37():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Trending Horror Movies[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/horror/0/99/207')



def main_menu38():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay XXX Movies Clips[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/top/506')



def main_menu39():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay XXX Movies Test[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/user/Borusssia/')



def main_menu20153():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Movie Streams - Page 1[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/browse/207/0/7//')



def main_menu20154():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Movie Streams - Page 2[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/browse/207/1/7//')



def main_menu20155():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Movie Streams - Page 3[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/browse/207/2/7//')



def main_menu20156():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Movie Streams - Page 4[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/browse/207/3/7//')



def main_menu20157():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Movie Streams - Page 5[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/browse/207/4/7//')



def main_menu20158():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Movie Streams - Page 6[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/browse/207/5/7//')



def main_menu20159():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Movie Streams - Page 7[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/browse/207/6/7//')



def main_menu20160():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Movie Streams - Page 8[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/browse/207/7/7//')



def main_menu20161():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Movie Streams - Page 9[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/browse/207/8/7//')



def main_menu20162():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Movie Streams - Page 10[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/browse/207/9/7//')



def main_menu20163():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Movie Streams - Page 11[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/browse/207/10/7//')



def main_menu20164():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Movie Streams - Page 12[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/browse/207/11/7//')



def main_menu20165():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Movie Streams - Page 13[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/browse/207/12/7//')



def main_menu20166():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Movie Streams - Page 14[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/browse/207/13/7//')



def main_menu20167():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Movie Streams - Page 15[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/browse/207/14/7//')



def main_menu20168():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Movie Streams - Page 16[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/browse/207/15/7//')



def main_menu20169():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Movie Streams - Page 17[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/browse/207/16/7//')



def main_menu20170():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Movie Streams - Page 18[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/browse/207/17/7//')



def main_menu20171():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Movie Streams - Page 19[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/browse/207/18/7//')



def main_menu20172():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay Top Movie Streams - Page 20[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/browse/207/19/7//')



def main_menu72020153():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 720p - Year 2019 - Page [/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/720p+2019/0/7/207//')



def main_menu72020154():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 720p - Year 2019 - Page 2[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/720p+2019/1/7/207//')



def main_menu72020155():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 720p - Year 2019- Page 3[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/720p+2019/2/7/207//')



def main_menu72020156():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 720p - Year 2018 - Page 1[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/720p+2018/0/7/207//')



def main_menu72020157():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 720p - Year 2018 - Page 2[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/720p+2018/1/7/207//')



def main_menu72020158():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 720p - Year 2018 - Page 3[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/720p+2018/2/7/207//')



def main_menu72020159():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 720p - Year 2013 - Page 1[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/720p+2017/0/7/207//')



def main_menu72020160():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 720p - Year 2012 - Page 2[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/720p+2017/1/7/207//')



def main_menu72020161():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 720p - Year 2011 - Page 3[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/720p+2017/2/7/207//')



def main_menu72020162():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 720p - Year 2010[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/720p+2010/0/7/207//')



def main_menu72020163():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 720p - Year 2009[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/720p+2009/0/7/207//')



def main_menu72020164():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 720p - Year 2008[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/720p+2008/0/7/207//')



def main_menu72020165():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 720p - Year 2007[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/720p+2007/0/7/207//')



def main_menu72020166():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 720p - Year 2006[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/720p+2006/0/7/207//')



def main_menu72020167():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 720p - Year 2005[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/720p+2005/0/7/207//')



def main_menu72020168():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 720p - Year 2004[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/720p+2004/0/7/207//')



def main_menu72020169():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 720p - Year 2003[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/720p+2003/0/7/207//')



def main_menu72020170():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 720p - Year 2002[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/720p+2002/0/7/207//')



def main_menu72020171():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 720p - Year 2001[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/720p+2001/0/7/207//')



def main_menu72020172():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 720p - Year 2000[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/720p+2000/0/7/207//')


	
def main_menu72020173():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 720p - Year 1999[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/720p+1999/0/7/207//')


	
def main_menu108020153():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 1080p - Year 2019 - Page [/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/1080p+2019/0/7/207//')



def main_menu108020154():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 1080p - Year 2019 - Page 2[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/1080p+2019/1/7/207//')



def main_menu108020155():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 1080p - Year 2019- Page 3[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/1080p+2019/2/7/207//')



def main_menu108020156():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 1080p - Year 2018 - Page 1[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/1080p+2018/0/7/207//')



def main_menu108020157():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 1080p - Year 2018 - Page 2[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/1080p+2018/1/7/207//')



def main_menu108020158():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 1080p - Year 2018 - Page 3[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/1080p+2018/2/7/207//')



def main_menu108020159():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 1080p - Year 2013 - Page 1[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/1080p+2017/0/7/207//')



def main_menu108020160():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 1080p - Year 2012 - Page 2[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/1080p+2017/1/7/207//')



def main_menu108020161():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 1080p - Year 2011 - Page 3[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/1080p+2017/2/7/207//')



def main_menu108020162():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 1080p - Year 2010[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/1080p+2010/0/7/207//')



def main_menu108020163():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 1080p - Year 2009[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/1080p+2009/0/7/207//')



def main_menu108020164():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 1080p - Year 2008[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/1080p+2008/0/7/207//')



def main_menu108020165():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 1080p - Year 2007[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/1080p+2007/0/7/207//')



def main_menu108020166():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 1080p - Year 2006[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/1080p+2006/0/7/207//')



def main_menu108020167():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 1080p - Year 2005[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/1080p+2005/0/7/207//')



def main_menu108020168():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 1080p - Year 2004[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/1080p+2004/0/7/207//')



def main_menu108020169():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 1080p - Year 2003[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/1080p+2003/0/7/207//')



def main_menu108020170():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 1080p - Year 2002[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/1080p+2002/0/7/207//')



def main_menu108020171():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 1080p - Year 2001[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/1080p+2001/0/7/207//')



def main_menu108020172():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 1080p - Year 2000[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/1080p+2000/0/7/207//')


	
def main_menu108020173():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 1080p - Year 1999[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/1080p+1999/0/7/207//')

	
	
def main_menu216020153():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 2160p - Year 2019 - Page [/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/2160p+2019/0/7/207//')



def main_menu216020154():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 2160p - Year 2019 - Page 2[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/2160p+2019/1/7/207//')



def main_menu216020155():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 2160p - Year 2019- Page 3[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/2160p+2019/2/7/207//')



def main_menu216020156():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 2160p - Year 2018 - Page 1[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/2160p+2018/0/7/207//')



def main_menu216020157():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 2160p - Year 2018 - Page 2[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/2160p+2018/1/7/207//')



def main_menu216020158():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 2160p - Year 2018 - Page 3[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/2160p+2018/2/7/207//')



def main_menu216020159():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 2160p - Year 2013 - Page 1[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/2160p+2017/0/7/207//')



def main_menu216020160():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 2160p - Year 2012 - Page 2[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/2160p+2017/1/7/207//')



def main_menu216020161():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 2160p - Year 2011 - Page 3[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/2160p+2017/2/7/207//')



def main_menu216020164():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 2160p - Year 2008[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/2160p+2008/0/7/207//')



def main_menu216020165():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 2160p - Year 2007[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/2160p+2007/0/7/207//')



def main_menu216020166():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 2160p - Year 2006[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/2160p+2006/0/7/207//')



def main_menu216020167():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 2160p - Year 2005[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/2160p+2005/0/7/207//')



def main_menu216020168():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 2160p - Year 2004[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/2160p+2004/0/7/207//')



def main_menu216020169():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 2160p - Year 2003[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/2160p+2003/0/7/207//')



def main_menu216020170():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 2160p - Year 2002[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/2160p+2002/0/7/207//')



def main_menu216020171():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 2160p - Year 2001[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/2160p+2001/0/7/207//')



def main_menu216020172():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 2160p - Year 2000[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/2160p+2000/0/7/207//')


	
def main_menu216020173():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Torrent HD 2160p - Year 1999[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/search/2160p+1999/0/7/207//')

	
	
def main_menu216020173001():

    kodi.create_item({'mode': ""}, '[COLOR gold]Pirate Bay - Top 100 Music[/COLOR]', is_folder=False, is_playable=False)

    GetTorLinks('https://proxyofthepiratebay.com/top/203//')

		

def StartTorrents(): 
    addDir('[B][COLOR gold]Pirate: [/COLOR][COLOR orange]TO USE THIS SECTION YOU MUST HAVE[/COLOR][/B]','url','',icon,fanart,'') 
    addDir('[B][COLOR gold]Pirate: [/COLOR][COLOR orange]Real-Debrid[/COLOR][/B]','url','',icon,fanart,'') 

    addDir('[B][COLOR gold]Pirate: [/COLOR][COLOR green]Open ResolveURL Settings[/COLOR][/B] (authorize accounts)','url',5555,icon,fanart,'') 
	
    addDir('[B][COLOR gold]Pirate: [/COLOR][COLOR white]Pirate Bay[/COLOR][/B] (Search)','https://thepiratebay.vip/search/',2002,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate: [/COLOR][COLOR white]GlowTorrents[/COLOR][/B] (Search)','http://glodls.to/search_results.php?search=',2009,icon,fanart,'')
    addDir('[B][COLOR gold]Pirate: [/COLOR][COLOR white]EZTV[/COLOR][/B] (Search)','https://eztv.io/search/',2002,icon,fanart,'')

    addDir('[B][COLOR gold]Pirate: [/COLOR][COLOR white]Pirate Bay[/COLOR][/B] (Top 200)','https://eztv.io/search/',2003,icon,fanart,'')

    addDir('[B][COLOR gold]Pirate: [/COLOR][COLOR lightgreen]Click Here to Get Real-Debrid[/COLOR][/B]','url',5556,icon,fanart,'')
    #addDir('[B][COLOR gold]Pirate: [/COLOR][COLOR lightgreen]Click Here to Get Premiumize[/COLOR][/B]','url',5557,icon,fanart,'')

def play_link(link):
   
    #logger.log('Playing Link: |%s|' % (link), log_utils.LOGDEBUG)
    hmf = urlresolver.HostedMediaFile(url=link)
    if not hmf:
        #logger.log('Indirect hoster_url not supported by urlresolver: %s' % (link))
        kodi.notify('Link Not Supported: %s' % (link), duration=7500)
        return False
    #logger.log('Link Supported: |%s|' % (link), log_utils.LOGDEBUG)
    
    try:
        stream_url = hmf.resolve()
        if not stream_url or not isinstance(stream_url, basestring):
            try: msg = stream_url.msg
            except: msg = link
            raise Exception(msg)
    except Exception as e:
        try: msg = str(e)
        except: msg = link
        kodi.notify('Resolve Failed: %s' % (msg), duration=7500)
        return False
    #logger.log('Link Resolved: |%s|%s|' % (link, stream_url), log_utils.LOGDEBUG)
        
    listitem = xbmcgui.ListItem(path=stream_url)
  
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def make_link(index, link, label, path):
    menu_items = []
    queries = {'mode': "", 'index': index, 'path': path}
    menu_items.append(('Delete Link', 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
    queries = {'mode': "", 'index': index, 'path': path}
    menu_items.append(('Edit Link', 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
    kodi.create_item({'mode': 7777, 'url': link}, label, is_folder=False, is_playable=True, menu_items=menu_items)	
	
def make_link2(index, link, label, path):
    menu_items = []
    queries = {'mode': "", 'index': index, 'path': path}
    menu_items.append(('Delete Link', 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
    queries = {'mode': "", 'index': index, 'path': path}
    menu_items.append(('Edit Link', 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
    kodi.create_item({'mode': 9999, 'url': link}, label, is_folder=False, is_playable=True, menu_items=menu_items)	
	
def SearchTors(site):
        search_entered = ''	
        keyboard = xbmc.Keyboard(search_entered, 'Enter Movie / TV Show Name For Torrent Search')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText().replace(' ','%20')   ##search_entered = keyboard.getText().replace(' ','+')
            if search_entered == 0:
                return False        
        #if search_entered == None or search_entered == "":
        #    main_menu()   
        #xbmc.log( search_entered , 2)
        #global mysearch		
        main_menu2(site+"/"+search_entered+"") 
		
def SearchTors2(site):
        search_entered = ''	
        keyboard = xbmc.Keyboard(search_entered, 'Enter Movie / TV Show Name For Torrent Search')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText().replace(' ','+')   ##search_entered = keyboard.getText().replace(' ','+')
            if search_entered == 0:
                return False        
        #if search_entered == None or search_entered == "":
        #    main_menu()   
        xbmc.log( site+""+search_entered+"&incldead=Search&order=asc" , 2)
        #global mysearch		
        main_menu2(site+""+search_entered+"&incldead=Search&order=asc") 
    
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
query=None
type=None
# OpenELEQ: query & type-parameter (added 2 lines above)


def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'

myplatform = platform()






def MainH(): 
    addDir("Welcome to Hector!", "", "", hectoricon)
    addDir("", "", "", hectoricon)
    addDir("[COLOR gold]EPG IPTV CHANNELS[/COLOR]", "http://vistatv.online/VistaEPG.m3u", 3, hectoricon)
    data = urllib2.urlopen("http://www.vistatv.online/m3u8/").read()
    data = data.split("\n") # then split it into lines
    count = 1
    for line in data:
        #line = line.split(" ") 
        addDir("[COLOR green]Hectors IPTV Server[/COLOR] :[COLOR gold]"+str(count)+"[/COLOR]", str(line), 2, hectoricon)
        #xbmc.log(str(line),2)
        count = count+1
    xbmcplugin.endOfDirectory(int(sys.argv[1]))











import urllib

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    iconimage=urllib.unquote_plus(params["iconimage"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass
try:
    description=urllib.unquote_plus(params["description"])
except:
    pass
try:
    query=urllib.unquote_plus(params["query"])
except:
    pass
try:
    type=urllib.unquote_plus(params["type"])
except:
    pass
# OpenELEQ: query & type-parameter (added 8 lines above)

if mode==None or url==None or len(url)<1:
    home()


elif mode==1:
    from resources.root import ukgeo
    ukgeo.get(url)
    
    
elif mode==2:
    from resources.root import webscrapers
    webscrapers.get(url)
    
    
elif mode==3:
    from resources.root import iptv
    iptv.get(url)
    
elif mode==4:
    from resources.root import android
    android.get(url)
    
    
elif mode==50:
    from resources.root import iptv
    iptv.listm3u(url)
    

    
elif mode==10:
    play(url,name)
    


elif mode==1000:
    from resources.root import ukgeo
    ukgeo.cat()
    
elif mode==2000:
    from resources.root import webscrapers
    android.cat()
	
elif mode==2001:
    StartTorrents()
	
elif mode==2002:
    SearchTors(url)
	
elif mode==2003:
    main_menu3()
	
elif mode==20030:
    main_menu30()
	
elif mode==20031:
    main_menu31()
	
elif mode==20032:
    main_menu32()
	
elif mode==20033:
    main_menu33()
	
elif mode==20034:
    main_menu34()
	
elif mode==20035:
    main_menu35()
	
elif mode==20036:
    main_menu36()
	
elif mode==20037:
    main_menu37()
	
elif mode==20038:
    main_menu38()
	
elif mode==20039:
    main_menu39()
	
elif mode==2009:
    SearchTors2(url)
	
elif mode==2015:
    main_menu4()
	
elif mode==2016:
    main_menu5()
	
elif mode==2017:
    main_menu6()
	
elif mode==2018:
    main_menu7()
	
elif mode==20150:
    main_menu20150()
	
elif mode==20151:
    main_menu20151()
	
elif mode==20152:
    main_menu20152()
	
elif mode==20153:
    main_menu20153()
	
elif mode==20154:
    main_menu20154()
	
elif mode==20155:
    main_menu20155()
	
elif mode==20156:
    main_menu20156()
	
elif mode==20157:
    main_menu20157()
	
elif mode==20158:
    main_menu20158()
	
elif mode==20159:
    main_menu20159()
	
elif mode==20160:
    main_menu20160()
	
elif mode==20161:
    main_menu20161()
	
elif mode==20162:
    main_menu20162()
	
elif mode==20163:
    main_menu20163()
	
elif mode==20164:
    main_menu20164()
	
elif mode==20165:
    main_menu20165()
	
elif mode==20166:
    main_menu20166()
	
elif mode==20167:
    main_menu20167()
	
elif mode==20168:
    main_menu20168()
	
elif mode==20169:
    main_menu20169()
	
elif mode==20170:
    main_menu20170()
	
elif mode==20171:
    main_menu20171()
	
elif mode==20172:
    main_menu20172()
	
elif mode==72020153:
    main_menu72020153()
	
elif mode==72020154:
    main_menu72020154()
	
elif mode==72020155:
    main_menu72020155()
	
elif mode==72020156:
    main_menu72020156()
	
elif mode==72020157:
    main_menu72020157()
	
elif mode==72020158:
    main_menu72020158()
	
elif mode==72020159:
    main_menu72020159()
	
elif mode==72020160:
    main_menu72020160()
	
elif mode==72020161:
    main_menu72020161()
	
elif mode==72020162:
    main_menu72020162()
	
elif mode==72020163:
    main_menu72020163()
	
elif mode==72020164:
    main_menu72020164()
	
elif mode==72020165:
    main_menu72020165()
	
elif mode==72020166:
    main_menu72020166()
	
elif mode==72020167:
    main_menu72020167()
	
elif mode==72020168:
    main_menu72020168()
	
elif mode==72020169:
    main_menu72020169()
	
elif mode==72020170:
    main_menu72020170()
	
elif mode==72020171:
    main_menu72020171()
	
elif mode==72020172:
    main_menu72020172()

elif mode==72020173:
    main_menu72020173()
	
elif mode==108020153:
    main_menu108020153()
	
elif mode==108020154:
    main_menu108020154()
	
elif mode==108020155:
    main_menu108020155()
	
elif mode==108020156:
    main_menu108020156()
	
elif mode==108020157:
    main_menu108020157()
	
elif mode==108020158:
    main_menu108020158()
	
elif mode==108020159:
    main_menu108020159()
	
elif mode==108020160:
    main_menu108020160()
	
elif mode==108020161:
    main_menu108020161()
	
elif mode==108020162:
    main_menu108020162()
	
elif mode==108020163:
    main_menu108020163()
	
elif mode==108020164:
    main_menu108020164()
	
elif mode==108020165:
    main_menu108020165()
	
elif mode==108020166:
    main_menu108020166()
	
elif mode==108020167:
    main_menu108020167()
	
elif mode==108020168:
    main_menu108020168()
	
elif mode==108020169:
    main_menu108020169()
	
elif mode==108020170:
    main_menu108020170()
	
elif mode==108020171:
    main_menu108020171()
	
elif mode==108020172:
    main_menu108020172()

elif mode==108020173:
    main_menu108020173()	

elif mode==216020153:
    main_menu216020153()
	
elif mode==216020154:
    main_menu216020154()
	
elif mode==216020155:
    main_menu216020155()
	
elif mode==216020156:
    main_menu216020156()
	
elif mode==216020157:
    main_menu216020157()
	
elif mode==216020158:
    main_menu216020158()
	
elif mode==216020159:
    main_menu216020159()
	
elif mode==216020160:
    main_menu216020160()
	
elif mode==216020161:
    main_menu216020161()
	
elif mode==216020162:
    main_menu216020162()
	
elif mode==216020163:
    main_menu216020163()
	
elif mode==216020164:
    main_menu216020164()
	
elif mode==216020165:
    main_menu216020165()
	
elif mode==216020166:
    main_menu216020166()
	
elif mode==216020167:
    main_menu216020167()
	
elif mode==216020168:
    main_menu216020168()
	
elif mode==216020169:
    main_menu216020169()
	
elif mode==216020170:
    main_menu216020170()
	
elif mode==216020171:
    main_menu216020171()
	
elif mode==216020172:
    main_menu216020172()

elif mode==216020173:
    main_menu216020173()
	
elif mode==216020173001:
    main_menu216020173001()
		
elif mode==3000:


    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.elysium/?action=movieNavigator",return)')
    
elif mode==4000:


    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.elysium/?action=tvNavigator",return)')

elif mode==9000:


    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.mtb.vr8fg8b/?action=searchNavigator",return)')

elif mode==9001:


    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.mtb.vr8fg8b/?action=tvNavigator",return)')

elif mode==9002:


    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.mtb.vr8fg8b/?action=movieNavigator",return)')

elif mode==9003:


    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.mtb.vr8fg8b/?action=tvNavigator",return)')

elif mode==9004:


    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.mtb.vr8fg8b/?action=toolNavigator",return)')
	
elif mode==90004444:


    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.movietheaterbutter.auto/?action=searchNavigator",return)')
	
elif mode==90014444:


    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.movietheaterbutter.auto/?action=tvNavigator",return)')

elif mode==90024444:


    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.movietheaterbutter.auto/?action=movieNavigator",return)')

elif mode==90034444:


    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.movietheaterbutter.auto/?action=tvNavigator",return)')

elif mode==90044444:


    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.movietheaterbutter.auto/?action=toolNavigator",return)')	
    
elif mode==5000:


    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.covenant/?action=movieNavigator",return)')
    
elif mode==5001:


    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.covenant/?action=tvNavigator",return)')
    
elif mode==5002:


    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.poseidon/?action=movieNavigator",return)')
    
elif mode==5003:


    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.poseidon/?action=tvNavigator",return)')

elif mode==5004:


    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.mtb.vr8fg8b/?action=movieSearch",return)')

elif mode==5005:


    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.mtb.vr8fg8b/?action=tvNavigator",return)')
    
elif mode==5006:


    xbmc.executebuiltin('ActivateWindow(10025,"plugin://script.module.streamhublive/?description&iconimage=http%3a%2f%2fwww.broadbandtvnews.com%2fwp-content%2fuploads%2f2017%2f04%2fTVPlayer.png&mode=1&name=%5bCOLOR%20white%5d%5bB%5dTv%20Player%5b%2fCOLOR%5d%5b%2fB%5d&url=tvplayer",return)')

elif mode==5007:


    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.showboxarize2/?action=movieNavigator",return)')
    
elif mode==5008:


    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.showboxarize2/?action=tvNavigator",return)')
	
elif mode == 5555:
    urlresolver.display_settings()
    exit()
	
elif mode == 5556:
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'http://real-debrid.com/?id=1811400' ) )
    else:
        opensite = webbrowser . open('http://real-debrid.com/?id=1811400')
    exit()
	
elif mode == 5557:
    if myplatform == 'android': # Android 
        opensite = xbmc.executebuiltin( 'StartAndroidActivity(,android.intent.action.VIEW,,%s)' % ( 'https://www.premiumize.me/ref/545890157' ) )
    else:
        opensite = webbrowser . open('https://www.premiumize.me/ref/545890157')
    exit()
	
elif mode == 6666:
    LiveMenu()
	
elif mode == 6667:
    LiveMenu1()
	
elif mode == 6668:
    LiveMenu2()
	
elif mode == 6669:
    LiveMenu3()
	
elif mode == 6670:
    LiveMenu4()
	
elif mode == 66704444:
    LiveMenu44444()	
	
elif mode == 6671:
    LiveMenu5()
	
elif mode == 6672:
    LiveMenu6()
	
elif mode == 6673:
    LiveMenu7()
	
elif mode == 6674:
    LiveMenu8()
	
elif mode == 10806674:
    LiveMenu10808()	
	
elif mode == 21606674:
    LiveMenu21608()
	
elif mode == 6675:
    LiveMenu9()
	
elif mode == 7777:
    play_link(url)
    
elif mode==9999:
    import xbmcgui,xbmcplugin
    from resources.modules import resolvers
    url = resolvers.resolve(url)
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels='')
    liz.setProperty("IsPlayable","true")
    liz.setPath(url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    

import xbmcplugin
xbmcplugin.endOfDirectory(int(sys.argv[1]))