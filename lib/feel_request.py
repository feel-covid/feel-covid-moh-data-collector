import datetime
import requests
from urllib.parse import urlencode
from hourly_update import HourlyUpdate


def feel_request():
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)

    params = {
        'startDate': f"\"{yesterday}\"",
        'endDate': f"\"{today}\"",
        'name': 'israel'
    }

    url = f'https://api.feel.co.il/api/country/stats?' + urlencode(params)

    response = requests.get(url)

    return HourlyUpdate.from_hourly_update_dict(response.json()[-1])


if __name__ == '__main__':
    feel_request()
