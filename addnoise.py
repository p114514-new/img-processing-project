import cv2
import numpy as np
import random
import matplotlib.pyplot as plt


# 读取图像


# 1. 高斯噪声
def gauss(img, mean=0, var=0.01):
    noise = np.random.normal(mean, var ** 0.5, img.shape)
    out_img = np.clip(img + noise, 0, 255).astype(np.uint8)  # 将噪声和原始图像进行相加得到加噪后的图像
    return out_img


# 2. 椒盐噪声
def sp_noise(image, amount=0.01):
    output = image.copy()
    threshold = 1 - amount  # 传入的参数,设置一个阙值
    # amount 越大，白色越多
    for i in range(image.shape[0]):  # shape[0]表示图片高
        for j in range(image.shape[1]):  # 图片宽
            rdm = random.random()  # 取0到1之间的浮点数
            if rdm < amount:  # 如果随机数小于参数，那么像素点取黑色
                output[i][j] = 0  # 亮度0%，取黑色
            elif rdm > threshold:
                output[i][j] = 255  # 取白色

    return output


# 3. gamma噪声
def gamma_noise(img, scale=50):
    noise = np.random.gamma(shape=1, scale=scale, size=img.shape)
    out_img = np.clip(img + noise, 0, 255).astype(np.uint8)  # 将噪声和原始图像进行相加得到加噪后的图像
    return out_img


# 4. 瑞利噪声
def rayl_noise(img, scale=50):
    noise = np.random.rayleigh(scale=scale, size=img.shape)
    out_img = np.clip(img + noise, 0, 255).astype(np.uint8)  # 将噪声和原始图像进行相加得到加噪后的图像
    return out_img


# 5. uniform
def uniform_noise(img, low=0, high=50):
    noise = np.random.uniform(low, high, size=img.shape)
    out_img = np.clip(img + noise, 0, 255).astype(np.uint8)  # 将噪声和原始图像进行相加得到加噪后的图像
    return out_img


# 6. exponential噪声
def exponential_noise(img, scale=50):
    noise = np.random.exponential(scale, size=img.shape)
    out_img = np.clip(img + noise, 0, 255).astype(np.uint8)  # 将噪声和原始图像进行相加得到加噪后的图像
    return out_img


if __name__ == '__main__':
    image = cv2.imread('./test_img/origin.jpg')
    noisy_image1 = gauss(image)
    noisy_image2 = sp_noise(image)
    noisy_image3 = gamma_noise(image)
    noisy_image4 = rayl_noise(image)
    noisy_image5 = uniform_noise(image)
    noisy_image6 = exponential_noise(image)
    plt.subplot(2, 4, 1), plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)), plt.title('Original')
    plt.subplot(2, 4, 2), plt.imshow(cv2.cvtColor(noisy_image1, cv2.COLOR_BGR2RGB)), plt.title('Gaussian Noise')
    plt.subplot(2, 4, 3), plt.imshow(cv2.cvtColor(noisy_image2, cv2.COLOR_BGR2RGB)), plt.title('Salt and Pepper Noise')
    plt.subplot(2, 4, 4), plt.imshow(cv2.cvtColor(noisy_image3, cv2.COLOR_BGR2RGB)), plt.title('Gamma Noise')
    plt.subplot(2, 4, 5), plt.imshow(cv2.cvtColor(noisy_image4, cv2.COLOR_BGR2RGB)), plt.title('Rayleigh Noise')
    plt.subplot(2, 4, 6), plt.imshow(cv2.cvtColor(noisy_image5, cv2.COLOR_BGR2RGB)), plt.title('Uniform Noise')
    plt.subplot(2, 4, 7), plt.imshow(cv2.cvtColor(noisy_image6, cv2.COLOR_BGR2RGB)), plt.title('Exponential Noise')

    plt.show()
