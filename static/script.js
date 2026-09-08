const form = document.getElementById("predictionForm");

const predictBtn = document.getElementById("predictBtn");
const btnText = document.getElementById("btnText");
const loader = document.getElementById("loader");

const resultCard = document.getElementById("resultCard");
const resultTitle = document.getElementById("resultTitle");
const resultText = document.getElementById("resultText");
const probabilityValue = document.getElementById("probabilityValue");
const progressBar = document.getElementById("progressBar");
const riskBadge = document.getElementById("riskBadge");
const resultIcon = document.getElementById("resultIcon");


form.addEventListener("submit", async function (event) {

    event.preventDefault();

    // Show loading state
    predictBtn.disabled = true;
    btnText.textContent = "Analyzing...";
    loader.style.display = "inline-block";

    // Collect form data
    const data = {

        gender: document.getElementById("gender").value,

        SeniorCitizen:
            document.getElementById("SeniorCitizen").value,

        Partner:
            document.getElementById("Partner").value,

        Dependents:
            document.getElementById("Dependents").value,

        tenure:
            document.getElementById("tenure").value,

        PhoneService:
            document.getElementById("PhoneService").value,

        MultipleLines:
            document.getElementById("MultipleLines").value,

        InternetService:
            document.getElementById("InternetService").value,

        OnlineSecurity:
            document.getElementById("OnlineSecurity").value,

        OnlineBackup:
            document.getElementById("OnlineBackup").value,

        DeviceProtection:
            document.getElementById("DeviceProtection").value,

        TechSupport:
            document.getElementById("TechSupport").value,

        StreamingTV:
            document.getElementById("StreamingTV").value,

        StreamingMovies:
            document.getElementById("StreamingMovies").value,

        Contract:
            document.getElementById("Contract").value,

        PaperlessBilling:
            document.getElementById("PaperlessBilling").value,

        PaymentMethod:
            document.getElementById("PaymentMethod").value,

        MonthlyCharges:
            document.getElementById("MonthlyCharges").value,

        TotalCharges:
            document.getElementById("TotalCharges").value
    };


    try {

        const response = await fetch("/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)
        });


        const result = await response.json();


        if (!result.success) {
            throw new Error(result.error);
        }


        // Display result
        resultCard.classList.remove("hidden");

        resultTitle.textContent = result.result;

        resultText.textContent =
            "The model has analyzed the customer information and estimated the churn risk.";

        probabilityValue.textContent =
            result.probability + "%";

        progressBar.style.width =
            result.probability + "%";

        riskBadge.textContent =
            result.risk;


        // Result styling
        if (result.prediction === "Yes") {

            resultIcon.textContent = "!";

            resultIcon.style.background = "#fff0f0";
            resultIcon.style.color = "#d93636";

            riskBadge.style.background = "#fff0f0";
            riskBadge.style.color = "#d93636";

        } else {

            resultIcon.textContent = "✓";

            resultIcon.style.background = "#eaf7ee";
            resultIcon.style.color = "#23934d";

            riskBadge.style.background = "#eaf7ee";
            riskBadge.style.color = "#23934d";
        }


        // Scroll to result
        resultCard.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });


    } catch (error) {

        alert("Prediction Error: " + error.message);

    } finally {

        predictBtn.disabled = false;
        btnText.textContent = "Predict Customer Churn";
        loader.style.display = "none";
    }

});