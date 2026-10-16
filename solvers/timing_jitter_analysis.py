import numpy as np

# Physical & Geometric Constraints
r_spot = 20e-6                   # Focal spot radius (20 micrometers)
P_0 = 334.59                     # Ideal peak pressure (334.59 TPa)
v_s = 83.4e3                     # Convergent shock velocity (83.4 km/s)
P_ignition_threshold = 301.13    # 90% ignition threshold floor (301.13 TPa)

# Calculate Maximum Allowable Laser Timing Jitter
sigma_max_ps = (r_spot / v_s) * np.sqrt(-2.0 * np.log(P_ignition_threshold / P_0)) * 1e12

# Parametric Decay Function
def calculate_pressure_decay(jitter_ps_val):
    delta_r = v_s * (jitter_ps_val * 1e-12)
    return P_0 * np.exp(-0.5 * (delta_r / r_spot)**2)

print(f"=== LASER ACTUATOR SYNCHRONIZATION METRICS ===")
print(f"Ablative Shock Velocity   : {v_s/1e3:.2f} km/s")
print(f"Ideal Peak Core Pressure  : {P_0:.2f} TPa")
print(f"Ignition Pressure Floor   : {P_ignition_threshold:.2f} TPa (90% P0)")
print(f"Max Allowable Jitter (σ)  : {sigma_max_ps:.2f} picoseconds")
print(f"Pressure at 11.01 ps      : {calculate_pressure_decay(11.01):.2f} TPa")
print(f"Pressure at 50.00 ps      : {calculate_pressure_decay(50.00):.2f} TPa")
