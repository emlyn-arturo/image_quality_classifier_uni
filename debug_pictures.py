import random
from PIL import Image
import cv2
import numpy as np
import math
import os
from sklearn.externals import joblib
from neural_network import Network
from image_preprocessing import ImageData


def sharpness(img_input):
    def var_laplacian(image_color):
        var = cv2.Laplacian(image_color, cv2.CV_64F).var()
        return var

    img_color_pil = img_input
    opencvimage = np.array(img_color_pil)
    # transforms from PIL to opencv format
    img_color = cv2.cvtColor(opencvimage, cv2.COLOR_RGB2BGR)
    # color to grayscale, sharpness doesn't need color
    img_grey = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    # returns sharpness as a scalar
    sharpness_scalar = var_laplacian(img_grey)

    return sharpness_scalar


def noise_differ_gaussian(img_input):
    img_color = cv2.cvtColor(np.array(img_input), cv2.COLOR_RGB2BGR)
    gaussian = cv2.GaussianBlur(img_color, (3, 3), 0)
    diff_gaus = np.asfarray(img_color) - np.asfarray(gaussian)
    noise_gaus = np.percentile(np.abs(diff_gaus), 98)
    return noise_gaus


def noise_differ_median(img_input):
    img_color = cv2.cvtColor(np.array(img_input), cv2.COLOR_RGB2BGR)
    median = cv2.medianBlur(img_color, 3)
    diff_median = np.asfarray(img_color) - np.asfarray(median)
    noise_median = np.percentile(np.abs(diff_median), 98)
    return noise_median


def noise_differ_noises(self):
    # This function is obsolete
    img_color = cv2.cvtColor(np.array(self), cv2.COLOR_RGB2BGR)
    median = cv2.medianBlur(img_color, 3)
    gaussian = cv2.GaussianBlur(img_color, (3, 3), 0)
    diff_noises = np.asfarray(gaussian) - np.asfarray(median)
    noise_noises = np.percentile(np.abs(diff_noises), 98)
    return noise_noises


def colorfulness(img_input):
    # calculates colorfulness with scientific
    # paper from Hasler and Susstrunk, 2003

    img = np.array(img_input, dtype='f')
    R, G, B = np.dsplit(img, 3)
    rg = R - G
    yb = ((1. / 2.) * (R + G)) - B
    stdRG = np.std(rg)
    meanRG = np.mean(rg)
    stdYB = np.std(yb)
    meanYB = np.mean(yb)
    stdRG_raised = (stdRG) ** 2
    stdYB_raised = (stdYB) ** 2
    stdRGYB = math.sqrt(stdRG_raised + stdYB_raised)
    meanRG_raised = (meanRG) ** 2
    meanYB_raise = (meanYB) ** 2
    meanRGYB = math.sqrt(meanRG_raised + meanYB_raise)
    C = stdRGYB + 0.3 * meanRGYB
    return C


def contrast(img_input):
    def shannon_calc(insig):
        array_len = insig.size
        t_list = list(set(insig))
        prob = [np.size(insig[insig == i]) / (1.0 * array_len) for i in t_list]
        entrp = -1 * np.sum([p * np.log2(p) for p in prob])
        return entrp

    color_img = img_input
    grey_img = color_img.convert('L')
    grey_array = np.asarray(grey_img)
    ent = np.asarray(grey_img)
    ent.flags.writeable = True
    array_shape = grey_array.shape
    neighbour_pixel = 5  # 10x10 neighborhood of pixel

    for line in range(array_shape[0]):
        for col in range(array_shape[1]):
            l_x = np.max([0, col - neighbour_pixel])
            u_x = np.min([array_shape[1], col + neighbour_pixel])
            l_y = np.max([0, line - neighbour_pixel])
            u_y = np.min([array_shape[0], line + neighbour_pixel])
            reg = grey_array[l_y:u_y, l_x:u_x].flatten()
            ent[line, col] = shannon_calc(reg)
    return sum(ent.flatten())


def feature_extract(img_input):
    features = [sharpness(img_input),
                noise_differ_gaussian(img_input),
                noise_differ_median(img_input),
                noise_differ_noises(img_input),
                colorfulness(img_input)]
    # features.append(self.hue())
    # features.append(contrast(img_input))
    # Todo: Add more features

    return features


imgs_clean = []
path = "/Users/DomiMac/Desktop/databaserelease2/wn"
valid_images = [".jpg", ".bmp", ".gif", ".png", ".tga"]
for f in os.listdir(path):
    ext = os.path.splitext(f)[1]
    if ext.lower() not in valid_images:
        continue
    imgs_clean.append(Image.open(os.path.join(path, f)))

imgs_gaussian = []
path_gaussian = "/Users/DomiMac/Desktop/databaserelease2/gblur"
valid_images = [".jpg", ".bmp", ".gif", ".png", ".tga"]
for f in os.listdir(path_gaussian):
    ext = os.path.splitext(f)[1]
    if ext.lower() not in valid_images:
        continue
    imgs_gaussian.append(Image.open(os.path.join(path_gaussian, f)))

imgs_fast = []
path_fast = "/Users/DomiMac/Desktop/databaserelease2/fastfading"
valid_images = [".jpg", ".bmp", ".gif", ".png", ".tga"]
for f in os.listdir(path_fast):
    ext = os.path.splitext(f)[1]
    if ext.lower() not in valid_images:
        continue
    imgs_fast.append(Image.open(os.path.join(path_fast, f)))

features_clean = []
for i in range(len(imgs_clean)):
    features_clean.append(feature_extract(imgs_clean[i]))

features_fast = []
for i in range(len(imgs_fast)):
    features_fast.append(feature_extract(imgs_fast[i]))

features_gaussian = []

for i in range(len(imgs_gaussian)):
    features_gaussian.append(feature_extract(imgs_gaussian[i]))

feature = features_fast + features_clean + features_gaussian

# create an ImageDataObject
i1 = ImageData()
i2 = ImageData()
i3 = ImageData()
i4 = ImageData()
i5 = ImageData()
i6 = ImageData()

i_list = [i1, i2, i3, i4, i5, i6]

for i, item in enumerate(i_list):
    item.data = feature[i]
    item.label = int(bool(random.getrandbits(1)))

# auskommentiert zum testen ob die trainierte datei korrekt geladen wird
network = Network()
# fit the network and persist the model for future use without having to
# retrain
network.train(i_list)
joblib.dump(network, 'network1.pkl')

# load fitted model from file
network = joblib.load(os.path.join(os.path.dirname(__file__),
                                   'neural_network', 'network_test_fit.pkl'))
for item in i_list:
    print('Class: ', network.evaluate(item))
