import json
import os

import requests
from flask_restful import Resource

from moh_request import moh_request


class PublishResource(Resource):
    def __init__(self):
        super().__init__()
        self.days_amount_to_update = int(os.getenv('DAYS_AMOUNT_TO_UPDATE'))

    def gen_post_struct(self, data_key, data):
        return {
            'data': {
                'countryId': os.getenv('FEEL_COUNTRY_ID'),
                data_key: data
            }
        }

    def _aggregate_ird(self, moh_response):
        daily_ird_dict = {
            current_day['date']: {'infected': current_day['amount'], 'recovered': current_day['recovered'],
                                  'date': current_day['date']} for current_day in
            moh_response[1]['data'][-self.days_amount_to_update:]}

        for current_day in moh_response[5]['data'][-self.days_amount_to_update:]:
            if daily_ird_dict.get(current_day['date']) is not None:
                daily_ird_dict[current_day['date']]['deceased'] = current_day['amount']

        return list(daily_ird_dict.values())

    def _aggregate_test_amount(self, moh_response):
        test_amount = []

        for current_day in moh_response[6]['data'][-self.days_amount_to_update:]:
            test_amount.append({
                'date': current_day['date'],
                'amount': current_day['amountVirusDiagnosis'],
                'positive': 0 if current_day['positiveAmount'] == -1 else round(
                    current_day['positiveAmount'] / current_day['amountVirusDiagnosis'] * 100, 2)
            })

        return test_amount

    def _aggregate_vaccinations(self, moh_response):
        return [
            {
                'date': current_day['Day_Date'],
                'first_dose_amount': current_day['vaccinated'],
                'first_dose_percentage': current_day['vaccinated_population_perc'],
                'first_dose_cumulative': current_day['vaccinated_cum'],
                'second_dose_amount': current_day['vaccinated_seconde_dose'],
                'second_dose_percentage': current_day['vaccinated_seconde_dose_population_perc'],
                'second_dose_cumulative': current_day['vaccinated_seconde_dose_cum']
            } for current_day in moh_response[7]['data'][-self.days_amount_to_update:]
        ]

    def post(self):
        moh_response = moh_request()
        daily_ird_data = self.gen_post_struct('dailyStatsData', self._aggregate_ird(moh_response))
        daily_test_amount_data = self.gen_post_struct('testsData', self._aggregate_test_amount(moh_response))
        daily_vaccinations_data = self.gen_post_struct('dailyVaccinationsData',
                                                       self._aggregate_vaccinations(moh_response))

        daily_ird_url = f'{os.getenv("FEEL_API_URL")}/api/daily-ird'
        daily_test_amount_url = f'{os.getenv("FEEL_API_URL")}/api/daily-test-amount'
        daily_vaccinations_url = f'{os.getenv("FEEL_API_URL")}/api/daily-vaccinations'
        headers = {'x-api-key': os.getenv('FEEL_API_KEY'), 'Content-Type': 'application/json'}

        daily_ird_res = requests.put(url=daily_ird_url, data=json.dumps(daily_ird_data), headers=headers)
        daily_test_amount_res = requests.put(url=daily_test_amount_url, data=json.dumps(daily_test_amount_data),
                                             headers=headers)
        daily_vaccinations_res = requests.put(url=daily_vaccinations_url, data=json.dumps(daily_vaccinations_data),
                                              headers=headers)

        response = {
            'status': {
                'daily_ird': daily_ird_res.status_code,
                'daily_test_amount': daily_test_amount_res.status_code,
                'daily_vaccinations': daily_vaccinations_res.status_code
            },
            'data': {
                'daily_ird': daily_ird_data,
                'daily_test_amount': daily_test_amount_data,
                'daily_vaccinations': daily_vaccinations_data
            },
        }

        return response
