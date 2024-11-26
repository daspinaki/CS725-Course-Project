import numpy as np


def inference(model, image):
    image = image.astype(np.float32)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    output_image = model(image)
    output_image = np.clip(output_image, 0, 255)
    output_image = output_image.astype(np.uint8)
    output_image = np.squeeze(output_image)
    return output_image
