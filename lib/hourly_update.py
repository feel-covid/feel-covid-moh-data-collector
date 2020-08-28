from __future__ import annotations
from utils import gen_iso_string, parse_iso_string
import json
import base64


class HourlyUpdate:
    def __init__(self,
                 total,
                 date,
                 severe,
                 intubated,
                 mid,
                 home,
                 hospital,
                 recovered,
                 deceased):
        self.total = total
        self.date = parse_iso_string(date)
        self.severe = severe
        self.intubated = intubated
        self.mid = mid
        self.home = home
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
                'hospital': self.hospital,
                'hotel': 0,
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
            total=hourly_update_dict.get('total', 0),
            date=hourly_update_dict['date'],
            severe=hourly_update_dict['severe']['cases'],
            intubated=hourly_update_dict['severe']['intubated'],
            mid=hourly_update_dict['mid']['cases'],
            home=hourly_update_dict['treatment']['home'],
            hospital=hourly_update_dict['treatment']['hospital'],
            recovered=hourly_update_dict['recovered'],
            deceased=hourly_update_dict['deceased']
        )

    def compare_values(self, other: HourlyUpdate):
        excluded_keys = ('date', 'total')
        diff = []

        self_values = self.__dict__.items()
        other_values = other.__dict__

        for key, value in self_values:
            if key not in excluded_keys and other_values[key] != value:
                diff.append(f'Wrong value on field "{key}": {value} != {other_values[key]}')

        return diff
