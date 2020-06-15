#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys,re,requests
import xbmc,xbmcgui,xbmcplugin,xbmcaddon

__addon_handle__ = int(sys.argv[1])
xbmcplugin.setContent(__addon_handle__,'movies')

def fix_encoding(path):
	if sys.platform.startswith('win'):return unicode(path,'utf-8')
	else:return unicode(path,'utf-8').encode('ISO-8859-1')

__addon__ =  xbmcaddon.Addon(id='script.module.hls.cache')
__addon_path__ = fix_encoding(__addon__.getAddonInfo('path'))

def clear_dir(dir_path):
	if os.path.exists(dir_path):

		for name in os.listdir(dir_path):
			path = os.path.join(dir_path,name)

			if os.path.isfile(path):
				try:os.unlink(path)
				except:pass

def cache_loader(m3u8_url,m3u8_headers={},segment_headers={}):

	ip = __addon__.getSetting('ip')
	if not ip:
		ip = xbmc.getIPAddress()
		__addon__.setSetting('ip',ip)
	port = __addon__.getSetting('port')

	cache_forward = int(__addon__.getSetting('cache_forward'))
	download_delay = int(__addon__.getSetting('download_delay'))
	cache_multiplier = int(__addon__.getSetting('cache_multiplier'))

	out = int(5)
	count = int(0)
	duration = int(0)
	chunk_size = int(1024*cache_multiplier)

	content_type = None
	sess = requests.Session()
	cache_path = os.path.abspath(os.path.join(__addon_path__,'cache'))
	new_m3u8_path = os.path.abspath(os.path.join(cache_path,'hls.m3u8'))
	req = sess.get(url=m3u8_url,stream=False,allow_redirects=False,timeout=out,headers=m3u8_headers)

	with open(new_m3u8_path,'wb',buffering=chunk_size) as m3u8:
		for line in req.iter_lines():
			line = line.strip()
			if line:

				if line.startswith('http'):
					m3u8.write('{0}\n'.format('http://'+ ip +':'+ port +'/cache/' + str(count)))
					count +=1
				else:m3u8.write('{0}\n'.format(line))

	count = 0
	for line in req.iter_lines():
		line = line.strip()
		if line:

			if line.startswith('#EXTINF:'):
				match = re.compile(r'#EXTINF:(\d+)',re.DOTALL).search(line)
				if match:duration = int(match.group(1))

			if line.startswith('http'):
				req = sess.get(url=line,stream=True,allow_redirects=False,timeout=out,headers=segment_headers)

				content_type = req.headers.get('Content-Type')
				if content_type:
					match = re.compile(r'(.+?);',re.DOTALL).search(content_type)
					if match:content_type = match.group(1)

				with open(os.path.abspath(os.path.join(cache_path,str(count))),'wb',buffering=chunk_size) as fi:
					while True:

						chunk = req.raw.read(chunk_size)
						if not chunk:break
						else:fi.write(chunk)

				if count == cache_forward:
					listitem = xbmcgui.ListItem(path='http://'+ ip +':'+ port +'/cache/hls.m3u8')
					if content_type == None:content_type = 'application/octet-stream'
					listitem.setMimeType(content_type)
					listitem.setContentLookup(False)
					xbmcplugin.setResolvedUrl(handle=__addon_handle__,succeeded=True,listitem=listitem)

				elif count  > cache_forward:
					if download_delay > 0:xbmc.sleep(duration * download_delay)
					if not xbmc.getCondVisibility('Player.HasMedia'):
							if os.path.exists(cache_path):clear_dir(cache_path)
							break

				count +=1

	while True:
		if not xbmc.getCondVisibility('Player.HasMedia'):
			clear_dir(cache_path)
			break
		else:xbmc.sleep(1500)