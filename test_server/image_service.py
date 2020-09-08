from PIL import Image
import numpy as np
import io

def get_red_persent(b_str, threshold = 0.5):
    """берет байтовый массив, конвертирует его в изображение и
    возвращает количество пикселей c пороговым значением красного выше чем threshold"""
    image = np.array(Image.open(io.BytesIO(b_str)))
    #data = np.asarray(image)
    new_data = image.transpose(0,1,2).reshape(-1, 3)
    msum = np.sum(new_data, axis=1)
    farr = new_data[:, 0]
    persent_array = np.divide(farr, msum)
    pixel_count = persent_array[persent_array > threshold].size
    all_pixel = new_data.shape[0]
    persent = pixel_count/all_pixel*100.0
    return persent