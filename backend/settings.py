BOT_NAME = 'selenium'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

ITEM_PIPELINES = {
    'pipelines.SeleniumPipeline': 270,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'oddchecker (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Create Database
DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'benglaser',
    'password': '',
    'database': 'scrape'
}


