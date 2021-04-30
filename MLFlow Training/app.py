from flask import Flask, request, jsonify
import mlflow.pyfunc
import pandas as pd
import json

app = Flask(__name__)

#Cargamos el modelo
model = mlflow.pyfunc.load_model('models/iris_model_pyfunc')

#Load the meta_data
f = open("./meta_data.txt","r")
load_meta_data = json.loads(f.read())

#El Root, returnará el metadata.
@app.route('/', methods=['GET'])
def meta_data():
    return jsonify(load_meta_data)

#Prediction endpoint
@app.route('/predict', methods=['POST'])

def predict():
    req = request.get_json()

    print({'request':req})

    #Volvemos el request a un Dataframe
    to_inference = pd.DataFrame(req['data'])

    pred = model.predict(to_inference).tolist()

    print({'response':pred})

    return jsonify(pred)

app.run(host='0.0.0.0', port = 5000, debug=True)
