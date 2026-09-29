import numpy as np
import pandas as pd
import os

# ==========================================
# 1. Configuration
# ==========================================
DATASET_DIR = 'fault_dataset'
CLASSES = ['Normal', 'Overload', 'ShortCircuit', 'ArcFault']
OUTPUT_FILE = 'fault_features.csv'

# ==========================================
# 2. Feature Extraction Functions
# ==========================================
def calculate_rms(signal):
    return np.sqrt(np.mean(signal**2))

def calculate_max_didt(signal, fs):
    """Calculate maximum rate of change of current (di/dt)"""
    # np.diff calculates the difference between consecutive samples
    didt = np.diff(signal) * fs 
    return np.max(np.abs(didt))

def calculate_zero_sequence(ia, ib, ic):
    """Calculate zero-sequence current (Ia + Ib + Ic)"""
    i_zero = ia + ib + ic
    return np.sqrt(np.mean(i_zero**2))

def calculate_hf_energy(signal, fs):
    """Calculate high-frequency energy using FFT"""
    N = len(signal)
    yf = np.fft.fft(signal)
    xf = np.fft.fftfreq(N, 1/fs)
    
    # Get positive frequencies only
    idx = np.where(xf > 0)
    xf = xf[idx]
    yf = np.abs(yf[idx]) / N
    
    # Sum energy above 500 Hz (where arc faults live)
    hf_mask = xf > 500
    hf_energy = np.sum(yf[hf_mask]**2)
    return hf_energy

# ==========================================
# 3. Main Processing Loop
# ==========================================
def main():
    print("Starting fault feature extraction...")
    data = []
    
    for cls in CLASSES:
        cls_dir = os.path.join(DATASET_DIR, cls)
        files = [f for f in os.listdir(cls_dir) if f.endswith('.csv')]
        
        print(f"Processing {len(files)} files for class: {cls}...")
        
        for filename in files:
            filepath = os.path.join(cls_dir, filename)
            df = pd.read_csv(filepath)
            
            # Extract signals
            ia = df['Ia'].values
            ib = df['Ib'].values
            ic = df['Ic'].values
            t = df['time'].values
            fs = 1 / (t[1] - t[0])
            
            # Extract Features
            rms_a = calculate_rms(ia)
            peak_a = np.max(np.abs(ia))
            didt_a = calculate_max_didt(ia, fs)
            zero_seq = calculate_zero_sequence(ia, ib, ic)
            hf_energy = calculate_hf_energy(ia, fs)
            
            # Append to our list
            data.append({
                'RMS_Current': rms_a,
                'Peak_Current': peak_a,
                'Max_di_dt': didt_a,
                'Zero_Sequence': zero_seq,
                'HF_Energy': hf_energy,
                'Label': cls
            })
            
    # Save to CSV
    features_df = pd.DataFrame(data)
    features_df.to_csv(OUTPUT_FILE, index=False)
    
    print(f"\nSuccess! Extracted features saved to '{OUTPUT_FILE}'")
    print(f"Total rows in dataset: {len(features_df)}")
    print("\nSample of extracted features:")
    print(features_df.head())

if __name__ == "__main__":
    main()