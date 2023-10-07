import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from scipy.ndimage import binary_dilation, binary_erosion, binary_closing, binary_opening


def show_image(image):
    plt.imshow(image, cmap='gray')
    plt.show()

def process_labaling(image, struct=np.ones((3,1))):
  return label(binary_erosion(image, struct))


def count_wires_parts(file_name):
  image = np.load(file_name)
  show_image(image)
  labeled = process_labaling(image)
  count =0
  x=0
  print(f"File: {file_name}")
  print(labeled)
  for j in range(labeled.shape[0]):
      
        if labeled[j, 0]: 
            x+=1
            print(f'Wire id: {x}, Pieces: ', abs(count - labeled[j].max()))
            count = labeled[j].max()
  print()      


def main():
    files = ['wires1.npy.txt', 'wires2.npy.txt', 'wires3.npy.txt', 'wires4.npy.txt', 'wires5.npy.txt', 'wires6.npy.txt']
    count_wires_parts('wires6.npy.txt')

main()