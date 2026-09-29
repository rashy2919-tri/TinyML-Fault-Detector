import numpy as np
import pandas as pd
import os

# ==========================================
# 1. Configuration
# ==========================================
fs = 10000          # Sampling frequency (10 kHz) - standard for protection relays
duration = 0.2      # 200 ms (10 cycles at 50Hz)
t = np.arange(0, duration, 1/fs)
f0 = 50             # Nominal frequency (50 Hz)
I_nominal = 10      # Nominal RMS current (Amps)
I_peak = I_nominal * np.sqrt(2)

N_SAMPLES = 50      # Start with 50 per class for testing
OUTPUT_DIR = 'fault_dataset'

# ==========================================
# 2. Fault Generation Functions
# ==========================================
def add_noise(signal, noise_level=0.02):
    """Adds realistic Gaussian noise"""
    noise = np.random.normal(0, noise_level * I_peak, len(signal))
    return signal + noise

def generate_normal(t):
    """Normal 3-phase balanced current"""
    Ia = I_peak * np.sin(2 * np.pi * f0 * t)
    Ib = I_peak * np.sin(2 * np.pi * f0 * t - 2*np.pi/3)
    Ic = I_peak * np.sin(2 * np.pi * f0 * t + 2*np.pi/3)
    return Ia, Ib, Ic

def generate_overload(t):
    """Overload: Current increases to 1.5x - 3x nominal"""
    factor = np.random.uniform(1.5, 3.0)
    Ia = (I_peak * factor) * np.sin(2 * np.pi * f0 * t)
    Ib = (I_peak * factor) * np.sin(2 * np.pi * f0 * t - 2*np.pi/3)
    Ic = (I_peak * factor) * np.sin(2 * np.pi * f0 * t + 2*np.pi/3)
    return Ia, Ib, Ic

def generate_short_circuit(t):
    """Short Circuit: Massive spike in current (5x - 20x nominal)"""
    factor = np.random.uniform(5.0, 20.0)
    t_fault = 0.05 # Fault occurs at 50ms
    Ia = I_peak * np.sin(2 * np.pi * f0 * t)
    Ib = I_peak * np.sin(2 * np.pi * f0 * t - 2*np.pi/3)
    Ic = I_peak * np.sin(2 * np.pi * f0 * t + 2*np.pi/3)
    
    # Inject fault into Phase A
    mask = t >= t_fault
    Ia[mask] = (I_peak * factor) * np.sin(2 * np.pi * f0 * t[mask])
    return Ia, Ib, Ic

def generate_arc_fault(t):
    """Arc Fault: High-frequency noise superimposed on the current"""
    Ia = I_peak * np.sin(2 * np.pi * f0 * t)
    Ib = I_peak * np.sin(2 * np.pi * f0 * t - 2*np.pi/3)
    Ic = I_peak * np.sin(2 * np.pi * f0 * t + 2*np.pi/3)
    
    # Arc fault adds high-frequency chaotic noise
    mask = (t >= 0.05) & (t <= 0.15)
    arc_noise = np.random.normal(0, 0.5 * I_peak, len(t[mask]))
    Ia[mask] += arc_noise
    return Ia, Ib, Ic

# ==========================================
# 3. Dataset Generation Loop
# ==========================================
def main():
    print("Starting Fault Dataset Generation...")
    classes = ['Normal', 'Overload', 'ShortCircuit', 'ArcFault']
    
    for cls in classes:
        cls_dir = os.path.join(OUTPUT_DIR, cls)
        os.makedirs(cls_dir, exist_ok=True)
        print(f"Generating {N_SAMPLES} samples for class: {cls}...")
        
        for i in range(N_SAMPLES):
            if cls == 'Normal':
                Ia, Ib, Ic = generate_normal(t)
            elif cls == 'Overload':
                Ia, Ib, Ic = generate_overload(t)
            elif cls == 'ShortCircuit':
                Ia, Ib, Ic = generate_short_circuit(t)
            elif cls == 'ArcFault':
                Ia, Ib, Ic = generate_arc_fault(t)
            
            # Add noise to all signals (realistic measurement)
            Ia = add_noise(Ia)
            Ib = add_noise(Ib)
            Ic = add_noise(Ic)
            
            # Save to CSV
            df = pd.DataFrame({
                'time': t,
                'Ia': Ia, 'Ib': Ib, 'Ic': Ic
            })
            filename = os.path.join(cls_dir, f'{cls}_{i:04d}.csv')
            df.to_csv(filename, index=False)
            
    print(f"\nSuccess! Dataset generated in '{OUTPUT_DIR}' folder.")
    print(f"Total files: {N_SAMPLES * len(classes)}")

if __name__ == "__main__":
    main()