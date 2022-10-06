import httpx
from config import headers
from upload_pic import *

post_data = {
    "variables": {
        "tweet_text": "",
        "media": {
            "media_entities": [],
            "possibly_sensitive": False
        },
        "withDownvotePerspective": False,
        "withReactionsMetadata": False,
        "withReactionsPerspective": False,
        "withSuperFollowsTweetFields": True,
        "withSuperFollowsUserFields": True,
        "semantic_annotation_ids": [],
        "dark_request": False
    },
    "features": {
        "tweetypie_unmention_optimization_enabled": True,
        "responsive_web_uc_gql_enabled": True,
        "vibe_api_enabled": True,
        "responsive_web_edit_tweet_api_enabled": True,
        "graphql_is_translatable_rweb_tweet_is_translatable_enabled": False,
        "interactive_text_enabled": True,
        "responsive_web_text_conversations_enabled": False,
        "standardized_nudges_misinfo": True,
        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":
        False,
        "responsive_web_graphql_timeline_navigation_enabled": False,
        "responsive_web_enhance_cards_enabled": True
    },
    "queryId": "3oCAhKqrb4PRuVPH59ySGQ"
}

url = 'https://twitter.com/i/api/graphql/3oCAhKqrb4PRuVPH59ySGQ/CreateTweet'

def _post(data):
    with httpx.Client(headers=headers) as client:
        post_res = client.post(url, json=post_data)
        res_json = post_res.json()
        # print(res_json)
        if 'errors' not in res_json.keys():
            print('send succeed')
            return res_json['data']['create_tweet']['tweet_results']['result']['rest_id']
        

def post_text_and_pic(text, img_urls):
    post_data['variables']['tweet_text'] = text
    post_data['variables']['media']['media_entities'] = []
    if 'reply' in post_data['variables'].keys():
        del post_data['variables']['reply']
    # set image data
    for i in img_urls:
        # get img ids
        image_id = upload_img(i)
        if image_id:
            post_data['variables']['media']['media_entities'].append({
                "media_id":
                image_id,
                "tagged_users": []
            })
    # print(post_data)
    return _post(post_data)


# "reply":{"in_reply_to_tweet_id":"1576909066772701185","exclude_reply_user_ids":[]}
def append_tweet(reply_id, text, img_urls):
    post_data['variables']['tweet_text'] = text
    post_data['variables']['media']['media_entities'] = []
    for i in img_urls:
        # get img ids
        image_id = upload_img(i)
        if image_id:
            post_data['variables']['media']['media_entities'].append({
                "media_id":
                image_id,
                "tagged_users": []
            })
    post_data['variables']['reply'] = {
        "in_reply_to_tweet_id": reply_id,
        "exclude_reply_user_ids": []
    }
    return _post(post_data)

if __name__ == '__main__':
	post_text_and_pic('hello world', [])
