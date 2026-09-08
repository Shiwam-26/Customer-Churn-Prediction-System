# =========================================================
# STUDENT MENTAL HEALTH PREDICTION API
# =========================================================

from pathlib import Path
from typing import Literal

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# =========================================================
# 1. MODEL PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "Mental_Health_Model.pkl"


# =========================================================
# 2. LOAD MACHINE LEARNING MODEL
# =========================================================

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Mental Health Model loaded successfully.")

except Exception as e:
    model = None
    print(f"❌ Error loading model: {e}")


# =========================================================
# 3. TOP COUNTRIES
# =========================================================

top_countries = [
    "Other",
    "India",
    "USA",
    "Canada",
    "Australia",
    "UK",
    "Germany",
    "Mexico",
    "Turkey",
    "France"
]


# =========================================================
# 4. CREATE FASTAPI APP
# =========================================================

app = FastAPI(
    title="Student Mental Health Predictor",
    description="Machine Learning API for predicting student mental health score.",
    version="1.0.0"
)


# =========================================================
# 5. CORS CONFIGURATION
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# 6. INPUT DATA MODEL
# =========================================================

class StudentData(BaseModel):

    age: int = Field(
        ...,
        ge=10,
        le=100,
        description="Student age"
    )

    gender: Literal[
        "Male",
        "Female"
    ]

    country: str = Field(
        ...,
        min_length=1,
        description="Student country"
    )

    academic_level: Literal[
        "Undergraduate",
        "Graduate",
        "High School"
    ]

    most_used_platform: Literal[
        "Facebook",
        "LinkedIn",
        "Instagram",
        "Snapchat",
        "Twitter",
        "YouTube",
        "TikTok",
        "LINE",
        "KakaoTalk",
        "VKontakte",
        "WhatsApp",
        "WeChat"
    ]

    purpose_of_use: Literal[
        "Networking",
        "Education",
        "Entertainment",
        "News"
    ]

    avg_daily_usage_hours: float = Field(
        ...,
        ge=0,
        le=24,
        description="Average daily social media usage in hours"
    )

    daily_unlocks: int = Field(
        ...,
        ge=0,
        description="Number of daily device unlocks"
    )

    study_hours: float = Field(
        ...,
        ge=0,
        le=24,
        description="Daily study hours"
    )

    physical_activity_hours: float = Field(
        ...,
        ge=0,
        le=24,
        description="Daily physical activity hours"
    )

    sleep_hours_per_night: float = Field(
        ...,
        ge=0,
        le=24,
        description="Average sleep hours per night"
    )

    stress_level: Literal[
        "Low",
        "Medium",
        "High",
        "Very High"
    ]


# =========================================================
# 7. OUTPUT DATA MODEL
# =========================================================

class PredictionResponse(BaseModel):

    predicted_mental_health_score: float


# =========================================================
# 8. ROOT ROUTE
# =========================================================

@app.get("/")
def root():

    return {
        "message": "Student Mental Health Predictor API is running.",
        "status": "success"
    }


# =========================================================
# 9. HEALTH CHECK ROUTE
# =========================================================

@app.get("/health")
def health_check():

    if model is None:

        return {
            "status": "error",
            "model_loaded": False
        }

    return {
        "status": "healthy",
        "model_loaded": True
    }


# =========================================================
# 10. PREDICTION ROUTE
# =========================================================

@app.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(data: StudentData):

    # -----------------------------------------------------
    # Check if model is loaded
    # -----------------------------------------------------

    if model is None:

        raise HTTPException(
            status_code=500,
            detail="Machine learning model is not loaded."
        )

    try:

        # -------------------------------------------------
        # Group country
        # -------------------------------------------------

        country_group = (
            data.country
            if data.country in top_countries
            else "Other"
        )

        # -------------------------------------------------
        # Create DataFrame
        # -------------------------------------------------

        input_row = pd.DataFrame([
            {
                "Age": data.age,

                "Gender": data.gender,

                "Country": data.country,

                "Academic_Level": data.academic_level,

                "Most_Used_Platform": data.most_used_platform,

                "Purpose_Of_Use": data.purpose_of_use,

                "Avg_Daily_Usage_Hours": data.avg_daily_usage_hours,

                "Daily_Unlocks": data.daily_unlocks,

                "Study_Hours": data.study_hours,

                "Physical_Activity_Hours": data.physical_activity_hours,

                "Sleep_Hours_Per_Night": data.sleep_hours_per_night,

                "Stress_Level": data.stress_level,

                "Grouped_Country": country_group
            }
        ])

        # -------------------------------------------------
        # Make prediction
        # -------------------------------------------------

        prediction = model.predict(input_row)[0]

        prediction = round(float(prediction), 2)

        # -------------------------------------------------
        # Return result
        # -------------------------------------------------

        return PredictionResponse(
            predicted_mental_health_score=prediction
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )