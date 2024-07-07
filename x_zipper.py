from __future__ import annotations

from importlib.util import spec_from_file_location, module_from_spec
from os.path import exists, getsize, dirname, realpath
from abc import ABC, abstractmethod
from csv import reader, DictReader
from math import cos, sin, pow
from sys import modules
from tqdm import tqdm
from os import chdir

NO_DATA = 'No data to write'
NO_FILE = 'File does not exist'


class Format(ABC):
    # list - one entry per animation frame
    #   dict
    #     t: frame time
    #     c: list - one entry per LED
    #          dict
    #            r: normalized red value
    #            g: normalized green value
    #            b: normalized blue value
    data: list | None
    filename: str
    ext: str = '.abstract'

    def __init__(self, data: list | None = None, filename: str = 'tree_effect') -> None:
        self.data = data
        self.filename = filename

    def convert(self, other: type[Format], *args, **kwargs) -> Format:
        if not self.data:
            raise EnvironmentError('No data to convert')
        return other(self.data, *args, **kwargs)

    @abstractmethod
    def read(self) -> Format:
        if not exists(self.filename + self.ext):
            raise EnvironmentError(NO_FILE)
        self.data = []
        with open(self.filename + self.ext, mode='r', encoding='utf-8') as f:
            _ = f  # IMPLEMENT read
        return self

    @abstractmethod
    def write(self) -> Format:
        if not self.data:
            raise EnvironmentError(NO_DATA)
        with open(self.filename + self.ext, mode='w', encoding='utf-8') as f:
            _ = f  # IMPLEMENT write
        return self


class Coordinates:
    # data
    # list - one entry per LED
    #   dict
    #     x: x coordinate
    #     y: y coordinate
    #     z: z coordinate
    data: list
    filename: str
    ext: str = '.csv'

    def __init__(self, data: list | None = None, filename: str = 'coordinates') -> None:
        self.data = data
        self.filename = filename

    def read(self) -> Coordinates:
        if not exists(self.filename + self.ext):
            raise EnvironmentError('File not found')
        with open(self.filename + self.ext, mode='r', encoding='utf-8') as f:
            self.data = []
            for line in DictReader(f, fieldnames=['x', 'y', 'z']):
                self.data.append({'x': float(line['x']), 'y': float(line['y']), 'z': float(line['z'])})
        return self

    def write(self) -> Coordinates:
        if not self.data:
            raise EnvironmentError(NO_DATA)
        with open(self.filename + self.ext, mode='w', encoding='utf-8') as f:
            for line in self.data:
                f.write(f"{round(line['x'], 12)},{round(line['y'], 12)},{round(line['z'], 12)}\n")
        return self

    def make(self, n: int = 500) -> Coordinates:
        self.data = []
        theta = 0
        height = 0.006
        for _ in range(n-1):
            radius = (0.006 * (n + 10) - height) / 3.6
            self.data.append({'x': radius * cos(theta), 'y': radius * sin(theta), 'z': height})
            theta = (theta + 0.174533 / pow(radius, 3 / 5)) % 6.28319
            height += 0.006
        self.data.append({'x': 0, 'y': 0, 'z': height + 0.012})
        return self


class PY(Format):
    coords: Coordinates
    filename: str = 'tree_effect'
    ext: str = '.py'

    def __init__(self,
                 data: list | None = None,
                 filename: str = 'tree_effect',
                 coordinates: Coordinates = Coordinates().make()
                 ) -> None:
        super().__init__(data, filename)
        self.coords = coordinates

    def read(self) -> PY:
        if not exists(self.filename + self.ext):
            raise EnvironmentError(NO_FILE)
        self.data = []
        spec = spec_from_file_location('tree_effect', self.filename + self.ext)
        tree_effect = modules['tree_effect'] = module_from_spec(spec)
        spec.loader.exec_module(tree_effect)
        storage = None
        print('Compiling effect frames...')
        for frame in tqdm(range(1, tree_effect.frame_max()+1)):
            colors, storage = tree_effect.run(self.coords.data, frame, storage)
            self.data.append({'t': tree_effect.frame_time(frame), 'c': colors})
        return self

    def write(self) -> None:
        raise EnvironmentError('Cannot reconstruct a script representation')


class CSV(Format):
    filename: str
    ext: str = '.csv'

    def read(self) -> CSV:
        if not exists(self.filename + self.ext):
            raise EnvironmentError(NO_FILE)
        self.data = []
        with open(self.filename + self.ext, mode='r', encoding='utf-8') as f:
            creader = reader(f)
            leds = range(1, int(((len(str(next(creader)).split(',')) - 1) / 3) + 1))  # get length from header
            self.data = [
                {'t': float(line[0]), 'c': [
                    {
                        'r': float(line[3 * i - 2]) / 255,
                        'g': float(line[3 * i - 1]) / 255,
                        'b': float(line[3 * i]) / 255
                    }
                    for i in leds
                ]}
                for line in creader
            ]
        return self

    def write(self) -> CSV:
        if not self.data:
            raise EnvironmentError(NO_DATA)
        with open(self.filename + self.ext, mode='w', encoding='utf-8') as f:
            f.write(
                f'FRAME_TIME,{",".join(f"{j}_{i}" for j in ["R", "G", "B"] for i in range(len(self.data[0]["c"])))}\n'
            )
        with open(self.filename + self.ext, mode='a+', encoding='utf-8') as f:
            for i in self.data:
                f.write(f'{i["t"]},{",".join(str(int(j[k] * 255)) for j in i["c"] for k in ["r", "g", "b"])}\n')
        return self


class XTREE(Format):
    filename: str
    ext: str = '.xtree'

    def read(self) -> XTREE:
        if not exists(self.filename + self.ext):
            raise EnvironmentError(NO_FILE)
        self.data = []
        with open(self.filename + self.ext, mode='br+') as f:
            leds = int.from_bytes(f.read(3), 'big', signed=False)
            for _ in range(int((getsize(self.filename + self.ext) - 3) / (leds * 3 + 2))):
                self.data.append({'t': 1/float(int.from_bytes(f.read(2), 'big', signed=False)), 'c': [
                    {
                        'r': float(int.from_bytes(f.read(1), 'big', signed=False)) / 255,
                        'g': float(int.from_bytes(f.read(1), 'big', signed=False)) / 255,
                        'b': float(int.from_bytes(f.read(1), 'big', signed=False)) / 255
                    }
                    for _ in range(leds)
                ]})
        return self

    def write(self) -> XTREE:
        if not self.data:
            raise EnvironmentError(NO_DATA)
        with open(self.filename + self.ext, mode='bw+') as f:
            f.write(int(len(self.data[0]['c'])).to_bytes(3, 'big', signed=False))
            for i in self.data:
                f.write(int(1/i['t']).to_bytes(2, 'big', signed=False))
                for j, k in ((j, k) for j in i['c'] for k in ['r', 'g', 'b']):
                    f.write(int(j[k] * 255).to_bytes(1, 'big', signed=False))
        return self


def main():
    print('X-zipper - a tool to convert between animation types')
    match input('From type (py/csv/xtree): '):
        case 'py':
            c = Coordinates(
                filename=(input(f'From coordinates [.csv]({Coordinates.filename}): ') or Coordinates.filename)
            )
            try:
                c.read()
            except EnvironmentError:
                c.make()
            a = PY(filename=(input(f'From file [{PY.ext}]({PY.filename}): ') or PY.filename), coordinates=c).read()
            match input('To type (csv/xtree): '):
                case 'csv':
                    a = a.convert(CSV, input(f'To file [{CSV.ext}]({CSV.filename})') or CSV.filename)
                case 'xtree':
                    a = a.convert(XTREE, input(f'To file [{XTREE.ext}]({XTREE.filename})') or XTREE.filename)
                case _:
                    raise NotImplementedError('No such type')
            a.write()
        case 'csv':
            a = CSV(filename=(input(f'From file [{CSV.ext}]({CSV.filename}): ') or CSV.filename)).read()
            a.convert(XTREE, input(f'To file [{XTREE.ext}]({XTREE.filename})') or XTREE.filename).write()
        case 'xtree':
            a = XTREE(filename=(input(f'From file [{XTREE.ext}]({XTREE.filename}): ') or XTREE.filename)).read()
            a.convert(CSV, input(f'To file [{CSV.ext}]({CSV.filename})') or CSV.filename).write()
        case _: raise NotImplementedError('No such type')


if __name__ == '__main__':
    chdir(dirname(realpath(__file__)))  # fix running by left click
    main()
