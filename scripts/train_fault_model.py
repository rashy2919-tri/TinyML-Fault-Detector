import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ==========================================
# 1. Load Data
# ==========================================
print("Loading fault dataset...")
df = pd.read_csv('fault_features.csv')

# Separate features (X) and labels (y)
X = df[['RMS_Current', 'Peak_Current', 'Max_di_dt', 'Zero_Sequence', 'HF_Energy']]
y = df['Label']

# ==========================================
# 2. Split Data
# ==========================================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training samples: {len(X_train)} | Testing samples: {len(X_test)}")

# ==========================================
# 3. Train AI Model
# ==========================================
print("\nTraining Random Forest Classifier for Protection...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ==========================================
# 4. Evaluate Model
# ==========================================
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n==========================================")
print(f"Model Accuracy: {accuracy * 100:.2f}%")
print(f"==========================================\n")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# ==========================================
# 5. Plot Confusion Matrix
# ==========================================
cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Reds', 
            xticklabels=model.classes_, yticklabels=model.classes_)
plt.title('Confusion Matrix - Electrical Fault Detection')
plt.xlabel('Predicted Fault')
plt.ylabel('True Fault')
plt.tight_layout()
plt.savefig('fault_confusion_matrix.png', dpi=300)
print("Confusion matrix saved as 'fault_confusion_matrix.png'")

# ==========================================
# 6. Show Feature Importance
# ==========================================
importances = model.feature_importances_
features = X.columns
print("\nFeature Importance (What the AI uses to detect faults):")
for feature, imp in zip(features, importances):
    print(f"  {feature}: {imp:.4f}")

plt.show()