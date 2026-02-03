import pandas as pd
import streamlit as st

@st.cache_data(ttl=600)  # Cache data for 10 minutes
def load_data(url):
    try:
        # Read CSV from URL
        df = pd.read_csv(url)
        
        # KEY STEP: Clean up the "merged cells" effect
        # Forward fill key columns that are only present in summary rows
        # The relevant columns based on analysis are: STT, Mã hàng hóa, Tên hàng hóa
        # But we should check if 'Tên hàng hóa' exists.
        
        cols_to_ffill = ['STT', 'Mã hàng hóa', 'Tên hàng hóa']
        
        # Verify columns exist before ffill
        existing_cols = [c for c in cols_to_ffill if c in df.columns]
        if existing_cols:
            df[existing_cols] = df[existing_cols].ffill()
            
        # Filter for rows that actually have a Serial Number
        # Based on CSV: "Từ serial" seems to be the column for Serial
        if 'Từ serial' in df.columns:
            # Drop rows where Serial is NaN (these might be just summary headers without items)
            # OR keep them if headers are useful, but for search we likely want items.
            # Let's clean it to only keep rows with valid data for search.
            df_items = df.dropna(subset=['Từ serial']).copy()
            
            # Standardize column types
            df_items['Từ serial'] = df_items['Từ serial'].astype(str).str.strip()
            if 'NHÂN VIÊN NHẬN' in df_items.columns:
                df_items['NHÂN VIÊN NHẬN'] = df_items['NHÂN VIÊN NHẬN'].astype(str).str.strip()
            
            return df_items
        else:
            return df # Return raw if 'Từ serial' not found, handle in UI
            
    except Exception as e:
        st.error(f"Lỗi khi tải dữ liệu: {e}")
        return pd.DataFrame()
