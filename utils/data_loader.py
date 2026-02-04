import pandas as pd
import streamlit as st

@st.cache_data(ttl=600)  # Cache data for 10 minutes
def load_data(url, is_private=False):
    try:
        # Read CSV from URL
        df = pd.read_csv(url)
        
        # 0. Clean Column Names (Strip whitespace)
        df.columns = df.columns.str.strip()
        
        # 1. Forward Fill (Handle merged cells)
        # This is CRITICAL for both private and public sheets with this structure
        # We forward fill key info from the "Summary Row" down to the "Detail Rows"
        cols_to_ffill = ['STT', 'Mã hàng hóa', 'Tên hàng hóa', 'NHÂN VIÊN NHẬN', 'Trạng thái', 'QUẬN/HUYỆN']
        
        # Only ffill columns that actually exist
        existing_cols = [c for c in cols_to_ffill if c in df.columns]
        if existing_cols:
            df[existing_cols] = df[existing_cols].ffill()

        # 2. Filter for Rows with Serial Numbers
        # The actual items are in rows where "Từ serial" is present
        if 'Từ serial' in df.columns:
            # First, drop rows where Serial is NaN
            df_items = df.dropna(subset=['Từ serial']).copy()
            
            # Clean up empty strings if any
            df_items['Từ serial'] = df_items['Từ serial'].astype(str).str.strip()
            df_items = df_items[df_items['Từ serial'] != '']
            
            # Additional cleanup for display
            if 'NHÂN VIÊN NHẬN' in df_items.columns:
                df_items['NHÂN VIÊN NHẬN'] = df_items['NHÂN VIÊN NHẬN'].astype(str).str.strip()
                
            return df_items
            
        else:
            return df

    except Exception as e:
        st.error(f"Lỗi khi tải dữ liệu: {e}")
        return pd.DataFrame()
