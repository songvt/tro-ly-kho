import pandas as pd
import streamlit as st
from utils.data_loader import load_data
import sys

# Force utf-8 for stdout if possible, or use replace
sys.stdout.reconfigure(encoding='utf-8')

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQYR3SYVD4hk4BasVIySZs9RPfVr4ijl0q2B7TUIwxN5oPQ7EKDziLCqLc11juIe5Zs6b-iJhEg6gIk/pub?gid=1456104723&single=true&output=csv"

print("--- DEBUGGING Data Loading ---")
try:
    # df_raw = pd.read_csv(url)
    # print("Raw Columns:", [c.encode('utf-8', 'replace').decode('utf-8') for c in df_raw.columns])
    
    print("\n--- Testing load_data function ---")
    df_clean = load_data(url)
    print("Clean Columns:", [c for c in df_clean.columns])
    
    if 'Tên hàng hóa' in df_clean.columns:
        print("\nFirst 5 rows cleaned (Tên hàng hóa, Từ serial):")
        # Print row by row to avoid large string encoding issues
        subset = df_clean[['Tên hàng hóa', 'Từ serial']].head()
        for i, row in subset.iterrows():
            print(f"Row {i}: {row['Tên hàng hóa']} | {row['Từ serial']}")
    else:
        print("Column 'Tên hàng hóa' MISSING!")
    
except Exception as e:
    print(f"Error: {e}")
