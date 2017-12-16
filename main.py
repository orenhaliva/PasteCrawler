import logging
import sys
import time

import schedule

from crawler.config import ScheduleConfig
from crawler.db_handler.paste_dal import PasteDal
from crawler.scrapping.paste_controller import PasteCrawler
from crawler.utils.time_state import LastTime

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def main():
    print("\n\n\n\n\n\n")
    print("<=================== start =====================>")
    ctrl = PasteCrawler()
    dal = PasteDal()

    for paste in ctrl.get_pastes(LastTime().state):
        dal.insert(paste)
        LastTime().state = paste.creation_date

    print("<=================== done ======================>")


if __name__ == '__main__':
    schedule.every(ScheduleConfig.INTERVAL_IN_SECONDS).seconds.do(main)
    while 1:
        schedule.run_pending()

        time.sleep(1)
