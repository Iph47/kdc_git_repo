#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys,time,hsk,xbmc,xbmcgui,math,re
_params_= hsk.get_params()

_BASE_URL_   = 'https://xcine.tv'
_MOVIES_URL_ = _BASE_URL_ + '/filme1'
_SERIES_URL_ = _BASE_URL_ + '/serien1'
hsk.set_content_type(content_type='movies')

def get_url_specific_headers(url):

	if url:
		if '?' in url:url = url.split('?')[0]
		return {
			'Origin':hsk.get_base_url(url),
			'Referer':url,
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'} # https://deviceatlas.com/blog/list-of-user-agent-strings #
	else:return {}

def get_url(url,headers_url):

	if('?' in url and '=' in url and not'?server=' in url and not '?key=' in url):

		post_data_dict = dict(x.strip().split('=') for x in url.split('?')[1].split('&')if '=' in x)
		post_data_dict.update({'load':'full-page'})

		return hsk.post_cfscraper_sess(url=url,data=post_data_dict,delay=5,headers_dict=get_url_specific_headers(headers_url))

	return hsk.get_cfscraper_sess(url=url,delay=5,headers_dict=get_url_specific_headers(headers_url))

def get_orderby_class_by_name(url,ontent,sort_method_name):# category,country,sort #

	match = hsk.regex_search('<select class="orderby" name="'+sort_method_name+'">[\s\S]*?<\/select>',content)
	if match:

		sort_list=[]
		category='';country='';sort=''
		for value,title in hsk.regex_findall('<option value="(.*?)"[\s\S]*?>(.*?)<\/option>',match.group(0)):

			if sort_method_name == 'category':category=value
			elif sort_method_name == 'country':country=value
			elif sort_method_name == 'sort':sort=value

			if value:sort_list.append({'sort_url':url + '?category='+category+'&country='+country+'&sort='+sort+'&key=&sort_type=desc','sort_title':title})
			if (sort_method_name == 'category' or sort_method_name == 'country'):sort_list.sort(key=lambda i:i.get('sort_title'),reverse=False)
		return sort_list

def get_page_data(content):
	match = hsk.regex_search('<\/li><li class="active"><a class="actived" href="javascript:">(\d+)<\/a><\/li><li><a href="(.+?)">(\d+)<\/a>',content)
	if match:return {'active_page_nr':match.group(1),'next_page_url':match.group(2),'next_page_nr':match.group(3)}

def get_video_list(content):
	match = hsk.regex_search('<div class="group-film-small">[\s\S]*?<\/a>\s<\/div>',content)
	if match:return hsk.regex_findall('<a href="(.+?)"[\s\S]*?(?:;|data-src=")(.+?)(?:&|")[\s\S]*?title-film">(.*?)<\/b>',match.group(0))

def get_video_infos(content):
	regex ='<ul class="infomation-film">'
	regex +='[\s\S]*?Originaltitel: <span>([^>]*?)<\/span>'
	regex +='[\s\S]*?Genre: <span>([^>]*?)<\/span>'
	regex +='[\s\S]*?Bewerten: <span>([^>]*?)<\/span>'
	regex +='[\s\S]*?Erscheinungsjahr: <span>([^>]*?)<\/span>'
	regex +='[\s\S]*?Regisseur: <span>([^>]*?)<\/span>'
	regex +='[\s\S]*?Schauspieler: <span>([^>]*?)<\/span>'
	regex +='[\s\S]*?Land: <span>([^>]*?)<\/span>'
	regex +='[\s\S]*?Laufzeit: <span>([^>]*?)<\/span>'
	regex +='[\s\S]*?<p class="content-film">([^>]*?)<\/p>'
	match = hsk.regex_search(regex,content)
	if match:

		cast = match.group(6)
		if ',' in cast:cast = [tuple(s for s in cast.split(','))]
		else:cast = [tuple(cast)]
		duration = hsk.regex_search('(\d+)',match.group(8))
		if duration:duration = int(duration.group(1))*60
		else:duration = 0

		return {'originaltitle':hsk.html_parser.unescape(match.group(1).decode('utf8')),'genre':match.group(2),'rating':match.group(3),'userrating':match.group(3),'year':match.group(4),'director':match.group(5),'cast':cast,'country':match.group(7),'duration':duration,'plot':hsk.html_parser.unescape(match.group(9).decode('utf8'))}

def get_big_play_button_url(content):
	match = hsk.regex_search('<a class="play-btn play-icon"\shref="(.+?)"',content)
	if match:
		url = match.group(1)
		if url.startswith('http'):return url

def get_episodes(content):
	return hsk.regex_findall('<a (?:class="current"|class="watched"|class="new")[\s\S]*?href="(.+?)" data-episode-id="(.+?)" title="(.+?)">',content)

def get_server_data(content,episode_id=''):
	movie_id = ''
	match = hsk.regex_search('data-movie-id="(.+?)"',content)
	if match:movie_id = match.group(1)

	if (episode_id == ''):
		match = hsk.regex_search('episode-id="(.+?)"',content)
		if match:episode_id = match.group(1)

	if (not movie_id == '' and not episode_id == ''):
		return {'server 0':_BASE_URL_ + '/movie/load-stream/{0}/{1}?'.format(movie_id,episode_id),
		'server 1':_BASE_URL_ + '/movie/load-stream/{0}/{1}?server=1'.format(movie_id,episode_id),
		'server 2':_BASE_URL_ + '/movie/load-stream/{0}/{1}?server=2'.format(movie_id,episode_id)}

def get_server0_and_server1_video_urls(content):
	return hsk.regex_findall('RESOLUTION=\d+x([\d]+)([^#]+)',content)

def get_server2_video_urls(content):
	match = hsk.regex_search('var sources = (\[.*?\]);',content)
	if match:return hsk.regex_findall('"label":"(.+?)","type":"(.+?)","file":"(.+?)"',match.group(1))
	else:return []

def video_file_downloader(url,title,dp_mode=1):
	save_path = hsk.dialog_browse(type=0,heading='',shares='files',mask='',useThumbs=False,treatAsFolder=False,defaultt='',enableMultiple=False)
	if save_path and hsk.path_exists(save_path):hsk.request_download_file_dp(file_name=hsk.clean_title(title),file_url=url,save_path=save_path,timeout=30,headers_dict={},dp_mode=dp_mode)

if _params_ is None:
	items=[]
	items.append({'title':'Filme','url':'','image':hsk.addon_icon,'fanart':hsk.addon_fanart,'imode':1,'add_info':{},'add_params':{},'add_contextmenu':[['Set the list view mode',3],['Set the info view mode',4]],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	items.append({'title':'Serien','url':'','image':hsk.addon_icon,'fanart':hsk.addon_fanart,'imode':2,'add_info':{},'add_params':{},'add_contextmenu':[['Set the list view mode',3],['Set the info view mode',4]],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	items.append({'title':'[COLOR gold]Suche[/COLOR]','url':_BASE_URL_+'/search?key=','image':hsk.addon_icon,'fanart':hsk.addon_fanart,'imode':3,'add_info':{},'add_params':{'search':'search'},'add_contextmenu':[['Set the list view mode',3],['Set the info view mode',4]],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	hsk.add_items(items)
	view = hsk.get_addon_settings('list_view_mode')
	if not view == '' and not view == '0': hsk.set_view_mode(view)

elif _params_.get('imode') == 1:
	items=[]
	items.append({'title':'Filme','url':_MOVIES_URL_,'image':hsk.addon_icon,'fanart':hsk.addon_fanart,'imode':3,'add_info':{},'add_params':{},'add_contextmenu':[['Set the list view mode',3],['Set the info view mode',4]],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	items.append({'title':'Genre','url':_MOVIES_URL_,'image':hsk.addon_icon,'fanart':hsk.addon_fanart,'imode':4,'add_info':{},'add_params':{'sort_method':'category'},'add_contextmenu':[['Set the list view mode',3],['Set the info view mode',4]],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	items.append({'title':'Land','url':_MOVIES_URL_,'image':hsk.addon_icon,'fanart':hsk.addon_fanart,'imode':4,'add_info':{},'add_params':{'sort_method':'country'},'add_contextmenu':[['Set the list view mode',3],['Set the info view mode',4]],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	items.append({'title':'Sort','url':_MOVIES_URL_,'image':hsk.addon_icon,'fanart':hsk.addon_fanart,'imode':4,'add_info':{},'add_params':{'sort_method':'sort'},'add_contextmenu':[['Set the list view mode',3],['Set the info view mode',4]],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	hsk.add_items(items)
	view = hsk.get_addon_settings('list_view_mode')
	if not view == '' and not view == '0': hsk.set_view_mode(view)

elif _params_.get('imode') == 2:
	items=[]
	items.append({'title':'Serien','url':_SERIES_URL_,'image':hsk.addon_icon,'fanart':hsk.addon_fanart,'imode':3,'add_info':{},'add_params':{},'add_contextmenu':[['Set the list view mode',3],['Set the info view mode',4]],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	items.append({'title':'Genre','url':_SERIES_URL_,'image':hsk.addon_icon,'fanart':hsk.addon_fanart,'imode':4,'add_info':{},'add_params':{'sort_method':'category'},'add_contextmenu':[['Set the list view mode',3],['Set the info view mode',4]],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	items.append({'title':'Land','url':_SERIES_URL_,'image':hsk.addon_icon,'fanart':hsk.addon_fanart,'imode':4,'add_info':{},'add_params':{'sort_method':'country'},'add_contextmenu':[['Set the list view mode',3],['Set the info view mode',4]],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	items.append({'title':'Sort','url':_SERIES_URL_,'image':hsk.addon_icon,'fanart':hsk.addon_fanart,'imode':4,'add_info':{},'add_params':{'sort_method':'sort'},'add_contextmenu':[['Set the list view mode',3],['Set the info view mode',4]],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	hsk.add_items(items)
	view = hsk.get_addon_settings('list_view_mode')
	if not view == '' and not view == '0': hsk.set_view_mode(view)

elif _params_.get('imode') == 3:

	base_url = _params_.get('url')

	if _params_.get('search') == 'search':
		search = hsk.dialog_imput_alphanum(heading='Suche ?')
		if search:base_url = base_url + search
		else:sys.exit(0)

	content = get_url(url=base_url,headers_url=base_url).content
	page_data = get_page_data(content)

	items=[]
	for url,img,title in get_video_list(content):
		items.append({'title':hsk.html_parser.unescape(title.decode('utf8')),'url':url,'image':img,'fanart':hsk.addon_fanart,'imode':5,'add_info':{},'add_params':{},'add_contextmenu':[['Set the list view mode',3],['Set the info view mode',4]],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	if page_data:items.append({'title':'[COLOR gold]Seite( ' + page_data['active_page_nr'] + ' )>>[/COLOR]','url':_BASE_URL_ +'/'+ page_data['next_page_url'] ,'image':'','fanart':hsk.addon_fanart,'imode':3,'add_info':{},'add_params':{},'add_contextmenu':[['Set the list view mode',3],['Set the info view mode',4]],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	hsk.add_items(items)
	view = hsk.get_addon_settings('list_view_mode')
	if not view == '' and not view == '0': hsk.set_view_mode(view)

elif _params_.get('imode') == 4:

	base_url = _params_.get('url')
	sort_method = _params_.get('sort_method')
	content = get_url(url=base_url,headers_url=base_url).content

	items=[]
	for sort_dict in get_orderby_class_by_name(base_url,content,sort_method):
		items.append({'title':sort_dict['sort_title'],'url':sort_dict['sort_url'],'image':'','fanart':hsk.addon_fanart,'imode':3,'add_info':{},'add_params':{},'add_contextmenu':[['Set the list view mode',3],['Set the info view mode',4]],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	hsk.add_items(items)
	view = hsk.get_addon_settings('list_view_mode')
	if not view == '' and not view == '0': hsk.set_view_mode(view)

elif _params_.get('imode') == 5:

	info_dict = {}
	base_title = _params_.get('title')
	base_img = _params_.get('image')
	base_url = _params_.get('url')

	episode_id = _params_.get('episode_id','')
	content = get_url(url=base_url,headers_url=base_url).content

	video_infos = get_video_infos(content)
	if video_infos:info_dict.update(video_infos)

	big_play_button_url = get_big_play_button_url(content)
	if not big_play_button_url:big_play_button_url=base_url

	if big_play_button_url:content = get_url(url=big_play_button_url,headers_url=base_url).content
	else:sys.exit(0)

	items=[]
	if (('-staffel-' in big_play_button_url or '/folge-' in big_play_button_url) and (episode_id == '')):
		for url,id,title in get_episodes(content):
			items.append({'title':title,'url':url,'image':base_img,'fanart':hsk.addon_fanart,'imode':5,'add_info':info_dict,'add_params':{'episode_id':id},'add_contextmenu':[['Set the list view mode',3],['Set the info view mode',4]],'type':'video','playlist':False,'is_folder':True,'is_playable':False})
	else:
		server_data = get_server_data(content,episode_id)
		server_selection = hsk.get_addon_settings('server_selection')

		if server_selection == 'SERVER 1' or server_selection == 'SERVER 1 & 2':

			try:
				content = get_url(url=server_data['server 0'],headers_url=big_play_button_url).content

				match = hsk.regex_search('urlVideo = "([^"]+)',content)
				if match:
					url = match.group(1)
					content = get_url(url=url,headers_url=big_play_button_url).content
					m3u8_base_url = hsk.dir_name(url)

					server0_and_server1_video_urls = get_server0_and_server1_video_urls(content)
					if server0_and_server1_video_urls:

						for qualy,url in server0_and_server1_video_urls:
							sort_qualy = int(re.sub('\D+','',qualy))
							url = m3u8_base_url +'/'+ url.strip()
							items.append({'title':base_title + ' | S1 | ' + qualy,'url':url,'image':base_img,'fanart':hsk.addon_fanart,'imode':6,'add_info':info_dict,'add_params':{'video_base_url':big_play_button_url,'server':'0','sort':sort_qualy},'add_contextmenu':[['Set the list view mode',3],['Set the info view mode',4]],'type':'video','playlist':False,'is_folder':False,'is_playable':False})

					else:items.append({'title':base_title + ' | S1 | Play','url':url,'image':base_img,'fanart':hsk.addon_fanart,'imode':6,'add_info':info_dict,'add_params':{'video_base_url':big_play_button_url,'server':'0','sort':'0'},'add_contextmenu':[['Set the list view mode',3],['Set the info view mode',4]],'type':'video','playlist':False,'is_folder':False,'is_playable':False})

			except:pass

		if server_selection == 'SERVER 2' or server_selection == 'SERVER 1 & 2':

			try:
				content = get_url(url=server_data['server 2'],headers_url=big_play_button_url).content

				for qualy,type,url in get_server2_video_urls(content):
					sort_qualy = int(re.sub('\D+','',qualy))
					url = hsk.normalize_url_backslashes(url)
					items.append({'title':base_title + ' | S2 | ' + qualy,'url':url,'image':base_img,'fanart':hsk.addon_fanart,'imode':6,'add_info':info_dict,'add_params':{'video_base_url':big_play_button_url,'server':'2','sort':sort_qualy},'add_contextmenu':[['Download video with DP',1],['Download video with BG',2],['Set the list view mode',3],['Set the info view mode',4]],'type':'video','playlist':False,'is_folder':False,'is_playable':False})

			except:pass

	if len(items) > 0:hsk.add_items(sorted(items,key=lambda i:i.get('add_params').get('sort'),reverse=True))
	else:
		hsk.dialog_notification_info(heading='Video info:',message='No video found !',time=2000,sound=True)
		sys.exit(0)

	if video_infos:
		view = hsk.get_addon_settings('info_view_mode')
		if not view == '' and not view == '0': hsk.set_view_mode(view)
	else:
		view = hsk.get_addon_settings('list_view_mode')
		if not view == '' and not view == '0': hsk.set_view_mode(view)

elif _params_.get('imode') == 6:

	url = _params_.get('url')
	server = _params_.get('server')
	video_base_url = _params_.get('video_base_url')

	if server == '0':hsk.set_resolved_url(url +'|Origin=' +_BASE_URL_+ '&Referer=' + video_base_url)
	elif server == '1':hsk.set_resolved_url(url)
	elif server == '2':hsk.set_resolved_url(url)

elif _params_.get('cmode') == 1:video_file_downloader(_params_.get('url'),_params_.get('title'),dp_mode=1)
elif _params_.get('cmode') == 2:video_file_downloader(_params_.get('url'),_params_.get('title'),dp_mode=2)

elif _params_.get('cmode') == 3:
	view = hsk.get_view_mode()
	hsk.set_addon_settings('list_view_mode',view)
	hsk.dialog_notification_info(heading='List view mode:',message='Set list view mode : ' + view,time=2000,sound=True)

elif _params_.get('cmode') == 4:
	view = hsk.get_view_mode()
	hsk.set_addon_settings('info_view_mode',view)
	hsk.dialog_notification_info(heading='Info view mode:',message='Set info view mode : ' + view,time=2000,sound=True)

hsk.set_end_of_directory(succeeded=True,updateListing=False,cacheToDisc=True)