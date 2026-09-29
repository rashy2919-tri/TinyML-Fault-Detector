import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import time

# ==========================================
# 1. Load Data
# ==========================================
df = pd.read_csv('fault_features.csv')
X = df[['RMS_Current', 'Peak_Current', 'Max_di_dt', 'Zero_Sequence', 'HF_Energy']]
y = df['Label']

# ==========================================
# 2. K-Fold Cross-Validation
# ==========================================
print("Running 5-Fold Cross-Validation...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')

print(f"Cross-Validation Scores: {cv_scores}")
print(f"Mean Accuracy: {cv_scores.mean() * 100:.2f}%")
print(f"Standard Deviation: {cv_scores.std() * 100:.2f}%")

# ==========================================
# 3. Noise Robustness Testing
# ==========================================
print("\nRunning Noise Robustness Testing...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

noise_levels = [0.0, 0.05, 0.10, 0.20, 0.30, 0.50]
accuracies = []

for noise in noise_levels:
    # Add random noise to the test set
    X_test_noisy = X_test + np.random.normal(0, noise * X_test.std(), X_test.shape)
    y_pred = model.predict(X_test_noisy)
    acc = accuracy_score(y_test, y_pred)
    accuracies.append(acc)
    print(f"  Noise Level {noise*100:.0f}% -> Accuracy: {acc*100:.2f}%")

# Plot Noise Robustness
plt.figure(figsize=(8, 5))
plt.plot([n*100 for n in noise_levels], [a*100 for a in accuracies], marker='o', color='purple', linewidth=2)
plt.title('Noise Robustness: AI Fault Detector')
plt.xlabel('Noise Level (% of Standard Deviation)')
plt.ylabel('Accuracy (%)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.ylim(0, 105)
plt.savefig('noise_robustness.png', dpi=300)
print("  -> Saved 'noise_robustness.png'")

# ==========================================
# 4. Baseline Comparison (Traditional Relay)
# ==========================================
print("\nComparing AI vs. Traditional Threshold Relay...")

# Traditional Relay Logic: If RMS Current > 15A OR Peak Current > 25A -> Trip (Fault)
# We will create a simple threshold-based classifier
def traditional_relay(X_data):
    predictions = []
    for _, row in X_data.iterrows():
        if row['RMS_Current'] > 15.0 or row['Peak_Current'] > 25.0:
            # It's a fault, but which one? Traditional relays can't tell!
            # We assume it trips (predicts 'ShortCircuit' as the most severe)
            predictions.append('ShortCircuit') 
        else:
            predictions.append('Normal')
    return np.array(predictions)

# Test Traditional Relay
y_pred_trad = traditional_relay(X_test)
acc_trad = accuracy_score(y_test, y_pred_trad)
acc_ai = accuracy_score(y_test, model.predict(X_test))

print(f"  Traditional Relay Accuracy: {acc_trad * 100:.2f}%")
print(f"  AI Model Accuracy:          {acc_ai * 100:.2f}%")

# Plot Comparison
plt.figure(figsize=(6, 5))
bars = plt.bar(['Traditional Relay', 'AI Model'], [acc_trad*100, acc_ai*100], color=['gray', 'green'])
plt.title('AI vs. Traditional Protection Relay')
plt.ylabel('Accuracy (%)')
plt.ylim(0, 110)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 2, f'{yval:.1f}%', ha='center', fontweight='bold')
plt.savefig('ai_vs_traditional.png', dpi=300)
print("  -> Saved 'ai_vs_traditional.png'")

print("\nValidation Complete! Check the generated PNG files.")