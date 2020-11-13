import os
import sys
from PIL import Image
from PIL import ImageOps

# https://pillow.readthedocs.io/en/stable/installation.html#basic-installation

iconDirectory = os.path.abspath(os.path.dirname(sys.argv[0]))

# icon filename to use
image = Image.open(os.path.join(iconDirectory, "icon.png"))

base = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64)]
linux = [(128, 128), (256, 256), (512, 512), (1024, 1024)]
mac = [(128, 128), (256, 256), (512, 512), (1024, 1024)]

# Create base icon sizes in src/main/icons/base
for size in base:
    outPath = os.path.join(iconDirectory, "base", str(size[0]) + ".png")
    scaledImage = image.resize(size)
    scaledImage.save(outPath)
    print('Icon created: ' + outPath)

# Create linux icon sizes in src/main/icons/linux
for size in linux:
    outPath = os.path.join(iconDirectory, "linux", str(size[0]) + ".png")
    scaledImage = image.resize(size)
    scaledImage.save(outPath)
    print('Icon created: ' + outPath)

# Create mac icon sizes in src/main/icons/mac
for size in mac:
    outPath = os.path.join(iconDirectory, "mac", str(size[0]) + ".png")

    padFactor = 0.2
    # Reduce image size (and fit padding)
    scale = (int(size[0] * (1-padFactor)), int(size[1] * (1-padFactor)))
    scaledImage = image.resize(scale)

    # Add padding
    padAmount = size[0] - scale[0]
    padding = (padAmount//2, padAmount//2, padAmount-(padAmount//2), padAmount-(padAmount//2))
    finalImage = ImageOps.expand(scaledImage, padding)
    finalImage.save(outPath)
    print('Icon created: ' + outPath)

# Create Icon.ico in src/main/icons/Icon.ico
new_logo_ico_filename = os.path.join(iconDirectory, "Icon.ico")
new_logo_ico = image.resize((128, 128))
new_logo_ico.save(new_logo_ico_filename, format="ICO", quality=90)
print('Icon created: ' + new_logo_ico_filename)