const form = document.getElementById("predictionForm");

const predictBtn = document.getElementById("predictBtn");
const buttonText = document.getElementById("buttonText");
const loader = document.getElementById("loader");

const resultCard = document.getElementById("resultCard");
const resultTitle = document.getElementById("resultTitle");
const resultMessage = document.getElementById("resultMessage");

const probabilityValue = document.getElementById("probabilityValue");
const progressBar = document.getElementById("progressBar");
const riskBadge = document.getElementById("riskBadge");
const resultIcon = document.getElementById("resultIcon");


// Check whether form exists
if (form) {

    form.addEventListener("submit", async function (event) {

        event.preventDefault();

        // Loading state
        predictBtn.disabled = true;
        buttonText.textContent = "Analyzing...";
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

            // Send data to Flask
            const response = await fetch(
                "http://127.0.0.1:5000/predict",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(data)
                }
            );


            const result = await response.json();


            // Check Flask response
            if (!response.ok || !result.success) {

                throw new Error(
                    result.error || "Prediction failed."
                );
            }


            // Show result card
            resultCard.classList.remove("hidden");


            // Result title
            resultTitle.textContent = result.result;


            // Result message
            resultMessage.textContent =
                "The model has analyzed the customer information and estimated the churn risk.";


            // Churn probability
            probabilityValue.textContent =
                result.probability + "%";


            // Progress bar
            progressBar.style.width =
                result.probability + "%";


            // Risk badge
            riskBadge.textContent =
                result.risk;


            // High Risk
            if (result.prediction === "Yes") {

                resultIcon.textContent = "!";

                resultIcon.style.background = "#450a0a";
                resultIcon.style.color = "#f87171";

                riskBadge.style.background = "#450a0a";
                riskBadge.style.color = "#f87171";
                riskBadge.style.borderColor = "#7f1d1d";

            }


            // Low Risk
            else {

                resultIcon.textContent = "✓";

                resultIcon.style.background = "#052e16";
                resultIcon.style.color = "#4ade80";

                riskBadge.style.background = "#052e16";
                riskBadge.style.color = "#4ade80";
                riskBadge.style.borderColor = "#166534";
            }


            // Scroll to result
            resultCard.scrollIntoView({
                behavior: "smooth",
                block: "center"
            });


        }

        catch (error) {

            console.error("Prediction Error:", error);

            alert(
                "Prediction Error: " + error.message
            );

        }

        finally {

            // Reset button
            predictBtn.disabled = false;

            buttonText.textContent =
                "Predict Customer Churn";

            loader.style.display = "none";
        }

    });

}