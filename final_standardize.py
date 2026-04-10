import pandas as pd
import os

csv_path = r'datasets\AP_DATASET.CSV'

if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found.")
    exit(1)

# Load the 7,166-row dataset using TAB as separator (discovered from hex check)
try:
    df = pd.read_csv(csv_path, sep='\t')
    df.columns = df.columns.str.strip()
    print(f"Loaded dataset with {len(df)} rows (TAB separated).")
except Exception as e:
    # Fallback to Comma if Tab fails
    print(f"Tab loading failed ({e}). Trying comma...")
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()
    print(f"Loaded dataset with {len(df)} rows (COMMA separated).")

# 1. Unify NTR District to Vijayawada
mask_vj = (df['District_Name'].astype(str).str.contains("NTR", case=False, na=False))
df.loc[mask_vj, 'City_Name'] = "Vijayawada"
print(f"Mapped {sum(mask_vj)} rows in NTR district to 'Vijayawada'.")

# 2. Unify Chittoor District to Tirupati
mask_tiru = (df['District_Name'].astype(str).str.contains("Chittoor|Tirupati", case=False, na=False))
df.loc[mask_tiru, 'City_Name'] = "Tirupati"
print(f"Mapped {sum(mask_tiru)} rows in Chittoor district to 'Tirupati'.")

# 3. Clean strings
for col in df.select_dtypes(include=['object']):
    df[col] = df[col].astype(str).str.strip()

# 4. Save as COMMA SEPARATED for app compatibility
df.to_csv(csv_path, index=False)

print(f"Dataset successfully standardized and converted to COMMA-separated. Total rows: {len(df)}.")
