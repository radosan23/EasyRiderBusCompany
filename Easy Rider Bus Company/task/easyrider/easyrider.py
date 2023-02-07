from collections import Counter
import json
import re


class EasyRider:

    def __init__(self, data):
        self.data = data
        self.template = {'stop_name': r'([A-Z][a-z]+ )+(Road|Avenue|Boulevard|Street)$',
                         'stop_type': r'[SOF]?$',
                         'a_time': r'([01]\d|2[0-3]):[0-5]\d$'}
        self.field_errors = Counter()

    def check_data(self):
        for dataset in self.data:
            for key, value in dataset.items():
                if key in self.template.keys() and re.match(self.template[key], value) is None:
                    self.field_errors.update([key])

    def disp_info(self):
        print(f'Format validation: {self.field_errors.total()} errors')
        for key in self.template.keys():
            print(f'{key}: {self.field_errors[key]}')


def main():
    data = json.loads(input())
    rider = EasyRider(data)
    rider.check_data()
    rider.disp_info()


if __name__ == '__main__':
    main()
