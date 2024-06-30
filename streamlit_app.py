iimport streamlit as st
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
    df = pd.DataFrame(data, columns=['Case', 'CO2', 'Boundary Heat Flux', 'Heat Release', 'NOx', 'Flame Surface Area', 'Radiation Heat Flux'])
    df.set_index('Case', inplace=True)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    df.plot(kind='bar', ax=ax)
    plt.title('Combustion Parameters Comparison')
    plt.xlabel('Case')
    plt.ylabel('Values')
    plt.xticks(rotation=0)
    st.pyplot(fig)

st.title('Combustion Parameter Calculator')

st.write("Stoichiometry: Constant with 25% excess air")

data = []
for i in range(1, 4):
    st.header(f'Case {i}')
    XH2 = st.number_input(f'Enter XH2 for Case {i} (0.25 to 1):', min_value=0.25, max_value=1.0, step=0.01, key=f'XH2_{i}')
    Power = st.number_input(f'Enter Power for Case {i} (15 to 25):', min_value=15, max_value=25, step=1, key=f'Power_{i}')
    
    if st.button(f'Calculate Case {i}', key=f'button_{i}'):
        results = calculate_values(XH2, Power)
        data.append([f'Case {i}', *results])
        st.write(f"CO2: {results[0]:.2f}")
        st.write(f"Boundary Heat Flux: {results[1]:.2f}")
        st.write(f"Heat Release: {results[2]:.2f}")
        st.write(f"NOx: {results[3]:.2f}")
        st.write(f"Flame Surface Area: {results[4]:.6f}")
        st.write(f"Radiation Heat Flux: {results[5]:.2f}")

if len(data) > 0:
    display_comparison_chart(data)
