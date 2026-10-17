"""
FBLA-PROP-2026-REV5: Multi-Physics Simulation Kernel
Lead Author / Principal Investigator: Abhishek Singh
Collaboration & Numerical Verification: Google Gemini (Google DeepMind)
ORCID: https://orcid.org/0009-0004-6913-096X
Copyright (c) 2026 Abhishek Singh. All Rights Reserved.

Description:
    Numba-accelerated parallel trajectory, thermal decay, and electrostatic steering
    solver for open-space Liquid Droplet Radiators (LDR) operating under active
    vehicle acceleration maneuvers.
"""

import numpy as np
import time
from numba import njit, prange


@njit(parallel=True, fastmath=True)
def simulate_charged_ldr_droplets(
    n_droplets,
    r_droplet,
    rho_liquid,
    cp_liquid,
    emissivity,
    v_launch,
    divergence_angle_rad,
    L_ldr,
    R_collector,
    a_ship,
    E_steer,
    q_droplet,
    T_init,
    T_space,
    dt,
    max_steps
):
    """
    Numba Parallel Trajectory Kernel with Active Electrostatic Steering (q * E).
    Simulates N charged droplets in the non-inertial accelerating vehicle frame.
    """
    sigma_sb = 5.670374419e-8  # Stefan-Boltzmann constant (W/m^2 K^4)
    vol_droplet = (4.0 / 3.0) * np.pi * (r_droplet ** 3)
    area_droplet = 4.0 * np.pi * (r_droplet ** 2)
    m_droplet = rho_liquid * vol_droplet

    final_x = np.zeros(n_droplets)
    final_y = np.zeros(n_droplets)
    final_T = np.zeros(n_droplets)
    transit_times = np.zeros(n_droplets)
    captured = np.zeros(n_droplets, dtype=np.bool_)

    ax_ship, ay_ship, az_ship = a_ship[0], a_ship[1], a_ship[2]
    Ex, Ey, Ez = E_steer[0], E_steer[1], E_steer[2]

    # Specific acceleration from electrostatic force: a_elec = (q * E) / m
    ax_elec = (q_droplet * Ex) / m_droplet
    ay_elec = (q_droplet * Ey) / m_droplet
    az_elec = (q_droplet * Ez) / m_droplet

    # Net relative acceleration vector in vehicle frame
    ax_net = ax_elec - ax_ship
    ay_net = ay_elec - ay_ship
    az_net = az_elec - az_ship

    for i in prange(n_droplets):
        theta = np.random.normal(0.0, divergence_angle_rad)
        phi = np.random.uniform(0.0, 2.0 * np.pi)

        vx = v_launch * np.sin(theta) * np.cos(phi)
        vy = v_launch * np.sin(theta) * np.sin(phi)
        vz = v_launch * np.cos(theta)

        x, y, z = 0.0, 0.0, 0.0
        T = T_init

        step = 0
        while z < L_ldr and step < max_steps:
            # Trajectory step incorporating electrostatic steering
            x += vx * dt + 0.5 * ax_net * (dt ** 2)
            y += vy * dt + 0.5 * ay_net * (dt ** 2)
            z += vz * dt + 0.5 * az_net * (dt ** 2)

            vx += ax_net * dt
            vy += ay_net * dt
            vz += az_net * dt

            # Radiative cooling decay
            q_rad = emissivity * sigma_sb * area_droplet * (T ** 4 - T_space ** 4)
            dT = (q_rad / (m_droplet * cp_liquid)) * dt
            T -= dT

            step += 1

        final_x[i] = x
        final_y[i] = y
        final_T[i] = T
        transit_times[i] = step * dt

        # Collector aperture capture check
        if np.sqrt(x**2 + y**2) <= R_collector:
            captured[i] = True

    return captured, final_x, final_y, final_T, transit_times, m_droplet


def run_electrostatic_ldr_test():
    print("=" * 65)
    print(" FBLA REV5: ELECTROSTATICALLY STEERED LDR SOLVER")
    print("=" * 65)

    n_droplets = 1_000_000
    r_droplet = 1.2e-4             # 240 um diameter liquid tin droplets
    rho_sn = 6800.0                # kg/m^3
    cp_sn = 240.0                  # J/kg K
    emissivity = 0.88              # Surface emissivity
    L_ldr = 25.0                   # 25 m flight distance
    R_collector = 0.45             # 45 cm collector radius (90 cm aperture)
    v_launch = 20.0                # m/s injection velocity
    gamma_sn = 0.52                # Surface tension (N/m) at 1,200 K
    eps_0 = 8.8541878128e-12

    # High-G Maneuver Vector (m/s^2): 2.5 m/s^2 lateral shift
    a_ship = np.array([2.50, 0.80, 0.10])

    # Droplet Mass and Rayleigh Charge Limit
    m_droplet = rho_sn * (4.0/3.0) * np.pi * (r_droplet**3)
    q_rayleigh = 8.0 * np.pi * np.sqrt(eps_0 * gamma_sn * (r_droplet**3))
    q_droplet = 0.35 * q_rayleigh  # 35% of Rayleigh stability limit

    # Closed-Loop Ideal Steering Field: E = (m / q) * a_ship
    E_steer = (m_droplet / q_droplet) * a_ship

    dt = 1.0e-5
    max_steps = 50000

    print(f"Droplet Count:              {n_droplets:,}")
    print(f"Rayleigh Charge Limit:      {q_rayleigh * 1e12:.2f} pC")
    print(f"Operational Droplet Charge: {q_droplet * 1e12:.2f} pC (35% Rayleigh limit)")
    print(f"High-G Maneuver Vector:     [{a_ship[0]:.2f}, {a_ship[1]:.2f}, {a_ship[2]:.2f}] m/s^2")
    print(f"Applied Steering Field (E): [{E_steer[0]/1e3:.1f}, {E_steer[1]/1e3:.1f}, {E_steer[2]/1e3:.1f}] kV/m")
    print("-" * 65)

    # Warmup JIT compilation
    _ = simulate_charged_ldr_droplets(
        10, r_droplet, rho_sn, cp_sn, emissivity, v_launch,
        0.0008, L_ldr, R_collector, a_ship, E_steer, q_droplet,
        1200.0, 4.0, dt, max_steps
    )

    t0 = time.time()
    captured, final_x, final_y, final_T, transit_times, _ = simulate_charged_ldr_droplets(
        n_droplets, r_droplet, rho_sn, cp_sn, emissivity, v_launch,
        0.0008, L_ldr, R_collector, a_ship, E_steer, q_droplet,
        1200.0, 4.0, dt, max_steps
    )
    t_sim = time.time() - t0

    capture_efficiency = (np.sum(captured) / n_droplets) * 100.0

    print(f"Computation Time:           {t_sim * 1000:.2f} ms")
    print(f"Capture Efficiency:         {capture_efficiency:.4f} %")
    print(f"Mean Final Temp:            {np.mean(final_T):.1f} K")
    print("-" * 65)
    if capture_efficiency >= 99.99:
        print("STATUS: PASSED [Electrostatic deflection successfully nullified High-G drift]")
    print("=" * 65)


if __name__ == "__main__":
    run_electrostatic_ldr_test()
