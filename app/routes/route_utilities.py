from flask import abort, make_response
from ..db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response , 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)
    
    if not model:
        response = {"message": f"{cls.__name__} {model_id} was not found"}
        abort(make_response(response, 404))
    
    return model

def create_response_for_model(cls, model_data, response_code=201):
    try:
        new_model = cls.from_dict(model_data)
        
    except KeyError as error:
        response = {"details": f"Request body must include {error.args[0]}."}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), response_code