from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
import importlib.util
import math
import csv
import sys
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))


class Format(ABC):
    # list - one entry per frame
    #   dict
    #     t: frame rate
    #     c: list - one entry per LED
    #          dict
    #            r: denormalized red value
    #            g: denormalized green value
    #            b: denormalized blue value
    data: list
    ext: str
    filename: str = 'tree_effect'

    def __init__(self, data: Optional[list] = None, filename: Optional[str] = None) -> None:
        self.data = data or []
        self.filename = filename or 'tree_effect'

    def convert(self, other: type[Format], filename: Optional[str] = None) -> Format:
        if not self.data:
            raise EnvironmentError('No data to convert')
        return other(self.data, filename=filename)

    @abstractmethod
    def read(self) -> Format:
        return self

    @abstractmethod
    def write(self) -> Format:
        if not self.data:
            raise EnvironmentError('Data unfilled')
        return self


class Coordinates(Format):
    # data
    # list - one entry per LED
    #   dict
    #     x: x coordinate
    #     y: y coordinate
    #     z: z coordinate
    ext: str = '.csv'
    filename: str = 'coordinates'
    generated: bool

    def __init__(self, data: Optional[list] = None, filename: Optional[str] = None) -> None:
        super().__init__(data, filename)
        self.filename = 'coordinates'
        self.generated = False

    def read(self) -> Coordinates:
        if os.path.exists(self.filename + '.csv'):
            with open(self.filename + '.csv', mode='r', encoding='utf-8-sig') as f:
                for line in f.readlines():
                    x, y, z = line.split(',')
                    self.data.append({'x': float(x), 'y': float(y), 'z': float(z)})
        else:
            self.generated = True
            theta = 0
            height = 0.006
            for _ in range(499):
                radius = (0.006 * 510 - height) / 3.6
                self.data.append({'x': radius * math.cos(theta), 'y': radius * math.sin(theta), 'z': height})
                theta = (theta + 0.174533 / math.pow(radius, 3 / 5)) % 6.28319
                height += 0.006
            self.data.append({'x': 0, 'y': 0, 'z': height + 0.012})
        return self

    def write(self) -> Coordinates:
        raise EnvironmentError('Cannot reconstruct a script representation')


class PY(Format):
    ext: str = '.py'
    coords: Coordinates

    def __init__(self,
                 coordinates: Coordinates,
                 data: Optional[list] = None,
                 filename: Optional[str] = None
                 ) -> None:
        super().__init__(data, filename)
        self.coords = coordinates

    def read(self) -> PY:
        if not os.path.exists(self.filename+self.ext):
            raise EnvironmentError('File does not exist')
        spec = importlib.util.spec_from_file_location('tree_effect', self.filename+self.ext)
        module = importlib.util.module_from_spec(spec)
        tree_effect = sys.modules['tree_effect'] = module
        spec.loader.exec_module(module)
        frame = 1
        storage = None
        while frame <= tree_effect.frame_max():
            storage, colors = tree_effect.run(storage, self.coords.data, frame)
            for i in colors:
                for j in ['r', 'g', 'b']:
                    i[j] = int(i[j]*255)
            self.data.append({'t': tree_effect.frame_rate(), 'c': colors})
            frame += 1
        return self

    def write(self) -> PY:
        raise EnvironmentError('Cannot reconstruct a script representation')


class CSV(Format):
    ext: str = '.csv'

    def read(self) -> CSV:
        if not os.path.exists(self.filename+self.ext):
            raise EnvironmentError('File does not exist')
        with open(self.filename+self.ext, mode='r', encoding='utf-8-sig') as f:
            reader = list(csv.reader(f))[1:]
            self.data = [
                {'t': int(1 / float(line[0])), 'c': [
                    {
                        'r': int(line[3 * i - 2]),
                        'g': int(line[3 * i - 1]),
                        'b': int(line[3 * i])
                    }
                    for i in range(1, int((len(reader[0]) - 1) / 3) + 1)
                ]}
                for line in reader
            ]
        return self

    def write(self) -> CSV:
        if not self.data:
            raise EnvironmentError('Data unfilled')
        with open(self.filename+self.ext, mode='w') as f:
            string = 'FRAME_TIME'
            for i in range(500):
                for j in ['R', 'G', 'B']:
                    string += f',{j}_{i}'
            f.write(f'{string}\n')
        with open(self.filename+self.ext, mode='a+') as f:
            for i in self.data:
                string = str(round(1/i['t'], 7))
                for j in i['c']:
                    for k in ['r', 'g', 'b']:
                        string += ',' + str(j[k])
                f.write(string + '\n')
        return self


class XTREE(Format):
    ext: str = '.xtree'

    def read(self) -> XTREE:
        if not os.path.exists(self.filename+self.ext):
            raise EnvironmentError('File does not exist')
        bytes_total = os.path.getsize(self.filename+self.ext)
        with open(self.filename+self.ext, mode='br+') as xf:
            leds = int.from_bytes(xf.read(2), 'big')
            frame_num = int((bytes_total - 2) / (leds * 3 + 2))
            for _ in range(frame_num):
                frame_rate = int.from_bytes(xf.read(2), 'big')
                colors = []
                for _ in range(leds):
                    colors.append({
                        'r': int.from_bytes(xf.read(1), 'big'),
                        'g': int.from_bytes(xf.read(1), 'big'),
                        'b': int.from_bytes(xf.read(1), 'big')
                    })
                self.data.append({'t': frame_rate, 'c': colors})
        return self

    def write(self) -> XTREE:
        if not self.data:
            raise EnvironmentError('Data unfilled')
        with open(self.filename+self.ext, mode='bw+') as xf:
            xf.write(int(len(self.data[0]['c'])).to_bytes(2, 'big'))
            for i in self.data:
                xf.write(i['t'].to_bytes(2, 'big'))
                for j in i['c']:
                    for k in ['r', 'g', 'b']:
                        xf.write(j[k].to_bytes(1, 'big'))
        return self


if __name__ == '__main__':
    print('X-zipper - a tool to convert between animation types')
    print('File type to convert from?')
    file_type = input('(py/csv/xtree): ')
    if file_type not in ['py', 'csv', 'xtree']:
        print('Error: No such type')
        raise NotImplementedError
    print('File name to read?')
    match file_type:
        case 'py':
            file_name = input(f'[{PY.ext}]({PY.filename}): ') or PY.filename
            print('Coordinate file name to read (ignore if none exists)?')
            c = Coordinates(filename=(input(f'[.csv]({Coordinates.filename}): ') or Coordinates.filename)).read()
            a = PY(filename=file_name, coordinates=c).read()
            print('File type to convert into?')
            convert_type = input('(csv/xtree): ')
            if convert_type not in ['csv', 'xtree']:
                print('Error: No such type')
                raise NotImplementedError
            match convert_type:
                case 'csv':
                    print('File name to write?')
                    a = a.convert(CSV, input(f'[{CSV.ext}]({CSV.filename})') or CSV.filename)
                case 'xtree':
                    print('File name to write?')
                    a = a.convert(XTREE, input(f'[{XTREE.ext}]({XTREE.filename})') or XTREE.filename)
            a.write()
        case 'csv':
            a = CSV(filename=(input(f'[{CSV.ext}]({CSV.filename}): ') or CSV.filename)).read()
            print('File name to write?')
            a.convert(XTREE, input(f'[{XTREE.ext}]({XTREE.filename})') or XTREE.filename).write()
        case 'xtree':
            a = XTREE(filename=(input(f'[{XTREE.ext}]({XTREE.filename}): ') or XTREE.filename)).read()
            print('File name to write?')
            a.convert(CSV, input(f'[{CSV.ext}]({CSV.filename})') or CSV.filename).write()
