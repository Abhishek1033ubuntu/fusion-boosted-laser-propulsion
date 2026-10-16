# Technical Case Study: Thermal Rejection Bottleneck & Energy Conversion / Mitigation Roadmap

**Document ID:** FBLA-PROP-2026-CASE-THERMAL  
**Classification:** Research Roadmap / REV5 Trade Study  
**Lead Author / Principal Investigator:** Abhishek Singh  
**Affiliation:** Independent Research Group, Madhya Pradesh, India  
**ORCID:** [https://orcid.org/0009-0004-6913-096X](https://orcid.org/0009-0004-6913-096X)  
**Primary Contact:** abhishek1033@gmail.com | abhishek.s@live.in  
**AI Computational & Multi-Physics Support:** Team Gemini (Google DeepMind)  
**Copyright:** Copyright (c) 2026 Abhishek Singh. All Rights Reserved.  

---

## 1. Problem Statement & Baseline Bottleneck Analysis

In the **FBLA-PROP-2026-REV4** baseline, the propulsion system rejects $368.25\text{ MW}_{\text{th}}$ of total waste thermal energy ($243.25\text{ MW}_{\text{th}}$ from the auxiliary acoustic breeder cycle and $125.00\text{ MW}_{\text{th}}$ from main engine magnetic nozzle and wall absorption).

Under standard Stefan-Boltzmann blackbody radiation scaling:

$$q_{\text{rad}} = \epsilon \cdot \sigma \cdot T_{\text{rad}}^4$$

For carbon-carbon composite heat pipes operating at $T_{\text{rad}} = 800\text{ K}$ with surface emissivity $\epsilon = 0.92$:

* **Emitted Specific Heat Flux ($q_{\text{rad}}$):** $21.37\text{ kW/m}^2$ (double-sided emission: $42.74\text{ kW/m}^2$ per footprint $\text{m}^2$).
* **Required Emitting Area ($A_{\text{rad}}$):** $17,233.89\text{ m}^2$.
* **System Dry Mass ($M_{\text{rad}}$):** $77.55\text{ metric tons}$ (at an areal structural density of $4.5\text{ kg/m}^2$).

### Core Critical Challenge
On a $100\text{-ton}$ dry vehicle platform, allocating **$77.55\%$ of dry mass** solely to passive heat rejection severely limits structural payload margins and vehicle $\Delta v$ performance.

---

## 2. Energy Conversion & Harvesting Potential

Rather than allowing high-grade thermal and plasma energy to degrade directly into waste heat, a significant fraction can be intercepted and converted back into electrical power.

```text
+-----------------------------------------------------------------------------------+
|                               THERMONUCLEAR BURN                                  |
|                 Total Energy: Plasma Kinetic + Thermal + Neutronic                |
+-----------------------------------------------------------------------------------+
                                          |
                   +----------------------+----------------------+
                   |                                             |
                   v                                             v
    +------------------------------+             +------------------------------+
    |  Direct Energy Conversion    |             |  High-T Thermionic / sCO2     |
    |  (Inductive Induction Coils) |             |  Waste Heat Harvesting       |
    +------------------------------+             +------------------------------+
                   |                                             |
                   v                                             v
    +------------------------------+             +------------------------------+
    |  Recycled Electrical Power   |             |  High-Density Storage        |
    |  (30% - 50% Efficiency)      |             |  (SMES / Pulse Capacitors)   |
    +------------------------------+             +------------------------------+
                   |                                             |
                   +----------------------+----------------------+
                                          |
                                          v
                         +---------------------------------+
                         |  Laser Drive & Subsystem Loop   |
                         |  (Reduced Net Thermal Load)     |
                         +---------------------------------+

```

### 2.1 Magnetohydrodynamic Direct Energy Conversion (DEC)

During plasma expansion inside the $5.0\text{ T}$ magnetic nozzle, expanding DT alpha particles ($3.5\text{ MeV}$) and target ions induce azimuthal currents ($J_\theta$).

* **Mechanism:** Pick-up induction coils integrated into the nozzle wall convert charged particle kinetic energy directly into high-voltage electricity prior to wall contact.
* **Conversion Efficiency Target:** $\eta_{\text{DEC}} = 45% - 65%.
* **Thermal Mitigation Impact:** Directly reduces the main engine wall heat load ($P_{\text{main\_waste}}$) from $125.00\text{ MW}_{\text{th}}$ down to $\sim 43.75\text{--}68.75\text{ MW}_{\text{th}}$, eliminating up to $17.0\text{ metric tons}$ of dedicated main-engine radiator mass.

### 2.2 Top-Cycle Thermionic / Thermoelectric Topping

* **Mechanism:** Thermionic energy converters (TECs) placed directly on the inner vessel lining operate at emitter temperatures of $1,400\text{--}1,800\text{ K}$.
* **Conversion Efficiency Target:** $\eta_{\text{TEC}} = 12\%\text{--}18\%$.
* **Output:** Generates $29.2\text{--}43.8\text{ MW}_e$ of secondary electrical power while stepping down the fluid temperature to the input threshold of the secondary sCO2 Brayton loop.

---

## 3. Energy Storage & Power Loop Integration

Recycled electrical energy must be stored and buffered to drive high-peak-power subsystems:

1. **Superconducting Magnetic Energy Storage (SMES):**
* **Role:** Buffers fast pulsed discharge cycles required by the 12-actuator phased laser drive array ($12.0\text{ J}$ per pulse at $10\text{ Hz}$).
* **Specific Energy:** $10\text{--}30\text{ Wh/kg}$ with ultra-high round-trip efficiency ($>95\%$).


2. **Solid-State Ultra-Capacitor Banks:**
* **Role:** High-rate buffering for bow-mounted Pulsed Plasma / MPD vernier RCS thrusters during dynamic slew maneuvers.


3. **Closed Electrical Loop Balance:**
* **Net Recycled Power:** $\sim 70\text{--}100\text{ MW}_e$.
* **Application:** Provides complete self-sufficiency for laser drive pumping, cryogenic pellet injection, superconducting magnet refrigeration, and life-support power loops.



---

## 4. Smart Thermal Mitigation Strategies

After maximizing energy conversion, the remaining unconvertible waste thermal power ($\sim 200\text{--}240\text{ MW}_{\text{th}}$) must be rejected using smart structural and thermodynamic methods.

### Strategy A: High-Temperature Radiator Elevation ($800\text{ K} \to 1,200\text{ K}$)

Because radiative flux scales with $T^4$, shifting the heat pipe working fluid from liquid lithium at $800\text{ K}$ to liquid silicon/tin at $1,200\text{ K}$ dramatically increases specific heat emission:

$$q_{\text{1200K}} = 0.92 \cdot (5.670374 \times 10^{-8}) \cdot (1200)^4 = 108.18\text{ kW/m}^2$$

* **Area Reduction Factor:**

$$\left(\frac{1200}{800}\right)^4 = 5.0625\times \text{ increase in emission per unit area}$$

* **New Required Emitting Area:** $3,404.2\text{ m}^2$ (down from $17,233.89\text{ m}^2$).
* **New Radiator Dry Mass:** **$15.32\text{ metric tons}$** (a net saving of **$62.23\text{ tons}$**).

### Strategy B: Liquid Droplet Radiators (LDR)

* **Mechanism:** Eliminates heavy solid containment pipes by launching sub-millimeter streams of low-vapor-pressure liquid metal/salt droplets directly through open space. The droplets radiate heat directly to space and are collected magnetically or mechanically at a return manifold.
* **Mass Reduction:** Eliminates panel substrate mass, dropping structural areal density from $4.5\text{ kg/m}^2$ down to $< 0.8\text{ kg/m}^2$.

### Strategy C: Phase-Change Latent Heat Buffering (Burst Mode Operation)

* **Mechanism:** Integrates Lithium Hydride ($\text{LiH}$) phase-change thermal storage tanks (latent heat of fusion $\Delta H_{\text{fus}} \approx 2.7\text{ MJ/kg}$).
* **Operational Profile:** Absorbs peak thermal surges during high-thrust orbital insertion burns ($10\text{--}30\text{ minutes}$), holding waste heat in latent chemical bonds and trickling heat out via smaller radiators over multi-hour coast phases.

---

## 5. Quantitative Phase II / REV5 Trade Study Matrix

| Architecture Metric | Baseline REV4 (Current) | Engineered REV5 (Target) | Performance Delta / Benefit |
| --- | --- | --- | --- |
| **Operating Temp ($T_{\text{rad}}$)** | $800\text{ K}$ | $1,200\text{ K}$ | $+50\%\text{ Temperature elevation}$ |
| **Direct Energy Conversion (DEC)** | None (Passive Nozzle) | $50\%\text{ Efficient Inductive DEC}$ | $-62.5\text{ MW}_{\text{th}}$ Direct heat reduction |
| **Rejection Heat Load** | $368.25\text{ MW}_{\text{th}}$ | $210.00\text{ MW}_{\text{th}}$ | $-42.9\%\text{ Unmitigated thermal load}$ |
| **Specific Radiative Flux** | $21.37\text{ kW/m}^2$ | $108.18\text{ kW/m}^2$ | **$+406.2\%\text{ Flux efficiency}$** |
| **Total Surface Area ($A_{\text{rad}}$)** | $17,233.89\text{ m}^2$ | $1,941.20\text{ m}^2$ | **$-88.7\%\text{ Radiator footprint}$** |
| **Radiator System Mass ($M_{\text{rad}}$)** | $77.55\text{ Tons}$ | **$8.74\text{ Tons}$** | **$-68.81\text{ Metric Tons}$ mass saving** |
| **Radiator Mass Fraction** | **$77.55\%$ of Dry Mass** | **$8.74\%$ of Dry Mass** | **Vehicle Payload Capacity Increased $4\times$** |

---

## 6. Research & Engineering Next Steps

1. **2D MHD Pick-Up Coil Simulation:** Extend `solvers/mhd_nozzle_2d_blackwell.py` to model induced counter-EMF and coil inductance during plasma jet passage.
2. **High-Temperature Material Compatibility:** Assess carbon-composite degradation rates when exposed to liquid tin/silicon fluids at $1,200\text{--}1,400\text{ K}$.
3. **Droplet Collector Hydrodynamics:** Develop a Numba/PyTorch solver module for sub-millimeter droplet trajectory tracking under variable spacecraft acceleration vectors.

```
