import random
import cv2
import numpy as np
import math
from scipy import stats
# leave it like that, if you only import scipy it'll give you a warning
from PIL import Image


IMAGE_DATA_SIZE = 6


class ImageData:
    network_result = None

    def __init__(self, file=None, data=None, label=None):
        self.file = file
        self.label = label
        self._data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, inp):
        if len(inp) == IMAGE_DATA_SIZE:
            self._data = inp
        else:
            raise Exception("Invalid feature array size.")

    def set_random_data(self):
        for i in range(IMAGE_DATA_SIZE):
            self._data[i] = random.randint % 1000 / 1000


class ImagePreprocessing(object):
    def __init__(self, image):
        self.image = image

    def feature_extract(self):
        """ concatenates the scalar-values to a 1D-list """
        features = []
        features.append(self.sharpness())
        features.append(self.noise_differ_gaussian())
        features.append(self.noise_differ_median())
        features.append(self.noise_differ_noises())
        features.append(self.colorfulness())
        features.append(self.contrast())

        self.image.data = features
        return self.image

    def extract_data(self):
        """ ursprünglich zum Entpacken der erhaltenen Bilder in einen array gedacht,
        vermutlich mittlerweile obsolet """
        img_unscaled = self.image.file
        img_unscaled_array = np.array(img_unscaled)
        if np.amax(img_unscaled_array) is not 0:
            img = img_unscaled_array / np.amax(img_unscaled_array)
        else:
            raise IOError("No image found!")
        features = img.flatten()
        return ImageData(data=features)

    def sharpness(self):
        """" returns sharpness as a scalar
        by calculating the variance of the laplacian """
        def var_laplacian(image_color):

            var = cv2.Laplacian(image_color, cv2.CV_64F).var()
            return var

        # gets image as an Image object in PIL
        img_color_pil = self.image.file

        if img_color_pil.format == "JPEG" or img_color_pil.format == "PNG":
            opencvimage = np.array(img_color_pil)

            # transforms from PIL to opencv format
            img_color = cv2.cvtColor(opencvimage, cv2.COLOR_RGB2BGR)

            # color to grayscale, sharpness doesn't need color
            img_grey = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

            # returns sharpness as a scalar
            sharpness_scalar = var_laplacian(img_grey)/25789
        else:
            raise IOError("PIL Image needed.")

        return sharpness_scalar

    """
    three noise_differ functions
    they are functions that calculate a blurred
    version of the input image and subtract it from that
    original, noisy images have low difference, sharp images
    should behave differently
    """

    def noise_differ_gaussian(self):

        img_color_pil = self.image.file
        # transform from PIL to opencv
        img_color = cv2.cvtColor(np.array(img_color_pil), cv2.COLOR_RGB2BGR)
        # blurs original Img with gaussian noise
        gaussian = cv2.GaussianBlur(img_color, (3, 3), 0)
        diff_gaus = np.asfarray(img_color) - np.asfarray(gaussian)
        noise_gaus = np.percentile(np.abs(diff_gaus), 98)
        noise_gaus_scaled = noise_gaus / 68
        return noise_gaus_scaled

    def noise_differ_median(self):
        """
        median filter is used instead of gaussian filter
        """
        img_color_pil = self.image.file
        img_color = cv2.cvtColor(np.array(img_color_pil), cv2.COLOR_RGB2BGR)
        # blurs image with median filter
        median = cv2.medianBlur(img_color, 3)
        diff_median = np.asfarray(img_color) - np.asfarray(median)
        noise_median = np.percentile(np.abs(diff_median), 98)
        noise_median_scaled = noise_median / 95
        return noise_median_scaled

    def noise_differ_noises(self):
        """
        takes image and applies gaussian aswell
        as median filter, subtract the noisy images
        shows if both images had noise
        """
        img_color_pil = self.image.file
        img_color = cv2.cvtColor(np.array(img_color_pil), cv2.COLOR_RGB2BGR)
        median = cv2.medianBlur(img_color, 3)
        gaussian = cv2.GaussianBlur(img_color, (3, 3), 0)
        diff_noises = np.asfarray(gaussian) - np.asfarray(median)
        noise_noises = np.percentile(np.abs(diff_noises), 98)
        noise_noises_scaled = noise_noises / 40
        return noise_noises_scaled

    def hue(self):
        """
        Did not sort out low s values nor did not keep
        V in intervall, doesn't work well yet
        """
        pil_img = self.image.file
        opencvImage = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        img_np = np.array(opencvImage, dtype='f')
        img_hsv = cv2.cvtColor(np.array(img_np), cv2.COLOR_BGR2HSV)

        hist = cv2.calcHist([img_hsv], [0], None, [20], [0, 500])
        hist_scaled = hist / sum(hist)

        nbins = 20
        h, s, v = np.dsplit(img_hsv, 3)
        hist, _ = np.histogram(h, bins=nbins, range=(0, 360))
        hist_scaled = hist / sum(hist)
        m = max(hist_scaled)
        N = []

        for i in hist_scaled:
            if i > m * 0.05:
                N.append(i)

        q_h = 20 - np.linalg.norm(N)
        return q_h
        """
        The Design of High-Level Features for Photo Quality Assessment
        by Yan Ke
        """

    def colorfulness(self):
        """
        calculates colorfulness of an Image
        from paper by Hasler and Susstrunk, 2003
        """
        img_color_pil = self.image.file
        img = np.array(img_color_pil, dtype='f')
        R, G, B = np.dsplit(img, 3)  # splits channel into three variables
        rg = R - G
        yb = ((1. / 2.) * (R + G)) - B
        stdRG = np.std(rg)  # standard deviation of RG
        meanRG = np.mean(rg)  # meanvalue of RG
        stdYB = np.std(yb)
        meanYB = np.mean(yb)
        stdRG_raised = (stdRG) ** 2
        stdYB_raised = (stdYB) ** 2
        stdRGYB = math.sqrt(stdRG_raised + stdYB_raised)
        meanRG_raised = (meanRG) ** 2
        meanYB_raise = (meanYB) ** 2
        meanRGYB = math.sqrt(meanRG_raised + meanYB_raise)
        Color = stdRGYB + 0.3 * meanRGYB
        return Color

    def contrast(self):
        """
        calculates the contrast via shannon entropy
        regions with high changing neighbours have
        higher "chaos" (Entropy)
        there were performance issues, thanks to
        optimization the algorithm works fast enough
        to use for training
        """

        def shannon_calc(insig):
            array_len = insig.size
            t_list = list(set(insig))
            prob = [np.size(insig[insig == i])/(1.0*array_len) for i in t_list]
            entrp = stats.entropy(prob, None, 2)
            return entrp

        color_img = self.image.file
        grey_img = color_img.convert('L')
        imgscale = np.asarray(grey_img.size)

        if (imgscale[0] > 800 and imgscale[1] > 800):
            grey_img = grey_img.resize((int(imgscale[0]/10),
                                       int(imgscale[1]/10)), Image.ANTIALIAS)
        if (imgscale[0] > 2000 and imgscale[1] > 2000):
            grey_img = grey_img.resize((int(imgscale[0]/20),
                                       int(imgscale[1]/20)), Image.ANTIALIAS)

        grey_array = np.asarray(grey_img)
        ent = np.asarray(grey_img)
        ent.flags.writeable = True
        array_shape = grey_array.shape
        neighbour_pixel = 4  # 8x8 neighborhood of pixel (better performance)

        for line in range(array_shape[0]):
            for col in range(array_shape[1]):
                l_x = np.max([0, col-neighbour_pixel])
                u_x = np.min([array_shape[1], col+neighbour_pixel])
                l_y = np.max([0, line-neighbour_pixel])
                u_y = np.min([array_shape[0], line+neighbour_pixel])
                reg = grey_array[l_y:u_y, l_x:u_x].flatten()
                ent[line, col] = shannon_calc(reg)

        contrast = sum(ent.flatten())
        contrast_scaled = contrast/50000

        return contrast_scaled
