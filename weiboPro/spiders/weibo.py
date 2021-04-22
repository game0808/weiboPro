import json
import time
import math
import scrapy
import random
import logging
from ..items import *
from time import sleep
from fake_useragent import UserAgent

ua = UserAgent()
logger = logging.getLogger(__name__)


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    # 要爬取的微博uid
    uid = ''
    # 要爬取的页数，不设置则爬取所有页数
    # weibo_page_range = 2

    headers = {
        'User-Agent': ua.random,
    }

    def start_requests(self):
        # 用户信息
        user_info_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + \
            self.uid + '&containerid=100505' + self.uid
        try:
            yield scrapy.Request(url=user_info_url, headers=self.headers, callback=self.parse_user)
        except:
            logger.error(user_info_url)

    def parse_user(self, response):
        user_info = json.loads(response.text)['data']['userInfo']
        self.weibo_page_range = math.ceil(
            float(user_info['statuses_count']) / 10)
        user_info_item = UserInfoItem()
        user_info_item['uid'] = user_info['id']
        user_info_item['screen_name'] = user_info['screen_name']
        user_info_item['statuses_count'] = user_info['statuses_count']
        user_info_item['description'] = user_info['description']
        if user_info['gender'] == 'f':
            user_info_item['gender'] = '女'
        elif user_info['gender'] == 'm':
            user_info_item['gender'] = '男'
        else:
            user_info_item['gender'] = '保密'
        user_info_item['followers_count'] = user_info['followers_count']
        user_info_item['follow_count'] = user_info['follow_count']
        yield user_info_item

        # 微博信息
        weibo_info_urls = []
        weibo_info_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + \
            self.uid + '&containerid=107603' + \
            self.uid + '&page='
        for i in range(1, self.weibo_page_range + 1):
            weibo_info_urls.append(weibo_info_url + str(i))

        for weibo_info_url in weibo_info_urls:
            sleep(random.random())
            try:
                yield scrapy.Request(url=weibo_info_url, headers=self.headers, callback=self.parse_weibo)
            except:
                logger.error(weibo_info_url)

    def parse_weibo(self, response):
        weibo_info = json.loads(response.text)['data']['cards']
        for card in weibo_info:
            if card['card_type'] == 9:
                user_weibo = card['mblog']
                user_weibo_item = UserWeiboItem()
                # 发布时间
                user_weibo_item['created_at'] = user_weibo['created_at']
                # time.strptime(user_weibo['created_at'],'%a %b %d %H:%M:%S %z %Y')
                # mid
                user_weibo_item['mid'] = user_weibo['mid']
                # 微博内容
                user_weibo_item['text'] = user_weibo['text'].replace('\\', '')
                # 发布来源
                user_weibo_item['source'] = user_weibo['source']
                # 转发
                user_weibo_item['reposts_count'] = user_weibo['reposts_count']
                # 评论
                user_weibo_item['comments_count'] = user_weibo['comments_count']
                # 点赞
                user_weibo_item['attitudes_count'] = user_weibo['attitudes_count']
                # 图片
                if user_weibo['pic_ids']:
                    user_weibo_pics_item = UserWeiboPicsItem()
                    user_weibo_pic_urls = []
                    for pic in user_weibo['pics']:
                        pic_url = pic['large']['url'].replace('\\', '')
                        user_weibo_pic_urls.append(pic_url)
                    user_weibo_item['pic_urls'] = user_weibo_pic_urls
                    user_weibo_pics_item['mid'] = user_weibo['mid']
                    user_weibo_pics_item['pic_urls'] = user_weibo_pic_urls
                    yield user_weibo_pics_item

                if 'page_info' in user_weibo:
                    # 视频
                    if user_weibo['page_info']['type'] == 'video':
                        user_weibo_videos_item = UserWeiboVideosItem()
                        user_weibo_videos_item['mid'] = user_weibo['mid']
                        user_weibo_video_urls = user_weibo['page_info']['urls']
                        if 'mp4_720p_mp4' in user_weibo_video_urls:
                            video_url = user_weibo_video_urls['mp4_720p_mp4'].replace(
                                '\\', '')
                        elif 'mp4_hd_mp4' in user_weibo_video_urls:
                            video_url = user_weibo_video_urls['mp4_hd_mp4'].replace(
                                '\\', '')
                        else:
                            video_url = user_weibo_video_urls['mp4_ld_mp4'].replace(
                                '\\', '')
                        user_weibo_item['video_url'] = video_url
                        user_weibo_videos_item['video_url'] = video_url
                        yield user_weibo_videos_item
                    # 文章
                    if user_weibo['page_info']['type'] == 'article':
                        user_weibo_item['article_url'] = user_weibo['page_info']['page_url'].replace(
                            '\\', '')
                # 转发
                if 'retweeted_status' in user_weibo:
                    retweet_weibo = user_weibo['retweeted_status']
                    # 发布时间
                    user_weibo_item['retweet_created_at'] = retweet_weibo['created_at']
                    # mid
                    user_weibo_item['retweet_mid'] = retweet_weibo['mid']
                    # 微博内容
                    user_weibo_item['retweet_text'] = retweet_weibo['text'].replace(
                        '\\', '')
                    # 发布来源
                    user_weibo_item['retweet_source'] = retweet_weibo['source']
                    # 转发
                    user_weibo_item['retweet_reposts_count'] = retweet_weibo['reposts_count']
                    # 评论
                    user_weibo_item['retweet_comments_count'] = retweet_weibo['comments_count']
                    # 点赞
                    user_weibo_item['retweet_attitudes_count'] = retweet_weibo['attitudes_count']
                    # 图片
                    if retweet_weibo['pic_ids']:
                        user_weibo_pics_item = UserWeiboPicsItem()
                        retweet_weibo_pic_urls = []
                        for pic in retweet_weibo['pics']:
                            pic_url = pic['large']['url'].replace('\\', '')
                            retweet_weibo_pic_urls.append(pic_url)
                        user_weibo_item['retweet_pic_urls'] = retweet_weibo_pic_urls
                        user_weibo_pics_item['mid'] = user_weibo['mid'] + \
                            '_retweet_' + retweet_weibo['mid']
                        user_weibo_pics_item['pic_urls'] = retweet_weibo_pic_urls
                        yield user_weibo_pics_item

                    if 'page_info' in retweet_weibo:
                        # 视频
                        if retweet_weibo['page_info']['type'] == 'video':
                            user_weibo_videos_item = UserWeiboVideosItem()
                            user_weibo_videos_item['mid'] = user_weibo['mid'] + \
                                '_retweet_' + retweet_weibo['mid']
                            retweet_weibo_video_urls = retweet_weibo['page_info']['urls']
                            if 'mp4_720p_mp4' in retweet_weibo_video_urls:
                                video_url = retweet_weibo_video_urls['mp4_720p_mp4'].replace(
                                    '\\', '')
                            elif 'mp4_hd_mp4' in retweet_weibo_video_urls:
                                video_url = retweet_weibo_video_urls['mp4_hd_mp4'].replace(
                                    '\\', '')
                            else:
                                video_url = retweet_weibo_video_urls['mp4_ld_mp4'].replace(
                                    '\\', '')
                            user_weibo_item['retweet_video_url'] = video_url
                            user_weibo_videos_item['video_url'] = video_url
                            yield user_weibo_videos_item
                        # 文章
                        if retweet_weibo['page_info']['type'] == 'article':
                            user_weibo_item['retweet_article_url'] = retweet_weibo['page_info']['page_url'].replace(
                                '\\', '')
                yield user_weibo_item
