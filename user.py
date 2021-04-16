import requests
import json
import pandas as pd

cookies = {
    '_ga': 'GA1.2.947737770.1618485835',
    '_gid': 'GA1.2.534356324.1618485835',
    '_twitter_sess': 'BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCDWS0dl4AToMY3NyZl9p%250AZCIlYjAxOTI2ZjUyOWJlNjFmMTg4ZGY3ZWY1YzE4MjcwNjg6B2lkIiU0YjUx%250AZDA4YjU2YzQzMDg1MTFjNzAyM2Y4NDllMjBhZToJdXNlcmwrCQDQ1%252FoTfgEP--6431e90925e030ef3d0e6e5bfae5be7196d32de2',
    'dnt': '1',
    'twid': 'u%3D1081284009823555584',
    'ct0': '9972f3651699789758545aa7359913dfd057cc64678b85803a1ae20aaa278b0c1a98b43d4b6120a7ceb21c399ac1309f8c44d4d7241daab2e40be8595bec29dee49e0f83e54b79e98760a3137044aff8',
    'ads_prefs': 'HBISAAA=',
    'auth_token': '77e96a512146da031581b24a9d4e385f6047478f',
    'kdt': 'A0C41bULaFlaBKVxvmWf9ssbbHSRa7M6Tl8k26aS',
    'remember_checked_on': '1',
    'gt': '1382975772793667585',
    'guest_id': 'v1%3A161856209252903684',
    'personalization_id': 'v1_wZGgXfto+lrDWDXtG0i0GQ==',
    '_sl': '1',
    'lang': 'en',
}

headers = {
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'Accept-Language': 'en-gb',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'twitter.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15',
    'Referer': 'https://twitter.com/meduzaproject/followers',
    'Connection': 'keep-alive',
    'x-guest-token': '1382975772793667585',
    'x-twitter-client-language': 'en',
    'x-csrf-token': '9972f3651699789758545aa7359913dfd057cc64678b85803a1ae20aaa278b0c1a98b43d4b6120a7ceb21c399ac1309f8c44d4d7241daab2e40be8595bec29dee49e0f83e54b79e98760a3137044aff8',
    'x-twitter-active-user': 'yes',
}

def getUserInfoResponse(username):
#     input (string): username
#     output (string): JSON response
    url = f"https://twitter.com/i/api/graphql/hc-pka9A7gyS3xODIafnrQ/UserByScreenName?variables=%7B%22screen_name%22%3A%22{username}%22%2C%22withHighlightedLabel%22%3Atrue%7D"
    payload={}

    response = requests.request("GET", url, headers=headers, data=payload, cookies=cookies)
    # print(json.loads(response.text))
    if 'errors' in json.loads(response.text):
        return None
    if json.loads(response.text)['data'] == {}:
        # raise ValueError('Wrong username:'+username)
        print('Wrong username:'+username)
        return None

    return response


def getUserInfo(username):
#     input (string): username
#     output (dict)

    response = getUserInfoResponse(username)

    if response == None:
        print(f'For username "{username}" no location found')
        return {'location': ''}

    data = json.loads(response.text)

    info = {}

    info['username'] = username
    info['rest_id'] = data['data']['user']['rest_id']
    info['location'] = data['data']['user']['legacy']['location']


    return info


def getUserFollowingResponse(rest_id, following_count = 15000):
    urlFollowing = f"https://twitter.com/i/api/graphql/taJbMVFxNBcULs8aHwX3cg/Following?variables=%7B%22userId%22%3A%22{rest_id}%22%2C%22count%22%3A{str(following_count)}%2C%22withHighlightedLabel%22%3Afalse%2C%22withTweetQuoteCount%22%3Afalse%2C%22includePromotedContent%22%3Afalse%2C%22withTweetResult%22%3Afalse%2C%22withUserResults%22%3Afalse%2C%22withNonLegacyCard%22%3Atrue%7D"
    payload={}

    response = requests.request("GET", urlFollowing, headers=headers, data=payload, cookies=cookies)

    if 'data' not in json.loads(response.text).keys():
        raise ValueError('Wrong REST id!')
        return None

    if {} == json.loads(response.text)['data']['user']['following_timeline']:
        raise ValueError('Wrong REST id!')
        return None

#     data = json.loads(response.text)

    return response


def getUserFollowing(rest_id):

    response = getUserFollowingResponse(rest_id)

    if response == None:
        return None

    data = json.loads(response.text)
    data = data['data']['user']['following_timeline']['timeline']['instructions'][len(data['data']['user']['following_timeline']['timeline']['instructions'])-1]['entries'][:-2]

    followingSeries = pd.DataFrame(data).content.apply(lambda x: [
        x['itemContent']['user']['rest_id'],
        x['itemContent']['user']['legacy']['screen_name'],
        x['itemContent']['user']['legacy']['name'],
        x['itemContent']['user']['legacy']['location']
    ])

    followingDF = pd.DataFrame.from_dict(dict(zip(followingSeries.index, followingSeries.values))).T
    followingDF.columns = pd.Index(['rest_id','username','public_name', 'location'])

    return followingDF
