import urllib
import urllib2
from cookielib import LWPCookieJar
import socket
from xml.dom.minidom import parseString
from datetime import date, datetime
import os, time

from data import mal_data_schema
from database import db as local_database
from globs import ac_log_path, ac_data_path

def _getAnimeList(username):

    fetch_base_url = 'http://myanimelist.net/malappinfo.php?status=all&u='
    fetch_url = fetch_base_url + username

    fetch_response = \
          unicode(urllib2.urlopen(fetch_url).read(), 'utf-8', 'replace')
    fetch_response = fetch_response.strip()
    fetch_response = fetch_response.encode("utf-8")
    xmldata = parseString(fetch_response)
    anime_nodes = xmldata.getElementsByTagName('anime')

    ac_remote_anime_dict = dict()
    listofNames = []
    for anime in anime_nodes:
        ac_node = dict()
        for node in anime.childNodes:
            if not node.childNodes or node.nodeName == u'my_tags':
                node.unlink()
            else:
                if mal_data_schema[node.nodeName] is datetime:
                    ac_node[node.nodeName] = \
                        datetime.fromtimestamp(int(node.firstChild.nodeValue))
                elif mal_data_schema[node.nodeName] is int:
                    ac_node[node.nodeName] = int(node.firstChild.nodeValue)
                elif mal_data_schema[node.nodeName] is date:
                    if node.firstChild.nodeValue != '0000-00-00':
                        (y,m,d) = node.firstChild.nodeValue.split('-')
                        (y,m,d) = int(y), int(m), int(d)
                        if y and m and d:
                            ac_node[node.nodeName] = date(y,m,d)
                else:
                    ac_node[node.nodeName] = node.firstChild.nodeValue

        listofNames.append(ac_node['series_title'].encode('ascii','ignore'))
    return listofNames
