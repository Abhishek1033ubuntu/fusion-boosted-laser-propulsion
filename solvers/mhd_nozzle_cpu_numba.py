import numpy as np
from numba import njit

# Grid Resolution & Domain Setup
Nz, Nr = 180, 110
Lz, Lr = 500e-6, 300e-6
dz, dr = Lz / Nz, Lr / Nr

z = np.linspace(0, Lz, Nz)
r = np.linspace(0, Lr, Nr)
Z, R = np.meshgrid(z, r, indexing='ij')

# Constants
kB, m_DT, E_alpha, gamma = 1.380649e-23, 4.17e-27, 5.607e-13, 1.67
R_chamber, r_throat, z_throat, theta_nozzle = 80e-6, 35e-6, 80e-6, np.radians(45.0)

r_wall = np.where(
    Z <= z_throat,
    r_throat + (R_chamber - r_throat) * np.cos(np.pi * Z / (2 * z_throat)),
    r_throat + (Z - z_throat) * np.tan(theta_nozzle)
)
fluid_mask = R <= r_wall

B_0, w_z = 5.0, 60e-6
Bz = B_0 * np.exp(-((Z - z_throat) / w_z)**2)
dBz_dz = -2.0 * ((Z - z_throat) / (w_z**2)) * Bz
Br = -0.5 * R * dBz_dz

@njit(fastmath=True)
def run_mhd_low_dissipation(rho, vz, vr, P, fluid_mask, Br, Bz, R, dz, dr, dt, Nt, gamma, m_DT, kB, E_alpha, sigma_plasma):
    Nz, Nr = rho.shape
    peak_v_exit_record = 0.0
    alpha_blend = 0.05
    for n in range(Nt):
        e_spec = P / ((gamma - 1.0) * np.maximum(1e-2, rho))
        Ti_keV = ((2.0 / 3.0) * (m_DT / kB) * e_spec) / 1.1604518e7
        S_alpha = np.zeros((Nz, Nr))
        for i in range(Nz):
            for j in range(Nr):
                if fluid_mask[i, j]:
                    r_dist = (i*dz)**2 + (j*dr)**2
                    if r_dist <= (20e-6)**2 and Ti_keV[i, j] > 0.5:
                        Ti = min(max(Ti_keV[i, j], 0.1), 100.0)
                        sv = 3.68e-18 * (Ti**(-0.6666667)) * np.exp(-19.94 * (Ti**(-0.3333333)))
                        n_i = rho[i, j] / m_DT
                        S_alpha[i, j] = 0.85 * 0.25 * (n_i**2) * sv * E_alpha

        J_theta = sigma_plasma * (vz * Br - vr * Bz)
        F_L_z = J_theta * Br
        F_L_r = -J_theta * Bz
        
        rho_new, vz_new, vr_new, P_new = np.copy(rho), np.copy(vz), np.copy(vr), np.copy(P)
        for i in range(1, Nz-1):
            for j in range(1, Nr-1):
                if fluid_mask[i, j]:
                    rho_avg = (1.0 - alpha_blend) * rho[i, j] + 0.25 * alpha_blend * (rho[i+1, j] + rho[i-1, j] + rho[i, j+1] + rho[i, j-1])
                    vz_avg  = (1.0 - alpha_blend) * vz[i, j]  + 0.25 * alpha_blend * (vz[i+1, j]  + vz[i-1, j]  + vz[i, j+1]  + vz[i, j-1])
                    vr_avg  = (1.0 - alpha_blend) * vr[i, j]  + 0.25 * alpha_blend * (vr[i+1, j]  + vr[i-1, j]  + vr[i, j+1]  + vr[i, j-1])
                    P_avg   = (1.0 - alpha_blend) * P[i, j]   + 0.25 * alpha_blend * (P[i+1, j]   + P[i-1, j]   + P[i, j+1]   + P[i, j-1])
                    
                    dP_dz = (P[i+1, j] - P[i-1, j]) / (2 * dz)
                    dP_dr = (P[i, j+1] - P[i, j-1]) / (2 * dr)
                    dvz_dz = (vz[i+1, j] - vz[i-1, j]) / (2 * dz)
                    dvr_dr = (vr[i, j+1] - vr[i, j-1]) / (2 * dr)
                    div_v = dvz_dz + dvr_dr + vr[i, j] / (R[i, j] + 1e-5)
                    r_safe = max(1e-2, rho[i, j])
                    
                    rho_new[i, j] = max(1e-2, rho_avg - dt * rho[i, j] * div_v)
                    vz_new[i, j]  = vz_avg - (dt / r_safe) * dP_dz + (dt / r_safe) * F_L_z[i, j]
                    vr_new[i, j]  = vr_avg - (dt / r_safe) * dP_dr + (dt / r_safe) * F_L_r[i, j]
                    P_new[i, j]   = max(1e5, P_avg - dt * gamma * P[i, j] * div_v + dt * (gamma - 1.0) * S_alpha[i, j])

        rho, vz, vr, P = rho_new, vz_new, vr_new, P_new
        for i in range(int(Nz * 0.7), Nz-1):
            for j in range(Nr):
                if fluid_mask[i, j] and vz[i, j] > peak_v_exit_record:
                    peak_v_exit_record = vz[i, j]

    return rho, vz, vr, P, peak_v_exit_record

if __name__ == "__main__":
    rho = np.full((Nz, Nr), 1.0)
    vz, vr = np.zeros((Nz, Nr)), np.zeros((Nz, Nr))
    P = np.full((Nz, Nr), 1e5)
    core_mask = (R**2 + Z**2) <= (20e-6)**2
    rho[core_mask], P[core_mask] = 250.0, 334.59e12
    dt = 0.04 * min(dz, dr) / np.sqrt(gamma * 334.59e12 / 250.0)
    Nt = int(4.0e-9 / dt)
    rho, vz, vr, P, v_exit = run_mhd_low_dissipation(rho, vz, vr, P, fluid_mask, Br, Bz, R, dz, dr, dt, Nt, gamma, m_DT, kB, E_alpha, 1.5e5)
    print(f"=== NUMBA CPU MHD SOLVER METRICS ===")
    print(f"Peak Axial Exit Velocity : {v_exit/1e3:.2f} km/s")
    print(f"Specific Impulse (Isp)   : {v_exit/9.80665:.1f} seconds")
