from flask import request, jsonify, Blueprint

import pandas as pd

from src.controllers.classify import classify

from src.learned_models.models import models, info_model

classify_route_blueprint = Blueprint('classify', __name__)

@classify_route_blueprint.route('/classify', methods=['GET', 'POST'])
def classify_route():
    if request.method == 'POST':
        data = request.get_json()
        
        try:
            model_id = int(data['model_id']) or 0
            text = data['text']
            
            classify_body = classify(model_id, text)
            
            if classify_body['success']:
                result = jsonify(classify_body) # Creating a classify of the model selected by id and the data selected by attributes
            else:
                result = jsonify(classify_body), 500
        except:
            result = jsonify({ 'success': False, 'message': 'Что-то пошло не так!'  }), 400
        return result
    else:
        clean_models = list(map(info_model, models))
        
        return jsonify(clean_models)