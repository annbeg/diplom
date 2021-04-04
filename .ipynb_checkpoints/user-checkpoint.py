import requests
import json
import pandas as pd


def getUserInfoResponse(username):
#     input (string): username 
#     output (string): JSON response
    url = f"https://twitter.com/i/api/graphql/hc-pka9A7gyS3xODIafnrQ/UserByScreenName?variables=%7B%22screen_name%22%3A%22{username}%22%2C%22withHighlightedLabel%22%3Atrue%7D"
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': '*/*',
      'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'en-gb',
      'Host': 'twitter.com',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15',
      'Connection': 'keep-alive',
      'Cookie': '_ga=GA1.2.1728120664.1614803046; _gid=GA1.2.959135695.1615041021; twid=u%3D1081284009823555584; lang=en; cd_user_id=177fcea35ad4f9-0146a181011fb8-48183201-13c680-177fcea35aea98; mbox=PC#5af5d131a3d8457eadff08a61d6501cc.38_0#1678100743|session#024ba0a521df4ae082d6bc2f0809dfc0#1614857802; external_referer=padhuUp37zj9xuUOXCNFvIbxLqKGGEyN|0|8e8t2xd8A2w%3D; des_opt_in=Y; ads_prefs="HBISAAA="; auth_token=015a5acdf5578ba8c16b2fe4ff9c53eb3b25d175; ct0=4eaea07b1ba828f9bf8a1c4fe5487c7b51cf702852445725432915052ea7b90d255860d9562695b66b69ce17ed8460abf5cc846c715c6f0445ff66b4ff09d2b4cd992445f177ea58458b9aef42ae7c8c; dnt=1; kdt=A0C41bULaFlaBKVxvmWf9ssbbHSRa7M6Tl8k26aS; remember_checked_on=1; guest_id=v1%3A161418947273669233; personalization_id="v1_3OfRfaPwtHPmzeXO7foP0g=="',
      'x-twitter-active-user': 'yes',
      'x-twitter-client-language': 'en',
      'x-csrf-token': '4eaea07b1ba828f9bf8a1c4fe5487c7b51cf702852445725432915052ea7b90d255860d9562695b66b69ce17ed8460abf5cc846c715c6f0445ff66b4ff09d2b4cd992445f177ea58458b9aef42ae7c8c',
      'x-twitter-auth-type': 'OAuth2Session'
    }
    
    response = requests.request("GET", url, headers=headers, data=payload)
    
    if json.loads(response.text)['data'] == {}:
        raise ValueError('Wrong username!')
        return None
    
    return response


def getUserInfo(username):
#     input (string): username
#     output (dict)
    
    response = getUserInfoResponse(username)
    
    if response == None:
        return None
    
    data = json.loads(response.text)
    
    info = {}
    
    info['username'] = username
    info['rest_id'] = data['data']['user']['rest_id']
    info['location'] = data['data']['user']['legacy']['location']
    
    
    return info


def getUserFollowingResponse(rest_id, following_count = 15000):
    urlFollowing = f"https://twitter.com/i/api/graphql/taJbMVFxNBcULs8aHwX3cg/Following?variables=%7B%22userId%22%3A%22{rest_id}%22%2C%22count%22%3A{str(following_count)}%2C%22withHighlightedLabel%22%3Afalse%2C%22withTweetQuoteCount%22%3Afalse%2C%22includePromotedContent%22%3Afalse%2C%22withTweetResult%22%3Afalse%2C%22withUserResults%22%3Afalse%2C%22withNonLegacyCard%22%3Atrue%7D"
    payload={}
    headers = {
      'Content-Type': 'application/json',
      'Accept': '*/*',
      'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'en-gb',
      'Host': 'twitter.com',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15',
      'Connection': 'keep-alive',
      'Cookie': '_ga=GA1.2.1728120664.1614803046; _gid=GA1.2.959135695.1615041021; twid=u%3D1081284009823555584; lang=en; cd_user_id=177fcea35ad4f9-0146a181011fb8-48183201-13c680-177fcea35aea98; mbox=PC#5af5d131a3d8457eadff08a61d6501cc.38_0#1678100743|session#024ba0a521df4ae082d6bc2f0809dfc0#1614857802; external_referer=padhuUp37zj9xuUOXCNFvIbxLqKGGEyN|0|8e8t2xd8A2w%3D; des_opt_in=Y; ads_prefs="HBISAAA="; auth_token=015a5acdf5578ba8c16b2fe4ff9c53eb3b25d175; ct0=4eaea07b1ba828f9bf8a1c4fe5487c7b51cf702852445725432915052ea7b90d255860d9562695b66b69ce17ed8460abf5cc846c715c6f0445ff66b4ff09d2b4cd992445f177ea58458b9aef42ae7c8c; dnt=1; kdt=A0C41bULaFlaBKVxvmWf9ssbbHSRa7M6Tl8k26aS; remember_checked_on=1; guest_id=v1%3A161418947273669233; personalization_id="v1_3OfRfaPwtHPmzeXO7foP0g=="',
      'x-twitter-active-user': 'yes',
      'x-twitter-client-language': 'en',
      'x-csrf-token': '4eaea07b1ba828f9bf8a1c4fe5487c7b51cf702852445725432915052ea7b90d255860d9562695b66b69ce17ed8460abf5cc846c715c6f0445ff66b4ff09d2b4cd992445f177ea58458b9aef42ae7c8c',
      'x-twitter-auth-type': 'OAuth2Session'
    }
    
    response = requests.request("GET", urlFollowing, headers=headers, data=payload)
    
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
    
