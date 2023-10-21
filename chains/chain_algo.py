import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label


def neighbours4(y, x):
    return (y, x + 1), (y, x - 1), (y - 1, x), (y + 1, x)


def neighbours8(y, x):
    return neighbours4(y, x) + ((y - 1, x + 1), (y + 1, x + 1), (y - 1, x - 1), (y + 1, x - 1))


def get_boundaries(image_labeled, lbl=1, connectivity=neighbours4):
    pos = np.where(image_labeled == lbl)
    bounds = []
    for y, x in zip(*pos):
        for yn, xn in connectivity(y, x):
            if yn < 0 or yn > image_labeled.shape[0] - 1:
                bounds.append((y, x))
                break
            elif xn < 0 or xn > image_labeled.shape[1] - 1:
                bounds.append((y, x))
                break
            elif image_labeled[yn, xn] == 0:
                bounds.append((y, x))
                break
    return bounds


def get_directions(y, x):
    return {
        (y, x + 1): 0,
        (y + 1, x + 1): 7,
        (y + 1, x): 6,
        (y + 1, x - 1): 5,
        (y, x - 1): 4,
        (y - 1, x - 1): 3,
        (y - 1, x): 2,
        (y - 1, x + 1): 1
    }


def get_chain(image_labeled, lbl):
    chain = []
    bounds = get_boundaries(image_labeled, lbl)
    y0, x0 = bounds[0]
    y, x = bounds[1]
    bounds = bounds[:]
    while y != y0 or x != x0:
        bounds.pop(bounds.index((y, x)))
        directions = get_directions(y, x)
        for direction in directions.keys():
            if direction in bounds:
                chain.append(directions[direction])
                y, x = direction
                break
    chain.append(0)
    return chain


def main():
    image = np.load("similar.npy")
    image_labeled = label(image)
    max_lbl = np.max(image_labeled)
    print()
    for i in range(1, max_lbl + 1):
        print(f"Figure #{i}: {get_chain(image_labeled, i)}")
    plt.imshow(image)
    plt.show()


if __name__ == '__main__':
    main()