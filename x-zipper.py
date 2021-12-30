import os
import csv
import time

frame_rates = []
colors = []


def read_csv():
    with open('tree_effect.csv', mode='r', encoding='utf-8-sig') as csv_input:
        file = list(csv.reader(csv_input))
        leds = int((len(file[0]) - 1) / 3)
        for row in file[1:]:
            frame_rates.append(int(1/float(row[0])))
            line_colors = []
            for i in range(leds):
                line_colors.append([int(row[3 * (i + 1) - 2]), int(row[3 * (i + 1) - 1]), int(row[3 * (i + 1)])])
            colors.append(line_colors)


def read_xtree():
    bytes_total = os.path.getsize('tree_effect.xtree')
    with open('tree_effect.xtree', mode='rb') as xtree_input:
        leds = int.from_bytes(xtree_input.read(2), 'big')
        frames = int((bytes_total - 2) / (leds * 3 + 2))
        for i in range(frames):
            frame_rates.append(int.from_bytes(xtree_input.read(2), 'big'))
            frame_colors = []
            for j in range(leds):
                led = [int.from_bytes(xtree_input.read(1), 'big'), int.from_bytes(xtree_input.read(1), 'big'), int.from_bytes(xtree_input.read(1), 'big')]
                frame_colors.append(led)
            colors.append(frame_colors)


def create_csv():
    with open('tree_effect.csv', mode='w') as csv_output:
        string = 'FRAME_TIME'
        for i in range(500):
            for j in range(3):
                color = 'R' if j % 3 == 0 else 'G' if j % 3 == 1 else 'B'
                string += f',{color}_{i}'
        csv_output.write(f'{string}\n')
        for i in range(len(colors)):
            csv_output.write(f'{round(1/frame_rates[i], 5)}')
            for j in range(len(colors[i])):
                for k in range(len(colors[i][j])):
                    csv_output.write(f',{colors[i][j][k]}')
            csv_output.write('\n')


def create_xtree():
    with open('tree_effect.xtree', mode='wb') as xtree_output:
        xtree_output.write((len(colors[0])).to_bytes(2, 'big'))
        # for each animation frame
        for i in range(len(colors)):
            xtree_output.write((frame_rates[i].to_bytes(2, 'big')))
            # for each LED
            for j in range(len(colors[i])):
                # for each RGB
                for k in range(len(colors[i][j])):
                    xtree_output.write(bytes([colors[i][j][k]]))


def main():
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
        time.sleep(2)
        exit()


if __name__ == '__main__':
    main()
