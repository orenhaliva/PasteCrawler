class TorConfig(object):
    URL = 'http://nzxj65x32vh2fkhk.onion/'
    TIMEOUT = 30

    TOR_PROXIES = {
        'http': 'socks5h://tor:9050',
        'https': 'socks5h://tor:9050'
    }


class PasteXPathConfig(object):
    PASTE_URL = '//div[@class="pre-info pre-header"]' \
                '//a[@class="btn btn-success"]/@href'
    PAGINATION = '//ul[@class="pagination"]/li'
    PASTE_ELEMENT = '//section[@id="show"]/div[1]'
    TITLE = '//h4/text()'
    CONTENT = '//ol/li/div/text()'
    FOOTER = '//div[@class="pre-info pre-footer"]' \
             '//div[@class="col-sm-6"][1]//text()'


class PasteNormalizeConfig(object):
    FOOTER_REGEX = r"\s+Posted by (?P<author>\w+) at (?P<date>.*) UTC\s+"
    DATE_FORMAT = '%d %b %Y, %H:%M:%S'
    UNKNOWN_AUTHORS = ["Guest", "Unknown", "Anonymous"]
    DEFAULT_AUTHOR = ""


class DBConfig(object):
    PATH_TO_DB = 'db.json'


class ScheduleConfig(object):
    INTERVAL_IN_SECONDS = 10
    DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
    LOCK_FILE_PATH = "lock.txt"
