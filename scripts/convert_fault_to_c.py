import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import emlearn

# ==========================================
# 1. Load Data & Train Model
# ==========================================
print("Training AI model for C conversion...")
df = pd.read_csv('fault_features.csv')
X = df[['RMS_Current', 'Peak_Current', 'Max_di_dt', 'Zero_Sequence', 'HF_Energy']]
y = df['Label']

# We use 10 trees with max_depth=5 to keep the C code small enough for an STM32
# (We sacrifice a tiny bit of accuracy for a huge gain in memory efficiency)
model = RandomForestClassifier(n_estimators=10, max_depth=5, random_state=42)
model.fit(X, y)

# ==========================================
# 2. Convert to C Code
# ==========================================
print("Converting AI model to C code...")
cmodel = emlearn.convert(model, method='inline')

# Save as a C header file
cmodel.save(file='fault_model.h', name='fault_detection_model')

print("\nSuccess! Generated 'fault_model.h'.")
print("This file is ready to be included in your STM32 firmware.")