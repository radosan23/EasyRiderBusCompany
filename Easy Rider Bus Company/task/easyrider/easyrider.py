from collections import Counter
import itertools
import json
import re
import sys


class BStop:

    def __init__(self, data):
        self.id = data['stop_id']
        self.name = data['stop_name']
        self.next = data['next_stop']
        self.type = data['stop_type']
        self.arrival = data['a_time']


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
        self.s_stops = {'Start stops': set(), 'Transfer stops': set(), 'Finish stops': set()}
        self.arr_err = {}

    def check_data(self):
        for dataset in self.data:
            for key, value in dataset.items():
                if type(value) != self.template[key]['type'] or \
                        type(value) == str and re.match(self.template[key]['format'], value) is None:
                    self.field_errors.update([key])

    def check_lines(self):
        for dataset in self.data:
            self.lines.setdefault(dataset['bus_id'], []).append(BStop(dataset))
        for line, stops in self.lines.items():
            if [stop.type for stop in stops].count('S') != 1 or [stop.type for stop in stops].count('F') != 1:
                print(f'There is no start or end stop for the line: {line}.')
                sys.exit()
            for stop in stops:
                if stop.type == 'S':
                    self.s_stops['Start stops'].add(stop.name)
                elif stop.type == 'F':
                    self.s_stops['Finish stops'].add(stop.name)
        for l1, l2 in itertools.combinations(self.lines.values(), 2):
            self.s_stops['Transfer stops'].update(set(x.name for x in l1) & set(x.name for x in l2))

    def check_arrivals(self):
        for line, stops in self.lines.items():
            stops_sorted = [stop for stop in stops if stop.type == 'S']
            next_s = stops_sorted[0].next
            for _ in range(len(stops)-1):
                stops_sorted.extend([stop for stop in stops if stop.id == next_s])
                next_s = stops_sorted[-1].next
            prev_time = '00:00'
            for stop in stops_sorted:
                if stop.arrival <= prev_time:
                    self.arr_err[line] = stop.name
                    break
                prev_time = stop.arrival

    def disp_info(self, *args):
        if 'errors' in args:
            print(f'\nValidation: {self.field_errors.total()} errors')
            for key in self.template.keys():
                print(f'{key}: {self.field_errors[key]}')
        if 'lines' in args:
            print('\nLine names and number of stops:')
            for line, stops in self.lines.items():
                print(f'bus_id: {line}, stops: {len(stops)}')
        if 'stops' in args:
            print()
            for key, value in self.s_stops.items():
                print(key + ':', len(value), sorted(list(value)))
        if 'arrivals' in args:
            print('\nArrival time test:')
            if not self.arr_err:
                print('OK')
            else:
                for line, stop in self.arr_err.items():
                    print(f'bus_id line {line}: wrong time on station {stop}')


def main():
    data = json.loads(input())
    rider = EasyRider(data)
    rider.check_data()
    rider.check_lines()
    rider.check_arrivals()
    rider.disp_info('arrivals')


if __name__ == '__main__':
    main()
