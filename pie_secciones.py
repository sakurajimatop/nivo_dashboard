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


# por mejorar

# el color de las letras de los ejes no se ve en el dark mode
# el color de las letras del pie chart no se ve en el light mode
# agregar dos gráficos interesantes más:
    # algún mapa
    # average profit shipment
    


st.set_page_config(layout="wide")
# As for Streamlit Elements, we will need all these objects.
# All available objects and there usage are listed there: https://github.com/okld/streamlit-elements#getting-started
bump_chart_data = [{'id': 'Brady Wells',
  'data': [{'x': 202301, 'y': 5299},
   {'x': 202302, 'y': 7162},
   {'x': 202303, 'y': 6116},
   {'x': 202304, 'y': 7011},
   {'x': 202305, 'y': 5952},
   {'x': 202306, 'y': 7404},
   {'x': 202307, 'y': 3455},
   {'x': 202308, 'y': 858},
   {'x': 202309, 'y': 4728},
   {'x': 202310, 'y': 6755},
   {'x': 202311, 'y': 2720},
   {'x': 202312, 'y': 10626},
   {'x': 202401, 'y': 8691},
   {'x': 202402, 'y': 7834},
   {'x': 202403, 'y': 17607},
   {'x': 202404, 'y': 726},
   {'x': 202405, 'y': 1541},
   {'x': 202406, 'y': 11052},
   {'x': 202407, 'y': 3983}]},
 {'id': 'Brenda Koch',
  'data': [{'x': 202301, 'y': 11494},
   {'x': 202302, 'y': 14208},
   {'x': 202303, 'y': 10888},
   {'x': 202304, 'y': 7606},
   {'x': 202305, 'y': 17404},
   {'x': 202306, 'y': 4293},
   {'x': 202307, 'y': 8382},
   {'x': 202308, 'y': 9933},
   {'x': 202309, 'y': 2721},
   {'x': 202310, 'y': 6810},
   {'x': 202311, 'y': 7030},
   {'x': 202312, 'y': 239},
   {'x': 202401, 'y': 15497},
   {'x': 202402, 'y': 2300},
   {'x': 202403, 'y': 6061},
   {'x': 202404, 'y': 7650},
   {'x': 202405, 'y': 9678},
   {'x': 202406, 'y': 13739},
   {'x': 202407, 'y': 7649}]},
 {'id': 'Joseph Jordan',
  'data': [{'x': 202301, 'y': 6349},
   {'x': 202302, 'y': 13921},
   {'x': 202303, 'y': 5442},
   {'x': 202304, 'y': 8214},
   {'x': 202305, 'y': 4063},
   {'x': 202306, 'y': 9016},
   {'x': 202307, 'y': 12266},
   {'x': 202308, 'y': 7591},
   {'x': 202309, 'y': 13267},
   {'x': 202310, 'y': 10149},
   {'x': 202311, 'y': 9351},
   {'x': 202312, 'y': 18681},
   {'x': 202401, 'y': 13216},
   {'x': 202402, 'y': 8435},
   {'x': 202403, 'y': 7942},
   {'x': 202404, 'y': 11473},
   {'x': 202405, 'y': 10099},
   {'x': 202406, 'y': 6740},
   {'x': 202407, 'y': 6088}]},
 {'id': 'Michael Scott DDS',
  'data': [{'x': 202301, 'y': 3120},
   {'x': 202302, 'y': 9619},
   {'x': 202303, 'y': 5676},
   {'x': 202304, 'y': 9083},
   {'x': 202305, 'y': 13643},
   {'x': 202306, 'y': 7696},
   {'x': 202307, 'y': 4126},
   {'x': 202308, 'y': 9561},
   {'x': 202309, 'y': 9127},
   {'x': 202310, 'y': 9405},
   {'x': 202311, 'y': 10991},
   {'x': 202312, 'y': 9630},
   {'x': 202401, 'y': 7145},
   {'x': 202402, 'y': 6995},
   {'x': 202403, 'y': 14038},
   {'x': 202404, 'y': 10980},
   {'x': 202405, 'y': 10584},
   {'x': 202406, 'y': 6134},
   {'x': 202407, 'y': 9658}]},
 {'id': 'Ryan Camacho',
  'data': [{'x': 202301, 'y': 20177},
   {'x': 202302, 'y': 15668},
   {'x': 202303, 'y': 17488},
   {'x': 202304, 'y': 19733},
   {'x': 202305, 'y': 22956},
   {'x': 202306, 'y': 13376},
   {'x': 202307, 'y': 15505},
   {'x': 202308, 'y': 13693},
   {'x': 202309, 'y': 16203},
   {'x': 202310, 'y': 17262},
   {'x': 202311, 'y': 23867},
   {'x': 202312, 'y': 13005},
   {'x': 202401, 'y': 10696},
   {'x': 202402, 'y': 12044},
   {'x': 202403, 'y': 22262},
   {'x': 202404, 'y': 16247},
   {'x': 202405, 'y': 18864},
   {'x': 202406, 'y': 15475},
   {'x': 202407, 'y': 11695}]}]


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
                    arcLinkLabelsTextColor="#141414",
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
        with mui.Card(key="media", sx={"display": "flex", "flexDirection": "column"}):

            # To make this header draggable, we just need to set its classname to 'draggable',
            # as defined above in dashboard.Grid's draggableHandle.

            mui.CardHeader(title="Sales Executive ranking evolution", className="draggable")

            # Like above, we want to make our content grow and shrink as the user resizes the card,
            # by setting flex to 1 and minHeight to 0.

            with mui.CardContent(sx={"flex": 1, "minHeight": 600}):
                with mui.Box(sx={"height": 500}):
                    nivo.AreaBump(
                        data=bump_chart_data,
                        margin={"top": 40, "right": 100, "bottom": 40, "left": 100},
                        spacing=8,
                        colors={"scheme": "nivo"},
                        blendMode="multiply",
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
                            {"match": {"id": "CoffeeScript"}, "id": "dots"},
                            {"match": {"id": "TypeScript"}, "id": "lines"}
                        ],
                        startLabel="id",
                        endLabel="id",
                        axisTop={
                            "tickSize": 5,
                            "tickPadding": 5,
                            "tickRotation": 0,
                            "legend": "",
                            "legendPosition": "middle",
                            "legendOffset": -36,
                            "truncateTickAt": 0
                        },
                        axisBottom={
                            "tickSize": 5,
                            "tickPadding": 5,
                            "tickRotation": 0,
                            "legend": "",
                            "legendPosition": "middle",
                            "legendOffset": 32,
                            "truncateTickAt": 0
                        }
                    )