import os
from PIL import Image


directory = input("Enter directory path: ")

for file in os.listdir(directory):
    if file.endswith(".jpg"):
        print(f"Converting {file} to png...")
        file = os.path.join(directory, file)
        image = Image.open(file)
        image.save(file.replace(".jpg", ".png"))
