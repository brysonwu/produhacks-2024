import streamlit as st
import uuid
import numpy as np
import pandas as pd
from datetime import datetime
from streamlit_lchart_card import streamlit_lchart_card

st.set_page_config(
    page_title='Home Page',
    layout='wide',
    initial_sidebar_state="auto"
)

with open( "preview/Style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    
st.markdown("""
<style>
	[data-testid="stDecoration"] {
		background-image: linear-gradient(90deg, #2D388A, #00AEEF);
	}
    [data-testid="stHeader"] {
		background-image: linear-gradient(90deg, #2D388A, #00AEEF);
	}
    [data-testid="stSidebar"] {
        background-image: linear-gradient(#2D388A, #00AEEF) !important;
        min-width: 10px !important;
        width: 130px !important;
    }
</style>
""",

unsafe_allow_html=True)

# def home():
#     st.write("Welcome to home page")
#     if st.button("Click Home"):
#         st.write("Welcome to home page")

# # call app class object
# app = MultiPage()
# # Add pages
# app.add_page("Home",home)
# app.add_page("About",about)
# app.add_page("Contact",contact)
# app.run()

st.title("GOOD MORNING, TREE")
st.header("Key Insights")

t = pd.date_range(start=datetime(year=2024, month=1, day=1, hour=0, minute=0),
                  end=datetime(year=2024, month=3, day=24, hour=0, minute=0), freq="48h")

nb_samples = len(t)
m_temp = 20.4
m_pH = 6.79
m_nitrate = 100.3
m_ammonia = 2.9

temps = [round(m, 1) for m in np.random.normal(m_temp, 2, nb_samples)]
pHs = [round(m, 2) for m in np.random.normal(m_pH, 1, nb_samples)]
nitrates = [round(m, 2) for m in np.random.normal(m_nitrate, 20, nb_samples)]
ammonias = [round(m, 2) for m in np.random.normal(m_ammonia, 0.1, nb_samples)]

df_temps = pd.DataFrame({"date": t, "measure": temps})
df_pHs = pd.DataFrame({"date": t, "measure": pHs})
df_nitrates = pd.DataFrame({"date": t, "measure": nitrates})
df_ammonias = pd.DataFrame({"date": t, "measure": ammonias})

multiple_graphs = st.columns(3)
with multiple_graphs[0]:
    streamlit_lchart_card(title="Sentiment Shift", df=df_temps, x="date", y="measure",
                          labels={"measure": "", "date": "Date"}, defaultColor="rgb(255, 180, 15)", thresh=20,
                          threshColor="rgb(255, 90, 132)", rounding=1, format="%d/%m %Hh",
                          key="streamlit_temp_lchart_card")
with multiple_graphs[1]:
    streamlit_lchart_card(title="Change of Mentions", df=df_nitrates, x="date", y="measure",
                          labels={"measure": "", "date": "Date"}, defaultColor="rgb(132, 99, 255)", thresh=95.2,
                          rounding=2, key="streamlit_nitrate_lchart_card")
with multiple_graphs[2]:
    streamlit_lchart_card(title="Change in Instagram Followers", df=df_pHs, x="date", y="measure",
                          labels={"measure": "", "date": "Date"}, defaultColor="rgb(99, 255, 132)", thresh=6,
                          rounding=2, key="streamlit_pH_lchart_card")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Echo: {prompt}"
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})