import streamlit as st
import requests
import json

st.set_page_config(
    page_title="InstaPredict",
    page_icon="🥡",
    layout="centered"
)

def apply_custom_theme():
    st.markdown("""
    <style>
        .main {
            background-color: #FFFFFF;
        }
        
        h1, h3 {
            color: #FC8019;
        }
        
        .stButton>button {
            background-color: #FC8019;
            color: #FFFFFF;
            border-radius: 8px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #E8721A;
            color: #FFFFFF;
        }
        
        .stSlider [data-baseweb="slider"] {
            color: #FC8019;
        }
        
        .stImage > img {
            border-radius: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)

apply_custom_theme()

BACKEND_URL = "https://delivery-time-estimation.onrender.com/predict"

st.title("InstaPredict 🥡")
st.markdown("### Instant Delivery Time Predictions")
st.markdown("---")

st.image("food_delivery_scooter.jpg", use_container_width=True)

st.markdown("---")

st.header("Enter Delivery Details")

with st.form(key="delivery_form"):
    age = st.number_input(
        label="Delivery Person's Age",
        min_value=18,
        max_value=120,
        value=25,
        help="Enter the age of the delivery person (18-119)."
    )
    
    rating = st.slider(
        label="Delivery Person's Rating",
        min_value=1.0,
        max_value=6.0,
        value=4.5,
        step=0.1,
        help="Select the rating of the delivery person (1.0-6.0)."
    )

    distance = st.number_input(
        label="Distance in Kilometers",
        min_value=1,
        max_value=100,
        value=10,
        help="Enter the total distance for the delivery."
    )

    submit_button = st.form_submit_button(label="Predict Delivery Time", use_container_width=True)

if submit_button:
    payload = {
        "age": age,
        "rating": rating,
        "distance": distance
    }

    try:
        response = requests.post(BACKEND_URL, json=payload)
        response.raise_for_status()

        prediction_data = response.json()
        predicted_time = prediction_data["Predicted Delivery Time in Minutes"]

        st.success("Prediction successful!")
        st.metric(
            label="Predicted Delivery Time",
            value=f"{predicted_time} Minutes"
        )
        st.balloons()

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the prediction service. Please ensure the backend is running.")
        st.error(f"Details: {e}")
        try:
            error_detail = response.json().get('detail')
            if error_detail:
                st.error(f"Backend Validation Error: {error_detail}")
        except:
            pass
