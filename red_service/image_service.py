from PIL import Image
import numpy as np
import io


def get_red_percent(b_str):

    """
    :param b_str: картинка в виде байтового массива
    :param threshold: пороговое значение красного в пикселе
    :return: процент пикселей, в котором уровень красного выше
             порогового значнеия

    функция берет байтовый массив, конвертирует его в изображение и
    возвращает количество пикселей c пороговым значением красного
    выше чем threshold
    """

    image = np.array(Image.open(io.BytesIO(b_str)))
    new_data = image.transpose(0, 1, 2).reshape(-1, 3)
    pixel_count = new_data[np.logical_and(new_data[:, 0] > new_data[:, 1],
                                          new_data[:, 0] > new_data[:, 2])].shape[0]
    all_pixel = new_data.shape[0]
    percent = pixel_count/all_pixel
    return percent
