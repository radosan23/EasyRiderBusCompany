from collections import Counter
import json
import re


class EasyRider:

    def __init__(self, data):
        self.data = data
        self.template = {'bus_id': {'type': int},
                         'stop_id': {'type': int},
                         'stop_name': {'type': str, 'format': r'([A-Z][a-z]+ )+(Road|Avenue|Boulevard|Street)$'},
                         'next_stop': {'type': int},
                         'stop_type': {'type': str, 'format': r'[SOF]?$'},
                         'a_time': {'type': str, 'format': r'([01]\d|2[0-3]):[0-5]\d$'}}
        self.field_errors = Counter()
        self.lines = {}

    def check_data(self):
        for dataset in self.data:
            for key, value in dataset.items():
                if type(value) != self.template[key]['type'] or \
                        type(value) == str and re.match(self.template[key]['format'], value) is None:
                    self.field_errors.update([key])
            self.lines.setdefault(dataset['bus_id'], []).append(dataset['stop_id'])

    def disp_info(self, *args):
        if 'errors' in args:
            print(f'\nValidation: {self.field_errors.total()} errors')
            for key in self.template.keys():
                print(f'{key}: {self.field_errors[key]}')
        if 'lines' in args:
            print('\nLine names and number of stops:')
            for line, stops in self.lines.items():
                print(f'bus_id: {line}, stops: {len(stops)}')


def main():
    data = json.loads(input())
    rider = EasyRider(data)
    rider.check_data()
    rider.disp_info('lines', 'errors')


if __name__ == '__main__':
    main()
