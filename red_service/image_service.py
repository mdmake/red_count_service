from PIL import Image
import numpy as np
import io


def get_red_percent(b_str):

    """
    :param b_str: image in byte array
    :return: number of pixels with a predominance of red
    Returns the number of pixels with a predominance of red
    """

    image = np.array(Image.open(io.BytesIO(b_str)))
    new_data = image.transpose(0, 1, 2).reshape(-1, 3)
    pixel_count = new_data[np.logical_and(new_data[:, 0] > new_data[:, 1],
                                          new_data[:, 0] > new_data[:, 2])].shape[0]
    all_pixel = new_data.shape[0]
    percent = pixel_count/all_pixel
    return round(percent, 2)
