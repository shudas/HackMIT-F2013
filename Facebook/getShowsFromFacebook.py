import facebook
import json
from flask_oauth import OAuth
app.config['SOCIAL_FACEBOOK'] = {
    'consumer_key': 'facebook app id',
    'consumer_secret': 'facebook app secret'
}
def makeThemLogin():
	facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'})
	return facebook['access_token_url']
def getShowsFromFacebook():
	#make them login
	#Make Graph API work
	# oauth_access_token = 'CAACEdEose0cBANAwO4Cz4owvnRidPVjZBpdbgj5Lu1QYZAw9q8oJFSpvLW35xCcZCPxYpr0dWYTuZCRMFiwR6dx4xuVHc2QpNHpsPpD3ZA3ZAfTTahAarxOOy5wlCxaH8CCxZCNGoKse8ORO186Ak1MpxAMKPEJhL7Y7xHZCvV1Sx87K56srU8D0GGbTmKEYdvNcULHsbxZBiAgZDZD'
	oauth_access_token = makeThemLogin()
	graph = facebook.GraphAPI(oauth_access_token)
	# GET https://graph.facebook.com/me?fields=name,birthday,photos.limit(10).fields(id, picture)
	profile = graph.get_object("me")
	shows = graph.get_connections("me","movies")['data']
	names = [show['name'] for show in shows]
	return names

print(getShowsFromFacebook())