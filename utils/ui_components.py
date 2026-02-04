import streamlit as st
import pandas as pd

def inject_custom_css():
    """Injects the Enterprise-grade CSS into the Streamlit app."""
    st.markdown("""
    <style>
        /* --- GLOBAL FONTS --- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            /* REMOVED global color override to fix Dark Mode contrast issues */
        }

        /* --- THEME COLORS --- */
        :root {
            --primary-color: #0f172a; /* Slate 900 */
            --secondary-color: #3b82f6; /* Blue 500 */
            --accent-color: #10b981; /* Emerald 500 */
            --text-dark: #334155; /* Slate 700 */
            --border-color: #e2e8f0; /* Slate 200 */
        }

        /* --- HEADER STYLING --- */
        .main-header {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        /* In Dark Mode, gradients might be hard to see. Add a fallback/override for dark text */
        @media (prefers-color-scheme: dark) {
            .main-header {
                background: linear-gradient(135deg, #60a5fa 0%, #e2e8f0 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
        }
        
        .sub-header {
            font-size: 1rem;
            color: #64748b; /* Slate 500 */
            margin-bottom: 2rem;
        }

        /* --- CHAT INPUT --- */
        .stChatInput {
            border-radius: 12px !important;
        }
        /* Transparent floating input fix */
        .stChatFloatingInputContainer {
            background: rgba(255, 255, 255, 0.1); 
            backdrop-filter: blur(12px);
            padding-bottom: 24px;
        }

        /* --- ASSET CARD (The "Smart Display") --- */
        /* --- ASSET CARD (The "Smart Display") --- */
        .asset-card {
            background-color: #ffffff; 
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid #e2e8f0;
            margin-bottom: 1.5rem;
            color: #1a1a1a;
            transition: all 0.2s ease;
        }
        
        .asset-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 16px;
            padding-bottom: 16px;
            border-bottom: 1px solid #e2e8f0;
        }
        .asset-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #0f172a; /* Slate 900 */
            margin: 0;
        }
        .asset-id {
            font-size: 0.875rem;
            color: #64748b; /* Slate 500 */
            margin-top: 4px;
            font-family: monospace;
        }
        .detail-label {
            font-size: 0.75rem;
            color: #64748b;
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 4px;
        }
        .detail-value {
            font-size: 1rem;
            color: #334155; /* Slate 700 */
            font-weight: 500;
        }

        /* --- DARK MODE SUPPORT --- */
        @media (prefers-color-scheme: dark) {
            .asset-card {
                background-color: #1e293b !important; /* Slate 800 */
                border-color: #334155 !important;
                color: #f1f5f9 !important; /* Slate 100 */
            }
            .asset-header {
                border-bottom-color: #334155 !important;
            }
            .asset-title {
                color: #f8fafc !important; /* Slate 50 */
            }
            .asset-id {
                color: #94a3b8 !important; /* Slate 400 */
            }
            .detail-label {
                color: #94a3b8 !important; /* Slate 400 */
            }
            .detail-value {
                color: #e2e8f0 !important; /* Slate 200 */
            }
        }

        /* --- BADGES --- */
        .asset-badge {
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        .badge-success { background-color: #d1fae5; color: #065f46; }
        .badge-warning { background-color: #fef3c7; color: #92400e; }
        .badge-danger { background-color: #fee2e2; color: #991b1b; }
        .badge-neutral { background-color: #f1f5f9; color: #475569; } 
    </style>
    """, unsafe_allow_html=True)

def get_status_badge(status):
    """Returns the CSS class for a status badge."""
    s = str(status).lower()
    if 'mới' in s or 'tốt' in s or 'new' in s:
        return 'badge-success'
    elif 'hỏng' in s or 'lỗi' in s or 'hư' in s:
        return 'badge-danger'
    elif 'bảo hành' in s or 'sửa' in s:
        return 'badge-warning'
    return 'badge-neutral'

def render_asset_card(row):
    """Renders a single asset as a beautiful card."""
    # Data extraction
    name = row.get('Tên hàng hóa', 'Sản phẩm không tên')
    serial = row.get('Từ serial', 'N/A')
    # Handle both ID columns if present
    code = row.get('Mã hàng hóa', row.get('MÃ HÀNG HÓA', 'N/A'))
    status = row.get('Trạng thái', row.get('Trạng Thái Chuẩn', 'Không xác định'))
    
    # Optional fields
    holder = row.get('NHÂN VIÊN NHẬN', 'Chưa bàn giao')
    location = row.get('QUẬN/HUYỆN', 'Không xác định')
    warehouse = row.get('LOẠI KHO', '')

    badge_class = get_status_badge(status)

    # Note: Using unicode escapes for emojis to avoid encoding issues on Windows
    html = f"""
    <div class="asset-card">
        <div class="asset-header">
            <div>
                <h3 class="asset-title">\U0001F4E6 {name}</h3>
                <div class="asset-id">SN: {serial} • ID: {code}</div>
            </div>
            <span class="asset-badge {badge_class}">{status}</span>
        </div>
        <div class="asset-details">
            <div class="detail-item">
                <span class="detail-label">\U0001F464 Người giữ</span>
                <span class="detail-value">{holder}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">\U0001F4CD Vị trí</span>
                <span class="detail-value">{location} {f"({warehouse})" if warehouse else ""}</span>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_results_table(df):
    """Renders the data table with improved column config."""
    # Columns to specifically look for and configure
    # Map friendly names
    column_config = {
        "Tên hàng hóa": st.column_config.TextColumn("\U0001F4E6 Tên Sản Phẩm", width="large"),
        "Từ serial": st.column_config.TextColumn("\U0001F522 Serial", width="medium"),
        "NHÂN VIÊN NHẬN": st.column_config.TextColumn("\U0001F464 Người Giữ", width="medium"),
        "Trạng thái": st.column_config.TextColumn(label="\u26A1 Trạng Thái"), 
        "Trạng Thái Chuẩn": st.column_config.TextColumn(label="\u26A1 Trạng Thái"),
        "QUẬN/HUYỆN": st.column_config.TextColumn("\U0001F4CD Khu Vực"),
        "Mã hàng hóa": st.column_config.TextColumn("\U0001F516 Mã BH"),
        "Số lượng": st.column_config.NumberColumn("\U0001F4CA SL"),
    }
    
    # Filter for columns that actually exist in this DF
    existing_cols = [c for c in df.columns if c in column_config or c in [
        'Tên hàng hóa', 'Từ serial', 'NHÂN VIÊN NHẬN', 'Trạng thái', 'Trạng Thái Chuẩn', 'QUẬN/HUYỆN', 'Mã hàng hóa', 'Số lượng'
    ]]
    
    # Priority columns first
    priority_order = ['Tên hàng hóa', 'Từ serial', 'Trạng thái', 'Trạng Thái Chuẩn', 'NHÂN VIÊN NHẬN', 'QUẬN/HUYỆN', 'Số lượng']
    # Sort existing columns based on priority
    final_cols = sorted(existing_cols, key=lambda x: priority_order.index(x) if x in priority_order else 999)

    # Deduplicate Status if both exist (Prioritize 'Trạng thái')
    if 'Trạng thái' in final_cols and 'Trạng Thái Chuẩn' in final_cols:
        final_cols.remove('Trạng Thái Chuẩn')

    st.dataframe(
        df[final_cols],
        column_config=column_config,
        hide_index=True,
        use_container_width=True
    )

def render_sidebar_stats(df):
    """Calculates and displays simple stats in the sidebar."""
    if df.empty:
        return

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Thống kê nhanh")
    
    total_items = len(df)
    
    # Try to calculate 'Available' vs 'In Use'
    # This is rough logic based on typical column values
    status_col = 'Trạng thái' if 'Trạng thái' in df.columns else 'Trạng Thái Chuẩn'
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Tổng số", f"{total_items:,}")
    
    if status_col in df.columns:
        # Count 'Mới' or similar
        good_items = df[df[status_col].astype(str).str.lower().str.contains('mới|new|tốt', na=False)]
        with col2:
            st.metric("Hàng tốt", f"{len(good_items):,}")
    
    st.sidebar.markdown("---")
