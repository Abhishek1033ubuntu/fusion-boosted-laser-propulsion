import numpy as np

# Thermal Load Allocations
P_aux_waste_MW = 243.25          # Auxiliary breeder thermal waste load (MW_th)
P_main_waste_MW = 125.00         # Main engine wall absorption load (MW_th)
P_total_waste_MW = P_aux_waste_MW + P_main_waste_MW # Total thermal rejection load

# Material & Radiator Parameters
sigma_SB = 5.670374e-8           # Stefan-Boltzmann constant (W/m^2*K^4)
emissivity = 0.92                # Pyrolytic graphite carbon-carbon composite emissivity
areal_density_kg_m2 = 4.5        # Panel specific structural density (kg/m^2)
T_design = 800.0                 # Liquid-lithium heat pipe operating temperature (K)

# Heat Rejection Calculations
q_design = emissivity * sigma_SB * (T_design**4) # Specific heat flux (W/m^2)
A_design_total = (P_total_waste_MW * 1e6) / q_design # Total emitting surface area
A_footprint = A_design_total / 2.0                   # Physical double-sided panel footprint
M_design_tons = (A_design_total * areal_density_kg_m2) / 1000.0 # Dry mass penalty

print(f"=== SPACE RADIATOR THERMAL MANAGEMENT METRICS ===")
print(f"Operating Temperature (T_rad) : {T_design:.0f} K")
print(f"Total Waste Thermal Power     : {P_total_waste_MW:.2f} MW_th")
print(f"Specific Heat Flux Density    : {q_design/1e3:.2f} kW/m²")
print(f"Total Emitting Surface Area   : {A_design_total:,.2f} m²")
print(f"Physical Panel Footprint      : {A_footprint:,.2f} m²")
print(f"Radiator System Dry Mass      : {M_design_tons:.2f} Metric Tons")
