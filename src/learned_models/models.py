import os 
import json

import pickle
import joblib

from keras.models import load_model

import warnings

def load_models():
        warnings.simplefilter("ignore")
        
        file = open(os.path.abspath('./src/learned_models/models.json'), encoding="utf8")
        models = json.load(file)
        
        file.close() 

        for model in models:
                model_path = os.path.abspath(model['path'] + model['file']) # Getting the model path
                model_ext = model['file'].split('.')[-1]
                
                if (model_ext == 'pickle'):
                        with open(f'{model_path}', 'rb') as handle:
                                model['model'] = pickle.load(handle) # Loading a model and saving it to the dictionary
                elif (model_ext == 'pkl'):
                        model['model'] = joblib.load(model_path) # Loading a model and saving it to the dictionary
                else:
                        model['model'] = load_model(model_path)
                        
                
                print(f'Loaded model { model["name"] }')
        
        return models
   
def info_model(model):
        clean_model = { **model }
        
        del clean_model['file']
        del clean_model['path']
        del clean_model['model']
        
        return clean_model


models = load_models()