import numpy as np

f_rep = 10.0                     # Pulse repetition rate (Hz)
m_pellet = 1.0e-6                # DT pellet mass (1.0 mg)
burn_fraction = 0.35            # Thermonuclear fuel burnup fraction
TBR_main = 0.88                  # Main engine nozzle tritium breeding ratio
TBR_aux = 1.35                   # Auxiliary 4pi breeder tritium breeding ratio
eta_thermo_aux = 0.40            # sCO2 Brayton cycle efficiency
m_T_atom = 5.008e-27             # Tritium atomic mass (kg)
MeV_to_J = 1.60218e-13           # Conversion factor

m_T_per_pellet = m_pellet * 0.60
m_T_burned_per_sec = f_rep * m_T_per_pellet * burn_fraction
m_T_burned_daily_g = m_T_burned_per_sec * 86400 * 1000.0

m_T_main_bred_daily_g = m_T_burned_daily_g * TBR_main
m_T_daily_deficit_g = m_T_burned_daily_g - m_T_main_bred_daily_g

N_reactions_needed_per_sec = (m_T_daily_deficit_g / 1000.0 / 86400) / m_T_atom / (TBR_aux - 1.0)
P_aux_fusion_MW = (N_reactions_needed_per_sec * 17.6 * MeV_to_J) / 1e6
P_aux_electric_MW = P_aux_fusion_MW * eta_thermo_aux
TBR_net = (m_T_main_bred_daily_g + (m_T_daily_deficit_g * TBR_aux)) / m_T_burned_daily_g

print(f"=== AUXILIARY ACOUSTIC BREEDER NEUTRONICS ===")
print(f"Main Engine Daily Burn Rate   : {m_T_burned_daily_g:.2f} g/day")
print(f"Main Nozzle Tritium Recovery  : {m_T_main_bred_daily_g:.2f} g/day")
print(f"Unmitigated Daily Deficit     : -{m_T_daily_deficit_g:.2f} g/day")
print(f"Aux Acoustic Thermal Power    : {P_aux_fusion_MW:.2f} MW_th")
print(f"Aux Auxiliary Electric Output : {P_aux_electric_MW:.2f} MW_e")
print(f"Net System Breeding Ratio     : {TBR_net:.2f} (Fuel Self-Sustaining)")
