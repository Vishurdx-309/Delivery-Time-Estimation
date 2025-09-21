from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
import numpy as np
from typing import Literal, Annotated
import pickle 
import math
import pandas as pd

# import the ML model 
with open('delivery_time_model.pkl','rb') as f:
    model = pickle.load(f)
    
app = FastAPI()


# pydantic model build to validate the input data

class UserInput(BaseModel):
    age : Annotated[int,Field(...,ge = 18, lt = 120,description = 'Age of the delivery person')]
    rating : Annotated[float,Field(...,ge = 1, le = 6 ,description = 'Delivery person Ratings')]
    distance : Annotated[int,Field(...,gt = 0,description = 'Total Distance to be covered')]
    
    
@app.post('/predict')
def predict_time(data: UserInput):
    features = np.array([[data.age, data.rating, data.distance]])
    prediction = model.predict(features)

    prediction_value = math.ceil(float(prediction[0]))

    return JSONResponse(
        status_code=200,
        content={"Predicted Delivery Time in Minutes": prediction_value}
    )
