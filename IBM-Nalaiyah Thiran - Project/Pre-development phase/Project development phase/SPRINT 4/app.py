from flask import Flask, render_template, request
import requests
import sys
API_KEY = "8cqf_Qc-PZbuOGpinZfs1SrsP-JbjMjye2X9oY4X-63H"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

app = Flask(__name__, static_url_path='')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/checkEligibility')
def checkEligibility():
    return render_template('register.html')

@app.route('/predict', methods=['POST'])
def predict():
    greScore = int(request.form['gre'])
    toeflScore = int(request.form['tofel'])
    univRank = int(request.form['university_rating'])
    sop = float(request.form['sop'])
    lor = float(request.form['lor'])
    cgpa = float(request.form['cgpa'])
    research = int(request.form['yes_no_radio'])
    array_of_values_to_be_scored = [greScore, toeflScore, univRank, sop, lor, cgpa, research]
    payload_scoring = {"input_data": [{"field": [["GRE Score","TOEFL Score","University Rating","SOP","LOR ","CGPA", "Research"]], "values": [array_of_values_to_be_scored]}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/35d1a0c8-7921-4798-bef9-c20ebffd3b9d/predictions?version=2022-11-17', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print(response_scoring.json())
    probability = response_scoring.json()['predictions'][0]['values'][0][0][0]
    print(probability, file=sys.stderr)
    if probability>0.50:
        return render_template('chance.html',probability=round(probability*100,5),title="You Have Chance",image="/image/chance.jpg",wish="ALL THE BEST....!")
    elif probability!=None:
        return render_template('chance.html',probability=round(probability*100,5),title="You have a LOW / NO chance",image="/image/nochance.jpg",wish="GOOD LUCK...!")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80,debug=True)


















