import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

x_f = []
y_f = []
x_s = []
y_s = []
x_t = []
y_t = []


def process_image(path: str):
    image = np.load(path)
    labeled = label(image)
    regions = regionprops(labeled)
    sorted_regions = sorted(regions, key=lambda x: x.area)
    origins_first = sorted_regions[0].centroid
    origins_second = sorted_regions[1].centroid
    origins_third = sorted_regions[2].centroid
    x_f.append(origins_first[0])
    y_f.append(origins_first[1])
    x_s.append(origins_second[0])
    y_s.append(origins_second[1])
    x_t.append(origins_third[0])
    y_t.append(origins_third[1])


def show_trajectory():
    plt.title("Balls Trajectories")
    plt.plot(x_f, y_f, label='First ball')
    plt.plot(x_s, y_s, label='Second ball')
    plt.plot(x_t, y_t, label='Third ball')
    plt.legend()
    plt.show()


def process_trajectory():
    for i in range(99):
        process_image(f'out/h_{i}.npy')
    show_trajectory()


def main():
    process_trajectory()


if __name__ == '__main__':
    main()
