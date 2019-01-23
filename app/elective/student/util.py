from datetime import datetime

def datetime_from_string(time_str):
    return datetime.strptime(str(time_str), '%Y-%m-%d %H:%M:%S')

def us_format(datetime):
    return '{:%B %d, %Y}'.format(datetime)