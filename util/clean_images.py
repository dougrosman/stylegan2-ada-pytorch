# This script loops through all image files in a directory called "input",
# and converts, resizes and crops them and saves them as JPGs in a directory
# called "output"


from PIL import Image, ExifTags
import pathlib

good_filetypes = (".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG", ".tif", ".TIF", ".tiff", ".TIFF", ".gif", ".GIF") 
dpi = 72
output_name = "cleaned"
img_count = 0

#iterate through input path (relative)
for input_img_path in pathlib.Path("input").iterdir():
    #relative output path
    output_img_path = str(input_img_path).replace("input","output")
  
    #only process image files
    myPath = str(input_img_path)
    if myPath.endswith(good_filetypes):

      #open image
      with Image.open(input_img_path) as im:
        # rotates the images correctly based on orientation in EXIF data
        try:
          for orientation in ExifTags.TAGS.keys():
              if ExifTags.TAGS[orientation]=='Orientation':
                  break
          exif = dict(im._getexif().items())

          # if exif[orientation] == 3:
          #     im=im.rotate(180, expand=True)
          # elif exif[orientation] == 6:
          #     im=im.rotate(270, expand=True)
          # elif exif[orientation] == 8:
          #     im=im.rotate(90, expand=True)

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
                
        #save as .jpg
        img_count_str = f'{img_count:05d}'
        im.save("output/" + output_name + img_count_str + ".jpg", format='JPEG', quality=80, dpi=(dpi,dpi))
        print(f"processing file {input_img_path} done...")
        img_count += 1
