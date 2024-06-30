import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def set_cambria_font():
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = 'Cambria Math'

def calculate_values(XH2, Power):
    XCO = 1 - XH2

    CO2 = 1286.864286 - 19.936 * Power - 2434.657 * XH2 + 322.986 * (XH2 ** 2)
    Boundary_Heat_Flux = (2228.473786 
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

    return CO2, Boundary_Heat_Flux, Heat_Release, NOx, Flame_Surface_Area, Radiation_Heat_Flux, XCO

def display_comparison_charts(data):
    parameters = ['CO2 (kg/m³)', 'Boundary Heat Flux (W/m²)', 'Heat Release (W)', 'NO? (kg/m³)', 'Flame Surface Area (m²)', 'Radiation Heat Flux (W/m²)']
    df = pd.DataFrame(data, columns=['Case'] + parameters + ['XCO', 'XH2'])
    df.set_index('Case', inplace=True)

    colors = ['blue', 'orange', 'green']
    
    for i, param in enumerate(parameters):
        fig, ax1 = plt.subplots()

        df[param].plot(kind='bar', ax=ax1, color=colors[i % len(colors)], position=0, width=0.4)
        ax1.set_title(f'Comparison of {param}')
        ax1.set_xlabel('Case')
        ax1.set_ylabel(param)
        ax1.grid(True, linestyle='--', linewidth=0.5)
        ax1.legend([param], loc='upper center')

        if param == 'Heat Release (W)' or param == 'CO2 (kg/m³)':
            ax2 = ax1.twinx()
            df['XCO'].plot(ax=ax2, color='red', marker='o', linestyle='dashed')
            ax2.set_ylabel('XCO')
            ax2.legend(['XCO'], loc='upper right')

        if param == 'NO? (kg/m³)':
            ax2 = ax1.twinx()
            df['XH2'].plot(ax=ax2, color='purple', marker='o', linestyle='dashed')
            ax2.set_ylabel('XH2')
            ax2.legend(['XH2'], loc='upper right')

        plt.tight_layout()
        st.pyplot(fig)

def display_results_table(data):
    df = pd.DataFrame(data, columns=['Case', 'CO2 (kg/m³)', 'Boundary Heat Flux (W/m²)', 'Heat Release (W)', 'NO? (kg/m³)', 'Flame Surface Area (m²)', 'Radiation Heat Flux (W/m²)', 'XCO', 'XH2'])
    df.set_index('Case', inplace=True)
    st.table(df)

st.title('Combustion Parameter Calculator')

st.write("This is a calculator tool for educational purposes based on Sandia ChnA burner for turbulent diffusion ideal gas (H2/CO) lean mixture flames with constant stoichiometry (25% excess air), the equations are based on machine learning optimisation and well established CFD numerical models. For any enquiries about this calculation tool, kindly contact abdulhadiodeh@gmail.com")

# Center the
