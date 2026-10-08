import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeRegressor
from datetime import datetime,timedelta

st.set_page_config(page_title="Smartphone Dashboard", layout="wide")

st.markdown("""
<style>
            header[data-testid="stHeader"] {
    background: #0F172A !important;
}

header[data-testid="stHeader"] * {
    color: white !important;
}
.stApp {
    background: linear-gradient(135deg, #0F172A, #111827);
    color: white;
}

section[data-testid="stSidebar"] {
    background: rgba(17, 25, 40, 0.75) !important;
    backdrop-filter: blur(16px);
    border-right: 1px solid rgba(255,255,255,0.1);
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 0 20px rgba(0,198,255,0.2);
}

.stButton>button {
    background: linear-gradient(90deg,#00C6FF,#0072FF);
    color: white;
    border: none;
    border-radius: 15px;
    height: 55px;
    font-size: 18px;
    font-weight: bold;
    box-shadow: 0 0 20px rgba(0,198,255,0.4);
}

.stTextInput input,
.stNumberInput input,
.stSelectbox div {
    background-color: rgba(255,255,255,0.08) !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}
.stNumberInput input {
    color: white !important;
    font-size: 28px !important;
    font-weight: bold !important;
    background-color: #0F172A !important;
}
.stNumberInput input {
    font-size: 40px !important;
    font-weight: 800 !important;
    color: white !important;
    height: 70px !important;
}
.stNumberInput input::placeholder {
    color: white !important;
    opacity: 1 !important;           
}

h1 {
    font-size: 50px !important;
    font-weight: 800 !important;
    color: #00C6FF !important;
            
label{
    color:#FFFFFF !important;
    font-size: 18px !important;
    font-weight: bold !important;}
}

</style>
""", unsafe_allow_html=True)

# TITLE
st.markdown("# 📱 Smartphone Price Drop Analytics Dashboard")
st.sidebar.title("Dashboard Menu")
st.sidebar.write("Mobile price prediction system")

# LOAD DATASET

df = pd.read_excel("smartphone_price_drop_dataset (1).xlsx")
print(df.columns)


# Encode categorical columns
le_brand = LabelEncoder()

df["brand"] = le_brand.fit_transform(df["brand"])

# Clean RAM & Storage
df["ram"] = df["ram"].str.replace("GB", "").astype(int)
df["storage"] = df["storage"].str.replace("GB", "").astype(int)

# Features & Target
target ="price_drop_target"
df.columns=df.columns.str.strip().str.lower()
df["price_drop_target"]=df["original_price"]-df["price"]
target="price_drop_target"
X = df.drop(columns=["source","model","scrape_date",target],errors="ignore")
y =df[target]
st.write(df.columns.tolist())

# TRAIN MODEL

model = DecisionTreeRegressor(random_state=42)

model.fit(X, y)

# PREDICTION

brand_name = st.selectbox("select brand",le_brand.classes_)

brand_encoded= int(le_brand.transform([brand_name])[0])
brand_models = {

    "iQOO": [
        "iQOO Neo 7",
        "iQOO Z9",
        "iQOO Z7 Pro"
    ],

    "Samsung": [
        "S25",
        "Galaxy F15",
        "Galaxy A15",
        "S25Ultra",
        "S26Ultra",
        "S26"
    ],

    "Motorola": [
        "G34",
        "Edge40",
        "G54",
    ],

    "Realme": [
        "C55",
        "11 Pro",
        "Narzo 60",
        "realme8pro",
        "realme11pro plus"
    ],
    "Redmi": [
        "Note12",
        "Note13",
        "Redmi 13C"
    ] 
}
# Model dropdown
model_name = st.selectbox(
    "Select Model",
    brand_models[brand_name]
)

# Encode brand
brand_encoded = int(
    le_brand.transform([brand_name])[0]
)

current_price = st.number_input("current_price",key="current_price")
original_price = st.number_input("original_price",key="original_price")
discount_percent = st.number_input("discount_percent",key="discount_percent")
rating = st.number_input("rating",key="rating")
review_count = st.number_input("review_count",key="review_count")
ram = st.number_input("ram",key="ram")
storage = st.number_input("storage",key="storage")
battery_mah= st.number_input("battery_mah",key="battery_mah")

import pandas as pd

input_data = pd.DataFrame([{
    "brand":brand_encoded,
    "price":current_price,
    "original_price":original_price,
    "discount_percent":discount_percent,
    "rating":rating,
    "review_count":review_count,
    "ram":ram,
    "storage":storage,
    "battery_mah":battery_mah,   
    "price_7days_ago":0,
    "price_30days_ago":0
}])
prediction = model.predict(input_data)[0]
print(input_data)
print(input_data.dtypes)

st.success(
        f"Predicted Price Drop: ₹{prediction:.2f}"
    )

user_input = {
    "brand":brand_encoded,
    "price":current_price,
    "original_price":original_price,
    "discount_percent":discount_percent,
    "rating":rating,
    "review_count":review_count,
    "ram":ram,
    "storage":storage,
    "battery_mah":battery_mah,
    "price_7days_ago":0,
    "price_30days_ago":0
 }
input_df=pd.DataFrame([user_input])

st.title("Smartphone price drop predictor")
#Drop date logic
import pandas as pd
if st.button("Predict Price Drop"):
    prediction=model.predict(input_df)[0]

    st.success(f"Expected Price Drop amount:{prediction:,.2f}")
    
    if prediction>=5000:
        days=10

    elif prediction>=3000:
        days=20

    else:
        days=45
    future_date=datetime.now()+timedelta(days=days)

    col1, col2, col3 = st.columns(3)

    with col1:
       st.metric("Predicted Drop", f"₹{prediction:,.0f}")

    with col2:
        st.metric("Expected Price", f"₹{current_price - prediction:,.0f}")

    with col3:
        st.metric("Drop Date", future_date.strftime("%d-%m-%Y"))

    st.info(f"Excepted Price Drop Date:{future_date.strftime('%d-%m-%Y')}")
#Smart Deal Rating
    st.subheader("Smart Deal Rating")

    if discount_percent >= 40 and rating >= 4:
        st.success("Excellent Deal")
    elif discount_percent >= 25 and rating >= 3.5:
        st.info("Good Deal")
    elif discount_percent >= 10:
        st.warning("Average Deal")
    else:
        st.error("Overpriced Deal")
#Price history graph sample
    price_data=pd.DataFrame({"Days":[0,days//4,days//2,days],
                             "Expected Price":[current_price,
                                               current_price-prediction*0.25,
                                               current_price-prediction*0.50,
                                               current_price-prediction
                                               ]
                             })
    st.subheader("Excepted Price Drop Graph")
    st.line_chart(price_data.set_index("Days"))
    
#Best time to Buy
    from datetime import datetime,timedelta
    drop_date=datetime.now()+timedelta(days=days)
    st.subheader("Best Time To Buy")
    if prediction>=3000:
        st.warning(f"Wait until {drop_date.strftime("%d-%m-%Y")}for better price.")
    else:
        st.success("You can buy now.Big drop not excepted.")
    st.info(f"Excepted price after drop:{current_price-prediction:,.2f}")


