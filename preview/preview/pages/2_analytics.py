import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
from streamlit_elements import elements, mui, dashboard, nivo, html
import pandas as pd
import numpy as np
np.random.seed(7)

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

# st.set_page_config(
#     layout='wide'
# )

c1, c2 = st.columns(2)

with c1:
    # df = px.data.medals_long()
    df = pd.DataFrame(
        data={
            'source': ['People'] * 3 + ['FOX'] * 3 + ['CNN'] * 3,
            'type': ['positive', 'neutral', 'negative'] * 3,
            'count': [24, 10, 9, 13, 15, 12, 11, 8, 12]
        }
    )
    # fig = px.bar(df, x='nation', y='count', color='medal', title='Medals by Country')
    fig = px.bar(df, x='source', y='count', color='type', title='Sentiment by Source')
    st.plotly_chart(fig, use_container_width=True)

with c2:
    df = px.data.tips()
    print(df)
    df = pd.DataFrame(
        data={
            'share': [300, 360, 80, 250],
            'source': ['Travis Kelce', 'Taylor Swift', 'Others', 'Kanye West'],
        }
    )
    # fig = px.pie(df, values='tip', names='day', title='Tips per Day')
    fig = px.pie(df, values='share', names='source', title='Share of Voice by Mentions')
    fig.update_traces(hoverinfo='label+percent', textinfo='value')
    st.plotly_chart(fig, use_container_width=True)

df = px.data.gapminder().query("continent == 'Oceania'")
print(df)
df = pd.DataFrame(
    data={
        'source': ['Twitter'] * 6 + ['Forums'] * 6 + ['News'] * 6 + ['Reddit'] * 6 + ['Comments'] * 6 + ['Other'] * 6,
        'date': list(pd.date_range('1/1/2024', '3/1/2024', periods=6)) * 6,
        'volume': list(np.random.randint(low=3000, high=7000, size = 6 * 5)) + list(np.random.randint(low=100, high=2000, size = 6)),
    }
)
# fig = px.line(df, x='year', y='lifeExp', color='country')
fig = px.line(df, x='date', y='volume', color='source', title='Mentions by Source')
st.plotly_chart(fig, use_container_width=True)

# with elements("dashboard"):

#     # You can create a draggable and resizable dashboard using
#     # any element available in Streamlit Elements.

#     # First, build a default layout for every element you want to include in your dashboard

#     layout = [
#         # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
#         dashboard.Item("first_item", 0, 0, 2, 2),
#         dashboard.Item("second_item", 2, 0, 2, 2),
#         dashboard.Item("third_item", 0, 2, 1, 1),
#         dashboard.Item("fourth_item", 1, 2, 3, 3),
#         dashboard.Item('fifth_item', 0, 5, 4, 3),
#     ]

#     # Next, create a dashboard layout using the 'with' syntax. It takes the layout
#     # as first parameter, plus additional properties you can find in the GitHub links below.
#     DATA = [
#             { "taste": "fruity", "chardonay": 93, "carmenere": 61, "syrah": 114 },
#             { "taste": "bitter", "chardonay": 91, "carmenere": 37, "syrah": 72 },
#             { "taste": "heavy", "chardonay": 56, "carmenere": 95, "syrah": 99 },
#             { "taste": "strong", "chardonay": 64, "carmenere": 90, "syrah": 30 },
#             { "taste": "sunny", "chardonay": 119, "carmenere": 94, "syrah": 103 },
#         ]

#     with dashboard.Grid(layout):
#         mui.Paper("First item", key="first_item")
#         mui.Paper("Second item (cannot drag)", key="second_item")
#         mui.Paper("Third item (cannot resize)", key="third_item")

#         with mui.Box(key="fourth_item"):
#             nivo.Radar(
#                 data=DATA,
#                 keys=[ "chardonay", "carmenere", "syrah" ],
#                 indexBy="taste",
#                 valueFormat=">-.2f",
#                 margin={ "top": 70, "right": 80, "bottom": 40, "left": 80 },
#                 borderColor={ "from": "color" },
#                 gridLabelOffset=36,
#                 dotSize=10,
#                 dotColor={ "theme": "background" },
#                 dotBorderWidth=2,
#                 motionConfig="wobbly",
#                 legends=[
#                     {
#                         "anchor": "top-left",
#                         "direction": "column",
#                         "translateX": -50,
#                         "translateY": -40,
#                         "itemWidth": 80,
#                         "itemHeight": 20,
#                         "itemTextColor": "#999",
#                         "symbolSize": 12,
#                         "symbolShape": "circle",
#                         "effects": [
#                             {
#                                 "on": "hover",
#                                 "style": {
#                                     "itemTextColor": "#000"
#                                 }
#                             }
#                         ]
#                     }
#                 ],
#                 # theme={
#                 #     "background": "#FFFFFF",
#                 #     "textColor": "#31333F",
#                 #     "tooltip": {
#                 #         "container": {
#                 #             "background": "#FFFFFF",
#                 #             "color": "#31333F",
#                 #         }
#                 #     }
#                 # }
#             )
    
#         # data = [
#         #     {
#         #         "id": "New Zealand",
#         #         "data": df[df['country'] == "New Zealand"][['year', 'lifeExp']].rename(columns={"year": "x", "lifeExp": "y"}).to_dict('records')
#         #     },
#         # ]

#         # print(data)
        
#         # with mui.Box(key='fifth_item'):
#         #     nivo.Line(
#         #         data=data,
#         #         yscale={
#         #             "min": 'auto',
#         #             "max": 'auto'
#         #         }
#         #     )
#         with mui.Box(key='fifth_item'):
#             components.html(fig.to_html())
