#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc,xbmcgui,xbmcplugin,xbmcaddon
from contextlib import closing
from urlparse import urlparse
import sys,os,urllib,re,cPickle,time
player_ = xbmc.Player()

import urlresolver
#import resolveurl as urlresolver

def fix_encoding(path):
	if sys.platform.startswith('win'):return unicode(path,'utf-8')
	else:return unicode(path,'utf-8').encode('iso-8859-1')

addon_ =  xbmcaddon.Addon()
addon_path_ = fix_encoding(addon_.getAddonInfo('path'))
cfi_ = os.path.join(addon_path_,'cookie')

sys.path.append(os.path.join(addon_path_,'resources','lib'))
import requests,cfscrape

def get_color_text(color,text):
	return '[COLOR '+color+']'+text+'[/COLOR]'

def get_dialog_numeric(heading=''):
	return xbmcgui.Dialog().numeric(0,heading)

def get_search_keyboard():
	return urllib.quote(xbmcgui.Dialog().input(get_color_text('lime','Search ?'), type=xbmcgui.INPUT_ALPHANUM).strip())

def save_cookies(res,cfi):
	cookie_list = res.raw.headers.getlist('Set-Cookie')
	if cookie_list:
		cookie_dict_list = []
		for cookie in cookie_list:
			cookie_dict_list.append(dict(x.strip().split('=') for x in cookie.split(';')if '=' in x))
		if cookie_dict_list:
			with open(cfi,'wb') as fi:cPickle.dump(cookie_dict_list,fi)

def set_cookies(ses,cfi):
	if os.path.exists(cfi):
		ses.cookies.clear()
		with open(cfi,'rb') as fi:
			for cd in cPickle.load(fi):ses.cookies.update(cd)

def get_cf_url(url,stream=False,timeout=30,allow_redirects=False,scraper_delay=3,headers_dict={}):
	ses = requests.Session()
	set_cookies(ses,cfi_)
	with closing(cfscrape.create_scraper(delay=scraper_delay,sess=ses)) as scraper:
		cfs = scraper.get(url,stream=stream,timeout=timeout,allow_redirects=allow_redirects,headers=headers_dict)
		save_cookies(cfs,cfi_)
	return cfs

def post_cf_url(url,data,stream=False,timeout=30,allow_redirects=True,scraper_delay=3,headers_dict={}):
	ses = requests.Session()
	set_cookies(ses,cfi_)
	with closing(cfscrape.create_scraper(delay=scraper_delay,sess=ses)) as scraper:
		cfs = scraper.post(url,data=data,stream=stream,timeout=timeout,allow_redirects=allow_redirects,headers=headers_dict)
		save_cookies(cfs,cfi_)
	return cfs

def add_items(items_array_dict=[['','','','',{},{}]], set_items_type_int=0, set_content_type_int=0, set_params_dict=True, is_folder_bool=True, Is_playable_bool=False):

	item_type_dict ={0:'music',1:'video',2:'pictures',3:'game'}
	content_type_dict={0:'files',1:'songs',2:'artists',3:'albums',4:'movies',5:'tvshows',6:'episodes',7:'musicvideos',8:'videos',9:'images',10:'games'}

	xbmcplugin.setContent(int(sys.argv[1]),content_type_dict[set_content_type_int])

	for array_dict in items_array_dict:

		listitem=xbmcgui.ListItem(label=array_dict[0],iconImage='DefaultFolder.png',thumbnailImage=array_dict[2],path=array_dict[1])

		infolabels_dict={'Title':array_dict[0]}
		infolabels_dict.update(array_dict[4])

		params_dict={'Title':array_dict[0],'Url':array_dict[1],'Img':array_dict[2]}
		params_dict.update(array_dict[5])

		listitem.setInfo(type=item_type_dict[set_items_type_int],infoLabels=infolabels_dict)
		listitem.setProperty('fanart_image',array_dict[3])

		if(set_params_dict == True):url=sys.argv[0] +'?'+ urllib.quote_plus(str(params_dict))
		if(set_params_dict == False):url=array_dict[1]

		if(Is_playable_bool == True):listitem.setProperty('IsPlayable','true')
		if(Is_playable_bool == False):listitem.setProperty('IsPlayable','false')

		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=listitem,isFolder=is_folder_bool,totalItems=len(items_array_dict))

	xbmcplugin.endOfDirectory(handle=int(sys.argv[1]),succeeded=True,updateListing=False,cacheToDisc=True)

def get_regex_search(regex,content):
	return re.compile(regex,re.DOTALL).search(content)

def get_regex_findall(regex,content):
	return re.compile(regex,re.DOTALL).findall(content)

def get_resolved_url(url):
	source = urlresolver.HostedMediaFile(url=url)
	if source.valid_url():return source.resolve()
	else:return ''

def get_xbmc_player(title='',url='',image='',type='video',windowed=False):
	listitem = xbmcgui.ListItem(label=title,iconImage=image,thumbnailImage=image,path=url)
	listitem.setInfo(type=type,infoLabels={'Title':title})
	listitem.setProperty('IsPlayable','true')
	xbmc.Player().play(item=url,listitem=listitem,windowed=windowed)
	sys.exit(0)

def get_genres(url,content,sort):

	genres = get_regex_search('<select class="orderby" name="category">[\s\S]*?\s<option value="">Genre<\/option>[\s\S]*?<\/select>',content)
	if genres:

		items_array_dict=[]
		for genre,title in get_regex_findall('<option value="(\S+)">(.*?)<\/option>',genres.group(0)):
			items_array_dict.append([title.strip(),url,'','',{},{'Run':'2','Genre':genre,'Sort':sort}])

		add_items(items_array_dict, set_items_type_int=1, set_content_type_int=0, set_params_dict=True, is_folder_bool=True, Is_playable_bool=False)

def get_entries(content):

	next_page = get_regex_search('<a href="(\S+\?\S+)">›<\/a>',content)
	max_page = get_regex_search('<a href="(\S+\?\S+)">»<\/a>',content)
	active_page = get_regex_search('<li class="active"><a>(\d+)<\/a><\/li>',content)

	if active_page:page_nr = active_page.group(1)
	else:active_page = '1'
	
	items_array_dict=[]
	for img,url,title in get_regex_findall('<div class="box-product clearfix"[\s\S]+?data-src="(.+?)"[\s\S]+?<a href="(.+?)"[\s\S]+?>(.+?)<\/a>',content):
		title = title.strip()
		items_array_dict.append([title,url,img,'',{},{'Run':'6'}])

	if next_page:
		next_page_url = 'https://hdfilme.cc/{0}'.format(next_page.group(1)).replace('&amp;','&')
		color_text = get_color_text('lime','Next >')
		items_array_dict.append([color_text,next_page_url,'','',{},{'Run':'4'}])

	if max_page:
		max_page_url = 'https://hdfilme.cc/{0}'.format(max_page.group(1)).replace('&amp;','&')
		color_text = get_color_text('lime','Page '+ page_nr)
		items_array_dict.append([color_text,max_page_url,'','',{},{'Run':'4','Page':'nr'}])

	add_items(items_array_dict, set_items_type_int=1, set_content_type_int=0, set_params_dict=True, is_folder_bool=True, Is_playable_bool=False)

def get_params_dict():
	argv = urllib.unquote_plus(sys.argv[2][1:])
	if argv.startswith('{') and argv.endswith('}'):return eval(argv)
	else:return {}
get_params_ = get_params_dict()

if get_params_ == {}:

	items_array_dict=[]
	items_array_dict.append(['Filme','','','',{},{'Run':'filme'}])
	items_array_dict.append(['Serien','','','',{},{'Run':'serien'}])
	items_array_dict.append(['Filme Genres','','','',{},{'Run':'filme_genres'}])
	items_array_dict.append(['Serien Genres','','','',{},{'Run':'serien_genres'}])
	items_array_dict.append([get_color_text('lime','Search'),'','','',{},{'Run':'5'}])
	add_items(items_array_dict, set_items_type_int=1, set_content_type_int=0, set_params_dict=True, is_folder_bool=True, Is_playable_bool=False)
	if os.path.exists(cfi_):os.remove(cfi_)

elif get_params_.get('Run') == 'filme':

	items_array_dict=[]
	items_array_dict.append(['Filme','https://hdfilme.cc/filme1?category=&country=&sort=&key=&sort_type=desc','','',{},{'Run':'3'}])
	items_array_dict.append(['Filme Update','https://hdfilme.cc/filme1?category=&country=&sort=top&key=&sort_type=desc','','',{},{'Run':'3'}])
	items_array_dict.append(['Filme Year','https://hdfilme.cc/filme1?category=&country=&sort=year&key=&sort_type=desc','','',{},{'Run':'3'}])
	items_array_dict.append(['Filme Name','https://hdfilme.cc/filme1?category=&country=&sort=name&key=&sort_type=desc','','',{},{'Run':'3'}])
	items_array_dict.append(['Filme IMDB','https://hdfilme.cc/filme1?category=&country=&sort=imdb_rate&key=&sort_type=desc','','',{},{'Run':'3'}])
	items_array_dict.append(['Filme Rate','https://hdfilme.cc/filme1?category=&country=&sort=rate_point&key=&sort_type=desc','','',{},{'Run':'3'}])
	items_array_dict.append(['Filme VIEW','https://hdfilme.cc/filme1?category=&country=&sort=view_total&key=&sort_type=desc','','',{},{'Run':'3'}])
	add_items(items_array_dict, set_items_type_int=1, set_content_type_int=0, set_params_dict=True, is_folder_bool=True, Is_playable_bool=False)

elif get_params_.get('Run') == 'serien':

	items_array_dict=[]
	items_array_dict.append(['Serien','https://hdfilme.cc/serien1?category=&country=&sort=&key=&sort_type=desc','','',{},{'Run':'3'}])
	items_array_dict.append(['Serien Update','https://hdfilme.cc/serien1?category=&country=&sort=top&key=&sort_type=desc','','',{},{'Run':'3'}])
	items_array_dict.append(['Serien Year','https://hdfilme.cc/serien1?category=&country=&sort=year&key=&sort_type=desc','','',{},{'Run':'3'}])
	items_array_dict.append(['Serien Name','https://hdfilme.cc/serien1?category=&country=&sort=name&key=&sort_type=desc','','',{},{'Run':'3'}])
	items_array_dict.append(['Serien IMDB','https://hdfilme.cc/serien1?category=&country=&sort=imdb_rate&key=&sort_type=desc','','',{},{'Run':'3'}])
	items_array_dict.append(['Serien Rate','https://hdfilme.cc/serien1?category=&country=&sort=rate_point&key=&sort_type=desc','','',{},{'Run':'3'}])
	items_array_dict.append(['Serien VIEW','https://hdfilme.cc/serien1?category=&country=&sort=view_total&key=&sort_type=desc','','',{},{'Run':'3'}])
	add_items(items_array_dict, set_items_type_int=1, set_content_type_int=0, set_params_dict=True, is_folder_bool=True, Is_playable_bool=False)

elif get_params_.get('Run') == 'filme_genres':

	items_array_dict=[]
	items_array_dict.append(['Filme Genres','https://hdfilme.cc/filme1','','',{},{'Run':'1','Sort':''}])
	items_array_dict.append(['Filme Genres Update','https://hdfilme.cc/filme1','','',{},{'Run':'1','Sort':'top'}])
	items_array_dict.append(['Filme Genres Year','https://hdfilme.cc/filme1','','',{},{'Run':'1','Sort':'year'}])
	items_array_dict.append(['Filme Genres Name','https://hdfilme.cc/filme1','','',{},{'Run':'1','Sort':'name'}])
	items_array_dict.append(['Filme Genres IMDB','https://hdfilme.cc/filme1','','',{},{'Run':'1','Sort':'imdb'}])
	items_array_dict.append(['Filme Genres Rate','https://hdfilme.cc/filme1','','',{},{'Run':'1','Sort':'rate_point'}])
	items_array_dict.append(['Filme Genres VIEW','https://hdfilme.cc/filme1','','',{},{'Run':'1','Sort':'view_total'}])
	add_items(items_array_dict, set_items_type_int=1, set_content_type_int=0, set_params_dict=True, is_folder_bool=True, Is_playable_bool=False)

elif get_params_.get('Run') == 'serien_genres':

	items_array_dict=[]
	items_array_dict.append(['Serien Genres','https://hdfilme.cc/serien1','','',{},{'Run':'1','Sort':''}])
	items_array_dict.append(['Serien Genres Update','https://hdfilme.cc/serien1','','',{},{'Run':'1','Sort':'top'}])
	items_array_dict.append(['Serien Genres Year','https://hdfilme.cc/serien1','','',{},{'Run':'1','Sort':'year'}])
	items_array_dict.append(['Serien Genres Name','https://hdfilme.cc/serien1','','',{},{'Run':'1','Sort':'name'}])
	items_array_dict.append(['Serien Genres IMDB','https://hdfilme.cc/serien1','','',{},{'Run':'1','Sort':'imdb'}])
	items_array_dict.append(['Serien Genres Rate','https://hdfilme.cc/serien1','','',{},{'Run':'1','Sort':'rate_point'}])
	items_array_dict.append(['Serien Genres VIEW','https://hdfilme.cc/serien1','','',{},{'Run':'1','Sort':'view_total'}])

	add_items(items_array_dict, set_items_type_int=1, set_content_type_int=0, set_params_dict=True, is_folder_bool=True, Is_playable_bool=False)

elif get_params_.get('Run') == '1':

	url = get_params_.get('Url')
	sort = get_params_.get('Sort')

	content = get_cf_url(url,stream=False,timeout=30,allow_redirects=True,scraper_delay=3,headers_dict={'Referer':'https://hdfilme.cc'}).content
	get_genres(url,content,sort)

elif get_params_.get('Run') == '2':

	url = get_params_.get('Url')
	genre = get_params_.get('Genre')
	sort = get_params_.get('Sort')

	url = '{0}?category={1}&sort={2}&sort_type=desc'.format(url,genre,sort)
	res = post_cf_url(url,data={'category':genre,'sort':sort,'sort_type':'desc','load':'full-page'},headers_dict={'Origin':'https://hdfilme.cc','Referer':url.split('?')[0],'X-Requested-With':'XMLHttpRequest'})
	get_entries(res.content)

elif get_params_.get('Run') == '3':

	url = get_params_.get('Url')

	data_dict={}
	for key,value in get_regex_findall('(\w+)\=(.*?)(?:&|$)',url):
		data_dict[key] = value
	data_dict['load'] = 'full-page'

	res = post_cf_url(url,data=data_dict,headers_dict={'Origin':'https://hdfilme.cc','Referer':url.split('?')[0],'X-Requested-With':'XMLHttpRequest'})
	get_entries(res.content)

elif get_params_.get('Run') == '4':

	url = get_params_.get('Url')

	data_dict={}
	for key,value in get_regex_findall('(\w+)\=(.*?)(?:&|$)',url):
		data_dict[key] = value
	data_dict['load'] = 'full-page'

	if get_params_.get('Page') == 'nr':

		page = data_dict['page']
		new_page_nr = get_dialog_numeric('Page 1 - ' + page)

		if ((len(new_page_nr) > 0) and (int(new_page_nr) >= 1) and (int(new_page_nr) <= int(page))):
			url = url.replace('page=' + page,'page=' + new_page_nr)
			page = new_page_nr
		else:sys.exit(0)

	res = post_cf_url(url,data=data_dict,headers_dict={'Origin':'https://hdfilme.cc','Referer':url.split('?')[0],'X-Requested-With':'XMLHttpRequest'})
	get_entries(res.content)

elif get_params_.get('Run') == '5':

	search_text = get_search_keyboard()
	if len(search_text) > 0:
		search_url = 'https://hdfilme.cc/search?key={0}'.format(search_text.strip())
		content = get_cf_url(search_url,stream=False,timeout=30,allow_redirects=True,scraper_delay=3,headers_dict={'Referer':'https://hdfilme.cc'}).content
		get_entries(content)
	else:sys.exit(0)

elif get_params_.get('Run') == '6':

	title = get_params_.get('Title').replace('Verwandte Filme | ','').replace('Folge | ','').replace('Stream | ','').strip()
	url = get_params_.get('Url')
	img = get_params_.get('Img')

	items_array_dict=[]
	base_content = get_cf_url(url,stream=True,timeout=30,allow_redirects=True,scraper_delay=3,headers_dict={'Referer':url}).content
	data = get_regex_search('<div class="big-play-btn">\n<a href="(.*?)"',base_content)
	if data:url = data.group(1)
	else:url = url

	base_content = get_cf_url(url,stream=True,timeout=30,allow_redirects=True,scraper_delay=3,headers_dict={'Referer':url}).content
	movie_id = get_regex_search('data-movie-id="(.+?)"',base_content)
	episode_id = get_regex_search(url +'"\sdata-episode-id="(.*?)"',base_content)

	if movie_id and episode_id :

		data_url = 'https://hdfilme.cc/movie/load-stream/' + movie_id.group(1) +'/'+ episode_id.group(1) + '?server=2'
		content = get_cf_url(data_url,stream=False,timeout=30,allow_redirects=True,scraper_delay=3,headers_dict={'Origin':'https://hdfilme.cc','Referer':url,'X-Requested-With':'XMLHttpRequest'}).content
		video_data = get_regex_search('var sources = (\[.*?\]);',content)
		if video_data:
			for quali,url in get_regex_findall('label":"(.+?)"[\s\S]+?file":"(.+?)"',video_data.group(1)):
				items_array_dict.append([title +' | ' + quali ,url.replace('\/','/'),img,'',{},{'Run':'7'}])

	if 'staffel' in get_params_.get('Url'):
		for url,title in get_regex_findall('class="new"[\s\S]*?href="(.*?)".data-episode-id[\s\S].*?title="(.*?)">',base_content):
			title = title.replace('stream','').strip()
			items_array_dict.append(['Folge | '+title,url,img,'',{},{'Run':'6'}])

	for img,url,title in get_regex_findall('<span class="over_play_min">[\s\S]*?data-src="(.*?)"[\s\S]*?<a href="(.*?)"[\s\S][^>]*?>(.*?)<\/a>',base_content):
		title = title.strip()
		items_array_dict.append(['Verwandte Filme | ' + title, url,img,'',{},{'Run':'6'}])

	add_items(items_array_dict, set_items_type_int=1, set_content_type_int=0, set_params_dict=True, is_folder_bool=True, Is_playable_bool=False)

elif get_params_.get('Run') == '7':

	title = get_params_.get('Title')
	url = get_params_.get('Url')
	img = get_params_.get('Img')
	get_xbmc_player(title=title,url=url,image=img)