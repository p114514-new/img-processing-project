import cv2
import numpy as np
import random
import matplotlib.pyplot as plt


# 读取图像

class Addnoise:
    #1. 高斯噪声
    def gauss(self,img, mean=0, var=0.01):
        img = np.array(img / 255, dtype=float)#灰度值除以255以便后续与高斯分布相加
        noise = np.random.normal(mean, var ** 0.5, img.shape)
        out_img=noise+img
        out_img = np.clip(out_img, 0, 1.0) # 将噪声和原始图像进行相加得到加噪后的图像
        out_img = np.uint8(out_img * 255)#恢复灰度值范围到0-255
        return out_img


    # def gauss(self,img,*values):
    #     val=[]
    #     for value in values:
    #         val.append(value)
    #     mean=val[0]
    #     var=val[1]
    #     noise = np.random.normal(mean, var ** 0.5, img.shape)
    #     out_img = np.clip(img + noise, 0, 255).astype(np.uint8)  # 将噪声和原始图像进行相加得到加噪后的图像
    #     return out_img

    # 2. 椒盐噪声
    def sp_noise_single(self,image, amount=0.01):
        output = image
        threshold = 1 - amount  # 设置一个阙值
        # amount 越大，255的值越多
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                r = random.random()  # 取0到1之间的数
                ##添加噪声
                if r < amount:
                    output[i][j] = 0
                elif r > threshold:
                    output[i][j] = 255
        return output

    def sp_noise(self, img,amount=0.01):
        channels = cv2.split(img)  # 通道分解
        ch = []
        for i in range(0, len(channels)):
            ch.append(self.sp_noise_single(np.array(channels[i]),amount))
        result = ch[0]
        for i in range(1, len(channels)):
            result = cv2.merge([result, ch[i]])
        return result

    # 3. gamma噪声
    def gamma_noise(self,img, scale=0.1):
        img = np.array(img / 255, dtype=float)  # 灰度值除以255以便后续分布相加
        noise = np.random.gamma(shape=1, scale=scale, size=img.shape)
        out_img = noise + img
        out_img = np.clip(out_img, 0, 1.0)  # 将噪声和原始图像进行相加得到加噪后的图像
        out_img = np.uint8(out_img * 255)  # 恢复灰度值范围到0-255
        return out_img


    # 4. 瑞利噪声
    def rayl_noise(self,img, scale=0.1):
        img = np.array(img / 255, dtype=float)  # 灰度值除以255以便后续分布相加
        noise = np.random.rayleigh(scale=scale, size=img.shape)
        out_img = noise + img
        out_img = np.clip(out_img, 0, 1.0)  # 将噪声和原始图像进行相加得到加噪后的图像
        out_img = np.uint8(out_img * 255)  # 恢复灰度值范围到0-255
        return out_img

    # 5. uniform
    def uniform_noise(self,img, low=0, high=0.1):
        img = np.array(img / 255, dtype=float)  # 灰度值除以255以便后续分布相加
        noise = np.random.uniform(low, high, size=img.shape)
        out_img = noise + img
        out_img = np.clip(out_img, 0, 1.0)  # 将噪声和原始图像进行相加得到加噪后的图像
        out_img = np.uint8(out_img * 255)  # 恢复灰度值范围到0-255
        return out_img
    # 6. exponential噪声
    def exponential_noise(self,img, scale=0.1):
        img = np.array(img / 255, dtype=float)  # 灰度值除以255以便后续分布相加
        noise = np.random.exponential(scale, size=img.shape)
        out_img = noise + img
        out_img = np.clip(out_img, 0, 1.0)  # 将噪声和原始图像进行相加得到加噪后的图像
        out_img = np.uint8(out_img * 255)  # 恢复灰度值范围到0-255
        return out_img






if __name__ == '__main__':
    image = cv2.imread('./test_img/origin.jpg')
    Noise=Addnoise()
    noisy_image1 = Noise.gauss(image)
    noisy_image2 = Noise.sp_noise(image)
    noisy_image3 = Noise.gamma_noise(image)
    noisy_image4 = Noise.rayl_noise(image)
    noisy_image5 = Noise.uniform_noise(image)
    noisy_image6 = Noise.exponential_noise(image)
    plt.subplot(2, 4, 1), plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)), plt.title('Original')
    plt.subplot(2, 4, 2), plt.imshow(cv2.cvtColor(noisy_image1, cv2.COLOR_BGR2RGB)), plt.title('Gaussian Noise')
    plt.subplot(2, 4, 3), plt.imshow(cv2.cvtColor(noisy_image2, cv2.COLOR_BGR2RGB)), plt.title('Salt and Pepper Noise')
    plt.subplot(2, 4, 4), plt.imshow(cv2.cvtColor(noisy_image3, cv2.COLOR_BGR2RGB)), plt.title('Gamma Noise')
    plt.subplot(2, 4, 5), plt.imshow(cv2.cvtColor(noisy_image4, cv2.COLOR_BGR2RGB)), plt.title('Rayleigh Noise')
    plt.subplot(2, 4, 6), plt.imshow(cv2.cvtColor(noisy_image5, cv2.COLOR_BGR2RGB)), plt.title('Uniform Noise')
    plt.subplot(2, 4, 7), plt.imshow(cv2.cvtColor(noisy_image6, cv2.COLOR_BGR2RGB)), plt.title('Exponential Noise')

    plt.show()
