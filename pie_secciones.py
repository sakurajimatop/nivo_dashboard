#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 15:08:00 2024

@author: sakurajima
"""
from pathlib import Path
import json
import pandas as pd
from streamlit_elements import elements, dashboard, mui, nivo
import streamlit as st

st.set_page_config(layout="wide")
# As for Streamlit Elements, we will need all these objects.
# All available objects and there usage are listed there: https://github.com/okld/streamlit-elements#getting-started
# data_chart = [
#     {'month': 'Jan', '2023': 67481.0911, '2024': 90932.1748},
#     {'month': 'Feb', '2023': 81507.061, '2024': 61093.6023},
#     {'month': 'Mar', '2023': 58702.8501, '2024': 98382.9113},
#     {'month': 'Apr', '2023': 62765.6294, '2024': 59867.3839},
#     {'month': 'May', '2023': 87234.2837, '2024': 72091.0803},
#     {'month': 'Jun', '2023': 56460.1538, '2024': 71122.3589},
#     {'month': 'Jul', '2023': 60003.0174, '2024': 52803.1782},
#     {'month': 'Aug', '2023': 65351.9784, '2024': None},  # Assuming no data for 2024
#     {'month': 'Sep', '2023': 61903.8176, '2024': None},  # Assuming no data for 2024
#     {'month': 'Oct', '2023': 68346.8672, '2024': None},  # Assuming no data for 2024
#     {'month': 'Nov', '2023': 74664.7885, '2024': None},  # Assuming no data for 2024
#     {'month': 'Dec', '2023': 81740.1852, '2024': None},  # Assuming no data for 2024
# ]

df = pd.read_csv(
    "shipments.csv",
    sep=";",
    encoding="latin1",decimal="."
)
df["Date"] = pd.to_datetime(df["Date"], yearfirst=True)

df['year'] = df['Date'].dt.year
df['month'] = df['Date'].dt.month
# df.columns


df["Gross Margin"] = df["Invoiced Value"] * df["Markup"]
margen_operativo = int(df['Gross Margin'].sum())
# margen_operativo
# df.columns


margin_dpto = df[['Gross Margin','Department']].groupby(['Department']).sum().reset_index()
#nivo usa id y value para cargar los datos en el gráfico
margin_dpto.rename(columns={'Department':'id', 'Gross Margin':'value'}, inplace=True)
#convertimos el df en un listado de diccionarios, es la estructura que necesita nivo
margin_dpto_dict = margin_dpto.to_dict(orient='records')


bar_chart_data=df.groupby(['year', 'month'])['Gross Margin'].sum().reset_index()
bar_chart_data = bar_chart_data.to_dict(orient='records')
# Change page layout to make the dashboard take the whole page.
month_mapping = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

# Initialize the result dictionary with all months
result = [{'month': month, '2023': None, '2024': None} for month in month_mapping.values()]

# Fill the result dictionary with data
for entry in bar_chart_data:
    month_name = month_mapping[entry['month']]
    year = str(entry['year'])
    gross_margin = entry['Gross Margin']
    
    # Find the corresponding month in the result list and update the year value
    for item in result:
        if item['month'] == month_name:
            item[year] = gross_margin


df_margin = df[['Gross Margin', ]]



# Initialize default data for code editor and chart.
#
# For this tutorial, we will need data for a Nivo Bump chart.
# You can get random data there, in tab 'data': https://nivo.rocks/bump/
#
# As you will see below, this session state item will be updated when our
# code editor change, and it will be read by Nivo Bump chart to draw the data.

if "data" not in st.session_state:
    with open("data.json", "r", encoding="utf-8") as file:
        st.session_state.data = Path("data.json").read_text()

# Define a default dashboard layout.
# Dashboard grid has 12 columns by default.
#
# For more information on available parameters:
# https://github.com/react-grid-layout/react-grid-layout#grid-item-props

layout = [
    # Editor item is positioned in coordinates x=0 and y=0, and takes 6/12 columns and has a height of 3.
    dashboard.Item("editor", 0, 0, 6, 3),
    # Chart item is positioned in coordinates x=6 and y=0, and takes 6/12 columns and has a height of 3.
    dashboard.Item("chart", 6, 0, 6, 3),
    # Media item is positioned in coordinates x=0 and y=3, and takes 6/12 columns and has a height of 4.
    dashboard.Item("media", 0, 2, 12, 4),
]

# Create a frame to display elements.

with elements("demo"):

    # Create a new dashboard with the layout specified above.
    #
    # draggableHandle is a CSS query selector to define the draggable part of each dashboard item.
    # Here, elements with a 'draggable' class name will be draggable.
    #
    # For more information on available parameters for dashboard grid:
    # https://github.com/react-grid-layout/react-grid-layout#grid-layout-props
    # https://github.com/react-grid-layout/react-grid-layout#responsive-grid-layout-props

    with dashboard.Grid(layout, draggableHandle=".draggable"):

        # First card, the code editor.
        #
        # We use the 'key' parameter to identify the correct dashboard item.
        #
        # To make card's content automatically fill the height available, we will use CSS flexbox.
        # sx is a parameter available with every Material UI widget to define CSS attributes.
        #
        # For more information regarding Card, flexbox and sx:
        # https://mui.com/components/cards/
        # https://mui.com/system/flexbox/
        # https://mui.com/system/the-sx-prop/


        # Second card, the Nivo Bump chart.
        # We will use the same flexbox configuration as the first card to auto adjust the content height.

        with mui.Card(key="chart", sx={"display": "flex", "flexDirection": "column"}):

            # To make this header draggable, we just need to set its classname to 'draggable',
            # as defined above in dashboard.Grid's draggableHandle.

            mui.CardHeader(title="Department Gross Margin", className="draggable")

            # Like above, we want to make our content grow and shrink as the user resizes the card,
            # by setting flex to 1 and minHeight to 0.

            with mui.CardContent(sx={"flex": 1, "minHeight": 0}):

                # This is where we will draw our Bump chart.
                #
                # For this exercise, we can just adapt Nivo's example and make it work with Streamlit Elements.
                # Nivo's example is available in the 'code' tab there: https://nivo.rocks/bump/
                #
                # Data takes a dictionary as parameter, so we need to convert our JSON data from a string to
                # a Python dictionary first, with `json.loads()`.
                #
                # For more information regarding other available Nivo charts:
                # https://nivo.rocks/

                nivo.Pie(
                    data=margin_dpto_dict,
                    margin={"top": 40, "right": 80, "bottom": 80, "left": 80},
                    innerRadius=0.5,
                    padAngle=0.7,
                    cornerRadius=3,
                    activeOuterRadiusOffset=8,
                    borderWidth=1,
                    borderColor={"from": "color", "modifiers": [["darker", 0.2]]},
                    arcLinkLabelsSkipAngle=10,
                    arcLinkLabelsTextColor="#FFFFFF",
                    arcLinkLabelsThickness=2,
                    arcLinkLabelsColor={"from": "color"},
                    arcLabelsSkipAngle=10,
                    arcLabelsTextColor={"from": "color", "modifiers": [["darker", 2]]},
                    defs=[
                        {
                            "id": "dots",
                            "type": "patternDots",
                            "background": "inherit",
                            "color": "rgba(255, 255, 255, 0.3)",
                            "size": 4,
                            "padding": 1,
                            "stagger": True
                        },
                        {
                            "id": "lines",
                            "type": "patternLines",
                            "background": "inherit",
                            "color": "rgba(255, 255, 255, 0.3)",
                            "rotation": -45,
                            "lineWidth": 6,
                            "spacing": 10
                        }
                    ],
                    fill=[
                        {"match": {"id": "ruby"}, "id": "dots"},
                        {"match": {"id": "c"}, "id": "dots"},
                        {"match": {"id": "go"}, "id": "dots"},
                        {"match": {"id": "python"}, "id": "dots"},
                        {"match": {"id": "scala"}, "id": "lines"},
                        {"match": {"id": "lisp"}, "id": "lines"},
                        {"match": {"id": "elixir"}, "id": "lines"},
                        {"match": {"id": "javascript"}, "id": "lines"},
                    ],
                    legends=[
                        {
                            "anchor": "bottom",
                            "direction": "row",
                            "justify": False,
                            "translateX": 0,
                            "translateY": 56,
                            "itemsSpacing": 0,
                            "itemWidth": 100,
                            "itemHeight": 18,
                            "itemTextColor": "#999",
                            "itemDirection": "left-to-right",
                            "itemOpacity": 1,
                            "symbolSize": 18,
                            "symbolShape": "circle",
                            "effects": [
                                {
                                    "on": "hover",
                                    "style": {
                                        "itemTextColor": "#000"
                                    }
                                }
                            ]
                        }
                    ]
                )
        with mui.Card(key="editor", sx={"display": "flex", "flexDirection": "column"}):

            # To make this header draggable, we just need to set its classname to 'draggable',
            # as defined above in dashboard.Grid's draggableHandle.

            mui.CardHeader(title="Gross Margin", className="draggable")

            # Like above, we want to make our content grow and shrink as the user resizes the card,
            # by setting flex to 1 and minHeight to 0.

            with mui.CardContent(sx={"flex": 1, "minHeight": 0}):

                # This is where we will draw our Bump chart.
                #
                # For this exercise, we can just adapt Nivo's example and make it work with Streamlit Elements.
                # Nivo's example is available in the 'code' tab there: https://nivo.rocks/bump/
                #
                # Data takes a dictionary as parameter, so we need to convert our JSON data from a string to
                # a Python dictionary first, with `json.loads()`.
                #
                # For more information regarding other available Nivo charts:
                # https://nivo.rocks/

                nivo.Bar(
                            data=result,
                            keys=['2023','2024'],
                            indexBy='month',
                            margin={"top": 50, "right": 130, "bottom": 50, "left": 60},
                            padding=0.3,
                            groupMode="grouped",
                            valueScale={"type": "linear"},
                            indexScale={"type": "band", "round": True},
                            valueFormat=" >+$,~r",
                            colors={"scheme": "nivo"},
                            defs=[
                                {
                                    "id": "dots",
                                    "type": "patternDots",
                                    "background": "inherit",
                                    "color": "#38bcb2",
                                    "size": 4,
                                    "padding": 1,
                                    "stagger": True
                                },
                                {
                                    "id": "lines",
                                    "type": "patternLines",
                                    "background": "inherit",
                                    "color": "#eed312",
                                    "rotation": -45,
                                    "lineWidth": 6,
                                    "spacing": 10
                                }
                            ],
                            fill=[
                                {"match": {"id": "fries"}, "id": "dots"},
                                {"match": {"id": "sandwich"}, "id": "lines"},
                            ],
                            borderColor={
                                "from": "color",
                                "modifiers": [["darker", 1.6]]
                            },
                            axisTop=None,
                            axisRight=None,
                            axisBottom={
                                "tickSize": 5,
                                "tickPadding": 5,
                                "tickRotation": 0,
                                "legend": "",
                                "legendPosition": "middle",
                                "legendOffset": 32,
                                "truncateTickAt": 0
                            },
                            axisLeft={
                                "tickSize": 5,
                                "tickPadding": 5,
                                "tickRotation": 0,
                                "legend": "Gross Margin",
                                "legendPosition": "middle",
                                "legendOffset": -52,
                                "truncateTickAt": 0
                            },
                            enableLabel= False,
                            labelSkipWidth=12,
                            labelSkipHeight=12,
                            labelTextColor="#ffffff",
                            legends=[
                                {
                                    "dataFrom": "keys",
                                    "anchor": "bottom-right",
                                    "direction": "column",
                                    "justify": False,
                                    "translateX": 120,
                                    "translateY": 0,
                                    "itemsSpacing": 2,
                                    "itemWidth": 100,
                                    "itemHeight": 20,
                                    "itemTextColor": "#999",
                                    "itemDirection": "left-to-right",
                                    "itemOpacity": 0.85,
                                    "symbolSize": 20,
                                    "effects": [
                                        {
                                            "on": "hover",
                                            "style": {
                                                "itemOpacity": 1
                                            }
                                        }
                                    ]
                                }
                            ],
                            role="application",
                            ariaLabel="Nivo bar chart demo",
                            barAriaLabel=lambda e: f"{e['id']}: {e['formattedValue']} in country: {e['indexValue']}"
                        )
