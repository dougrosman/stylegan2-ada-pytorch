import os
import sys
import bz2
# from keras.utils import get_file
from face_alignment import image_align
from landmarks_detector import LandmarksDetector

LANDMARKS_MODEL_URL = 'http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2'


def unpack_bz2(src_path):
    data = bz2.BZ2File(src_path).read()
    dst_path = src_path[:-4]
    with open(dst_path, 'wb') as fp:
        fp.write(data)
    return dst_path


if __name__ == "__main__":
    """
    Extracts and aligns all faces from images using DLib and a function from original FFHQ dataset preparation step
    python align_images.py /raw_images /aligned_images
    """

    #landmarks_model_path = unpack_bz2(get_file('shape_predictor_68_face_landmarks.dat.bz2',
                                               #LANDMARKS_MODEL_URL, cache_subdir='temp'))

    landmarks_model_path = unpack_bz2('shape_predictor_68_face_landmarks.dat.bz2')

    RAW_IMAGES_DIR = sys.argv[1]
    ALIGNED_IMAGES_DIR = sys.argv[2]

    landmarks_detector = LandmarksDetector(landmarks_model_path)
    for img_name in [x for x in os.listdir(RAW_IMAGES_DIR) if x[0] not in '._']:
        raw_img_path = os.path.join(RAW_IMAGES_DIR, img_name)
        for i, face_landmarks in enumerate(landmarks_detector.get_landmarks(raw_img_path), start=1):
            face_img_name = '%s_%02d.png' % (os.path.splitext(img_name)[0], i)
            aligned_face_path = os.path.join(ALIGNED_IMAGES_DIR, face_img_name)
            os.makedirs(ALIGNED_IMAGES_DIR, exist_ok=True)
            image_align(raw_img_path, aligned_face_path, face_landmarks)


## ADDED BY DOUG


# As you can see many answers above, But i would like to post a quick solution which works for sure in Anaconda3. I haven't chosen Visual Studio as it consumes lot of memory.

# Please follow the below steps.

# Step 1:
# Install windows cmake.msi and configure environment variable

# Step 2:
# Create a conda environment, and install cmake using the below command.
# pip install cmake

# Step 3:
# conda install -c conda-forge dlib

# Note you can find few other dlib packages, but the above one will works perfectly with this procedure.

# dlib will be successfully installed.


# https://stackoverflow.com/questions/41912372/dlib-installation-on-windows-10