# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import scrapy
import random
import logging
from fake_useragent import UserAgent
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline


logger = logging.getLogger(__name__)
ua = UserAgent()
headers = {
    'User-Agent': ua.random
}


class UserInfoPipeline:
    def process_item(self, item, spider):
        if item.__class__.__name__ == 'UserInfoItem':
            print('start write user info...')
            fp = open('./user_info.csv', 'w',
                      newline='', encoding='utf-8')
            fieldnames = [
                'uid',
                'screen_name',
                'statuses_count',
                'description',
                'gender',
                'followers_count',
                'follow_count',
            ]
            writer = csv.DictWriter(fp, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(item)
            print('user info over...')
            fp.close()
        # item传递给下一个执行的管道类
        logger.warning(item)
        return item


class UserWeiboPipeline:
    def open_spider(self, spider):
        print('start write weibo info...')
        self.fp = open('./weibo_info.csv', 'a', newline='', encoding='utf-8')
        self.fieldnames = [
            'created_at',
            'mid',
            'text',
            'source',
            'reposts_count',
            'comments_count',
            'attitudes_count',
            'pic_urls',
            'video_url',
            'article_url',
            # 转发
            'retweet_created_at',
            'retweet_mid',
            'retweet_text',
            'retweet_source',
            'retweet_reposts_count',
            'retweet_comments_count',
            'retweet_attitudes_count',
            'retweet_pic_urls',
            'retweet_video_url',
            'retweet_article_url'
        ]
        self.writer = csv.DictWriter(self.fp, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def process_item(self, item, spider):
        if item.__class__.__name__ == 'UserWeiboItem':
            self.writer.writerow(item)

        # item传递给下一个执行的管道类
        logger.warning(item)
        return item

    def close_spider(self, spider):
        print('weibo info over...')
        self.fp.close()


class WeiboPicsPipeLine(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item.__class__.__name__ == 'UserWeiboPicsItem':
            i = 0
            for pic_url in item['pic_urls']:
                i += 1
                yield scrapy.Request(pic_url, meta={'i': str(i)}, headers=headers)

    def file_path(self, request, response=None, info=None, *, item):
        if item.__class__.__name__ == 'UserWeiboPicsItem':
            fileName = item['mid'] + '_' + request.meta['i'] + '.jpg'
            print(f'{fileName} downloading...')
            return fileName

    def item_complete(self, results, item, info):
        # 返回给下个即将执行的管道类
        logger.warning(item)
        return item


class WeiboVideosPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        if item.__class__.__name__ == 'UserWeiboVideosItem':
            video_url = item['video_url']
            yield scrapy.Request(video_url, headers=headers)

    def file_path(self, request, response=None, info=None, *, item):
        if item.__class__.__name__ == 'UserWeiboVideosItem':
            fileName = item['mid'] + '.mp4'
            print(f'{fileName} downloading...')
            return fileName

    def item_complete(self, results, item, info):
        # 返回给下个即将执行的管道类
        logger.warning(item)
        return item
