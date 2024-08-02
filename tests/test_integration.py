from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status":"ok","database":"connected"}

## adicionando mais testes da api
## https://fastapi.tiangolo.com/tutorial/testing/

# usando o history sem ter usado o predict
def test_model_history_no_prediction():

    response = client.get("/model/history")

    response_json = response.json()

    assert response.status_code == 200
    assert response_json['status'] == 'ok'
    assert response_json['history'] == []


# usando o predict sem carregar o modelo
def test_model_predict_no_model_loaded():
    payload = {
        "dep_delay": 10,
        "origin": "JFK",
        "dest": "ORD",
        "carrier": "AA",
        "distance": 400
        }
    response = client.post("/model/predict", json=payload)

    response_json = response.json()
 
    assert response.status_code == 400
    assert response_json == {'detail': 'Model not loaded'}

# teste que vai carregar um arquivo errado (model.txt) na api
@pytest.mark.xfail
def test_model_load_wrong_file():
    with open('model.txt', 'rb') as file:
        response = client.post("/model/load",files={"file": file} )
    assert response.status_code == 200
    assert response.json() == {"status": "Model loaded successfully"}


# teste que vai carregar o modelo na api e testar o endpoint /model/load
def test_model_load():
    with open('model.pkl', 'rb') as file:
        response = client.post("/model/load",files={"file": file} )
    assert response.status_code == 200
    assert response.json() == {"status": "Model loaded successfully"}


# usando floats nas variáveis
def test_model_predict_floats():
    payload = {
        "dep_delay": 10,
        "origin": "JFK",
        "dest": "ORD",
        "carrier": "AA",
        "distance": 400
        }
    response = client.post("/model/predict", json=payload)

    response_json = response.json()
    print(response_json['prediction'])
    assert response.status_code == 200
    assert type(response_json['prediction']) == float

# testando falha se houver um 'typo' no payload 
@pytest.mark.xfail
def test_model_predict_wrong_data():
    payload = {
        "dep_delay": 10,
        "origin": "JFKERRADO",
        "dest": "ORD",
        "carrier": "AA",
        "distance": 400
        }
    response = client.post("/model/predict", json=payload)

    response_json = response.json()

    assert response.status_code == 200



# usando strings ao invés de floats
def test_model_predict_strings():
    payload = {
    "dep_delay": '10',
    "origin": "JFK",
    "dest": "ORD",
    "carrier": "AA",
    "distance": '400.53'
    }
    response = client.post("/model/predict", json=payload)

    response_json = response.json()
    assert response.status_code == 200
    assert type(response_json['prediction']) == float

# alterando a ordem dos elementos do payload
def test_model_predict_order():
    payload = {
    "origin": "JFK",    
    "dep_delay": 10,
    "distance": 400.53,
    "dest": "ORD",
    "carrier": "AA"
    }
    response = client.post("/model/predict", json=payload)

    response_json = response.json()

    assert response.status_code == 200
    assert type(response_json['prediction']) == float

# alterando a ordem dos elementos do payload
def test_model_history():

    response = client.get("/model/history")

    response_json = response.json()

    assert response.status_code == 200
    assert response_json['status'] == 'ok'
    assert type(response_json['history']) == list
    assert type(response_json['history'][0]) == dict
    assert type(response_json['history'][1]) == dict

