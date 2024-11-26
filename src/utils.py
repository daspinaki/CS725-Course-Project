import json
import numpy as np
from PIL import Image
import requests
from io import BytesIO


def load_image(image_path, dim=None, resize=False):
    img = Image.open(image_path)
    if dim:
        if resize:
            img = img.resize(dim)
        else:
            img.thumbnail(dim)
    img = img.convert("RGB")
    return np.array(img)


def load_url_image(url, dim=None, resize=False):
    img_request = requests.get(url)
    img = Image.open(BytesIO(img_request.content))
    if dim:
        if resize:
            img = img.resize(dim)
        else:
            img.thumbnail(dim)
    img = img.convert("RGB")
    return np.array(img)


def array_to_img(array):
    array = np.array(array, dtype=np.uint8)
    if np.ndim(array) > 3:
        assert array.shape[0] == 1
        array = array[0]
    return Image.fromarray(array)


def save_image(image, path):
    image.save(path)


def get_style_image_arguments(args):
    if args.config:
        try:
            with open(args.config, "r") as f:
                style_args = json.load(f)
            return style_args
        except Exception as e:
            print("Error Occurred while loading config: ", e)

    style_args = {}
    if args.checkpoint:
        style_args["checkpoint"] = args.checkpoint
    else:
        raise Exception("No Path to saved checkpoints found")
    if args.image:
        style_args["image"] = args.image
    else:
        raise Exception("No image found to style")
    style_args["image_size"] = args.image_size
    style_args["output"] = args.output
    return style_args


def get_style_video_arguments(args):
    if args.config:
        try:
            with open(args.config, "r") as f:
                style_args = json.load(f)
            return style_args
        except Exception as e:
            print("Error Occurred while loading config: ", e)

    style_args = {}
    if args.checkpoint:
        style_args["checkpoint"] = args.checkpoint
    else:
        raise Exception("No Path to saved checkpoints found")
    if args.video:
        style_args["video"] = args.video
    else:
        raise Exception("No image found to style")
    style_args["format"] = args.format
    style_args["output"] = args.output
    if args.size:
        style_args["size"] = args.size
    return style_args


def get_style_webcam_arguments(args):
    if args.config:
        try:
            with open(args.config, "r") as f:
                style_args = json.load(f)
            return style_args
        except Exception as e:
            raise Exception("Error Occurred while loading config: ", e)

    style_args = {}
    if args.checkpoint:
        style_args["checkpoint"] = args.checkpoint
    else:
        raise Exception("No Path to saved checkpoints found")
    if args.video:
        style_args["camera"] = args.camera
    else:
        raise Exception("No image found to style")
    style_args["format"] = args.format
    style_args["output"] = args.output
    if args.size:
        style_args["size"] = args.size
    return style_args
