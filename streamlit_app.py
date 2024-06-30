import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Ensure you have a function to calculate values
def calculate_values(XH2, Flame_Thermal_Output):
    # Placeholder calculation function
    CO2 = XH2 * 0.5
    Total_Boundary_Heat_Flux = Flame_Thermal_Output * 0.1
    Heat_Release = Flame_Thermal_Output * 0.8
    NOx = XH2 * 0.2
    Flame_Surface_Area = XH2 * 0.05
    Radiation_Heat_Flux = Flame_Thermal_Output * 0.3
    XCO = XH2 * 0.4
    Flame_Temperature = Flame_Thermal_Output * 10
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

# Repeat similar functions for the other plots...

# Streamlit app layout
st.title('Combustion Parameter Calculator')

st.write("""
This is a calculator tool for educational purposes based on Sandia ChnA burner for turbulent diffusion ideal gas (H₂/CO) lean mixture flames with constant stoichiometry (25% excess air), 
the equations are based on machine learning optimisation and well established CFD numerical models. 
For any enquiries about this calculation tool, kindly contact abdulhadiodeh@gmail.com
""")

# Center the image
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.image('burner.jpg', caption='Sandia chnA Burner')

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

    