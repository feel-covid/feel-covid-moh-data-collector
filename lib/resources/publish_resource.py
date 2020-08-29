import json
import os

import requests
from flask_restful import Resource

from moh_request import moh_request


def _aggregate_ird(moh_response):
    daily_ird_dict = {
        current_day['date']: {'infected': current_day['amount'], 'recovered': current_day['recovered'],
                              'date': current_day['date']} for current_day in moh_response[1]['data']}

    for current_day in moh_response[6]['data']:
        daily_ird_dict[current_day['date']]['deceased'] = current_day['amount']

    return list(daily_ird_dict.values())[-20:]


def _aggregate_test_amount(moh_response):
    test_amount = []

    for current_day in moh_response[14]['data']:
        test_amount.append({
            'date': current_day['date'],
            'amount': current_day['amountVirusDiagnosis'],
            'positive': 0 if current_day['positiveAmount'] == -1 else round(
                current_day['positiveAmount'] / current_day['amountVirusDiagnosis'] * 100, 2)
        })

    return test_amount[-20:]


class PublishResource(Resource):
    def __init__(self):
        super().__init__()

    def gen_post_struct(self, data_key, data):
        return {
            'data': {
                'countryId': os.getenv('FEEL_COUNTRY_ID'),
                data_key: data
            }
        }

    def post(self):
        moh_response = moh_request()
        daily_ird_data = self.gen_post_struct('dailyStatsData', _aggregate_ird(moh_response))
        daily_test_amount_data = self.gen_post_struct('testsData', _aggregate_test_amount(moh_response))

        daily_stat_url = f'{os.getenv("FEEL_API_URL")}/api/daily-stats'
        test_amount_url = f'{os.getenv("FEEL_API_URL")}/api/tests-amount'
        headers = {'x-api-key': os.getenv('FEEL_API_KEY'), 'Content-Type': 'application/json'}

        daily_ird_res = requests.put(url=daily_stat_url, data=json.dumps(daily_ird_data), headers=headers)
        daily_test_amount_res = requests.put(url=test_amount_url, data=json.dumps(daily_test_amount_data),
                                             headers=headers)

        response = {
            'status': {
                'daily_ird': daily_ird_res.status_code,
                'daily_test_amount': daily_test_amount_res.status_code
            },
            'data': {
                'daily_ird': daily_ird_data,
                'daily_test_amount': daily_test_amount_data
            },
        }

        return response
