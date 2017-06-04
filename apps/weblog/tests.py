#from .models import PvModel,UvModel,IvModel
# Create your tests here.
import datetime

def pvview():
    now = datetime.datetime.now()
    now_formatted = now.strftime("%Y-%m-%d")
    yesterday = now + datetime.timedelta(days=-1)
    yesterday_formatted = yesterday.strftime("%Y-%m-%d")
    print now_formatted,yesterday_formatted
    if yesterday_formatted > now_formatted:
        print '1'

pvview()