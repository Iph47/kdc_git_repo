#!/usr/bin/python
# -*- coding: utf-8 -*-
from hsk_tools import*
_params_= get_params()

_BASE_URL_   = 'https://hdfilme.cc'
_MOVIES_URL_ = 'https://hdfilme.cc/filme1'
_SERIES_URL_ = 'https://hdfilme.cc/serien1'

def get_url_specific_headers(url):

	if url:
		if '?' in url:url = url.split('?')[0]
		return {
			'Origin':get_base_url(url),
			'Referer':url,
			'User-Agent':'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'} # https://deviceatlas.com/blog/list-of-user-agent-strings #
	else:return {}

def get_url(url,headers_url):

	if('?' in url and '=' in url and not'?server=' in url and not '?key=' in url):

		post_data_dict = dict(x.strip().split('=') for x in url.split('?')[1].split('&')if '=' in x)
		post_data_dict.update({'load':'full-page'})

		return post_cfscraper_sess(url=url,data=post_data_dict,delay=3,headers_dict=get_url_specific_headers(headers_url))

	return get_cfscraper_sess(url=url,delay=3,headers_dict=get_url_specific_headers(headers_url))

def get_orderby_class_by_name(url,ontent,sort_method_name):# category,country,sort #

	match = regex_search('<select class="orderby" name="'+sort_method_name+'">[\s\S]*?<\/select>',content)# https://regex101.com/r/JDeyrm/14 #
	if match:

		sort_list=[]
		category='';country='';sort=''
		for value,title in regex_findall('<option value="(.*?)"[\s\S]*?>(.*?)<\/option>',match.group(0)):# https://regex101.com/r/JDeyrm/15 #:

			if sort_method_name == 'category':category=value
			elif sort_method_name == 'country':country=value
			elif sort_method_name == 'sort':sort=value

			if value:sort_list.append({'sort_url':url + '?category='+category+'&country='+country+'&sort='+sort+'&key=&sort_type=desc','sort_title':title})
		return sort_list

def get_page_data(content):
	match = regex_search('<\/li><li class="active"><a>(\d+)<\/a><\/li><li><a href="(.+?)">(\d+)<\/a>',content)# https://regex101.com/r/JDeyrm/6 #
	if match:return {'active_page_nr':match.group(1),'next_page_url':match.group(2),'next_page_nr':match.group(3)}

def get_video_list(content):
	return regex_findall('<li>\s<div class="box-product clearfix"[\s\S]+?href="(.+?)"[\s\S]+?data-src="(.+?)"[\s\S]+?title="(.+?)">\s(.+?)\s<\/a>',content)# https://regex101.com/r/JDeyrm/17 #

def get_big_play_button_url(content):
	match = regex_search('<div class="big-play-btn">\s<a href="(.+?)"',content)# https://regex101.com/r/JDeyrm/8 #
	if match:return match.group(1)

def get_episodes(content):
	return regex_findall('<a (?:class="current"|class="watched"|class="new")[\s\S]*?href="(.+?)" data-episode-id="(.+?)" title="(.+?)">',content)# https://regex101.com/r/LoyYf2/3 #

def get_server_data(content,episode_id='',server='0'):
	movie_id = ''
	match = regex_search('data-movie-id="(.+?)"',content)# https://regex101.com/r/JDeyrm/9 #
	if match:movie_id = match.group(1)

	if (episode_id == ''):
		match = regex_search('episode-id="(.+?)"',content)
		if match:episode_id = match.group(1)

	if (not movie_id == '' and not episode_id == ''):
		if server=='0':return {'url':'https://hdfilme.cc/movie/load-stream/{0}/{1}?'.format(movie_id,episode_id),'server':'0'}
		elif server=='1':return {'url':'https://hdfilme.cc/movie/load-stream/{0}/{1}?server=1'.format(movie_id,episode_id),'server':'1'}
		elif server=='2':return {'url':'https://hdfilme.cc/movie/load-stream/{0}/{1}?server=2'.format(movie_id,episode_id),'server':'2'}

def get_server0_and_server1_video_urls(content):
	return regex_findall('RESOLUTION=\d+x([\d]+)([^#]+)',content)

def server0_m3u8_editor(req,dir_path):
	new_m3u8_path = os.path.abspath(os.path.join(dir_path,'new.m3u8'))
	with open(new_m3u8_path,'wb') as m3u8:
		for line in req.iter_lines():
			line = line.strip()
			if line:
				if line.startswith('#EXT-X-VERSION:'):m3u8.write('{0}\n{1}\n'.format(line,'#EXT-X-BYTERANGE:6@0'))
				else:m3u8.write('{0}\n'.format(line))
	return new_m3u8_path

def get_server2_video_urls(content):
	match = regex_search('var sources = (\[.*?\]);',content)# https://regex101.com/r/JDeyrm/11 #
	if match:return regex_findall('"label":"(.+?)","type":"(.+?)","file":"(.+?)"',match.group(1))# https://regex101.com/r/JDeyrm/10 #

def video_file_downloader(url,title,dp_mode=1):
	save_path = dialog_browse(type=0,heading='',shares='files',mask='',useThumbs=False,treatAsFolder=False,defaultt='',enableMultiple=False)
	if save_path and path_exists(save_path):request_download_file_dp(file_name=clean_title(title),file_url=url,save_path=save_path,timeout=30,headers_dict={},dp_mode=dp_mode)

if _params_ is None:
	items=[]
	items.append({'title':'Filme','url':'','image':addon_icon,'fanart':addon_fanart,'imode':1,'add_info':{},'add_params':{},'add_contextmenu':[],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	items.append({'title':'Serien','url':'','image':addon_icon,'fanart':addon_fanart,'imode':2,'add_info':{},'add_params':{},'add_contextmenu':[],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	items.append({'title':'[COLOR lime]Suche[/COLOR]','url':'https://hdfilme.cc/search?key=','image':addon_icon,'fanart':addon_fanart,'imode':3,'add_info':{},'add_params':{'search':'search'},'add_contextmenu':[['Download-Item',1]],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	add_items(items)

elif _params_.get('imode') == 1:
	items=[]
	items.append({'title':'Filme','url':_MOVIES_URL_,'image':addon_icon,'fanart':addon_fanart,'imode':3,'add_info':{},'add_params':{},'add_contextmenu':[],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	items.append({'title':'Genre','url':_MOVIES_URL_,'image':addon_icon,'fanart':addon_fanart,'imode':4,'add_info':{},'add_params':{'sort_method':'category'},'add_contextmenu':[],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	items.append({'title':'Land','url':_MOVIES_URL_,'image':addon_icon,'fanart':addon_fanart,'imode':4,'add_info':{},'add_params':{'sort_method':'country'},'add_contextmenu':[],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	items.append({'title':'Sort','url':_MOVIES_URL_,'image':addon_icon,'fanart':addon_fanart,'imode':4,'add_info':{},'add_params':{'sort_method':'sort'},'add_contextmenu':[],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	add_items(items)

elif _params_.get('imode') == 2:
	items=[]
	items.append({'title':'Serien','url':_SERIES_URL_,'image':addon_icon,'fanart':addon_fanart,'imode':3,'add_info':{},'add_params':{},'add_contextmenu':[],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	items.append({'title':'Genre','url':_SERIES_URL_,'image':addon_icon,'fanart':addon_fanart,'imode':4,'add_info':{},'add_params':{'sort_method':'category'},'add_contextmenu':[],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	items.append({'title':'Land','url':_SERIES_URL_,'image':addon_icon,'fanart':addon_fanart,'imode':4,'add_info':{},'add_params':{'sort_method':'country'},'add_contextmenu':[],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	items.append({'title':'Sort','url':_SERIES_URL_,'image':addon_icon,'fanart':addon_fanart,'imode':4,'add_info':{},'add_params':{'sort_method':'sort'},'add_contextmenu':[],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	add_items(items)

elif _params_.get('imode') == 3:

	base_url = _params_.get('url')

	if _params_.get('search') == 'search':
		search = dialog_imput_alphanum(heading='Suche ?')
		if search:base_url = base_url + search
		else:sys.exit(0)

	content = get_url(url=base_url,headers_url=base_url).content
	page_data = get_page_data(content)

	items=[]
	for url,img,title1,title2 in get_video_list(content):
		items.append({'title':title2,'url':url,'image':img,'fanart':addon_fanart,'imode':5,'add_info':{},'add_params':{},'add_contextmenu':[],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	if page_data:items.append({'title':'[COLOR lime]Seite( ' + page_data['active_page_nr'] + ' )>>[/COLOR]','url':_BASE_URL_ +'/'+ page_data['next_page_url'] ,'image':'','fanart':addon_fanart,'imode':3,'add_info':{},'add_params':{},'add_contextmenu':[],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	add_items(items)

elif _params_.get('imode') == 4:

	base_url = _params_.get('url')
	sort_method = _params_.get('sort_method')
	content = get_url(url=base_url,headers_url=base_url).content

	items=[]
	for sort_dict in get_orderby_class_by_name(base_url,content,sort_method):
		items.append({'title':sort_dict['sort_title'],'url':sort_dict['sort_url'],'image':'','fanart':addon_fanart,'imode':3,'add_info':{},'add_params':{},'add_contextmenu':[],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	add_items(items)

elif _params_.get('imode') == 5:

	base_title = _params_.get('title')
	base_img = _params_.get('image')
	base_url = _params_.get('url')

	episode_id = _params_.get('episode_id','')
	content = get_url(url=base_url,headers_url=base_url).content

	big_play_button_url = get_big_play_button_url(content)
	if not big_play_button_url:big_play_button_url=base_url
	content = get_url(url=big_play_button_url,headers_url=base_url).content

	items=[]
	if ('staffel' in big_play_button_url and episode_id == ''):
		for url,id,title in get_episodes(content):
			items.append({'title':title,'url':url,'image':base_img,'fanart':addon_fanart,'imode':5,'add_info':{},'add_params':{'episode_id':id},'add_contextmenu':[],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	else:
		server_data = get_server_data(content,episode_id,get_addon_settings('server_selection'))
		content = get_url(url=server_data['url'],headers_url=big_play_button_url).content

		server = server_data['server']
		if server in ('0','1'):

			match = regex_search('urlVideo = "([^"]+)',content)
			if match:
				url = match.group(1)
				content = get_url(url=url,headers_url=big_play_button_url).content
				m3u8_base_url = get_base_url(url)

				for qualy,url in get_server0_and_server1_video_urls(content):
					url = m3u8_base_url + url.strip()
					items.append({'title':base_title +' | '+ qualy,'url':url,'image':base_img,'fanart':addon_fanart,'imode':6,'add_info':{},'add_params':{'video_base_url':big_play_button_url,'server':server},'add_contextmenu':[],'type':'video','playlist':False,'is_folder':False,'is_playable':False})
			
		elif server == '2':
			for qualy,type,url in get_server2_video_urls(content):
				url = normalize_url_backslashes(url)
				items.append({'title':base_title +' | '+ qualy,'url':url,'image':base_img,'fanart':addon_fanart,'imode':6,'add_info':{},'add_params':{'video_base_url':big_play_button_url,'server':server},'add_contextmenu':[['Download-Video-DP',1],['Download-Video-BG',2]],'type':'video','playlist':False,'is_folder':False,'is_playable':False})

	add_items(items)

elif _params_.get('imode') == 6:

	url = _params_.get('url')
	server = _params_.get('server')
	video_base_url = _params_.get('video_base_url')

	if server == '0':
		cfs = get_url(url=url,headers_url=video_base_url)
		new_m3u8_path = server0_m3u8_editor(cfs,addon_path)
		set_resolved_url(new_m3u8_path)

	elif server == '1':set_resolved_url(url)
	elif server == '2':set_resolved_url(url)

elif _params_.get('imode') == 7:set_resolved_url(_params_.get('url'))
elif _params_.get('cmode') == 1:video_file_downloader(_params_.get('url'),_params_.get('title'),dp_mode=1)
elif _params_.get('cmode') == 2:video_file_downloader(_params_.get('url'),_params_.get('title'),dp_mode=2)

set_content_type(content_type='movies')
set_end_of_directory(succeeded=True,updateListing=False,cacheToDisc=True)