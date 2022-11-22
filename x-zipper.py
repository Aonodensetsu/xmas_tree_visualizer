# import required libraries
import csv
import os

# fix for running via left click (changes cwd to file location)
os.chdir(os.path.dirname(os.path.realpath(__file__)))

frames = []  # {t: 1/frame rate, c: [{r, g, b} per LED, normalized]} per frame


# read frame descriptions
def read_csv():
    global frames
    print('Reading CSV')
    with open('tree_effect.csv', mode='r', encoding='utf-8-sig') as f:
        reader = list(csv.reader(f))[1:]
        # overwrite table to prevent corruption
        frames = [
            {'tr': int(1/float(line[0])), 'c': [
                {
                    'r': int(line[3*i-2]),
                    'g': int(line[3*i-1]),
                    'b': int(line[3*i])
                }
                for i in range(1, int((len(reader[0]) - 1) / 3) + 1)
            ]}
            for line in reader
        ]


def read_xtree():
    global frames
    print('Reading XTREE')
    bytes_total = os.path.getsize('tree_effect.xtree')
    with open('tree_effect.xtree', mode='br+') as xf:
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
            frames.append({'tr': frame_rate, 'c': colors})


def create_csv():
    global frames
    print('Creating CSV')
    # create the csv header string
    # the string if very long, so construct it programmatically
    with open('tree_effect.csv', mode='w') as f:
        string = 'FRAME_TIME'
        for i in range(500):
            for j in ['R', 'G', 'B']:
                string += f',{j}_{i}'
        f.write(f'{string}\n')
    with open('tree_effect.csv', mode='a+') as f:
        for i in frames:
            string = str(round(1/i['tr'], 7))
            for j in i['c']:
                for k in ['r', 'g', 'b']:
                    string += ','+str(j[k])
            f.write(string+'\n')


def create_xtree():
    global frames
    print('Creating XTREE')
    with open('tree_effect.xtree', mode='bw+') as xf:
        # amount of LEDs
        xf.write(int(len(frames[0]['c'])).to_bytes(2, 'big'))
        # for each animation frame
        for i in frames:
            xf.write(i['tr'].to_bytes(2, 'big'))
            # for each LED
            for j in i['c']:
                # for each RGB
                for k in ['r', 'g', 'b']:
                    xf.write(j[k].to_bytes(1, 'big'))


def main():
    global frames
    print('X-zipper - a tool to compress CSV animations')
    print('Which type of file to convert?')
    file_type = input('(csv/xtree): ')
    if file_type == 'csv':
        read_csv()
        create_xtree()
    elif file_type == 'xtree':
        read_xtree()
        create_csv()
    else:
        print('Error: No such type')
        input()
        exit()


if __name__ == '__main__':
    main()
