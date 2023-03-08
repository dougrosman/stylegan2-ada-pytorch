from io import BytesIO
from zipfile import ZipFile
from PIL import Image, ImageOps, ExifTags
import os
import sys

good_filetypes = (".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG", ".tif", ".TIF", ".tiff", ".TIFF", ".gif", ".GIF") 
dpi = 72
output_name = "cleaned"
img_count = 0

if len(sys.argv) != 3:
    print("Usage: python process_images.py input_file_path max_dimension")
    sys.exit()

input_file_path = sys.argv[1]
max_dimension = int(sys.argv[2])

# read in zip file
with ZipFile(input_file_path, "r") as zip:
  # create a new zip file to store processed images
  with ZipFile("output.zip", "w") as output_zip:
    for name in zip.namelist():
      # check if the file is an image file
      if os.path.splitext(name)[1] in good_filetypes:
        with zip.open(name) as file:
          # read image file from zip file
          with Image.open(file) as im:
            # rotates the images correctly based on orientation in EXIF data
            try:
              for orientation in ExifTags.TAGS.keys():
                  if ExifTags.TAGS[orientation]=='Orientation':
                      break
              exif = dict(im._getexif().items())

              if exif[orientation] == 3:
                  im=im.transpose(Image.ROTATE_180)
              elif exif[orientation] == 6:
                  im=im.transpose(Image.ROTATE_270)
              elif exif[orientation] == 8:
                  im=im.transpose(Image.ROTATE_90)

            except (AttributeError, KeyError, IndexError):
              # cases: image don't have getexif
              pass

            # check if "P", "RGBA" or "CMYK" so we can convert to RGB
            if im.mode in ["CMYK"]:
                im = im.convert('RGB')
            # if "P", convert to "RGBA" first
            if im.mode in ["P"]:
                im = im.convert('RGBA')
            if im.mode in ["RGBA"]:
                # the default im.convert('RGB') doesn't do a good job dealing
                # with transparency. It replaces the alpha channel with a black
                # background, and creates jagged edges around objects.
                # here, we "paste" the RGBA image onto a new all-white RGB
                # image, which results in much better JPG outputs
                background = Image.new("RGB", im.size, (255, 255, 255))
                background.paste(im, mask=im.split()[3])
                im = background

            img_w, img_h = im.size
            scale = 1
            if img_w > max_dimension or img_h > max_dimension:

              if img_w >= img_h:
                scale = max_dimension/img_w
              else: 
                scale = max_dimension/img_h
              width = scale * img_w
              height = scale * img_h
              im = ImageOps.fit(im, (int(width), int(height)))  

            # save as .jpg
            img_count_str = f'{img_count:05d}'
            # save processed image to BytesIO buffer
            with BytesIO() as buf:
              im.save(buf, format='JPEG', quality=80, dpi=(dpi,dpi))
              # add processed image to output zip file
              output_zip.writestr(output_name + img_count_str + ".jpg", buf.getvalue())
            img_count += 1
            print(f"processing file {name} done...")
