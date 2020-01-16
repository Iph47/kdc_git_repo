#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcaddon, xbmcplugin, os

addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path').decode('utf-8')

name = "I Love Prog-House"
url = "https://bit.ly/35h33uz"
iconimage = os.path.join(addon_path,"icon.png")

liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="audio", infoLabels={ "Title": name } )
xbmc.Player ().play(url, liz, True)