from __future__ import annotations
from utils import gen_iso_string, parse_iso_string
import json
import base64
from functools import reduce


class HourlyUpdate:
    def __init__(self,
                 total,
                 date,
                 severe,
                 intubated,
                 mid,
                 home,
                 hotel,
                 hospital,
                 recovered,
                 deceased):
        self.total = total
        self.date = parse_iso_string(date)
        self.severe = severe
        self.intubated = intubated
        self.mid = mid
        self.home = home
        self.hotel = hotel
        self.hospital = hospital
        self.recovered = recovered
        self.deceased = deceased

    def as_dict(self):
        hourly_update_dict = {
            'total': self.total,
            'date': gen_iso_string(self.date),
            'severe': {
                'cases': self.severe,
                'intubated': self.intubated,
            },
            'mid': {
                'cases': self.mid
            },
            'treatment': {
                'home': self.home,
                'hotel': self.hotel,
                'hospital': self.hospital,
                'undecided': 0
            },
            'recovered': self.recovered,
            'deceased': self.deceased
        }

        return hourly_update_dict

    def as_json(self) -> str:
        return json.dumps(self.as_dict())

    def as_base64_string(self):
        return base64.b64encode(bytes(self.as_json(), 'utf-8')).decode('utf-8')

    @classmethod
    def from_hourly_update_dict(cls, hourly_update_dict):
        return cls(
            total=hourly_update_dict['deceased'] + hourly_update_dict['recovered'] + hourly_update_dict['mid'][
                'cases'] + hourly_update_dict['severe']['cases'] + hourly_update_dict['light']['cases'],
            date=hourly_update_dict['date'],
            severe=hourly_update_dict['severe']['cases'],
            intubated=hourly_update_dict['severe']['intubated'],
            mid=hourly_update_dict['mid']['cases'],
            home=hourly_update_dict['treatment']['home'],
            hotel=hourly_update_dict['treatment']['hotel'],
            hospital=hourly_update_dict['treatment']['hospital'],
            recovered=hourly_update_dict['recovered'],
            deceased=hourly_update_dict['deceased']
        )

    @staticmethod
    def _aggregate_moh_field(res, index, key='amount'):
        return reduce(
            lambda x, y: x + y,
            map(
                lambda x: x[key],
                res[index]['data']
            )
        )

    @classmethod
    def from_moh_response(cls, response):
        return cls(
            total=cls._aggregate_moh_field(response, 1),
            date=response[0]['data']['lastUpdate'],
            severe=response[2]['data'][0]['amount'],
            intubated=response[4]['data'][-1]['CountBreath'],
            mid=response[2]['data'][1]['amount'],
            home=response[3]['data'][0]['amount'],
            hotel=response[3]['data'][1]['amount'],
            hospital=response[3]['data'][2]['amount'],
            recovered=cls._aggregate_moh_field(response, 1, 'recovered'),
            deceased=response[5]['data'][-1]['total']
        )

    def compare_values(self, other: HourlyUpdate):
        excluded_keys = ('date',)
        diff = []
        validated_values = []

        self_values = self.__dict__.items()
        other_values = other.__dict__

        for key, value in self_values:
            if key not in excluded_keys:
                if other_values[key] != value:
                    diff.append(f'Wrong value on field "{key}": {value} != {other_values[key]}')
                else:
                    validated_values.append(f'Correct value for field "{key}": {value} == {other_values[key]}')

        return diff, validated_values
