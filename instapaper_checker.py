import requests
import arrow
from dateutil import tz
from pushover import Client
from os.path import dirname, realpath, join

CWD = dirname(realpath(__file__))
GDPR_MESSAGE = 'Instapaper is temporarily unavailable for residents in Europe'

def send_pushover_notification(message):
    print ('Sending Pushover notification')
    config_path = join(CWD, 'pushoverrc')
    Client(config_path=config_path).send_message(message, title="Instapaper status:")

def instapaper_page_has_gdpr_message():
    request = requests.get('https://www.instapaper.com/')
    return GDPR_MESSAGE in request.text

def days_between_now_and_gdpr_day():
    gdpr_day = arrow.get(2018, 5, 25, tzinfo=tz.gettz('Europe/London'))
    return (arrow.utcnow().to('Europe/London') - gdpr_day).days
    

def check_instapaper_status():

    print('{}: Checking Instapaper EU status'.format(arrow.utcnow().to('Europe/London').format('YYYY-MM-DD HH:mm:ss')))
    days_since_gdpr = days_between_now_and_gdpr_day()
    
    if (instapaper_page_has_gdpr_message()):
        message = 'Instapaper is STILL is not up for EU users. GDPR came in {} days ago...'.format(days_since_gdpr)
    else:
        message = 'Instapaper is back up! After a mere {} days...'.format()

    send_pushover_notification(message)

if __name__ == '__main__':
    check_instapaper_status()
    print('\n')