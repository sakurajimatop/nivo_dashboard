#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 12:39:30 2024

@author: sakurajima
"""
from datetime import datetime
from datetime import date
import random
import pandas as pd
from faker import Faker

fake = Faker()

# List of companies
company_names = [
    "NexaTech Manufacturing", "QuantumForge Industries", "TerraVista Fabrication", 
    "SkyHigh Engineering","UrbanEdge Machinery", "StellarWave Manufacturing", 
    "ApexFusion Works", "BlueHorizon Steel","OptiCore Fabrication", 
    "BrightMinds Machining", "GreenWave Manufacturing", "ZenithWorks Industries",
    "SwiftStream Foundry", "NovaSphere Fabrication", "InfiniteCrest Engineering",
    "PrismPeak Manufacturing","UltraNet Foundry", "EcoVista Steelworks", 
    "OmniTech Fabrication", "CrystalClear Machining","AeroNext Engineering", 
    "VitalEdge Manufacturing", "QuantumEcho Foundry", "PureWave Fabrication",
    "SummitRise Steelworks", "RapidFlow Machining", "PeakPerformance Engineering",
    "SolarFlare Fabrication","HorizonX Foundry", "Ascendia Steelworks",
    'Martin-Holden','Ward-Hays','CarterGroup','Allen,WilliamsandWhite',
    'Chandler,TurnerandHouston','Perry-Garcia','Wells-Randall','Martinez-Wilson',
    'Simmons-Turner','Mcdaniel,MooreandJackson','Bennett,VillegasandFowler',
    'MortonandSons','Walker,CruzandGarcia','Stone,WestandBurns','Klein,RobinsonandMiller',
    'HintonLLC','Waters,ReynoldsandHoward','ShortLtd','LeachGroup',
    'Harris,CrawfordandScott','Williams,GouldandLewis','GarciaGroup',
    'Ward-Wilcox','HintonGroup','ElliottLtd','Henderson,BoydandShelton',
    'Bass-Bolton','Santiago,HarrisandLynch','SmithLtd','Nolan,MeyersandJohnson'
    ]

# List of locations including Barcelona
locations = ["Barcelona", "Shanghai", "Muscat", "Buenos Aires", "Dubai",
             "New York", "Casablanca", "Riyadh", "Tokyo", "Sydney"
             , "Los Angeles", "Chicago", "Johanesburg", "Doha", "Delhi"]

# Function to determine the department based on origin and destination
def determine_department(origin, destination):
    'generamos el departamento de cada envío'
    if destination == "Barcelona":
        return random.choice(["Air Import", "Import Sea"])
    elif origin == "Barcelona":
        return random.choice(["Air Export", "Export Sea"])
    else:
        return random.choice(["Air Export", "Air Import", "Export Sea", "Import Sea"])

# Function to generate a random shipment
def generate_shipment(shipment_number):
    'general los envíos tomando en cuanta el departamento, el origen y el destino'
    customer = random.choice(company_names)
    date2 = fake.date_between(date.fromisoformat('2023-01-01'), date.fromisoformat('2024-07-25'))
    origin = random.choice(locations)
    destination = "Barcelona" if origin != "Barcelona" else random.choice([loc for loc in locations if loc != "Barcelona"])
    weight = random.randint(100, 4000)
    volume = round(random.uniform(1, 7), 2)
    cost_value = round(random.uniform(500, 10000), 2)
    markup = round(random.uniform(0.05, 0.30), 2)
    invoiced_value = round(cost_value * (1 + markup), 2)
    department = determine_department(origin, destination)
    return [shipment_number, customer, date2, origin,
            destination, weight, volume, invoiced_value,
            cost_value, markup, department]

# Generate 1200 shipments
shipments = [generate_shipment(i+1) for i in range(1200)]

# Create DataFrame
columns = ["shipment_number", "Customer", "Date", "Origin",
           "Destination", "Weight (kgs)", "Volume (cubic meters)", 
           "Invoiced Value", "Cost Value", "Markup", "Department"]
df_shipments = pd.DataFrame(shipments, columns=columns)

# Display the first few rows of the DataFrame
print(df_shipments.head())

# Save to CSV
df_shipments.to_csv('shipments.csv', index=False, sep=';')

customers = pd.DataFrame(data=company_names)

comercial = []
list = []
for i in range(10):
    list.append(fake.name())

for i in range(59):
    comercial.append(random.choice(list))

customers['sales_ex'] = comercial

customers = customers.rename(columns={0:"Customer"}, errors='raise')

df = pd.read_csv(
    "shipments.csv",
    sep=";",
    encoding="latin1",
)

result = pd.merge(df, customers, how='left', on=["Customer"])
