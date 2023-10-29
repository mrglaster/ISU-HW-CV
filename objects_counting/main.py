import numpy as np
import hashlib
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

def read_image(file_path:str='ps.npy.txt'):
  return label(np.load(file_path))

def get_names() -> dict:
  return {
      "d215aa0b64f88549c5e6883a85e837ce7d559eec535d849855abdc835ae43a72": "Arc. Horns to right",
      "db76485246285a11ee6e0911faa96ae8efbdec5c2c166aec96b97c918b1aea2e": "Arc. Horns left",
      "7c5ce66f0f9ab50b97e0be22a339d754c3696b123eba5718fdc4d6601c158044": "Arc. Horns up",
      "5b8b4d29020ea5b1bc427c40a0cab2bf944be057ec482110f1d12b68008cd286": "Rectangle",
      "6b607262a5daf6a86ae1e2377b00233f81442b48fce3b9598bf322607e9e7764": "Arc. Horns down"
  }

def sort_dictionary(hashes:dict):
  return sorted(hashes.items(), key=lambda x:x[1])



def print_answer(hashes:dict) -> None:
  names = get_names()
  hashes = dict(sorted(hashes.items(), key=lambda item: item[1]))
  for i in hashes:
    if i in names:
      print(f"{names[i]}: {hashes[i]}")
    else:
      print(f"Unknown: {hashes[i]}")


def process_objects() -> dict:
  regions = regionprops(read_image())
  print(f"Objects detected: {len(regions)}\n")
  image_hashes = {}
  for region in regions:
    image_hash = hashlib.sha256(region.image.tobytes()).hexdigest()
    if image_hash in image_hashes:
      image_hashes[image_hash] += 1
    else:
      image_hashes[image_hash] = 1
  return image_hashes


def main():
  hashes = process_objects()
  print_answer(hashes)


if __name__ == '__main__':
  main()

