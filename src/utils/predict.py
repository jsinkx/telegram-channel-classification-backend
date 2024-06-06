import numpy as np
import pandas as pd

import re

from pymystem3 import Mystem

import nltk
from nltk.corpus import stopwords

from tensorflow.keras.preprocessing.sequence import pad_sequences

def remove_special_characters(text):
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\d', ' ', text)
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    return text

def unpack_predict(predict):
    if isinstance(predict, (int)):
        return predict
    if len(predict) > 1:
        return np.argmax(predict)
    return unpack_predict(predict[0])
    
def predict(model, tokenizer, text, max_news_len, is_proba=False):
    _df = pd.DataFrame({'post_text': [text]})
    
    _df['post_text'] = _df['post_text'].apply(lambda x: x.lower())
    _df['post_text'] = _df['post_text'].apply(remove_special_characters)
    _df['tokens'] = _df['post_text'].apply(nltk.word_tokenize)
    
    _stop_words = set(stopwords.words('russian'))
    
    _df['tokens'] = _df['tokens'].apply(lambda x: [word for word in x if word not in _stop_words])

    _m = Mystem()
    _df['tokens'] = _df['tokens'].apply(lambda x: [_m.lemmatize(word)[0] for word in x])
    _df['processed_text'] = _df['tokens'].apply(lambda x: ' '.join(x))
    _df.replace("", pd.NA, inplace=True)
    _df.dropna(inplace=True)
    
    _sequences = tokenizer.texts_to_sequences(_df['processed_text'])
      
    x_predict = pad_sequences(_sequences, maxlen=max_news_len)
    
    if is_proba:
        return model.predict_proba(x_predict)
    
    return model.predict(x_predict)
        
def predict_class(model, tokenizer, text, max_news_len, model_ext):
    try:
        class_labels = ['АВТО БАТЯ', 'АЭРОФЛОТ', 'Телеграмма РЖД'] # ! Hardcode
        predictions = predict(model, tokenizer, text, max_news_len)
        
        predictions = predictions.tolist()
        
        # [[0.7172009348869324, 0.243381530046463, 0.03941752761602402]] - nn
        # [0] - rfc
        # [[1]] - cat
        # [1] - lin reg
        
        if model_ext == 'pkl':
            predicted_probabilities = predict(model, tokenizer, text, max_news_len, is_proba=True).tolist()[0]
        else:
            predicted_probabilities = predictions[0]
        
        predicted_class_index = unpack_predict(predictions)
        predicted_class = class_labels[predicted_class_index]
        
        return {
            'predicted_class': predicted_class,
            'predicted_probabilities': predicted_probabilities,
            'success': True
        }
        
    except:
        return {
            'message': 'Не удалось классифицировать',
            'success': False
        }
    
 
    