# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UserInfoItem(scrapy.Item):
    uid = scrapy.Field()
    screen_name = scrapy.Field()
    statuses_count = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field()
    followers_count = scrapy.Field()
    follow_count = scrapy.Field()


class UserWeiboItem(scrapy.Item):
    created_at = scrapy.Field()
    mid = scrapy.Field()
    text = scrapy.Field()
    source = scrapy.Field()
    reposts_count = scrapy.Field()
    comments_count = scrapy.Field()
    attitudes_count = scrapy.Field()
    pic_urls = scrapy.Field()
    video_url = scrapy.Field()
    article_url = scrapy.Field()
    # 转发
    retweet_created_at = scrapy.Field()
    retweet_mid = scrapy.Field()
    retweet_text = scrapy.Field()
    retweet_source = scrapy.Field()
    retweet_reposts_count = scrapy.Field()
    retweet_comments_count = scrapy.Field()
    retweet_attitudes_count = scrapy.Field()
    retweet_pic_urls = scrapy.Field()
    retweet_video_url = scrapy.Field()
    retweet_article_url = scrapy.Field()


class UserWeiboPicsItem(scrapy.Item):
    mid = scrapy.Field()
    pic_urls = scrapy.Field()


class UserWeiboVideosItem(scrapy.Item):
    mid = scrapy.Field()
    video_url = scrapy.Field()
