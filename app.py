from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

model = joblib.load("customer_churn_logistic_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        customer_data = pd.DataFrame([{
            "gender": data["gender"],
            "SeniorCitizen": int(data["SeniorCitizen"]),
            "Partner": data["Partner"],
            "Dependents": data["Dependents"],
            "tenure": float(data["tenure"]),
            "PhoneService": data["PhoneService"],
            "MultipleLines": data["MultipleLines"],
            "InternetService": data["InternetService"],
            "OnlineSecurity": data["OnlineSecurity"],
            "OnlineBackup": data["OnlineBackup"],
            "DeviceProtection": data["DeviceProtection"],
            "TechSupport": data["TechSupport"],
            "StreamingTV": data["StreamingTV"],
            "StreamingMovies": data["StreamingMovies"],
            "Contract": data["Contract"],
            "PaperlessBilling": data["PaperlessBilling"],
            "PaymentMethod": data["PaymentMethod"],
            "MonthlyCharges": float(data["MonthlyCharges"]),
            "TotalCharges": float(data["TotalCharges"])
        }])

        prediction = model.predict(customer_data)[0]

        probabilities = model.predict_proba(customer_data)[0]
        classes = model.classes_

        churn_index = list(classes).index("Yes")
        churn_probability = probabilities[churn_index] * 100

        if prediction == "Yes":
            result = "Customer is likely to CHURN"
            risk = "High Risk"
        else:
            result = "Customer is likely to STAY"
            risk = "Low Risk"

        return jsonify({
            "success": True,
            "prediction": prediction,
            "result": result,
            "risk": risk,
            "probability": round(churn_probability, 2)
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


if __name__ == "__main__":
    app.run(debug=True)