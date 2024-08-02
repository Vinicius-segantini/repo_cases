from fastapi import FastAPI, UploadFile, File, HTTPException
from database import InMemoryDatabase
import pickle
from pydantic import BaseModel, constr
from io import BytesIO
import uvicorn
import pandas as pd




app = FastAPI()

# variaveis globais
model = None
features = None
dummies_columns = None

# modelo de input do payload
class FlightData(BaseModel):
    dep_delay: float
    origin: constr(min_length=3, max_length=3)
    dest: constr(min_length=3, max_length=3)
    carrier: constr(min_length=2, max_length=2)
    distance: float





def format_prediction_input(flight_data): 
    input_df = pd.DataFrame([flight_data.model_dump()])
    model_input = pd.get_dummies(input_df[features], drop_first=True) 
    
    # Adicionar colunas ausentes
    missing_cols = list(set(dummies_columns) - set(model_input.columns))
    missing_cols_df = pd.DataFrame(0, index=model_input.index, columns=missing_cols)
    model_input = pd.concat([model_input, missing_cols_df], axis=1)

    # Garantir a ordem correta das colunas
    model_input = model_input[dummies_columns]
    return model_input




# API 

@app.post("/model/predict", status_code=200, tags=["predict"], summary="Get the flight information and returns the prediction for arrival delay in minutes")
async def predict(flight_data: FlightData):
    
    if model is None:
        raise HTTPException(status_code=400, detail="Model not loaded")
    
    db = InMemoryDatabase()
    
    model_input = format_prediction_input(flight_data)

    # Fazer a previsão
    prediction = model.predict(model_input)[0]
    
    # Salvar no histórico
    data = {"input": flight_data.model_dump(), "prediction": prediction}
    flights = db.get_collection('flights')
    flights.insert_one(data)
    
    return {"prediction": prediction}





@app.post("/model/load/", status_code=200, tags=["load"], summary="Loads the model from a pickle file")
async def load_model(file: UploadFile = File(...)):
    global model, features, dummies_columns
    try:
        # Ler o arquivo do modelo
        file_content = await file.read()
        model = pickle.load(BytesIO(file_content))
        dummies_columns = model["dummies_columns"]
        features = model["features"]
        model = model["model"]
        return {"status": "Model loaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error loading model: {e}")
    





@app.get("/model/history", status_code=200, tags=["history"], summary="Shows the history of the predictions made")
async def history():
    db = InMemoryDatabase()
    flights = db.get_collection('flights')
    return {"status": "ok", "history": [x for x in flights.find({},{"_id": 0})]}





@app.get("/health", status_code=200, tags=["health"], summary="Health check")
async def health():
    db_status = InMemoryDatabase.connection_test()
    
    if db_status:
        return {"status": "ok", "database": "connected"}
    else:
        raise HTTPException(status_code=503, detail="Database connection failed")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")