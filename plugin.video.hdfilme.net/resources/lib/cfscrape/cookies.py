#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,cPickle

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