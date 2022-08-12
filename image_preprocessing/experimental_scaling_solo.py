import cv2
import numpy as np
import math
from PIL import Image
import os
import os.path


imgs_clean = []
path = "DATABSE\\\databaserelease2\\wn_clean"  # use your own path
valid_images = [".jpg", ".bmp", ".gif", ".png", ".tga"]
for f in os.listdir(path):
    ext = os.path.splitext(f)[1]
    if ext.lower() not in valid_images:
        continue
    imgs_clean.append(Image.open(os.path.join(path, f)))

imgs_gaussian = []
path_gaussian = "DATABSE\\\databaserelease2\\gblur_clean"  # use your own path
valid_images = [".jpg", ".bmp", ".gif", ".png", ".tga"]
for f in os.listdir(path_gaussian):
    ext = os.path.splitext(f)[1]
    if ext.lower() not in valid_images:
        continue
    imgs_gaussian.append(Image.open(os.path.join(path_gaussian, f)))


imgs_fast = []
path_fast = "DATABSE\\databaserelease2\\fastfading_clean"  # use your own path
valid_images = [".jpg", ".bmp", ".gif", ".png", ".tga"]
for f in os.listdir(path_fast):
    ext = os.path.splitext(f)[1]
    if ext.lower() not in valid_images:
        continue
    imgs_fast.append(Image.open(os.path.join(path_fast, f)))


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


def entropy_calc(img_input):
    def shannon_calc(insig):
        array_len = insig.size
        t_list = list(set(insig))
        prob = [np.size(insig[insig == i])/(1.0*array_len) for i in t_list]
        entrp = -1*np.sum([p*np.log2(p) for p in prob])
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
            l_x = np.max([0, col-neighbour_pixel])
            u_x = np.min([array_shape[1], col+neighbour_pixel])
            l_y = np.max([0, line-neighbour_pixel])
            u_y = np.min([array_shape[0], line+neighbour_pixel])
            reg = grey_array[l_y:u_y, l_x:u_x].flatten()
            ent[line, col] = shannon_calc(reg)
    return sum(ent.flatten())


sharpie_clean = []
noise_differ_g_clean = []
noise_differ_m_clean = []
noise_differ_n_clean = []
color_clean = []
entropy_clean = []

for i in range(len(imgs_clean)):
    sharpie_clean.append(sharpness(imgs_clean[i]))
    noise_differ_g_clean.append(noise_differ_gaussian(imgs_clean[i]))
    noise_differ_m_clean.append(noise_differ_median(imgs_clean[i]))
    noise_differ_n_clean.append(noise_differ_noises(imgs_clean[i]))
    color_clean.append(colorfulness(imgs_clean[i]))
    entropy_clean.append(entropy_calc(imgs_clean[i]))


sharpie_fast = []
noise_differ_g_fast = []
noise_differ_m_fast = []
noise_differ_n_fast = []
color_fast = []
entropy_fast = []

for i in range(len(imgs_fast)):
    sharpie_fast.append(sharpness(imgs_fast[i]))
    noise_differ_g_fast.append(noise_differ_gaussian(imgs_fast[i]))
    noise_differ_m_fast.append(noise_differ_median(imgs_fast[i]))
    noise_differ_n_fast.append(noise_differ_noises(imgs_fast[i]))
    color_fast.append(colorfulness(imgs_fast[i]))
    entropy_fast.append(entropy_calc(imgs_fast[i]))


sharpie_gaussian = []
noise_differ_g_g = []
noise_differ_m_g = []
noise_differ_n_g = []
color_g = []
entropy_g = []

for i in range(len(imgs_gaussian)):
    sharpie_gaussian.append(sharpness(imgs_gaussian[i]))
    noise_differ_g_g.append(noise_differ_gaussian(imgs_gaussian[i]))
    noise_differ_m_g.append(noise_differ_median(imgs_gaussian[i]))
    noise_differ_n_g.append(noise_differ_noises(imgs_gaussian[i]))
    color_g.append(colorfulness(imgs_gaussian[i]))
    entropy_g.append(entropy_calc(imgs_gaussian[i]))


sharpie = sharpie_fast + sharpie_clean + sharpie_gaussian
noise_gaussian = noise_differ_g_fast + noise_differ_g_clean + noise_differ_g_g
noise_median = noise_differ_m_fast + noise_differ_m_clean + noise_differ_m_g
noise_noises = noise_differ_n_fast + noise_differ_n_clean + noise_differ_n_g
color = color_fast + color_clean + color_g
entropy = entropy_fast + entropy_clean + entropy_g


sharpie_scaled = np.array(sharpie) / 25789
noise_gaussian_scaled = np.array(noise_gaussian) / 68
noise_median_scaled = np.array(noise_median) / 95
noise_noises_scaled = np.array(noise_noises) / 40
color_scaled = np.array(color) / 86


"""
print("Median= ",np.median(entropy_clean))
# print("Mean= ", np.mean(entropy_clean))


print("Median= ",np.median(noise_differ_n_clean))
print("Mean= ", np.mean(noise_differ_n_clean))
#40

print("Median= ",np.median(color_clean))
print("Mean= ", np.mean(color_clean))
#86



print(len(sharpie))
print(np.amax(sharpie))
print(np.median(sharpie_clean))
print(np.mean(sharpie_clean))




mean_sharpie_clean = math.ceil((np.mean(sharpie_clean)))
sharpienp = np.array(sharpie)/mean_sharpie_clean




print("Median= ",np.median(sharpie_clean))
print("Mean= ", np.mean(sharpie_clean))



print("Median_m=",np.median(noise_differ_g_clean))
print("Mean_m=",np.mean(noise_differ_g_clean))
#68


print("Median_m=",np.median(noise_differ_m_clean))
print("Mean_m=",np.mean(noise_differ_m_clean))
#95

print(np.amax(noise_differ_m_clean)/95)

print("Median= ",np.median(entropy_clean))
print("Mean= ", np.mean(entropy_clean))


max = math.ceil((np.amax(sharpie_fast)))
sharpie_fastnp = np.array(sharpie_fast)/max
print(math.ceil(np.amax(sharpie_fastnp)))
print( np.amax(sharpienp))

"""


"""
plt.plot(color_scaled)
plt.title('Scaled Colorfulness')
plt.ylabel('Range')
#plt.plot(noise_noises_scaled)
plt.show()
"""
