import pandas as pd
import numpy as np
import time

# 读取路径
# 'uid/user_info.csv'
# 'uid/weibo_info.csv'
user_info_df = pd.read_csv('')
user_weibo_df = pd.read_csv('')
# 处理时间
for i in range(user_weibo_df.shape[0]):
    user_weibo_df.loc[i, 'created_at'] = time.strptime(
        user_weibo_df.loc[i, 'created_at'], '%a %b %d %H:%M:%S %z %Y')
    user_weibo_df.loc[i,
                      'created_year'] = user_weibo_df.loc[i, 'created_at'][0]
    user_weibo_df.loc[i,
                      'created_month'] = user_weibo_df.loc[i, 'created_at'][1]
    user_weibo_df.loc[i, 'created_day'] = user_weibo_df.loc[i, 'created_at'][2]
    user_weibo_df.loc[i,
                      'created_hour'] = user_weibo_df.loc[i, 'created_at'][3]

user_weibo_df.loc[:, 'created_year':'created_hour'] = user_weibo_df.loc[:,
                                                                        'created_year':'created_hour'].astype(int)
user_weibo_df = user_weibo_df.sort_values(by='created_at', ascending=True)
# 处理转发数
user_weibo_df['reposts_count'].replace('100万+', 1000000, inplace=True)
user_weibo_df.loc[:, 'reposts_count'] = user_weibo_df.loc[:,
                                                          'reposts_count'].astype(int)
# 处理评论数
user_weibo_df['comments_count'].replace('100万+', 1000000, inplace=True)
user_weibo_df.loc[:, 'comments_count'] = user_weibo_df.loc[:,
                                                           'comments_count'].astype(int)


# 名称
# user_name = user_info_df['screen_name'].str.split()[0][0]
user_name = user_info_df['screen_name'].values[0]
# 粉丝数
user_followers_count = int(user_info_df['followers_count'])
# 关注数
user_follow_count = int(user_info_df['follow_count'])
# 总微博数
user_statuses_count = int(user_info_df['statuses_count'])
# 每月微博数
user_weibo_month_df = user_weibo_df.groupby(
    ['created_year', 'created_month']).count().loc[:, 'created_at']

'''
原创
'''
original_weibo_df = user_weibo_df.loc[user_weibo_df['retweet_created_at'].isnull(
)]
# 原创微博数
total_original_weibo = original_weibo_df.shape[0]
# 最高转发
max_reposts_count_original_weibo = original_weibo_df.loc[:, 'reposts_count'].max(
)
# 最高评论
max_comments_count_original_weibo = original_weibo_df.loc[:, 'comments_count'].max(
)
# 最高点赞
max_attitudes_count_original_weibo = original_weibo_df.loc[:, 'attitudes_count'].max(
)

'''
视频
'''
original_weibo_video_df = original_weibo_df.loc[original_weibo_df['video_url'].notnull(
)]
# 视频数
original_weibo_video_count = original_weibo_video_df.shape[0]
# 最高转发
max_reposts_count_original_weibo_video = original_weibo_video_df.loc[:, 'reposts_count'].max(
)
# 最高评论
max_comments_count_original_weibo_video = original_weibo_video_df.loc[:, 'comments_count'].max(
)
# 最高点赞
max_attitudes_count_original_weibo_video = original_weibo_video_df.loc[:, 'attitudes_count'].max(
)
# 每月视频数


'''
图片
'''
original_weibo_pic_df = original_weibo_df.loc[original_weibo_df['pic_urls'].notnull(
)]
# 图片数
original_weibo_pic_count = original_weibo_pic_df.shape[0]
# 最高转发
max_reposts_count_original_weibo_pic = original_weibo_pic_df.loc[:, 'reposts_count'].max(
)
# 最高评论
max_comments_count_original_weibo_pic = original_weibo_pic_df.loc[:, 'comments_count'].max(
)
# 最高点赞
max_attitudes_count_original_weibo_pic = original_weibo_pic_df.loc[:, 'attitudes_count'].max(
)
# 每月图片数


'''
文章
'''
original_weibo_article_df = original_weibo_df.loc[original_weibo_df['article_url'].notnull(
)]
# 文章数
original_weibo_article_count = original_weibo_article_df.shape[0]
# 最高转发
max_reposts_count_original_weibo_article = original_weibo_article_df.loc[:, 'reposts_count'].max(
)
# 最高评论
max_comments_count_original_weibo_article = original_weibo_article_df.loc[:, 'comments_count'].max(
)
# 最高点赞
max_attitudes_count_original_weibo_article = original_weibo_article_df.loc[:, 'attitudes_count'].max(
)
# 每月文章数


'''
转发
'''
retweet_weibo_df = user_weibo_df.loc[user_weibo_df['retweet_created_at'].notnull(
)]
# 转发微博数
total_retweet_weibo = retweet_weibo_df.shape[0]
# 转发视频数
retweet_weibo_video_count = retweet_weibo_df.loc[retweet_weibo_df['retweet_video_url'].notnull(
)].shape[0]
# 转发图片数
retweet_weibo_pic_count = retweet_weibo_df.loc[retweet_weibo_df['retweet_pic_urls'].notnull(
)].shape[0]
# 转发文章数
retweet_weibo_article_count = retweet_weibo_df.loc[retweet_weibo_df['retweet_article_url'].notnull(
)].shape[0]

d = {
    '名称': user_name,
    '粉丝数': user_followers_count,
    '关注数': user_follow_count,
    '总微博数': user_statuses_count,
    # 每月微博数

    '原创微博数': total_original_weibo,
    '最高转发微博': max_reposts_count_original_weibo,
    '最高评论微博': max_comments_count_original_weibo,
    '最高点赞微博': max_attitudes_count_original_weibo,

    '视频数': original_weibo_video_count,
    '最高转发视频': max_reposts_count_original_weibo_video,
    '最高评论视频': max_comments_count_original_weibo_video,
    '最高点赞视频': max_attitudes_count_original_weibo_video,
    # 每月视频数

    '图片数': original_weibo_pic_count,
    '最高转发图片': max_reposts_count_original_weibo_pic,
    '最高评论图片': max_comments_count_original_weibo_pic,
    '最高点赞图片': max_attitudes_count_original_weibo_pic,
    # 每月图片数

    '文章数': original_weibo_article_count,
    '最高转发文章': max_reposts_count_original_weibo_article,
    '最高评论文章': max_comments_count_original_weibo_article,
    '最高点赞文章': max_attitudes_count_original_weibo_article,
    # 每月文章数

    '转发微博数': total_retweet_weibo,
    '转发视频数': retweet_weibo_video_count,
    '转发图片数': retweet_weibo_pic_count,
    '转发文章数': retweet_weibo_article_count,
}

for k, v in d.items():
    print(f'{k}:{v}')
