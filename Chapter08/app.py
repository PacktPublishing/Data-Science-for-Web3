from clean_text import *
import requests
import json
import numpy as np

import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

model= tf.keras.models.load_model('chapter7_model.h5')

with open('text_tokenizer.json') as f:
    data = json.load(f)
    tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(data)

# Replace YOUR_API_KEY with your CryptoPanic API key
url = f"https://cryptopanic.com/api/v1/posts/?auth_token=[YOUR_API_KEY]&public=true&filter=hot"

response = requests.get(url)

if response.status_code == 200:
    feeds = response.json()['results']
    for feed in feeds:
        title = feed['title']
        string = get_clean_text (title)
        string = [string]
        string = tokenizer.texts_to_sequences (string)
        string = pad_sequences(string, maxlen=32, padding='post')
        pred_string=model.predict(string)
        classes_x=(np.argmax(pred_string,axis=1)).item()
        prediction_map ={0: 'negative', 1: 'positive', 2: 'neutral'}
        reply = prediction_map.get(classes_x)
        print (title, reply)
else:
    print("Error fetching feeds.")