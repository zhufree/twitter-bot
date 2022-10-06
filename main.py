import httpx
from config import *
import json, time
from post_tweet import *

def sync_weibo(weibo_json_file):
    with open(weibo_json_file, 'r', encoding='utf') as json_file:
        weibo_list = json_file.read().split('\n')
        weibo_list.reverse()
        for weibo in weibo_list:
            time.sleep(5)
            weibo_json = json.loads(weibo)
            # 一次最多140字4张图
            tweet_list = [] # each tweet less than 140 chars
            tweet_pics_list = [] # pics of each tweet
            reply_id = '' # reply id that append tweet need
            content = weibo_json['content'].strip().replace('\u200b', '')
            # cut content
            if len(content) > 140:
                while len(content) > 140:
                    tweet_list.append(content[0:140])
                    content = content[140:]
            tweet_list.append(content)

            # add links
            if 'refer' in weibo_json.keys():
                for r in weibo_json['refer']:
                    tweet_list.append(r)
            if 'video' in weibo_json.keys():
                tweet_list.append(weibo_json['video'])

            # add pics
            if 'pics' in weibo_json.keys():
                jpg_pic_list = []
                for p in weibo_json['pics']:
                    if p.endswith('.gif'):
                        # gif one for each tweet
                        tweet_pics_list.append([p])
                    else:
                        # jpg 4 for each tweet
                        jpg_pic_list.append(p)
                        if len(jpg_pic_list) == 4:
                            tweet_pics_list.append(jpg_pic_list)
                            jpg_pic_list = []
                if len(jpg_pic_list) > 0:
                    tweet_pics_list.append(jpg_pic_list)
            for i, t in enumerate(tweet_list):
                print(t)
                if i == 0:
                    if len(tweet_pics_list) > i:
                        print(tweet_pics_list[i])
                        reply_id = post_text_and_pic(t, tweet_pics_list[i])
                    else:
                        reply_id = post_text_and_pic(t, [])
                else:
                    if len(tweet_pics_list) > i:
                        print(tweet_pics_list[i])
                        reply_id = append_tweet(reply_id, t, tweet_pics_list[i])
                    else:
                        reply_id = append_tweet(reply_id, t, [])
                print(reply_id)
            # post remain pics
            if len(tweet_pics_list) > len(tweet_list):
                for pics in tweet_pics_list[len(tweet_list):]:
                    reply_id = append_tweet(reply_id, "", pics)


if __name__ == '__main__':
    sync_weibo('weibo_json_file')