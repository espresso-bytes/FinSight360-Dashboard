import streamlit as st
import yfinance as yf
import pandas as pd

# Midnight Blue Theme with Creamy Fonts
st.markdown("""
    <style>
        /* Overall App Background */
        .stApp {
            background-color: #091f36;
            color: #d9d9d9;
            
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color:  #393f4d;
            color: #FFFAF0;
        }

        /* Headings */
        h1, h2, h3, .stMarkdown h1, .stMarkdown h2 {
            color: #FFFAF0;
        }

        /* Regular Text */
        html, body, [class*="css"] {
            color: #d9d9d9;
            font-family: 'Segoe UI', sans-serif;
        }

        /* DataFrames and Table cells */
        .stDataFrame {
            background-color: #0f172a;
            border: 1px solid #FFFAF0;
            color: #ffffff;
        }

        /* Buttons */
        .stButton>button {
            background-color: #0f2862;;
            color: #d9d9d9;
            font-weight: bold;
            border-radius: 6px;
            border: 1px solid #0f2862;;
            padding: 0.4em 1em;
        }

        .stButton>button:hover {
            background-color: #1e90ff;
            color: white;
        }

        /* Horizontal Lines */
        hr {
            border: 1px solid #FFFAF0;
        }
    </style>
""", unsafe_allow_html=True)



st.set_page_config(page_title="FinSight 360", layout="centered")
st.title("📊 FinSight 360: Company & Market Research Dashboard")

# Company selection
st.sidebar.header("Choose a Company")
ticker = st.sidebar.selectbox("Select a company ticker", ["TCS.NS", "INFY.NS", "RELIANCE.NS", "SBIN.NS", "HDFCBANK.NS"])

# Fetching data
company = yf.Ticker(ticker)
info = company.info

# Company Header
st.header(f"📌 Company Overview: {info.get('longName', ticker)}")
st.markdown("---")

# Display key metrics
st.subheader("📈 Key Financial Metrics")
st.write(f"**Sector:** {info.get('sector', 'N/A')}")
st.write(f"**Industry:** {info.get('industry', 'N/A')}")
st.write(f"**Market Cap:** ₹{info.get('marketCap', 0):,}")
st.write(f"**Trailing P/E Ratio:** {info.get('trailingPE', 'N/A')}")
st.write(f"**EPS:** {info.get('trailingEps', 'N/A')}")
st.write(f"**Return on Equity (ROE):** {info.get('returnOnEquity', 'N/A')}")
st.write(f"**Profit Margin:** {info.get('profitMargins', 'N/A')}")
st.markdown("---")

# Historical price data
st.subheader("📊 Stock Price - Last 6 Months")
hist = company.history(period="6mo")


st.line_chart(hist['Close'])
st.markdown("---")


st.subheader("🏆 Peer Comparison")

# Define peers
peers = ["TCS.NS", "INFY.NS", "WIPRO.NS"]

comparison = {
    "Company": [],
    "P/E Ratio": [],
    "EPS": [],
    "Market Cap (₹)": []
}

for peer in peers:
    data = yf.Ticker(peer).info
    comparison["Company"].append(data.get("shortName", peer))
    comparison["P/E Ratio"].append(data.get("trailingPE", "N/A"))
    comparison["EPS"].append(data.get("trailingEps", "N/A"))
    comparison["Market Cap (₹)"].append(data.get("marketCap", 0))

df_comparison = pd.DataFrame(comparison)
st.dataframe(df_comparison)

import requests

st.markdown("---")
st.subheader("🗞️ Latest News for the Selected Company")

api_key = "pub_fbe5271c87924d22b0b346aab0404432"  # ← Replace with your actual API key
query = info.get('shortName', ticker).split()[0]

url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={query}&country=in&language=en"

response = requests.get(url)
data = response.json()

if "results" in data:
    news_list = data["results"][:3]  # Show top 3 news articles
    for news in news_list:
        st.write(f"🔹 **{news['title']}**")
        st.caption(news.get("description", "No description available."))
        st.markdown(f"[Read more]({news['link']})")
else:
    st.warning("No news found or API limit reached.")


st.markdown("""
---
<center>
    Built with 💙 using Python & Streamlit | ©VarshaSingh 2025
</center>
""", unsafe_allow_html=True)

