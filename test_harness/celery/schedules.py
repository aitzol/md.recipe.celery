CRON_REPR = """\
<crontab: {0.minute} {0.hour} {0.day_of_week} \
{0.day_of_month} {0.month_of_year} (m/h/d/dM/MY)>\
"""

class crontab(object):
    """ Mock object for testing crontab """
    def __init__(self, minute='*', hour='*', day_of_week='*',
                 day_of_month='*', month_of_year='*', nowfun=None, app=None):
        self.minute = minute
        self.hour = hour
        self.day_of_week = day_of_week
        self.day_of_month = day_of_month
        self.month_of_year = month_of_year
        self.nowfun = nowfun
        self.app = app

    def __repr__(self):
        return CRON_REPR.format(self)
