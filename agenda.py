from datetime import datetime



def get_rang_week(self, num_week):
    """
    :param num_week:
    :return:
    """
    _now_week = this_week()
    dif_day = ( _now_week - num_week ) * 7 + datetime.today().weekday()
    day = self.dif_date(dif_day)
    day_week = []
    day_week.append({
                    'date_init' : day,
                    'date_final' : self.dif_date(-6, day)
    })
    return day_week

def get_gap_week(self, _date_init):
    """
    :param _date_init:
    :return:  all days in the week
    """
    week = []
    day_week = 0
    while day_week < 7:
        week.append(self.dif_date(-day_week, _date_init))
        day_week += 1
    return week

def dif_date(self, day, date=None):
    """
    :param day:
    :param date:
    :return:
    """
    if date is None: date = datetime.today().date()
    day = date.toordinal() - day
    return date.fromordinal(day)
