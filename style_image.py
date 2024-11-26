from src.inference import inference
from src.model import NSTModel
from src.utils import load_image, load_url_image, array_to_img
from src.utils import get_style_image_arguments
import argparse
import time
import tensorflow as tf

parser = argparse.ArgumentParser(description="Create Styled Images")

parser.add_argument("--config", "-con", help="Path to style image config file")
parser.add_argument("--checkpoint", "-ckpt", help="Path to trained style checkpoints")
parser.add_argument("--image", "-img", help="url or file path to image to style")
parser.add_argument(
    "--image_size",
    "-size",
    nargs="+",
    type=int,
    default=[256, 256],
    help="output image size",
)
parser.add_argument(
    "--output", "-out", default="output/styled.jpg", help="Path to save output image"
)

args = get_style_image_arguments(parser.parse_args())


style_model = tf.keras.models.load_model(args["checkpoint"])

input_shape = args["image_size"]
image_path = args["image"]
if image_path.startswith("http"):
    image = load_url_image(image_path, dim=input_shape)
else:
    image = load_image(image_path, dim=input_shape)

start = time.time()
styled_image = inference(style_model, image)
end = time.time()
print(f"Time Taken: {end-start:.2f}s")
pil_image = array_to_img(styled_image)
pil_image.show()
pil_image.save(args["output"])
