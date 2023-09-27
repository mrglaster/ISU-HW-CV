import numpy as np
import matplotlib.pyplot as plt


def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1


def draw_gradient(size: int = 100, color_first: list = [255, 128, 0], color_second: list = [0, 128, 255]) -> None:
    image = np.zeros((size, size, 3), dtype="uint8")
    assert image.shape[0] == image.shape[1]
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            t = (i + j) / (2.0 * (size - 1))
            r = lerp(color_second[0], color_first[0], t)
            g = lerp(color_second[1], color_first[1], t)
            b = lerp(color_second[2], color_first[2], t)
            image[i, j, :] = [r, g, b]
    plt.figure(1)
    plt.imshow(image)
    plt.show()


def main():
    draw_gradient()


if __name__ == '__main__':
    main()
