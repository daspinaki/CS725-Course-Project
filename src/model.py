import tensorflow as tf
import keras


"""
All Neural Network Layers implementation required
"""


@keras.saving.register_keras_serializable(package="Custom")
class ReflectionPadding2D(tf.keras.layers.Layer):
    def __init__(self, padding=(1, 1), **kwargs):
        super(ReflectionPadding2D, self).__init__(**kwargs)
        self.padding = tuple(padding)

    def call(self, input_tensor):
        padding_width, padding_height = self.padding
        return tf.pad(
            input_tensor,
            [
                [0, 0],
                [padding_height, padding_height],
                [padding_width, padding_width],
                [0, 0],
            ],
            "REFLECT",
        )

    def get_config(self):
        config = super().get_config()
        config.update({"padding": self.padding})
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)


@keras.saving.register_keras_serializable(package="Custom")
class InstanceNormalization(tf.keras.layers.Layer):
    def __init__(self, epsilon=1e-3, **kwargs):
        super(InstanceNormalization, self).__init__(**kwargs)
        self.epsilon = epsilon

    def build(self, input_shape):
        channels = input_shape[-1]
        self.scale = self.add_weight(
            shape=(channels,), initializer="ones", trainable=True, name="scale"
        )
        self.shift = self.add_weight(
            shape=(channels,), initializer="zeros", trainable=True, name="shift"
        )

    def call(self, inputs):
        mu, var = tf.nn.moments(inputs, axes=[1, 2], keepdims=True)
        normalized = (inputs - mu) / tf.sqrt(var + self.epsilon)
        return self.scale * normalized + self.shift

    def get_config(self):
        config = super().get_config()
        config.update({"epsilon": self.epsilon})
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)


@keras.saving.register_keras_serializable(package="Custom")
class ConvLayer(tf.keras.layers.Layer):
    def __init__(self, filters, kernel_size, strides=1, **kwargs):
        super(ConvLayer, self).__init__(**kwargs)
        self.padding = ReflectionPadding2D([k // 2 for k in kernel_size])
        self.conv2d = tf.keras.layers.Conv2D(filters, kernel_size, strides)
        self.bn = InstanceNormalization()

    def call(self, inputs):
        x = self.padding(inputs)
        x = self.conv2d(x)
        x = self.bn(x)
        return x

    def get_config(self):
        config = super().get_config()
        config.update(
            {"filters": self.conv2d.filters, "kernel_size": self.conv2d.kernel_size}
        )
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)


@keras.saving.register_keras_serializable(package="Custom")
class ResidualLayer(tf.keras.layers.Layer):
    def __init__(self, filters, kernel_size, **kwargs):
        super(ResidualLayer, self).__init__(**kwargs)
        self.conv2d_1 = ConvLayer(filters, kernel_size)
        self.conv2d_2 = ConvLayer(filters, kernel_size)
        self.relu = tf.keras.layers.ReLU()
        self.add = tf.keras.layers.Add()

    def call(self, inputs):
        residual = inputs
        x = self.conv2d_1(inputs)
        x = self.relu(x)
        x = self.conv2d_2(x)
        x = self.add([x, residual])
        return x

    def get_config(self):
        config = super().get_config()
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)


@keras.saving.register_keras_serializable(package="Custom")
class UpsampleLayer(tf.keras.layers.Layer):
    def __init__(self, filters, kernel_size, strides=1, upsample=2, **kwargs):
        super(UpsampleLayer, self).__init__(**kwargs)
        self.upsample = tf.keras.layers.UpSampling2D(size=upsample)
        self.padding = ReflectionPadding2D([k // 2 for k in kernel_size])
        self.conv2d = tf.keras.layers.Conv2D(filters, kernel_size, strides)
        self.bn = InstanceNormalization()

    def call(self, inputs):
        x = self.upsample(inputs)
        x = self.padding(x)
        x = self.conv2d(x)
        return self.bn(x)

    def get_config(self):
        config = super().get_config()
        config.update(
            {"filters": self.conv2d.filters, "kernel_size": self.conv2d.kernel_size}
        )
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)


@keras.saving.register_keras_serializable(package="Custom")
class NSTModel(tf.keras.Model):
    def __init__(self, **kwargs):
        super(NSTModel, self).__init__(**kwargs)
        self.conv2d_1 = ConvLayer(
            filters=32, kernel_size=(9, 9), strides=1, name="conv2d_1_32"
        )
        self.conv2d_2 = ConvLayer(
            filters=64, kernel_size=(3, 3), strides=2, name="conv2d_2_64"
        )
        self.conv2d_3 = ConvLayer(
            filters=128, kernel_size=(3, 3), strides=2, name="conv2d_3_128"
        )
        self.res_1 = ResidualLayer(filters=128, kernel_size=(3, 3), name="res_1_128")
        self.res_2 = ResidualLayer(filters=128, kernel_size=(3, 3), name="res_2_128")
        self.res_3 = ResidualLayer(filters=128, kernel_size=(3, 3), name="res_3_128")
        self.res_4 = ResidualLayer(filters=128, kernel_size=(3, 3), name="res_4_128")
        self.res_5 = ResidualLayer(filters=128, kernel_size=(3, 3), name="res_5_128")
        self.deconv2d_1 = UpsampleLayer(
            filters=64, kernel_size=(3, 3), name="deconv2d_1_64"
        )
        self.deconv2d_2 = UpsampleLayer(
            filters=32, kernel_size=(3, 3), name="deconv2d_2_32"
        )
        self.deconv2d_3 = ConvLayer(
            filters=3, kernel_size=(9, 9), strides=1, name="deconv2d_3_3"
        )
        self.relu = tf.keras.layers.ReLU()

    def call(self, inputs):
        x = self.conv2d_1(inputs)
        x = self.relu(x)
        x = self.conv2d_2(x)
        x = self.relu(x)
        x = self.conv2d_3(x)
        x = self.relu(x)
        x = self.res_1(x)
        x = self.res_2(x)
        x = self.res_3(x)
        x = self.res_4(x)
        x = self.res_5(x)
        x = self.deconv2d_1(x)
        x = self.relu(x)
        x = self.deconv2d_2(x)
        x = self.relu(x)
        x = self.deconv2d_3(x)
        x = (tf.nn.tanh(x) + 1) * (255.0 / 2)
        return x

    def get_config(self):
        return super().get_config()

    @classmethod
    def from_config(cls, config):
        return cls(**config)
