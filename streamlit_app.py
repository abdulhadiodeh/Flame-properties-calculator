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
def calculate_values(XH2, Flame_Thermal_Output):
    XCO = 1 - XH2

    CO2 = 1286.864286 - 19.936 * Flame_Thermal_Output - 2434.657 * XH2 + 322.986 * (XH2 ** 2)
    Total_Boundary_Heat_Flux = (2228.473786 
                          + 1.0948285385919965e-09 * (Flame_Thermal_Output ** 4)
                          + 0.002598920294605942 * (Flame_Thermal_Output ** 3)
                          - 0.0003150675147342936 * (Flame_Thermal_Output ** 2)
                          + 86.142857142853 * XH2
                          - 4354.285714285742 * (XH2 ** 2))
    Heat_Release = (8134.033965 
                    + 9.68349751426234e-09 * (Flame_Thermal_Output ** 4)
                    + 0.005923714484535841 * (Flame_Thermal_Output ** 3)
                    - 5.484696052882043e-08 * (Flame_Thermal_Output ** 2)
                    + 939.5081967213116 * XCO
                    + 3154.098360655737 * (XCO ** 2))
    NOx = (157.885714 
           + 2.3599999999986045 * Flame_Thermal_Output 
           - 284.3428571428405 * XH2 
           + 12.30769230769231 * (Flame_Thermal_Output * XH2))
    Flame_Surface_Area = (0.00168 
                          - 2.3160000000030116e-05 * Flame_Thermal_Output 
                          + 0.003953142857 * XH2 
                          - 0.003953142857 * (XH2 ** 2))
    Radiation_Heat_Flux = (1042.857143 
                           + 30.599999999995454 * Flame_Thermal_Output 
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
    ax2.plot(data['Case'], data['XH2'], color='black', marker='o', linestyle='--', label='XH₂')
    ax2.set_ylabel('XH₂')
    
    fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2, frameon=True, edgecolor='black')
    fig.tight_layout()
    
    return fig

def plot_co2(data):
    fig, ax1 = plt.subplots()
    ax1.bar(data['Case'], data['CO2'], color='orange', label='CO₂ (kg/m³)')
    ax1.set_xlabel('Flame Conditions')
    ax1.set_ylabel('CO₂ (kg/m³)')
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
    ax2.plot(data['Case'], data['XH2'], color='black', marker='o', linestyle='--', label='XH₂')
    ax2.set_ylabel('XH₂')
    
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
    ax2.plot(data['Case'], data['Flame_Thermal_Output'], color='black', marker='o', linestyle='--', label='Flame Thermal Output (kW)')
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
    ax2.plot(data['Case'], data['XH2'], color='black', marker='o', linestyle='--', label='XH₂')
    ax2.set_ylabel('XH₂')
    
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

et_cambria_font()

data = []
col1, col2 = st.columns([1, 2])

with col1:
    for i, case_label in enumerate(['Flame conditions A', 'Flame conditions B', 'Flame conditions C'], start=1):
        st.header(case_label)
        XH2 = st.number_input(f'Enter H₂ volume percentage (XH₂) for {case_label} (0.25 to 1.0):', min_value=0.25, max_value=1.0, step=0.01, key=f'XH2_{i}')
        Flame_Thermal_Output = st.number_input(f'Enter Flame Thermal Output (kW) for {case_label} (15 to 25):', min_value=15, max_value=25, step=0.1, key=f'Flame_Thermal_Output_{i}')
        
        if st.button(f'Calculate {case_label}', key=f'button_{i}'):
            results = calculate_values(XH2, Flame_Thermal_Output)
            data.append([case_label, *results, Flame_Thermal_Output, XH2])
            st.write(f"CO₂: {results[0]:.2f} kg/m³")
            st.write(f"Total Boundary Heat Flux: {results[1]:.2f} W/m²")
            st.write(f"Heat Release: {results[2]:.2f} W")
            st.write(f"NOₓ: {results[3]:.2f} kg/m³")
            st.write(f"Flame Surface Area: {results[4]:.6f} m²")
            st.write(f"Radiation Heat Flux: {results[5]:.2f} W/m²")
            st.write(f"Flame Temperature: {results[7]:.2f} K")

with col2:
    if data:
        df = pd.DataFrame(data, columns=['Case', 'CO2', 'Total_Boundary_Heat_Flux', 'Heat_Release', 'NOx', 'Flame_Surface_Area', 'Radiation_Heat_Flux', 'XCO', 'Flame_Temperature', 'Flame_Thermal_Output', 'XH2'])

        st.subheader('Comparison Charts')

        st.pyplot(plot_nox(df))
        st.pyplot(plot_co2(df))
        st.pyplot(plot_flame_surface_area(df))
        st.pyplot(plot_heat_release(df))
        st.pyplot(plot_heat_flux(df))
        st.pyplot(plot_temperature(df))