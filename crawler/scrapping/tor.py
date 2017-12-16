import requests

from crawler.config import TorConfig


def send_get_request(url):
    response = requests.get(url,
                            proxies=TorConfig.TOR_PROXIES,
                            timeout=TorConfig.TIMEOUT)
    if response.status_code != 200:
        raise IOError("something went wrong:{0}".format(response.text))
    return response.text
