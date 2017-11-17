#-*- coding: UTF-8 -*- 
import urllib2
class HtmlDownloader(object):
    
    def download(self, url):
        if url is None:
            return None
        
        response = urllib2.urlopen(url)
        
        if response.getcode() != 200:
            return None
        
        return response.read()
        
'''
Created on 2017年11月16日

@author: liuwei
'''