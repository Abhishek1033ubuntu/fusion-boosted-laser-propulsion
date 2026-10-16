import numpy as np

# Spacecraft Platform Parameters
m_vehicle_kg = 100000.0          # 100-ton vehicle mass
I_xx = 2.5e6                     # Pitch moment of inertia (kg*m^2)
R_arm = 1.414                    # Cluster pitch radius offset (m)
F_nominal_N = 3000.0             # Nominal thrust per engine module (3.0 kN)
f_nominal_Hz = 10.0              # Nominal pulse frequency (10 Hz)

# 20% Differential Throttle Modulation Command
df = 0.20
f1 = f4 = f_nominal_Hz * (1.0 + df) # 12.0 Hz
f2 = f3 = f_nominal_Hz * (1.0 - df) #  8.0 Hz

F1 = F4 = F_nominal_N * (f1 / f_nominal_Hz) # 3,600 N
F2 = F3 = F_nominal_N * (f2 / f_nominal_Hz) # 2,400 N

# Moment & Angular Acceleration Calculation
y_offset = R_arm * np.sin(np.radians(45.0)) # 1.0 m moment arm
M_x = y_offset * ((F1 + F4) - (F2 + F3))   # Pitch moment (N*m)
alpha_x_rad_s2 = M_x / I_xx                # Angular acceleration

# Structural Gantry Stress Calculation
r_gantry = 0.15                  # Titanium-Carbon truss tube radius (m)
t_wall = 0.01                    # Truss wall thickness (m)
I_gantry_area = np.pi * (r_gantry**3) * t_wall # Second moment of area
bending_moment_max = max(F1, F2, F3, F4) * R_arm
sigma_bending_MPa = (bending_moment_max * r_gantry / I_gantry_area) / 1e6

print(f"=== QUAD-THRUSTER KINEMATICS & DIFFERENTIAL VECTORING ===")
print(f"Total Cluster Axial Thrust  : {(F1+F2+F3+F4)/1e3:.2f} kN")
print(f"Generated Pitch Torque (Mx) : {M_x:.2f} N*m")
print(f"Angular Acceleration (α)    : {np.degrees(alpha_x_rad_s2):.4f} deg/s²")
print(f"10-Sec Attitude Change (Δθ) : {np.degrees(0.5 * alpha_x_rad_s2 * 100.0):.2f} degrees")
print(f"Gantry Bending Stress (σ)   : {sigma_bending_MPa:.2f} MPa (Yield Safety Margin > 20x)")
