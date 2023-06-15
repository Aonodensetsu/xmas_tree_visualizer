from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from tqdm import tqdm
import importlib.util
import math
import csv
import sys
import os

# fix running by left click
os.chdir(os.path.dirname(os.path.realpath(__file__)))


class Format(ABC):
    # list - one entry per animation frame
    #   dict
    #     t: frame time
    #     c: list - one entry per LED
    #          dict
    #            r: normalized red value
    #            g: normalized green value
    #            b: normalized blue value
    data: list
    filename: str = 'tree_effect'
    ext: str = '.format'

    def __init__(self, data: Optional[list] = None, filename: Optional[str] = None) -> None:
        self.data = data
        self.filename = filename or 'tree_effect'
        if not data:
            self.read()

    def convert(self, other: type[Format], *args, **kwargs) -> Format:
        if not self.data:
            raise EnvironmentError('No data to convert')
        return other(self.data, *args, **kwargs)

    @abstractmethod
    def read(self) -> Format:
        if not os.path.exists(self.filename + self.ext):
            raise EnvironmentError('File does not exist')
        self.data = []
        with open(self.filename + self.ext, mode='r') as f:
            pass  # read file into data
        return self

    @abstractmethod
    def write(self) -> Format:
        if not self.data:
            raise EnvironmentError('No data to write')
        with open(self.filename + self.ext, mode='w') as f:
            pass  # write data into file
        return self


class Coordinates:
    # data
    # list - one entry per LED
    #   dict
    #     x: x coordinate
    #     y: y coordinate
    #     z: z coordinate
    data: list
    filename: str = 'coordinates'
    ext: str = '.csv'

    def __init__(self, data: Optional[list] = None, filename: Optional[str] = None) -> None:
        self.data = data
        self.filename = filename or 'coordinates'

    def read(self) -> Coordinates:
        if not os.path.exists(self.filename + self.ext):
            raise EnvironmentError('File not found')
        self.data = []
        with open(self.filename + self.ext, mode='r', encoding='utf-8-sig') as f:
            for line in f.readlines():
                x, y, z = line.split(',')
                self.data.append({'x': float(x), 'y': float(y), 'z': float(z)})
        return self

    def write(self) -> Coordinates:
        if not self.data:
            raise EnvironmentError('No data to write')
        with open(self.filename + self.ext, mode='w', encoding='utf-8-sig') as f:
            for line in self.data:
                f.write(f"{round(line['x'], 9)},{round(line['y'], 9)},{round(line['z'], 9)}")
        return self

    def make(self) -> Coordinates:
        self.data = []
        theta = 0
        height = 0.006
        for _ in range(499):
            radius = (0.006 * 510 - height) / 3.6
            self.data.append({'x': radius * math.cos(theta), 'y': radius * math.sin(theta), 'z': height})
            theta = (theta + 0.174533 / math.pow(radius, 3 / 5)) % 6.28319
            height += 0.006
        self.data.append({'x': 0, 'y': 0, 'z': height + 0.012})
        return self


class PY(Format):
    coords: Coordinates
    ext: str = '.py'

    def __init__(self,
                 data: Optional[list] = None,
                 filename: Optional[str] = None,
                 coordinates: Optional[Coordinates] = None
                 ) -> None:
        self.coords = coordinates or Coordinates().make()
        super().__init__(data, filename)

    def read(self) -> PY:
        if not os.path.exists(self.filename + self.ext):
            raise EnvironmentError('File does not exist')
        self.data = []
        spec = importlib.util.spec_from_file_location('tree_effect', self.filename + self.ext)
        module = importlib.util.module_from_spec(spec)
        tree_effect = sys.modules['tree_effect'] = module
        spec.loader.exec_module(module)
        storage = None
        print('Compiling effect...')
        for frame in tqdm(range(1, tree_effect.frame_max()+1)):
            colors, storage = tree_effect.run(self.coords.data, frame, storage)
            self.data.append({'t': tree_effect.frame_time(frame), 'c': colors})
            frame += 1
        return self

    def write(self) -> PY:
        raise EnvironmentError('Cannot reconstruct a script representation')


class CSV(Format):
    ext: str = '.csv'

    def read(self) -> CSV:
        if not os.path.exists(self.filename + self.ext):
            raise EnvironmentError('File does not exist')
        self.data = []
        with open(self.filename + self.ext, mode='r', encoding='utf-8-sig') as f:
            reader = list(csv.reader(f))[1:]
            self.data = [
                {'t': float(line[0]), 'c': [
                    {
                        'r': float(line[3 * i - 2])/255,
                        'g': float(line[3 * i - 1])/255,
                        'b': float(line[3 * i])/255
                    }
                    for i in range(1, int((len(reader[0]) - 1) / 3) + 1)
                ]}
                for line in reader
            ]
        return self

    def write(self) -> CSV:
        if not self.data:
            raise EnvironmentError('No data to write')
        with open(self.filename + self.ext, mode='w') as f:
            string = 'FRAME_TIME'
            for i in range(500):
                for j in ['R', 'G', 'B']:
                    string += f',{j}_{i}'
            f.write(f'{string}\n')
        with open(self.filename + self.ext, mode='a+') as f:
            for i in self.data:
                string = str(i['t'])
                for j in i['c']:
                    for k in ['r', 'g', 'b']:
                        string += ',' + str(int(j[k]*255))
                f.write(string + '\n')
        return self


class XTREE(Format):
    ext: str = '.xtree'

    def read(self) -> XTREE:
        if not os.path.exists(self.filename + self.ext):
            raise EnvironmentError('File does not exist')
        self.data = []
        bytes_total = os.path.getsize(self.filename + self.ext)
        with open(self.filename + self.ext, mode='br+') as xf:
            leds = int.from_bytes(xf.read(2), 'big')
            frame_num = int((bytes_total - 2) / (leds * 3 + 2))
            for _ in range(frame_num):
                frame_time = 1/float(int.from_bytes(xf.read(2), 'big'))
                colors = []
                for _ in range(leds):
                    colors.append({
                        'r': float(int.from_bytes(xf.read(1), 'big'))/255,
                        'g': float(int.from_bytes(xf.read(1), 'big'))/255,
                        'b': float(int.from_bytes(xf.read(1), 'big'))/255
                    })
                self.data.append({'t': frame_time, 'c': colors})
        return self

    def write(self) -> XTREE:
        if not self.data:
            raise EnvironmentError('No data to write')
        with open(self.filename + self.ext, mode='bw+') as xf:
            xf.write(int(len(self.data[0]['c'])).to_bytes(2, 'big'))
            for i in self.data:
                xf.write(int(1/i['t']).to_bytes(2, 'big'))
                for j in i['c']:
                    for k in ['r', 'g', 'b']:
                        xf.write(int(j[k]*255).to_bytes(1, 'big'))
        return self


def main():
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
            c = Coordinates(filename=(input(f'[.csv]({Coordinates.filename}): ') or Coordinates.filename))
            try:
                c.read()
            except EnvironmentError:
                c.make()
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


if __name__ == '__main__':
    main()
