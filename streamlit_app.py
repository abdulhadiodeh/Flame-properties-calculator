import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

    return CO2, Boundary_Heat_Flux, Heat_Release, NOx, Flame_Surface_Area, Radiation_Heat_Flux

def display_comparison_chart(data):
    parameters = ['CO2 (kg/m^3)', 'Boundary Heat Flux (W/m^2)', 'Heat Release (W)', 'NOx (kg/m^3)', 'Flame Surface Area (m^2)', 'Radiation Heat Flux (W/m^2)']
    df = pd.DataFrame(data, columns=['Case'] + parameters)
    df.set_index('Case', inplace=True)
    
    fig, axs = plt.subplots(3, 2, figsize=(15, 15))
    axs = axs.flatten()
    
    for ax, param in zip(axs, parameters):
        df[param].plot(kind='bar', ax=ax)
        ax.set_title(f'Comparison of {param}')
        ax.set_xlabel('Case')
        ax.set_ylabel(param)
        ax.grid(True, linestyle='--', linewidth=0.5)
        ax.legend(loc='upper center')
        ax.set_xticklabels(df.index, rotation=0)
    
    plt.tight_layout()
    st.pyplot(fig)

st.title('Combustion Parameter Calculator')

st.write("This is a calculator based on Sandia chnA burner for turbulent diffusion ideal gas (H2/CO) lean mixture flames with constant stoichiometry (25% excess air).")

# Add an image to the app
st.image('burner.jpg', caption='Sandia chnA Burner')

data = []
for i in range(1, 4):
    st.header(f'Case {i}')
    XH2 = st.number_input(f'Enter XH2 for Case {i} (0.25 to 1):', min_value=0.25, max_value=1.0, step=0.01, key=f'XH2_{i}')
    Power = st.number_input(f'Enter Power for Case {i} (15 to 25):', min_value=15, max_value=25, step=1, key=f'Power_{i}')
    
    if st.button(f'Calculate Case {i}', key=f'button_{i}'):
        results = calculate_values(XH2, Power)
        data.append([f'Case {i}', *results])
        st.write(f"CO2: {results[0]:.2f} kg/m^3")
        st.write(f"Boundary Heat Flux: {results[1]:.2f} W/m^2")
        st.write(f"Heat Release: {results[2]:.2f} W")
        st.write(f"NOx: {results[3]:.2f} kg/m^3")
        st.write(f"Flame Surface Area: {results[4]:.6f} m^2")
        st.write(f"Radiation Heat Flux: {results[5]:.2f} W/m^2")

if len(data) > 0:
    display_comparison_chart(data)
