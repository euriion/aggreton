# Scrapy settings for daumpeople project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'daumkeywords_bot'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

ITEM_PIPELINES = {
    'scrapy.contrib.pipeline.images.ImagesPipeline': 1,
    # 'daumpeople.pipelines.DaumPeopleProfilePipeline': 50,
    # 'daumpeople.pipelines.DeduplicatePeopleNamePipeline': 100,
    # 'daumpeople.pipelines.DaumPeopleNamePipeline': 101,
    'pipelines.DaumKeywordPipeline': 102,
    # 'daumpeople.pipelines.FinalPipeline': 100,
}

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36"
DOWNLOAD_DELAY = 1
COOKIES_ENABLED = True

# import os
# IMAGES_STORE = "%s/data/crawled_images" % os.environ['DZ_HOME']
# IMAGES_EXPIRES = 30
# IMAGES_THUMBS = {
#     'small': (50, 50),
#     'big': (270, 270),
# }
# IMAGES_MIN_HEIGHT = 110
# IMAGES_MIN_WIDTH = 110