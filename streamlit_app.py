import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set font and style
def set_cambria_font():
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = 'Cambria Math'
    plt.rcParams['axes.edgecolor'] = 'black'
    plt.rcParams['axes.linewidth'] = 2

# Calculation functions
def calculate_values(XH2, Power):
    XCO = 1 - XH2

    CO2 = 1286.864286 - 19.936 * Power - 2434.657 * XH2 + 322.986 * (XH2 ** 2)
    Total_Boundary_Heat_Flux = (2228.473786 
                          + 1.0948285385919965e-09 * (Power ** 4)
                          + 0.002598920294605942 * (Power ** 3)
                          - 0.0003150675147342936 * (Power ** 2)
                          + 86.142857142853 * XH2
                          - 4354.285714285742 * (XH2 ** 2))
    Heat_Release = (8134.033965 
                    + 9.68349751426234e-09 * (Power ** 4)
                    + 0.005923714484535841 * (Power ** 3)
                    - 5.484696052882043e-08 * (Power ** 2)
                    + 939.5081967213116 * XCO
                    + 3154.098360655737 * (XCO ** 2))
    NOx = (157.885714 
           + 2.3599999999986045 * Power 
           - 284.3428571428405 * XH2 
           + 12.30769230769231 * (Power * XH2))
    Flame_Surface_Area = (0.00168 
                          - 2.3160000000030116e-05 * Power 
                          + 0.003953142857 * XH2 
                          - 0.003953142857 * (XH2 ** 2))
    Radiation_Heat_Flux = (1042.857143 
                           + 30.599999999995454 * Power 
                           - 2411.428571428527 * XH2 
                           + 322.9857142857029 * (XH2 ** 2))
    Flame_Temperature = 2160.0 + 152.0 * XH2

    return CO2, Total_Boundary_Heat_Flux, Heat_Release, NOx, Flame_Surface_Area, Radiation_Heat_Flux, XCO, Flame_Temperature

# Plot functions
def plot_nox(data):
    fig, ax1 = plt.subplots()
    ax1.bar(data['Case'], data['NOx'], color='red', label='NOx (kg/m³)')
    ax1.set_xlabel('Flame Conditions')
    ax1.set_ylabel('NOx (kg/m³)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, linestyle='--', linewidth=0.5)
    
    ax2 = ax1.twinx()
    ax2.plot(data['Case'], data['XH2'], color='black', marker='o', linestyle='--', label='XH2')
    ax2.set_ylabel('XH2')
    
    fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2, frameon=True, edgecolor='black')
    fig.tight_layout()
    
    return fig

def plot_co2(data):
    fig, ax1 = plt.subplots()
    ax1.bar(data['Case'], data['CO2'], color='orange', label='CO2 (kg/m³)')
    ax1.set_xlabel('Flame Conditions')
    ax1.set_ylabel('CO2 (kg/m³)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, linestyle='--', linewidth=0.5)
    
    ax2 = ax1.twinx()
    ax2.plot(data['Case'], data['XCO'], color='black', marker='o', linestyle='--', label='XCO')
    ax2.set_ylabel('XCO')
    
    fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2, frameon=True, edgecolor='black')
    fig.tight_layout()
    
    return fig

def plot_flame_surface_area(data):
    fig, ax1 = plt.subplots()
    ax1.bar(data['Case'], data['Flame_Surface_Area'], color='blue', label='Flame Surface Area (m²)')
    ax1.set_xlabel('Flame Conditions')
    ax1.set_ylabel('Flame Surface Area (m²)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, linestyle='--', linewidth=0.5)
    
    ax2 = ax1.twinx()
    ax2.plot(data['Case'], data['XH2'], color='black', marker='o', linestyle='--', label='XH2')
    ax2.set_ylabel('XH2')
    
    fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2, frameon=True, edgecolor='black')
    fig.tight_layout()
    
    return fig

def plot_heat_release(data):
    fig, ax1 = plt.subplots()
    ax1.bar(data['Case'], data['Heat_Release'], color='purple', label='Heat Release (W)')
    ax1.set_xlabel('Flame Conditions')
    ax1.set_ylabel('Heat Release (W)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, linestyle='--', linewidth=0.5)
    
    ax2 = ax1.twinx()
    ax2.plot(data['Case'], data['Power'], color='black', marker='o', linestyle='--', label='Flame Thermal Output (kW)')
    ax2.set_ylabel('Flame Thermal Output (kW)')
    
    fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2, frameon=True, edgecolor='black')
    fig.tight_layout()
    
    return fig

def plot_heat_flux(data):
    fig, ax1 = plt.subplots()
    ax1.bar(data['Case'], data['Total_Boundary_Heat_Flux'], color='darkgrey', label='Total Boundary Heat Flux (W/m²)')
    ax1.bar(data['Case'], data['Radiation_Heat_Flux'], color='lightcoral', label='Radiation Heat Flux (W/m²)', bottom=data['Total_Boundary_Heat_Flux'])
    ax1.set_xlabel('Flame Conditions')
    ax1.set_ylabel('Heat Flux (W/m²)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, linestyle='--', linewidth=0.5)
    
    fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2, frameon=True, edgecolor='black')
    fig.tight_layout()
    
    return fig

def plot_temperature(data):
    fig, ax1 = plt.subplots()
    ax1.bar(data['Case'], data['Flame_Temperature'], color='red', edgecolor='black', linestyle='--', label='Flame Temperature (K)')
    ax1.set_xlabel('Flame Conditions')
    ax1.set_ylabel('Flame Temperature (K)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, linestyle='--', linewidth=0.5)
    
    ax2 = ax1.twinx()
    ax2.plot(data['Case'], data['XH2'], color='black', marker='o', linestyle='--', label='XH2')
    ax2.set_ylabel('XH2')
    
    fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2, frameon=True, edgecolor='black')
    fig.tight_layout()
    
    return fig

# Streamlit app layout
st.title('Combustion Parameter Calculator')

st.write("This is a calculator tool for educational purposes based on Sandia ChnA burner for turbulent diffusion ideal gas (H₂/CO) lean mixture flames with constant stoichiometry (25% excess air), the equations are based on machine learning optimisation and well established CFD numerical models. For any enquiries about this calculation tool, kindly contact abdulhadiodeh@gmail.com")

# Center the image
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.write("")
with col2:
    st.image('burner.jpg', caption='Sandia chnA Burner')
with col3:
    st.write("")

set_cambria_font()

data = []
col1, col2 = st.columns([1, 2])

with col1:
    for i, case_label in enumerate(['Flame conditions A', 'Flame conditions B', 'Flame conditions C'], start=1):
        st.header(f'{case_label}')
        XH2 = st.number_input(f'Enter H₂ volume percentage (XH₂) for {case_label} (0.25 to 1.0):
