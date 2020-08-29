import datetime
import requests
from urllib.parse import urlencode
from models.hourly_update import HourlyUpdate
from connectors import telegram_connector_instance
from moh_request import moh_request
from utils import gen_iso_string


def _feel_request():
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)

    params = {
        'startDate': f"\"{yesterday}\"",
        'endDate': f"\"{today}\"",
        'name': 'israel'
    }

    url = f'https://api.feel.co.il/api/country/stats?' + urlencode(params)

    response = requests.get(url)

    return response.json()[-1]


def job_notify_on_moh_update(notifier=telegram_connector_instance):
    try:
        moh_data = HourlyUpdate.from_moh_response(moh_request())
        feel_data = HourlyUpdate.from_hourly_update_dict(_feel_request())

        print('---------------------------')
        if feel_data.date != moh_data.date:
            url = f"https://priceless-murdock-f4daba.netlify.app/?moh-data={moh_data.as_base64_string()}"
            notifier.notify(
                f"הנתונים בדשבורד הקורונה של משרד הבריאות עודכנו, ניתן לעדכן את האתר כאן:\n {url}")
            return
        else:
            print(f"{gen_iso_string(datetime.datetime.now())} - No Update Found")
            print(f"Feel Date - {feel_data.date}")
            print(f"Moh Date  - {moh_data.date}")

        values_diff = moh_data.compare_values(feel_data)

        if values_diff:
            header = 'נמצאו ערכים לא תואמים בין האתר לדשבורד משרד הבריאות'
            nl = '\n'
            notifier.notify(f'{header}:\n {nl.join(values_diff)}')
        else:
            print(f'All values are correct: {values_diff}')
        print('---------------------------')

    except Exception as ex:
        notifier.notify(f'התרחשה שגיאה בבדיקה: {ex}')
