import plotly.express as px
import streamlit as st

st.set_page_config(
    layout='wide'
)

c1, c2 = st.columns(2)

with c1:
    df = px.data.medals_long()
    fig = px.bar(df, x='nation', y='count', color='medal', title='Medals by Country')
    st.plotly_chart(fig, use_container_width=True)

with c2:
    df = px.data.tips()
    fig = px.pie(df, values='tip', names='day', title='Tips per Day')
    fig.update_traces(hoverinfo='label+percent', textinfo='value')
    st.plotly_chart(fig, use_container_width=True)

df = px.data.gapminder().query("continent == 'Oceania'")
fig = px.line(df, x='year', y='lifeExp', color='country')
st.plotly_chart(fig, use_container_width=True)
