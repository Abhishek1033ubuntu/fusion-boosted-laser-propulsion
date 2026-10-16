import torch
import numpy as np

# Select CUDA GPU if available, else CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Executing PyTorch MHD Solver on: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")

# Grid Resolution & Spatial Scale
Nz, Nr = 450, 280
Lz, Lr = 500e-6, 300e-6
dz, dr = Lz / Nz, Lr / Nr

z = torch.linspace(0, Lz, Nz, device=device)
r = torch.linspace(0, Lr, Nr, device=device)
Z, R = torch.meshgrid(z, r, indexing='ij')

# Fundamental Physical Constants
kB, m_DT, E_alpha, gamma = 1.380649e-23, 4.17e-27, 5.607e-13, 1.67
R_chamber, r_throat, z_throat, theta_nozzle = 80e-6, 35e-6, 80e-6, np.radians(45.0)

# Chamber Wall Geometry
r_wall = torch.where(
    Z <= z_throat,
    r_throat + (R_chamber - r_throat) * torch.cos(np.pi * Z / (2 * z_throat)),
    r_throat + (Z - z_throat) * np.tan(theta_nozzle)
)
fluid_mask = R <= r_wall

# Applied Superconducting Magnetic Field Profile (B0 = 5.0 T)
B_0, w_z = 5.0, 60e-6
Bz = B_0 * torch.exp(-((Z - z_throat) / w_z)**2)
dBz_dz = -2.0 * ((Z - z_throat) / (w_z**2)) * Bz
Br = -0.5 * R * dBz_dz
sigma_plasma = 1.5e5

# Target Core Mass & Energy Initialization
R_dist = torch.sqrt(Z**2 + R**2)
core_factor = 0.5 * (1.0 - torch.tanh((R_dist - 20e-6) / 2e-6))

rho = 1.0 + (250.0 - 1.0) * core_factor
vz = torch.zeros((Nz, Nr), device=device)
vr = torch.zeros((Nz, Nr), device=device)
P = 1e5 + (334.59e12 - 1e5) * core_factor

def get_dt_reactivity_gpu(Ti_keV):
    Ti = torch.clamp(Ti_keV, 0.1, 100.0)
    return 3.68e-18 * (Ti**(-0.6666667)) * torch.exp(-19.94 * (Ti**(-0.3333333)))

# Time Integration
t_final = 5.0e-9
c_max = np.sqrt(gamma * 334.59e12 / 250.0)
dt = 0.05 * min(dz, dr) / c_max
Nt = int(t_final / dt)
peak_v_exit_record = 0.0
alpha_visc = 0.02

for n in range(Nt):
    e_spec = P / ((gamma - 1.0) * torch.clamp(rho, min=1e-2))
    Ti_keV = ((2.0 / 3.0) * (m_DT / kB) * e_spec) / 1.1604518e7
    n_i = rho / m_DT
    sv = get_dt_reactivity_gpu(Ti_keV)
    burn_zone = (rho > 5.0) & (Ti_keV > 0.5) & (R_dist <= 22e-6)
    
    S_alpha = torch.zeros((Nz, Nr), device=device)
    S_alpha[burn_zone] = 0.85 * 0.25 * (n_i[burn_zone]**2) * sv[burn_zone] * E_alpha
    
    J_theta = sigma_plasma * (vz * Br - vr * Bz)
    F_L_z = J_theta * Br
    F_L_r = -J_theta * Bz
    
    rho_avg = 0.25 * (torch.roll(rho, -1, 0) + torch.roll(rho, 1, 0) + torch.roll(rho, -1, 1) + torch.roll(rho, 1, 1))
    vz_avg  = 0.25 * (torch.roll(vz, -1, 0) + torch.roll(vz, 1, 0) + torch.roll(vz, -1, 1) + torch.roll(vz, 1, 1))
    vr_avg  = 0.25 * (torch.roll(vr, -1, 0) + torch.roll(vr, 1, 0) + torch.roll(vr, -1, 1) + torch.roll(vr, 1, 1))
    P_avg   = 0.25 * (torch.roll(P, -1, 0) + torch.roll(P, 1, 0) + torch.roll(P, -1, 1) + torch.roll(P, 1, 1))
    
    dP_dz = (torch.roll(P, -1, 0) - torch.roll(P, 1, 0)) / (2 * dz)
    dP_dr = (torch.roll(P, -1, 1) - torch.roll(P, 1, 1)) / (2 * dr)
    dvz_dz = (torch.roll(vz, -1, 0) - torch.roll(vz, 1, 0)) / (2 * dz)
    dvr_dr = (torch.roll(vr, -1, 1) - torch.roll(vr, 1, 1)) / (2 * dr)
    
    div_v = dvz_dz + dvr_dr + vr / (R + 1e-5)
    r_safe = torch.clamp(rho, min=1e-2)
    
    rho_new = (1.0 - alpha_visc) * rho + alpha_visc * rho_avg - dt * rho * div_v
    vz_new  = (1.0 - alpha_visc) * vz  + alpha_visc * vz_avg  - dt * (1.0 / r_safe) * dP_dz + dt * (1.0 / r_safe) * F_L_z
    vr_new  = (1.0 - alpha_visc) * vr  + alpha_visc * vr_avg  - dt * (1.0 / r_safe) * dP_dr + dt * (1.0 / r_safe) * F_L_r
    P_new   = (1.0 - alpha_visc) * P   + alpha_visc * P_avg   - dt * gamma * P * div_v + dt * (gamma - 1.0) * S_alpha
    
    rho = torch.clamp(rho_new, min=1e-2, max=5000.0)
    vz, vr = vz_new, vr_new
    P = torch.clamp(P_new, min=1e5, max=5000e12)
    
    max_jet_v = torch.max(vz[fluid_mask]).item()
    if max_jet_v > peak_v_exit_record:
        peak_v_exit_record = max_jet_v

v_exit_kms = peak_v_exit_record / 1e3
Isp_eq = peak_v_exit_record / 9.80665

print(f"=== GPU MHD SOLVER METRICS ===")
print(f"Peak Axial Velocity (v_z) : {v_exit_kms:.2f} km/s")
print(f"Macroscopic Specific Isp  : {Isp_eq:.1f} seconds")
