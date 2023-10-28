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


def get_chain(image_labeled, lbl=1):
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


def curvature(chain):
    result = []
    for i in range(len(chain)):
        if i == len(chain) - 1:
            result.append(chain[i] - chain[0])
        else:
            result.append(chain[i] - chain[i + 1])
    return result


def normalize(chain):
    for i in range(len(chain)):
        chain[i] = chain[i] % 8


def is_equal(res1, res2):
    res_copy = res1.copy()
    while res_copy != res2:
        last = res_copy[len(res_copy) - 1]
        res_copy = [res_copy[i - 1] if i else 0 for i in range(len(res_copy))]
        res_copy[0] = last
    return res_copy == res2


def main_prev_task():
    image = np.load("similar.npy")
    image_labeled = label(image)
    max_lbl = np.max(image_labeled)
    print()
    for i in range(1, max_lbl + 1):
        print(f"Figure #{i}: {get_chain(image_labeled, i)}")
    plt.imshow(image)
    plt.show()


def main():
    fig1 = np.zeros((5, 5))
    fig1[1:3, 1:-1] = 1
    fig2 = fig1.T

    result1 = get_chain(fig1, 1)
    result2 = get_chain(fig2, 1)
    print(f"Fig #1 {result1}")
    print(f"Fig #2 {result2}")

    curved_first = curvature(result1)
    curved_second = curvature(result2)

    normalize(curved_first)
    normalize(curved_second)

    print(f"\nFig #1: {curved_first}")
    print(f"Fig #2: {curved_second}")

    equality = is_equal(curved_first, curved_second)
    print("\nResult: Figures are equal") if equality else print("\nResult: Figures aren't equal")


if __name__ == '__main__':
    main()
