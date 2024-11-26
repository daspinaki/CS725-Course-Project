# Neural Style Transfer (CS725 Project)

## Members

- Tarun Bisht (23D0386)
- Pinaki Das (23D2050)
- Lavinia Nongbri (23D0383)
- Manish Kumar Saini (24M2112)

### Installing dependencies

The command below will install all the required dependencies from `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### Image Stylization

```bash
python style_image.py --config=configs/image_config.json
```

or

```bash
python style_image.py --checkpoint data/models/udnie/model_checkpoint.ckpt --image data/images/content.jpg --image_size 1366 768 --output output/styled.jpg
```

### Video Stylization

```bash
python style_video.py --config=configs/video_config.json
```

### Live Webcam Feed Stylization

```bash
python style_webcam.py --config=configs/webcam_config.json
```

### Training

- [Gatys, L. A., Ecker, A. S., & Bethge, M. (2015). A Neural Algorithm of Artistic Style. ArXiv.](https://arxiv.org/abs/1508.06576)

Use notebook `neural-style-transfer-1.ipynb`

- [Johnson, J., & Alahi, A. (2016). Perceptual Losses for Real-Time Style Transfer and Super-Resolution. ArXiv.](https://arxiv.org/abs/1603.08155)

Use notebook `neural-style-transfer-2.ipynb`

To perform multi-style neural style transfer, use the notebook `neural-style-transfer-multi-style.py`. 
You can adjust the influence of each style by modifying the `gamm_ratio` parameter in the code.
