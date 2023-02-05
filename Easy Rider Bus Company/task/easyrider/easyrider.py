from collections import Counter
import json


class EasyRider:

    def __init__(self, data):
        self.data = data
        self.field_errors = Counter()

    def check_data(self):
        template = {'bus_id': int, 'stop_id': int, 'stop_name': str,
                    'next_stop': int, 'stop_type': str, 'a_time': str}
        for dataset in self.data:
            for key, value in dataset.items():
                if type(value) != template[key] or \
                        template[key] == str and key != 'stop_type' and not value or \
                        key == 'stop_type' and len(value) > 1:
                    self.field_errors.update([key])

    def disp_info(self):
        print(f'Type and required field validation: {self.field_errors.total()} errors')
        for key in self.data[0].keys():
            print(f'{key}: {self.field_errors[key]}')


def main():
    data = json.loads(input())
    rider = EasyRider(data)
    rider.check_data()
    rider.disp_info()


if __name__ == '__main__':
    main()
