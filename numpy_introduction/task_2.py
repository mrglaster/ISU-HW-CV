import numpy as np
import matplotlib.pyplot as plt

def get_cent(img):
    rows, cols = img.shape
    x_sum = 0
    y_sum = 0
    count = 0
    for i in range(rows):
        for j in range(cols):
            if img[i, j] == 1:
                x_sum+=j
                y_sum+=i
                count+=1
    if count == 0:
        return None, None
    return x_sum/count, y_sum/count
    

def main():
  file_first = np.loadtxt(f"test_files/task_2/img1.txt", skiprows=2)
  file_second = np.loadtxt(f"test_files/task_2/img2.txt", skiprows=2)
  center_first = get_cent(file_first)
  center_second = get_cent(file_second)
  if center_first[0] is not None and center_second[0] is not None:
    print(f"Shift X is: {center_second[0] - center_first[0]}")
    print(f"Shit Y is: {center_second[1] - center_first[1]}")
  else:
    print("There is no shift!")


if __name__ == '__main__':
  main()


