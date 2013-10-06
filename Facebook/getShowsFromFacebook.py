import facebook
import json
from flask_oauth import OAuth
import flask
# app.config['SOCIAL_FACEBOOK'] = {
#     'consumer_key': 'facebook app id',
#     'consumer_secret': 'facebook app secret'
# }
# FACEBOOK_APP_ID = '188477911223606'
# FACEBOOK_APP_SECRET = '621413ddea2bcc5b2e83d42fc40495de'

def getShowsFromFacebook():
	oauth = OAuth()
	facebooklogin = oauth.remote_app('facebook',
		base_url='https://graph.facebook.com/',
		request_token_url=None,
		access_token_url='/oauth/access_token',
		authorize_url='https://www.facebook.com/dialog/oauth',
		consumer_key='104980197484',
		consumer_secret='848e655bf22e44cad1581dab9a1937b5',
		request_token_params={'scope': 'email'})
	#make them login
	#Make Graph API work
	# oauth_access_token = 'CAACEdEose0cBANAwO4Cz4owvnRidPVjZBpdbgj5Lu1QYZAw9q8oJFSpvLW35xCcZCPxYpr0dWYTuZCRMFiwR6dx4xuVHc2QpNHpsPpD3ZA3ZAfTTahAarxOOy5wlCxaH8CCxZCNGoKse8ORO186Ak1MpxAMKPEJhL7Y7xHZCvV1Sx87K56srU8D0GGbTmKEYdvNcULHsbxZBiAgZDZD'
	oauth_access_token = facebooklogin.get('access_token_url')
	graph = facebook.GraphAPI(oauth_access_token)
	# GET https://graph.facebook.com/me?fields=name,birthday,photos.limit(10).fields(id, picture)
	profile = graph.get_object("me")
	shows = graph.get_connections("me","movies")['data']
	names = [show['name'] for show in shows]
	return names

print(getShowsFromFacebook())