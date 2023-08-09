from fastapi import APIRouter, Depends, HTTPException

from application.dependencies import get_db, get_current_user
from application.service.tweets import get_last_tweets, create_tweet, get_all_tweets

router = APIRouter(
    prefix="/tweets",
    dependencies=[Depends(get_current_user)]
)


@router.get("/refresh")
def refresh(db=Depends(get_db)):
    tweets = get_last_tweets()
    if tweets is None:
        raise HTTPException(status_code=500, detail="Refresh tweets failed")
    for tweet in tweets:
        username = tweet['username']
        screen_name = tweet['screen_name']
        tweets_time = tweet['time']
        full_text = tweet['full_text']
        create_tweet(db, username, screen_name, tweets_time, full_text)
    return {"data": tweets}


@router.get("/list")
def get_tweets(db=Depends(get_db)):
    tweets = get_all_tweets(db)
    if tweets is None:
        raise HTTPException(status_code=500, detail="Refresh tweets failed")
    return {"data": tweets}
