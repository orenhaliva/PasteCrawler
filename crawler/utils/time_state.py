import logging
import os
from datetime import datetime

from crawler.config import ScheduleConfig


class LastTime(object):
    def __init__(self):
        self._last_run_time = self._get_last_run_time()
        self.logger = logging.getLogger(__name__)

    def _get_last_run_time(self):
        if not os.path.exists(ScheduleConfig.LOCK_FILE_PATH):
            return None

        with open(ScheduleConfig.LOCK_FILE_PATH, "r") as f:
            date = f.read()

        try:
            return datetime.strptime(date, ScheduleConfig.DATETIME_FORMAT)
        except TypeError:
            self.logger.exception("The date: {0} inside the file wasn't good"
                                  .format(date))
            raise

    @property
    def state(self):
        return self._last_run_time

    @state.setter
    def state(self, date):
        if self._last_run_time:
            new_date = max(date, self._last_run_time)
        else:
            new_date = date

        with open(ScheduleConfig.LOCK_FILE_PATH, "w") as f:
            date_str = new_date.strftime(ScheduleConfig.DATETIME_FORMAT)
            f.write(date_str)
