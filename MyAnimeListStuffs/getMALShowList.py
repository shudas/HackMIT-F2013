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
    # """
    # Retrive Anime XML from MyAnimeList server.
    
    # return: dictionary object
    # """

    fetch_base_url = 'http://myanimelist.net/malappinfo.php?status=all&u='
    # fetch_request_data = urllib.urlencode({
    #     'status': 'all',
    #     'u': username})
    fetch_url = fetch_base_url + username

    # read the server xml file and do preliminary spacer sanitation for parsing
    fetch_response = \
          unicode(urllib2.urlopen(fetch_url).read(), 'utf-8', 'replace')
    fetch_response = fetch_response.strip()
    # phrase data and extract anime entry nodes
    # try:
    #     unicode(fetch_response, "utf-8")
    # except UnicodeError:
    #     fetch_response = fetch_response.encode("utf-8")
    # else:
    # # value was valid ASCII data
    #     pass
    fetch_response = fetch_response.encode("utf-8")
    xmldata = parseString(fetch_response)
    anime_nodes = xmldata.getElementsByTagName('anime')

    # walk through all the anime nodes and convert the data to a python
    # dictionary
    ac_remote_anime_dict = dict()
    listofNames = []
    for anime in anime_nodes:
        ac_node = dict()
        for node in anime.childNodes:
            # tags and empty nodes are excluded for the time being
            if not node.childNodes or node.nodeName == u'my_tags':
                node.unlink()
            else:
                # process my_last_updated unix timestamp
                if mal_data_schema[node.nodeName] is datetime:
                    ac_node[node.nodeName] = \
                        datetime.fromtimestamp(int(node.firstChild.nodeValue))
                # process integer slots
                elif mal_data_schema[node.nodeName] is int:
                    ac_node[node.nodeName] = int(node.firstChild.nodeValue)
                # proces date slots
                elif mal_data_schema[node.nodeName] is date:
                    if node.firstChild.nodeValue != '0000-00-00':
                        (y,m,d) = node.firstChild.nodeValue.split('-')
                        (y,m,d) = int(y), int(m), int(d)
                        if y and m and d:
                            ac_node[node.nodeName] = date(y,m,d)
                # process string slots
                else:
                    ac_node[node.nodeName] = node.firstChild.nodeValue

        # series titles are used as anime identifiers
        # the keys for the resulting dictionary are encoded to ASCII, so they
        # can be simply put into shelves
        listofNames.append(ac_node['series_title'].encode('ascii','ignore'))
        # key = ac_node['series_title'].encode('utf-8')
        
        # print(ac_node['series_title'])

        # add node entry to the resulting nodelist
        # ac_remote_anime_dict[key] = ac_node

    # the resulting dict is like this:
    # {<ASCII-fied key from title>: {<mal_data_schema-fields>: <values>}, ...}
    return listofNames
def getImagesGivenShows(listofNames):
    searchQuery = ""
    for name in listofNames:
        searchQuery = searchQuery + name + "hd wallpaper"
    return "baka"

print((_getAnimeList('mmmsplay10')))
    #Insert Code to make shit for all elements in list.