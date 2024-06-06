from src.learned_models.models import models

from src.utils.predict import predict_class

MAX_NEWS_LEN = 100

def find_model(model_id):
        return (list(filter(lambda v: v['id'] == model_id, models)) or models)[0]

tokenizer = find_model('_tokenizer')['model']

def classify(model_id, text):
        # If the model is not found, the first model of all is taken
        model = find_model(model_id)
        model_ext = model['file'].split('.')[-1]
        
        prediction = predict_class(model['model'], tokenizer, text, MAX_NEWS_LEN, model_ext)
        
        if prediction['success']:
                return {
                        'text': text,
                        'model_name': model['name'], 
                        'model_ru_name': model['ru_name'], 
                        'predicted_class': prediction['predicted_class'],
                        'predicted_probabilities': prediction['predicted_probabilities'], # [probability_class_0, probability_class_1, probability_class_2]
                        'success': True 
                }  
        else:
                return {
                        'text': text,
                        'message': prediction['message'],
                        'success': False 
                }