from PIL import Image
import numpy as np
import io

def get_red_persent(b_str, threshold = 0.5):

    """
    :param b_str: картинка в виде байтового массива
    :param threshold: пороговое значение красного в пикселе
    :return: процент пикселей, в котором уровень красного выше
             порогового значнеия

    функция берет байтовый массив, конвертирует его в изображение и
    возвращает количество пикселей c пороговым значением красного
    выше чем threshold
    """

    # регуляризующий параметр
    reg_par = 0.001
    image = np.array(Image.open(io.BytesIO(b_str)))
    new_data = image.transpose(0,1,2).reshape(-1, 3)
    msum = np.sum(new_data, axis=1)
    farr = new_data[:, 0]
    persent_array = np.divide(farr, msum+reg_par)
    pixel_count = persent_array[persent_array > threshold].size
    all_pixel = new_data.shape[0]
    persent = int(pixel_count/all_pixel*100)
    return persent