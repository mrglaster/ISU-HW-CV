import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label
from skimage.morphology import binary_erosion


def get_file():
    return np.load('stars.npy')


def show_image(image):
    plt.imshow(image)
    plt.show()


def get_structures():
    cross = np.array([[1, 0, 0, 0, 1], [0, 1, 0, 1, 0], [0, 0, 1, 0, 0], [0, 1, 0, 1, 0], [1, 0, 0, 0, 1]])
    plus = np.array([[0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [1, 1, 1, 1, 1], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0]])
    return [cross, plus]


def process_image(image):
    names = ["Crosses", "Stars"]
    cntr = 0
    general = 0
    for structure in get_structures():
        img = binary_erosion(image, structure)
        img, count = label(img)
        print(f"{names[cntr]}es: {count}")
        cntr += 1
        general += count
    print(f"General: {general}")


def main():
    stars = get_file()
    process_image(stars)


if __name__ == '__main__':
    main()
