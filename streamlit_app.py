import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# Function to calculate values based on provided equations
def calculate_combustion_parameters(Flame_Thermal_Output, XH2):
    XCO = 1 - XH2
    
    CO2 = (
        8.3365e4 + (-33.776 * Flame_Thermal_Output) + (-1.1729e6 * XCO)
        + (-661.08 * (Flame_Thermal_Output ** 2)) + (1.5680e5 * (Flame_Thermal_Output * XCO))
        + (-3.7333e6 * (XCO ** 2)) + (21.418 * (Flame_Thermal_Output ** 3))
        + (-3.6640e3 * ((Flame_Thermal_Output ** 2) * XCO)) + (2.4320e5 * (Flame_Thermal_Output * (XCO ** 2)))
        + (5.0489e6 * (XCO ** 3))
    )
    
    Flame_Surface_Area = (
        -1.3920e-3 + (8.4829e-8 * Flame_Thermal_Output) + (1.6181e-2 * XH2)
        + (1.6612e-6 * (Flame_Thermal_Output ** 2)) + (-2.1212e-4 * (Flame_Thermal_Output * XH2))
        + (-2.9621e-2 * (XH2 ** 2)) + (-2.3533e-9 * (Flame_Thermal_Output ** 3))
        + (-3.5040e-6 * ((Flame_Thermal_Output ** 2) * XH2)) + (3.8160e-4 * (Flame_Thermal_Output * (XH2 ** 2)))
        + (1.6647e-2 * (XH2 ** 3))
    )
    
    Heat_Release = (
        -355.79 + (873.96 * Flame_Thermal_Output) + (784.75 * XCO)
        + (0.1495 * (Flame_Thermal_Output ** 2)) + (81.22 * (Flame_Thermal_Output * XCO))
        + (-0.0243 * (Flame_Thermal_Output ** 3)) + (2.1239 * ((Flame_Thermal_Output ** 2) * XCO))
        + (-22.75 * (Flame_Thermal_Output * (XCO ** 2))) + (277.48 * (XCO ** 3))
    )
    
    Total_Boundary_Heat_Flux = (
        1181.0 + (0.8963 * Flame_Thermal_Output) + (91.556 * XH2)
        + (17.548 * (Flame_Thermal_Output ** 2)) + (-9.800 * (Flame_Thermal_Output * XH2))
        + (-0.2241 * (Flame_Thermal_Output ** 3)) + (-0.72 * ((Flame_Thermal_Output ** 2) * XH2))
        + (-100.0 * (Flame_Thermal_Output * (XH2 ** 2))) + (1031.1 * (XH2 ** 3))
    )
    
    Radiation_Heat_Flux = (
        -253.33 + (0.1829 * Flame_Thermal_Output) + (8411.1 * XH2)
        + (3.5800 * (Flame_Thermal_Output ** 2)) + (-234.0 * (Flame_Thermal_Output * XH2))
        + (-12667.0 * (XH2 ** 2)) + (-0.0713 * (Flame_Thermal_Output ** 3))
        + (-0.64 * ((Flame_Thermal_Output ** 2) * XH2)) + (360.0 * (Flame_Thermal_Output * (XH2 ** 2)))
        + (4835.6 * (XH2 ** 3))
    )
    
    NOx = (
        99.41 + (2.3945e-3 * Flame_Thermal_Output) + (194.78 * XH2)
        + (4.6899e-2 * (Flame_Thermal_Output ** 2)) + (2.992 * (Flame_Thermal_Output * XH2))
        + (-728.0 * (XH2 ** 2)) + (3.8502e-4 * (Flame_Thermal_Output ** 3))
        + (-0.1792 * ((Flame_Thermal_Output ** 2) * XH2)) + (-0.64 * (Flame_Thermal_Output * (XH2 ** 2)))
        + (630.04 * (XH2 ** 3))
    )
    
    Flame_Temperature = 2160.0 + 152.0 * XH2
    
    return CO2, Total_Boundary_Heat_Flux, Heat_Release, NOx, Flame_Surface_Area, Radiation_Heat_Flux, XCO, Flame_Temperature

# Plot functions with updated styles
def plot_nox(data):
    fig, ax1 = plt.subplots(facecolor='#f0f0f0', edgecolor='black', linewidth=2)
    ax1.bar(data['Case'], data['NOx'], color='red', edgecolor='black', label='NOx (kg/m³)', width=0.35)
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
    fig, ax1 = plt.subplots(facecolor='#f0f0f0', edgecolor='black', linewidth=2)
    ax1.bar(data['Case'], data['CO2'], color='orange', edgecolor='black', label='CO₂ (kg/m³)', width=0.35)
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
    fig, ax1 = plt.subplots(facecolor='#f0f0f0', edgecolor='black', linewidth=2)
    ax1.bar(data['Case'], data['Flame_Surface_Area'], color='blue', edgecolor='black', label='Flame Surface Area (m²)', width=0.35)
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
    fig, ax1 = plt.subplots(facecolor='#f0f0f0', edgecolor='black', linewidth=2)
    ax1.bar(data['Case'], data['Heat_Release'], color='purple', edgecolor='black', label='Heat Release (W)', width=0.35)
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
    fig, ax1 = plt.subplots(facecolor='#f0f0f0', edgecolor='black', linewidth=2)
    ax1.bar(data['Case'], data['Radiation_Heat_Flux'], color='lightcoral', edgecolor='black', label='Radiation Heat Flux (W/m²)', width=0.35)
    ax1.bar(data['Case'], data['Total_Boundary_Heat_Flux'] - data['Radiation_Heat_Flux'], color='darkgrey', edgecolor='black', label='Total Boundary Heat Flux (W/m²)', bottom=data['Radiation_Heat_Flux'], width=0.35)
    ax1.set_ylabel('Heat Flux (W/m²)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, linestyle='--', linewidth=0.5)
    
    fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2, frameon=True, edgecolor='black')
    fig.tight_layout()
    
    return fig

def plot_temperature(data):
    fig, ax1 = plt.subplots(facecolor='#f0f0f0', edgecolor='black', linewidth=2)
    ax1.bar(data['Case'], data['Flame_Temperature'], color='red', edgecolor='black', label='Flame Temperature (K)', width=0.35)
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

st.write("""
This is a calculator tool for educational purposes based on Sandia ChnA burner for turbulent diffusion ideal gas (H₂/CO) lean mixture flames with constant stoichiometry (25% excess air), 
the equations are based on machine learning optimisation and well-established CFD numerical models. 
For any enquiries about this calculation tool, kindly contact abdulhadiodeh@gmail.com.
""")

# Center the image
st.markdown("<h2 style='text-align: center;'>Sandia ChnA Burner</h2>", unsafe_allow_html=True)
image = Image.open('burner.jpg')
rotated_image = image.rotate(-90, expand=True)
st.image(rotated_image, caption='Sandia ChnA Burner')

# Placeholder function for setting font style
def set_cambria_font():
    st.markdown(
        """
        <style>
        .streamlit-container {
            font-family: 'Cambria', serif;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

set_cambria_font()

data = []
st.header('Flame Conditions Input')
for i, case_label in enumerate(['Flame conditions A', 'Flame conditions B', 'Flame conditions C'], start=1):
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.subheader(case_label)
        XH2 = st.number_input(f'Enter H₂ volume percentage (XH₂) for {case_label} (0.25 to 1.0):', min_value=0.25, max_value=1.0, step=0.01, key=f'XH2_{i}')
        Flame_Thermal_Output = st.number_input(f'Enter Flame Thermal Output (kW) for {case_label} (15 to 25):', min_value=15.0, max_value=25.0, step=0.1, key=f'Flame_Thermal_Output_{i}')
        
        results = calculate_combustion_parameters(Flame_Thermal_Output, XH2)
        data.append([case_label, *results, Flame_Thermal_Output, XH2])
        st.write(f"CO₂: {results[0]:.2f} kg/m³/s")
        st.write(f"Total Boundary Heat Flux: {results[1]:.2f} W/m²")
        st.write(f"Heat Release: {results[2]:.2f} W")
        st.write(f"NOₓ: {results[3]:.2f} kg/m³/s")
        st.write(f"Flame Surface Area: {results[4]:.6f} m²")
        st.write(f"Radiation Heat Flux: {results[5]:.2f} W/m²")
        st.write(f"Flame Temperature: {results[7]:.2f} K")

if data:
    df = pd.DataFrame(data, columns=['Case', 'CO2', 'Total_Boundary_Heat_Flux', 'Heat_Release', 'NOx', 'Flame_Surface_Area', 'Radiation_Heat_Flux', 'XCO', 'Flame_Temperature', 'Flame_Thermal_Output', 'XH2'])

    st.subheader('Comparison Charts')

    st.pyplot(plot_nox(df))
    st.markdown("---")  # Horizontal line

    st.pyplot(plot_co2(df))
    st.markdown("---")  # Horizontal line

    st.pyplot(plot_flame_surface_area(df))
    st.markdown("---")  # Horizontal line

    st.pyplot(plot_heat_release(df))
    st.markdown("---")  # Horizontal line

    st.pyplot(plot_heat_flux(df))
    st.markdown("---")  # Horizontal line

    st.pyplot(plot_temperature(df))
