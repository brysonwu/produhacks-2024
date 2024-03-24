import streamlit as st

st.set_page_config(
    page_title='Home Page',
    layout='wide',
    initial_sidebar_state="auto"
)

st.write('# Welcome to PReview!')

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
    }
</style>
""",

unsafe_allow_html=True)