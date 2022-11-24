from flask import Flask, render_template, request
import pickle as pc
app = Flask(__name__)
web_phish_model = open('templates\Skripsi.pkl', 'rb')
web_phish_model_ls = pc.load(web_phish_model)

@app.route('/', methods=['GET'])
def main():
    data = {
        "link" : "",
        "result" : ""
    }
    return render_template('index.html', data = data)

@app.route('/', methods=['POST'])
def predict():
    features = request.form.get("masuklink")
    X_Predict = []
    X_Predict.append(str(features))
    y_Predict = web_phish_model_ls.predict(X_Predict)
    if y_Predict == 'bad':
        result = "Ini Website phishing!!"
    else:
        result = "Ini Bukan Website Phishing"

    data = {
        "link" : features,
        "result" : result
    }

    return render_template('index.html',data = data)
if __name__ == '__main__':
    app.run(port=3000, debug=True)