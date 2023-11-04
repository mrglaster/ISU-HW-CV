import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops


def get_perfect_data():
    return ['D', 'X', '/', '*', '1', '*', 'A', 'A', 'P', '8', '1', 'D', 'D', 'D', '8', '*', 'P', '-', '8', 'P', '/',
            'P',
            'D', '-', 'P', 'D', '/', 'A', '8', 'B', 'P', 'A', '*', 'W', '-', 'X', '8', 'A', 'A', '-', '0', 'P', '*',
            '8',
            'D', '8', '1', '1', 'B', 'A', '-', 'P', 'A', 'X', 'B', '*', 'P', '8', '*', '8', 'D', 'W', 'P', 'B', 'A',
            '/',
            'D', 'B', '-', '/', '-', '8', 'W', '1', '8', '*', 'B', '0', '*', 'X', '*', '*', '/', '0', '*', '*', '0',
            'B',
            '0', '-', '-', '/', '/', 'A', 'W', '/', 'W', '8', '8', '0', 'D', '/', 'P', 'B', 'A', '1', '8', '1', '/',
            'A',
            '*', '1', 'B', 'P', 'B', '0', 'B', 'W', '1', 'P', 'X', 'D', 'W', '*', 'D', 'B', 'W', '8', '-', '*', '/',
            '1',
            '*', 'A', '*', 'X', '*', 'A', 'B', '/', 'B', 'A', '0', '*', 'A', '/', '-', '1', 'A', '0', '/', '1', '-',
            '1',
            'W', '0', '*', '*', 'X', 'B', 'P', '8', 'B', '1', 'W', 'B', 'B', 'A', 'A', 'B', '*', '/', '0', 'A', 'B',
            '-',
            '-', 'P', '/', 'A', '-', 'X', '*', 'P', 'X', 'D', '*', 'B', 'P', '0', '-', 'A', 'D', '0', 'W', 'P', 'B',
            '/',
            '8', '0', '1', '8', 'D', '-', '*', '0', 'P', 'B', 'D', 'W', 'D', '*', 'W', 'P', '8', '-', 'X', 'A', '-',
            'D',
            '/', '0', 'B', '-', 'B', 'P', 'B', 'B', 'D', '1', 'W', '1', 'W', '-', '*', 'X', '8', 'B', '-', '*', '0',
            'X',
            'A', '0', 'P', '/', '*', 'B', '8', 'A', '1', 'P', '1', 'A', '-', 'W', 'A', '/', 'B', 'W', '1', 'B', '/',
            '0',
            'X', '*', 'D', 'P', '1', '0', '1', '1', 'P', '-', '*', '8', '*', 'X', 'A', '0', '1', '1', '-', '8', 'X',
            'P',
            'W', 'W', 'A', '1', '1', 'D', 'W', '0', 'D', '1', 'X', 'P', '0', '*', '/', '/', 'P', '-', 'W', 'X', 'P',
            '8',
            '8', 'B', '-', '/', '/', '1', '1', 'X', '*', 'D', 'P', '/', '*', '1', 'D', '1', '8', '0', '*', '*', '8',
            '1',
            'W', 'D', 'W', 'B', '1', 'D', 'P', 'B', '8', 'D', 'B', '8', '-', 'A', '8', '/', 'D', 'P', '*', 'P', '1',
            '0',
            '/', '1', '0', 'P', '0', '1', 'A', '1', '*', 'W', 'X', '/', '/', 'X', '/', '-', '0', 'P', 'X', '0', '/',
            'P',
            'B', 'A', 'W', '8', 'D', '/', 'W', 'X', '8', 'A', '-', 'B', 'P', 'X', '/', '1', 'D', 'A', 'B', 'D', '-',
            '1',
            '8', 'A', '0', '*']


def filling_factor(region):
    return region.image.mean()


def load_image(filename):
    img = plt.imread(filename)
    gray_image = np.mean(img, axis=2)
    binary_image = (gray_image > 0).astype(int)
    return binary_image


def get_euler(tmp_processed):
    tmp_labeled = label(tmp_processed)
    tmp_regions = regionprops(tmp_labeled)
    return tmp_regions[0].euler_number


def show_image(image):
    plt.imshow(image)
    plt.show()


def recognize(region):
    if filling_factor(region) == 1:
        return '-'
    else:
        match region.euler_number:
            case -1:  # B or 8
                if 1 in region.image.mean(0)[:2]:
                    return 'B'
                return '8'

            case 0:  # A, 0, P, D, 1
                region_copy = region.image.copy()

                if 1 in region.image.mean(0)[:2]:
                    region_copy[-1, :] = 1
                    region_copy[:, -len(region_copy[0]) // 2:] = 1
                    region_labeled = label(region_copy)
                    buf_regions = regionprops(region_labeled)
                    euler = buf_regions[0].euler_number
                    if euler == 0:
                        return 'D'
                    elif euler == -1:
                        return 'P'

                region_copy[-1, :] = 1
                region_labeled = label(region_copy)
                buf_regions = regionprops(region_labeled)
                if 1 in region.image.mean(1):
                    return '*'
                if buf_regions[0].euler_number == -1:
                    return 'A'

                return '0'

            case 1:  # 1, W, X, *. /
                if ''.join(map(str, [1., 1.])) in ''.join(map(str, region.image.mean(0))):
                    return '1'
                region_copy = region.image.copy()
                region_copy[[0, -1], :] = 1
                region_labeled = label(region_copy)
                buf_regions = regionprops(region_labeled)
                euler = buf_regions[0].euler_number
                if euler == -1:
                    return 'X'
                elif euler == -2:
                    return 'W'
                elif region.eccentricity > 0.5:
                    return '/'
                return '*'
            case _:
                return '?'


def main():
    counts = {}
    regions = regionprops(label(load_image('symbols.png')))
    current_symbol = 0
    test_data = get_perfect_data()
    cntr = 0
    for region in regions:

        symbol = recognize(region)
        if symbol != test_data[current_symbol]:
            raise ValueError(
                f"Values don't correspond! Expected: {test_data[current_symbol]}. Got: {symbol}. Position: {current_symbol}")
        cntr += 1
        current_symbol += 1
        if symbol not in counts:
            counts[symbol] = 1
        else:
            counts[symbol] += 1

    print(f"\nObjects detected: {len(regions)}")
    print(f"\nCounts:")
    for i in counts:
        print(f"{i} : {counts[i]}")


if __name__ == '__main__':
    main()
