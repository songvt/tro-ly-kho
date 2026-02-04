import pandas as pd
import streamlit as st
from utils.data_loader import load_data

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQYR3SYVD4hk4BasVIySZs9RPfVr4ijl0q2B7TUIwxN5oPQ7EKDziLCqLc11juIe5Zs6b-iJhEg6gIk/pub?gid=1456104723&single=true&output=csv"

print("--- DEBUGGING Data Loading ---")
try:
    df_raw = pd.read_csv(url)
    print("Raw Columns:", df_raw.columns.tolist())
    print("\nFirst 5 rows raw:")
    print(df_raw.head().to_string())
    
    print("\n--- Testing load_data function ---")
    df_clean = load_data(url)
    print("Clean Columns:", df_clean.columns.tolist())
    print("\nFirst 5 rows cleaned:")
    print(df_clean[['Tên hàng hóa', 'Từ serial']].head().to_string() if 'Tên hàng hóa' in df_clean.columns else "Column 'Tên hàng hóa' missing")
    
except Exception as e:
    print(f"Error: {e}")
