from pathlib import Path
import json

import streamlit as st

from src.predict import load_model, predict_price


st.set_page_config(page_title="Car Price Prediction", page_icon="🚗", layout="centered")

# Light styling: price card and spacing
st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; max-width: 820px; }
    .price-card {
        background: linear-gradient(135deg, #1e3a8a, #2563eb);
        color: white;
        border-radius: 16px;
        padding: 1.6rem;
        text-align: center;
        margin-top: 1rem;
    }
    .price-card .label { font-size: 0.95rem; opacity: 0.85; letter-spacing: 0.05em; }
    .price-card .value { font-size: 2.6rem; font-weight: 700; margin: 0.3rem 0; }
    .price-card .details { font-size: 0.9rem; opacity: 0.85; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def get_model():
    return load_model()


# Load valid categories
project_root = Path(__file__).resolve().parent.parent
categories_path = project_root / "config" / "valid_categories.json"

with open(categories_path, "r", encoding="utf-8") as file:
    valid_categories = json.load(file)

# Header
st.title("🚗 Car Price Prediction")
st.markdown(
    "Estimate the advertised price of a used car with a **CatBoost** model "
    "trained on listings from eight European markets."
)

# Section 1: Vehicle (dependent menus: Make → Fuel → Model)
with st.container(border=True):
    st.subheader("Vehicle")
    col1, col2, col3 = st.columns(3)

    with col1:
        make = st.selectbox("Make", valid_categories["make"])

    available_fuels = sorted(valid_categories["models_by_make_and_fuel"][make].keys())
    with col2:
        fuel = st.selectbox("Fuel category", available_fuels)

    available_models = valid_categories["models_by_make_and_fuel"][make][fuel]
    with col3:
        model_name = st.selectbox("Model", available_models)

# Section 2: Specifications
with st.container(border=True):
    st.subheader("Specifications")
    col1, col2, col3 = st.columns(3)

    with col1:
        mileage = st.number_input("Mileage (km)", min_value=0, value=80000, step=5000)
    with col2:
        vehicle_age = st.number_input("Vehicle age (years)", min_value=0, value=5)
    with col3:
        power = st.number_input("Power (hp)", min_value=1, value=190, step=10)

    col1, col2, col3 = st.columns(3)
    with col1:
        transmission = st.selectbox("Transmission", valid_categories["transmission"])
    with col2:
        body_type = st.selectbox("Body type", valid_categories["body_type"])
    with col3:
        country = st.selectbox("Country", valid_categories["country_code"])

# Predict price
if st.button("Predict Price", type="primary", width="stretch"):
    car = {
        "make": make,
        "model": model_name,
        "mileage_numeric": mileage,
        "vehicle_age": vehicle_age,
        "power_hp": power,
        "fuel_category": fuel,
        "transmission": transmission,
        "body_type": body_type,
        "country_code": country,
    }

    with st.spinner("Estimating price..."):
        predicted_price = predict_price(get_model(), car)

    st.markdown(
        f"""
        <div class="price-card">
            <div class="label">ESTIMATED PRICE</div>
            <div class="value">€{predicted_price:,.0f}</div>
            <div class="details">{make} {model_name} · {fuel} · {vehicle_age} years · {mileage:,} km</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()
st.caption(
    "Predictions are estimates of advertised prices, based on data from "
    "eight European markets. Rare or very expensive vehicles may have "
    "larger prediction errors."
)
