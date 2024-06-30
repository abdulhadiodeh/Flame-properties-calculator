import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate values based on provided equations
def calculate_combustion_parameters(Flame_Thermal_Output, XH2):
    XCO = 1 - XH2
    
    CO2 = (
        48083.30 + 74352.21990073 * Flame_Thermal_Output - 1185046.15095059 * XH2
        + 3306.55222 * (Flame_Thermal_Output ** 2) - 55440.5787 * (Flame_Thermal_Output * XH2)
        + 109125 * (XH2 ** 2) + 72124.94 * (Flame_Thermal_Output ** 3)
        - 16295.85 * (Flame_Thermal_Output ** 2 * XH2) + 45729.92 * (Flame_Thermal_Output * (XH2 ** 2))
        - 112269.25 * (XH2 ** 3) + 4959.83 * (Flame_Thermal_Output ** 4)
        - 83160.87 * ((Flame_Thermal_Output ** 3) * XH2) - 44042.30 * ((Flame_Thermal_Output ** 2) * (XH2 ** 2))
        - 44536.51 * (Flame_Thermal_Output * (XH2 ** 3)) + 218250 * (XH2 ** 4)
    )
    
    Total_Boundary_Heat_Flux = (
        0 + 1588.44 * Flame_Thermal_Output - 483.70 * XH2
        + 67.96 * (Flame_Thermal_Output ** 2) - 170.54 * (Flame_Thermal_Output * XH2)
        + 11.76 * (XH2 ** 2) - 68.11 * (Flame_Thermal_Output ** 3)
        + 3.20 * ((Flame_Thermal_Output ** 2) * XH2) - 22.04 * (Flame_Thermal_Output * (XH2 ** 2))
        + 30.63 * (XH2 ** 3) + 6.96 * (Flame_Thermal_Output ** 4)
        - 12.64 * ((Flame_Thermal_Output ** 3) * XH2) - 11.25 * ((Flame_Thermal_Output ** 2) * (XH2 ** 2))
        + 7.74 * (Flame_Thermal_Output * (XH2 ** 3)) + 0.07 * (XH2 ** 4)
    )
    
    Heat_Release = (
        0 + 3305.10 * Flame_Thermal_Output - 791.35 * XH2
        + 0 * (Flame_Thermal_Output ** 2) + 0 * (Flame_Thermal_Output * XH2)
        + 0 * (XH2 ** 2) + 270.18 * (Flame_Thermal_Output ** 3)
        - 5.19 * ((Flame_Thermal_Output ** 2) * XH2) + 0 * (Flame_Thermal_Output * (XH2 ** 2))
        - 35.22 * (XH2 ** 3) + 0 * (Flame_Thermal_Output ** 4)
        - 162.42 * ((Flame_Thermal_Output ** 3) * XH2) - 1.74 * ((Flame_Thermal_Output ** 2) * (XH2 ** 2))
        + 48.32 * (Flame_Thermal_Output * (XH2 ** 3)) - 0.97 * (XH2 ** 4)
    )
    
    NOx = (
        0.00 + (-2.84579658) * Flame_Thermal_Output + 20.12910846 * XH2
        + (-1.37452773) * (Flame_Thermal_Output ** 2) + (-7.19582609) * (Flame_Thermal_Output * XH2)
        + 33.84552102 * (XH2 ** 2)
    )
    
    Flame_Surface_Area = (
        1.52259958e-5 * Flame_Thermal_Output + 7.09019888e-4 * XH2
        - 1.66423950e-5 * (Flame_Thermal_Output ** 2) + 2.24465086e-5 * (XH2 ** 2)
        + 1.46250000e-4 * (Flame_Thermal_Output * XH2) + 2.28389938e-5 * (Flame_Thermal_Output ** 3)
        - 4.86453016e-5 * (XH2 ** 3) + 4.83081780e-5 * ((Flame_Thermal_Output ** 2) * XH2)
        + 3.68019521e-4 * (Flame_Thermal_Output * (XH2 ** 2)) - 2.49635925e-5 * (Flame_Thermal_Output ** 4)
        + 3.36697630e-5 * (XH2 ** 4) + 4.35744642e-6 * ((Flame_Thermal_Output ** 3) * XH2)
        + 2.44217460e-5 * (Flame_Thermal_Output * (XH2 ** 3)) + 2.92500000e-4
    )
    
    Radiation_Heat_Flux = (
        0 + 46.41 * Flame_Thermal_Output + 529.73 * XH2
        - 9.89 * (Flame_Thermal_Output ** 2) + 66.98 * (Flame_Thermal_Output * XH2)
        + 54.66 * (XH2 ** 2) + 69.62 * (Flame_Thermal_Output ** 3)
        - 4.59 * ((Flame_Thermal_Output ** 2) * XH2) + 104.23 * (Flame_Thermal_Output * (XH2 ** 2))
        + 167.90 * (XH2 ** 3) - 14.83 * (Flame_Thermal_Output ** 4)
        + 100.47 * ((Flame_Thermal_Output ** 3) * XH2) + 7.53 * ((Flame_Thermal_Output ** 2) * (XH2 ** 2))
        + 1.07 * (Flame_Thermal_Output * (XH2 ** 3)) + 109.33 * (XH2 ** 4)
    )
    
    Flame_Temperature = 2160.0 + 152.0 * XH2
    
    return CO2, Total_Boundary_Heat_Flux, Heat_Release, NOx, Flame_Surface_Area, Radiation_Heat_Flux, XCO, Flame_Temperature

# Plot functions with updated styles
def plot_nox(data):
    fig, ax1 = plt.subplots(facecolor='#f0f0f0')
    ax1.bar(data['Case'], data['NOx'], color='red', edgecolor='blue', label='NOx (kg/m³)', width=0.35)
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
    fig, ax1 = plt.subplots(facecolor='#f0f0f0')
    ax1.bar(data['Case'], data['CO2'], color='orange', edgecolor='blue', label='CO₂ (kg/m³)', width=0.35)
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
    fig, ax1 = plt.subplots(facecolor='#f0f0f0')
    ax1.bar(data['Case'], data['Flame_Surface_Area'], color='blue', edgecolor='blue', label='Flame Surface Area (m²)', width=0.35)
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
    fig, ax1 = plt.subplots(facecolor='#f0f0f0')
    ax1.bar(data['Case'], data['Heat_Release'], color='purple', edgecolor='blue', label='Heat Release (W)', width=0.35)
    ax1.set_ylabel('Heat Release (W)')
    ax1.tick_params(axis='x', rotation=45.05)
    ax1.grid(True, linestyle='--', linewidth=0.5)
    
    ax2 = ax1.twinx()
    ax2.plot(data['Case'], data['Flame_Thermal_Output'], color='black', marker='o', linestyle='--', label='Flame Thermal Output (kW)')
    ax2.set_ylabel('Flame Thermal Output (kW)')
    
    fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2, frameon=True, edgecolor='black')
    fig.tight_layout()
    
    return fig

def plot_heat_flux(data):
    fig, ax1 = plt.subplots(facecolor='#f0f0f0')
    ax1.bar(data['Case'], data['Radiation_Heat_Flux'], color='lightcoral', edgecolor='blue', label='Radiation Heat Flux (W/m²)', width=0.35)
    ax1.bar(data['Case'], data['Total_Boundary_Heat_Flux'] - data['Radiation_Heat_Flux'], color='darkgrey', edgecolor='blue', label='Total Boundary Heat Flux (W/m²)', bottom=data['Radiation_Heat_Flux'], width=0.35)
    ax1.set_ylabel('Heat Flux (W/m²)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, linestyle='--', linewidth=0.5)
    
    fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2, frameon=True, edgecolor='black')
    fig.tight_layout()
    
    return fig

def plot_temperature(data):
    fig, ax1 = plt.subplots(facecolor='#f0f0f0')
    ax1.bar(data['Case'], data['Flame_Temperature'], color='red', edgecolor='blue', label='Flame Temperature (K)', width=0.35)
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
the equations are based on machine learning optimisation and well established CFD numerical models. 
For any enquiries about this calculation tool, kindly contact abdulhadiodeh@gmail.com
""")

# Center the image
st.markdown("<h2 style='text-align: center;'>Sandia ChnA Burner</h2>", unsafe_allow_html=True)
st.image('burner.jpg', caption='Sandia ChnA Burner')

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
        st.write(f"CO₂: {results[0]:.2f} kg/m³")
        st.write(f"Total Boundary Heat Flux: {results[1]:.2f} W/m²")
        st.write(f"Heat Release: {results[2]:.2f} W")
        st.write(f"NOₓ: {results[3]:.2f} kg/m³")
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
