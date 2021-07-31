import datetime
import requests
from urllib.parse import urlencode
from models.hourly_update import HourlyUpdate
from connectors import telegram_connector_instance
from moh_request import moh_request
from utils import gen_iso_string
import traceback
import os


def _feel_request():
    today = datetime.datetime.now()
    week_ago = today - datetime.timedelta(days=800)

    params = {
        'startDate': f"\"{week_ago}\"",
        'endDate': f"\"{today}\"",
        'name': 'israel'
    }

    url = f'{os.getenv("FEEL_API_URL")}/api/country/hourly-updates?' + urlencode(params)

    response = requests.get(url, timeout=20)

    return response.json()[-1]


def job_notify_on_moh_update(notifier=telegram_connector_instance):
    try:
        moh_data = HourlyUpdate.from_moh_response(moh_request())
        feel_data = HourlyUpdate.from_hourly_update_dict(_feel_request())
        url = f"{os.getenv('SIMPLE_GUI_URL')}/?moh-data={moh_data.as_base64_string()}"

        print('###########################')
        print('---------------------------')
        if moh_data.date > feel_data.date:
            notifier.notify(
                f"הנתונים בדשבורד הקורונה של משרד הבריאות עודכנו, ניתן לעדכן את האתר כאן:\n {url}")
            return
        else:
            print(f"{gen_iso_string(datetime.datetime.now())} - No Update Found")
            print(f"Feel Date - {feel_data.date}")
            print(f"Moh Date  - {moh_data.date}")
        print('---------------------------')

        if moh_data.date == feel_data.date:
            values_diff, validated_values = moh_data.compare_values(feel_data)

            if values_diff:
                header = 'נמצאו ערכים לא תואמים בין האתר לדשבורד משרד הבריאות'
                nl = '\n'
                notifier.notify(f'{header}:\n {nl.join(values_diff)}')
                notifier.notify(
                    f"קישור לנתונים המעודכנים:\n {url}")
            else:
                print('All values are correct:')
                print('\n'.join(validated_values))
            print('---------------------------')

    except Exception as ex:
        traceback.print_exc()
        if os.getenv("NOTIFICATION_ON_FAILURE") == '1':
            notifier.notify(f'התרחשה שגיאה בבדיקה: {ex}')
