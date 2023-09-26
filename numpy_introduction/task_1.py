import numpy as np
import matplotlib.pyplot as plt


def process_file(file:str) -> None:
  with open(file, 'r', encoding='utf-8') as f:
     lines = f.readlines()
     size  = float(lines[0].split()[0])
     s = []
     lines = lines[2:]
     for line in lines:
        arr = list(map(int, line.split()))
        s.append(sum(arr))
     if max(s) == 0:
        print(f"It seems, there is no figure in the file: {file}")
     else:
        print(f"Nominal resolution for file {file} is: {size/max(s)}")
     
def main():
  for i in range(1, 7):
    process_file(f"figure{i}.txt")

if __name__ == '__main__':
  main()
