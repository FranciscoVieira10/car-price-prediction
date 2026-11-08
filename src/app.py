from pathlib import Path
import base64
import json

import streamlit as st

from src.predict import load_model, predict_price


st.set_page_config(page_title="AutoValue", page_icon="🚗", layout="wide")

# Electric cars are a recent technology (dataset maximum: 11 years)
MAX_AGE_ELECTRIC = 18

COUNTRY_NAMES = {
    "AT": "Austria",
    "BE": "Belgium",
    "DE": "Germany",
    "ES": "Spain",
    "FR": "France",
    "IT": "Italy",
    "LU": "Luxembourg",
    "NL": "Netherlands",
}

# Design tokens: deep navy surfaces, one amber accent, Outfit for display text
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;700;800&display=swap');

:root { --navy: #0f172a; --navy-2: #1e293b; --muted: #94a3b8; --accent: #f59e0b; }

header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1400px; padding: 1.5rem 2.5rem 3rem; }

.hero {
    background: var(--navy); color: #f8fafc; border-radius: 24px;
    padding: 1.6rem 2.5rem 2.6rem; margin-bottom: 2rem; font-family: 'Outfit', sans-serif;
}
.nav { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2.4rem; }
.brand { font-size: 1.35rem; font-weight: 800; letter-spacing: -0.02em; }
.brand span { color: var(--accent); }
.nav .links { color: var(--muted); font-size: 0.9rem; }
.nav .links { display: flex; align-items: center; gap: 0.9rem; }
.flags { display: flex; gap: 0.35rem; }
.flag { width: 22px; height: 15px; border-radius: 3px; box-shadow: 0 0 0 1px #ffffff22; }
.flag.at { background: linear-gradient(#ed2939 33.3%, #fff 33.3% 66.6%, #ed2939 66.6%); }
.flag.be { background: linear-gradient(90deg, #000 33.3%, #fdda24 33.3% 66.6%, #ef3340 66.6%); }
.flag.de { background: linear-gradient(#000 33.3%, #dd0000 33.3% 66.6%, #ffce00 66.6%); }
.flag.es { background: linear-gradient(#aa151b 25%, #f1bf00 25% 75%, #aa151b 75%); }
.flag.fr { background: linear-gradient(90deg, #002395 33.3%, #fff 33.3% 66.6%, #ed2939 66.6%); }
.flag.it { background: linear-gradient(90deg, #009246 33.3%, #fff 33.3% 66.6%, #ce2b37 66.6%); }
.flag.lu { background: linear-gradient(#ed2939 33.3%, #fff 33.3% 66.6%, #00a1de 66.6%); }
.flag.nl { background: linear-gradient(#ae1c28 33.3%, #fff 33.3% 66.6%, #21468b 66.6%); }
.hero .title {
    font-family: 'Outfit', sans-serif; color: #f8fafc; font-weight: 800;
    font-size: clamp(2rem, 4.2vw, 3.4rem); line-height: 1.05; letter-spacing: -0.03em;
    margin: 0; padding: 0; max-width: 720px;
}
.hero .title span { color: var(--accent); }
.hero p { color: var(--muted); font-size: 1.05rem; margin: 1rem 0 0; max-width: 560px; }

.section {
    font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 700;
    margin: 0.4rem 0 0.2rem; display: flex; align-items: center; gap: 0.6rem;
}
.section small { color: var(--accent); font-size: 0.8rem; font-weight: 700; }

.panel {
    background: var(--navy); color: #f8fafc; border-radius: 24px;
    padding: 2rem; font-family: 'Outfit', sans-serif;
}
.panel .eyebrow { color: var(--accent); font-size: 0.75rem; font-weight: 700; letter-spacing: 0.18em; }
.panel .car { display: flex; align-items: center; gap: 0.75rem; font-size: 1.5rem; font-weight: 700; margin-top: 0.8rem; }
.panel .logo {
    width: 3rem; height: 3rem; flex-shrink: 0; border-radius: 14px; background: #fff;
    display: flex; align-items: center; justify-content: center; padding: 0.4rem;
}
.panel .logo img { max-width: 100%; max-height: 100%; object-fit: contain; }

.hero { position: relative; overflow: hidden; }
.hero .car-art {
    position: absolute; right: 2.5rem; bottom: 1.6rem; width: min(34%, 420px);
    opacity: 0.9; pointer-events: none;
}
@media (max-width: 900px) { .hero .car-art { display: none; } }
.panel .price { font-variant-numeric: tabular-nums; }
.panel .price {
    font-size: clamp(2.6rem, 4.5vw, 3.8rem); font-weight: 800;
    letter-spacing: -0.03em; line-height: 1.1; margin: 0.3rem 0 1.4rem;
}
.panel .row {
    display: flex; justify-content: space-between; padding: 0.6rem 0;
    border-top: 1px solid var(--navy-2); font-size: 0.95rem;
}
.panel .row span:first-child { color: var(--muted); }
.panel .empty { color: var(--muted); margin: 1rem 0 0.5rem; line-height: 1.6; }
.panel .note { color: var(--muted); font-size: 0.8rem; margin-top: 1.4rem; }

.panel { margin-bottom: 0.9rem; }
div.stButton > button[kind="primary"] {
    background: var(--accent); border: none; color: var(--navy);
    font-weight: 700; font-size: 1rem; padding: 0.85rem; border-radius: 14px;
    box-shadow: 0 6px 18px #f59e0b40; transition: transform 0.15s, box-shadow 0.15s;
}
div.stButton > button[kind="primary"]:hover {
    background: #fbbf24; color: var(--navy); transform: translateY(-1px); box-shadow: 0 10px 24px #f59e0b55;
}
div.stButton > button[kind="primary"]:active { transform: translateY(0); box-shadow: 0 4px 12px #f59e0b40; }

@media (max-width: 640px) {
    .block-container { padding: 1rem 1rem 2rem; }
    .hero { padding: 1.2rem 1.4rem 1.8rem; }
    .nav .links .text { display: none; }
}
</style>
"""


def html(markup, target=st):
    """Render HTML; indentation is stripped so Markdown never turns it into a code block."""
    target.markdown(" ".join(line.strip() for line in markup.splitlines()), unsafe_allow_html=True)


def section(number, title):
    html(f'<div class="section"><small>0{number}</small>{title}</div>')


# Animates the price from €0 to its value (ease-out, about 1 second)
COUNT_UP_JS = """
<script>
document.querySelectorAll('.panel .price[data-target]').forEach((el) => {
    const target = Number(el.dataset.target);
    const start = performance.now();
    const step = (now) => {
        const t = Math.min((now - start) / 1000, 1);
        const value = Math.round(target * (1 - Math.pow(1 - t, 3)));
        el.textContent = '€' + value.toLocaleString('en-US');
        if (t < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
});
</script>
"""


@st.cache_data
def logo_html(make):
    """Manufacturer logo from assets/logos (embedded, so no internet is needed)."""
    logo_path = Path(__file__).resolve().parent.parent / "assets" / "logos" / f"{make.lower().replace(' ', '-')}.png"
    if not logo_path.exists():
        return ""
    encoded = base64.b64encode(logo_path.read_bytes()).decode()
    return f'<span class="logo"><img src="data:image/png;base64,{encoded}" alt="{make} logo"></span>'


@st.cache_resource
def get_model():
    return load_model()


# Load valid categories
project_root = Path(__file__).resolve().parent.parent
categories_path = project_root / "config" / "valid_categories.json"

with open(categories_path, "r", encoding="utf-8") as file:
    valid_categories = json.load(file)

html(CSS)

# Hero
FLAGS = "".join(f'<span class="flag {code.lower()}" title="{name}"></span>' for code, name in COUNTRY_NAMES.items())
FLAGS = f'<span class="flags">{FLAGS}</span>'
html(f"""
<div class="hero">
    <div class="nav">
        <div class="brand">Auto<span>Value</span></div>
        <div class="links"><span class="text">Used car valuation · 8 European markets</span>{FLAGS}</div>
    </div>
    <div class="title">Know what your car is <span>worth</span>.</div>
    <p>Enter a few details about the vehicle and get an instant estimate of its market price.</p>
    <svg class="car-art" viewBox="0 0 420 150" fill="none" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M18 108 V92 Q20 80 46 76 L120 68 Q158 36 214 31 L268 31 Q312 34 350 66 L392 73 Q408 77 406 94 V108"/>
        <path d="M18 108 H74 M126 108 H294 M346 108 H406"/>
        <path d="M134 68 Q166 42 214 38 H226 V68 Z M238 38 H266 Q300 41 324 66 H238 Z"/>
        <circle cx="100" cy="108" r="24"/><circle cx="100" cy="108" r="9"/>
        <circle cx="320" cy="108" r="24"/><circle cx="320" cy="108" r="9"/>
        <path d="M384 82 H400 M22 86 H36" stroke-width="4"/>
        <path d="M40 140 H380" stroke="#334155" stroke-width="2"/>
    </svg>
</div>
""")

form_col, price_col = st.columns([1.7, 1], gap="large")

# Form
with form_col:
    section(1, "Vehicle")
    col1, col2, col3 = st.columns(3)
    with col1:
        make = st.selectbox("Make", valid_categories["make"])

    available_fuels = sorted(valid_categories["models_by_make_and_fuel"][make].keys())
    with col2:
        fuel = st.selectbox("Fuel category", available_fuels)

    available_models = valid_categories["models_by_make_and_fuel"][make][fuel]
    with col3:
        model_name = st.selectbox("Model", available_models)

    st.divider()
    section(2, "Specifications")
    col1, col2, col3 = st.columns(3)
    with col1:
        mileage = st.number_input("Mileage (km)", min_value=0, value=80000, step=5000)
    with col2:
        # Only electric cars have an age limit
        max_age = MAX_AGE_ELECTRIC if fuel == "Electric" else None
        vehicle_age = st.number_input("Age (years)", min_value=0, max_value=max_age, value=5,
                                      key=f"age_{max_age}")
    with col3:
        # Start at the typical power of the selected model; the key resets it when the model changes
        typical_power = valid_categories["power_median_by_make_fuel_model"][make][fuel][model_name]
        power = st.number_input("Power (hp)", min_value=1, value=max(typical_power, 1), step=10,
                                key=f"power_{make}_{fuel}_{model_name}")

    col1, col2 = st.columns(2)
    with col1:
        available_transmissions = valid_categories["transmissions_by_make_fuel_model"][make][fuel][model_name]
        transmission = st.selectbox("Transmission", available_transmissions)
    with col2:
        available_body_types = valid_categories["body_types_by_make_fuel_model"][make][fuel][model_name]
        body_type = st.selectbox("Body type", available_body_types)

    st.divider()
    section(3, "Market")
    country = st.selectbox(
        "Country",
        valid_categories["country_code"],
        format_func=lambda code: COUNTRY_NAMES.get(code, code),
    )


# The exact inputs sent to the model
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

def estimate(car):
    """Runs on button click, before the page reruns, so the panel never flickers."""
    st.session_state.result = {"car": car, "price": predict_price(get_model(), dict(car))}


# Only show a result if it was computed from the inputs currently on screen
result = st.session_state.get("result")
is_current = result is not None and result["car"] == car

# Price panel
with price_col:
    if is_current:
        details = {
            "Fuel": fuel,
            "Transmission": transmission,
            "Body type": body_type,
            "Mileage": f"{mileage:,} km",
            "Age": f"{vehicle_age} years",
            "Power": f"{power} hp",
            "Market": COUNTRY_NAMES.get(country, country),
        }
        rows = "".join(f'<div class="row"><span>{k}</span><span>{v}</span></div>'
                       for k, v in details.items())
        content = f"""
            <div class="car">
                {logo_html(make)}
                {make} {model_name}
            </div>
            <div class="price" data-target="{result["price"]:.0f}">€{result["price"]:,.0f}</div>
            {rows}
        """
    elif result is not None:
        content = """
            <div class="empty">The vehicle details have changed. Click
            <b>Estimate price</b> to update the valuation.</div>
        """
    else:
        content = """
            <div class="empty">Complete the vehicle details and click
            <b>Estimate price</b> to see its estimated market value.</div>
        """

    # st.html (not st.markdown) so the small count-up script can run
    st.html(f"""
    <div class="panel">
        <div class="eyebrow">ESTIMATED VALUE</div>
        {content}
        <div class="note">This is an estimate of the advertised price, not a final sale price.</div>
    </div>
    {COUNT_UP_JS}
    """, unsafe_allow_javascript=True)
    st.button("Estimate price  →", type="primary", width="stretch", on_click=estimate, args=(car,))
