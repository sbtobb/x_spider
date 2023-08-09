from datetime import datetime

import httpx

from sqlalchemy.orm import Session

from application.config import auth_token, ct0
from application.models import Tweets


def send_request():
    try:
        response = httpx.get(
            url="https://twitter.com/i/api/graphql/XicnWRbyQ3WgVY__VataBQ/UserTweets",
            params={
                "variables": "{\"userId\":\"44196397\",\"count\":20,\"includePromotedContent\":true,\"withQuickPromoteEligibilityTweetFields\":true,\"withVoice\":true,\"withV2Timeline\":true}",
                "features": "{\"rweb_lists_timeline_redesign_enabled\":true,\"responsive_web_graphql_exclude_directive_enabled\":true,\"verified_phone_label_enabled\":false,\"creator_subscriptions_tweet_preview_api_enabled\":true,\"responsive_web_graphql_timeline_navigation_enabled\":true,\"responsive_web_graphql_skip_user_profile_image_extensions_enabled\":false,\"tweetypie_unmention_optimization_enabled\":true,\"responsive_web_edit_tweet_api_enabled\":true,\"graphql_is_translatable_rweb_tweet_is_translatable_enabled\":true,\"view_counts_everywhere_api_enabled\":true,\"longform_notetweets_consumption_enabled\":true,\"responsive_web_twitter_article_tweet_consumption_enabled\":false,\"tweet_awards_web_tipping_enabled\":false,\"freedom_of_speech_not_reach_fetch_enabled\":true,\"standardized_nudges_misinfo\":true,\"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled\":true,\"longform_notetweets_rich_text_read_enabled\":true,\"longform_notetweets_inline_media_enabled\":true,\"responsive_web_media_download_video_enabled\":false,\"responsive_web_enhance_cards_enabled\":false}",
            },
            headers={
                "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
                "dnt": "1",
                "x-twitter-client-language": "zh-cn",
                "x-csrf-token": "f23d3f1ee3aecd926c32a311a24a8d4b6275c075f20ba454d1eaa26dde64b934cffaeffce81cac58f36e507eeffa9b432f90d0e610097cac080c93d1ee2374f1029efc7b6dc9be8c46754a71d2a52c6a",
                "sec-ch-ua-mobile": "?0",
                "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                "content-type": "application/json",
                "x-client-transaction-id": "KIBK/8Vm7JDOniK305+6WK5GnLCeRpw23gKwuVXKKO73hqL54wJzqc5wH+TMCjL7IYphqiiVBiIvdGGNu4OsjPj6plRjKQ",
                "x-twitter-auth-type": "OAuth2Session",
                "x-client-uuid": "19e7a83e-319d-4d0b-ae3c-18cec8ac01c5",
                "x-twitter-active-user": "yes",
                "sec-ch-ua-platform": "\"macOS\"",
                "accept": "*/*",
                "sec-fetch-site": "same-origin",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://twitter.com/elonmusk",
                "accept-encoding": "gzip, deflate",
                "accept-language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7",

            },
            cookies={
                "auth_token": auth_token,
                "ct0": ct0
            }
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response encoding: {content}'.format(
            content=response.encoding))

        return response.json()
    except httpx._exceptions.RequestError:
        print('HTTP Request failed')


def get_last_tweets(num=10):
    """
    获取最新推文
    :param num:  推文条数 max 20 默认 10
    :return:
    """
    data = send_request()
    tweets = None
    instructions = data['data']['user']['result']['timeline_v2']['timeline']['instructions']
    for instruction in instructions:
        if instruction['type'] == "TimelineAddEntries":
            tweets = instruction['entries']
            break

    results = []
    if tweets is None:
        return results
    nonce = 0
    for tweet in tweets:
        if tweet['content']['entryType'] != "TimelineTimelineItem":
            continue
        # 解析推文信息
        content = tweet['content']['itemContent']['tweet_results']['result']
        user_results = content['core']['user_results']['result']['legacy']
        username = user_results['name']
        screen_name = user_results['screen_name']
        created_at = content['legacy']['created_at']
        full_text = content['legacy']['full_text']

        # 转换时间格式
        time = datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y').timestamp()

        # 构造JSON数据
        result = {
            'username': username,
            'screen_name': screen_name,
            'time': int(time),
            'full_text': full_text
        }
        print(result)
        results.append(result)
        nonce += 1
        if nonce > num:
            break
    return results


def create_tweet(db: Session, username, screen_name, tweets_time, full_text):
    exist = tweet_is_exist(db, username, full_text)
    if exist is not None:
        return exist
    tweet = Tweets(username=username, screen_name=screen_name, tweets_time=tweets_time, full_text=full_text)
    db.add(tweet)
    db.commit()
    return tweet


def tweet_is_exist(db: Session, username, full_text):
    tweets = db.query(Tweets).filter_by(username=username, full_text=full_text)
    if tweets is None:
        return False
    return tweets.first()


def get_tweet_by_id(db: Session, id):
    tweet = db.query(Tweets).filter_by(id=id).first()
    return tweet


def get_tweet_by_username(db: Session, username):
    tweets = db.query(Tweets).filter_by(username=username).all()
    return tweets


def get_all_tweets(db: Session):
    tweets = db.query(Tweets).all()
    return tweets


def update_tweet(db: Session, tweet, text):
    tweet.full_text = text
    db.commit()


def delete_tweet(db: Session, tweet):
    db.delete(tweet)
    db.commit()


if __name__ == '__main__':
    get_last_tweets()
