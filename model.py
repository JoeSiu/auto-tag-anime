from asyncio.windows_events import NULL
import sys
import tensorflow as tf
import numpy as np
import PIL

model_path = "./model"

class deepdanbooruModel():
    def __init__(self):
        self.model = self.load_model()

    def load_model(self):
        print('loading model...')
        try:
            model = tf.keras.models.load_model(model_path + "/model-resnet_custom_v3.h5", compile=False)
        except Exception as e:
            print (e)
            print('Model not in folder. Download it from https://github.com/KichangKim/DeepDanbooru')
            sys.exit()
        with open(model_path + "/tags.txt", 'r') as tags_stream:
            self.tags = np.array([tag for tag in (tag.strip() for tag in tags_stream) if tag])
        print('done. Adding tags')
        return model

    def classify_image(self, image_path):
        try:
            image = np.array(PIL.Image.open(image_path).convert('RGB').resize((512, 512))) / 255.0
        except IOError:
            return 'fail', []

        results = self.model.predict(np.array([image])).reshape(self.tags.shape[0])
        result_tags = {}
        for i in range(len(self.tags)):
            if results[i] > 0.4:
                result_tags[self.tags[i]] = results[i]

        return 'success', list(result_tags.keys())