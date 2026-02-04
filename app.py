import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.search_engine import search_inventory

# Page Config
st.set_page_config(page_title="Trợ Lý Kho AI", page_icon="🤖", layout="wide")

# Custom CSS
st.markdown("""
<style>
    /* Global Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Chat Input Container */
    .stChatFloatingInputContainer {
        bottom: 20px !important;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding-bottom: 20px;
    }
    
    /* Result Card Style */
    .result-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #f0f2f6;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        border-color: #4CAF50;
    }
    .card-title {
        color: #1a1a1a;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 8px;
    }
    .card-row {
        display: flex;
        justify-content: space-between;
        font-size: 0.9rem;
        color: #555;
        margin-bottom: 4px;
    }
    .card-label {
        font-weight: 500;
        color: #888;
    }
    .status-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    /* Header Gradient */
    .main-header {
        background: linear-gradient(90deg, #4CAF50 0%, #008CBA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Application Title
st.markdown("<h1 class='main-header'>🤖 Trợ Lý Kho AI</h1>", unsafe_allow_html=True)
st.caption("Tra cứu thông tin nhanh chóng - Chính xác - Tự động")

# Sidebar - Configuration
with st.sidebar:
    # Data Source Selection
    source_option = st.radio("Chọn Kho tra cứu", ["KHO NHÂN VIÊN", "KHO ĐƠN VỊ"])
    
    # URL Definitions
    public_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQYR3SYVD4hk4BasVIySZs9RPfVr4ijl0q2B7TUIwxN5oPQ7EKDziLCqLc11juIe5Zs6b-iJhEg6gIk/pub?gid=1456104723&single=true&output=csv"
    private_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQYR3SYVD4hk4BasVIySZs9RPfVr4ijl0q2B7TUIwxN5oPQ7EKDziLCqLc11juIe5Zs6b-iJhEg6gIk/pub?gid=1050267960&single=true&output=csv"
    
    selected_url = public_url
    is_authenticated = True

    if source_option == "KHO ĐƠN VỊ":
        password = st.text_input("🔑 Nhập mật khẩu quản trị:", type="password")
        if password == "150590":
            st.success("✅ Đã mở khóa dữ liệu riêng tư!")
            selected_url = private_url
            is_authenticated = True
        else:
            if password:
                st.error("⛔ Mật khẩu không đúng!")
            is_authenticated = False
            st.warning("🔒 Vui lòng nhập mật khẩu để truy cập.")

    st.markdown("### 📖 Hướng dẫn")
    st.info("""
    1. **Tìm Serial:** Nhập số Serial chính xác.
    2. **Tìm Tên:** Nhập một phần tên (vd: 'IP952').
    3. **Tìm Người:** Nhập tên nhân viên.
    """)
    st.markdown("---")
    st.caption("✅ Dữ liệu tự động cập nhật 10 phút/lần.")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "👋 Chào bạn! Bạn cần tìm thông tin gì hôm nay?"}]

# Main Application Logic
if is_authenticated:
    # Load Data
    with st.spinner("⏳ Đang tải dữ liệu kho..."):
        df = load_data(selected_url, is_private=(source_option == "KHO ĐƠN VỊ"))

    if df.empty:
        st.error("❌ Không thể tải dữ liệu. Vui lòng kiểm tra kết nối mạng.")
    else:
        # Data is already pre-processed by load_data
        pass

        # Display Chat
        for msg in st.session_state.messages:
            role_icon = "👤" if msg["role"] == "user" else "🤖"
            with st.chat_message(msg["role"], avatar=role_icon):
                st.markdown(msg["content"])
                # Render DataFrame if results exist
                if "results" in msg and msg["results"] is not None and not msg["results"].empty:
                     # Show limited columns for clarity
                    display_cols = ['Tên hàng hóa', 'Từ serial', 'NHÂN VIÊN NHẬN', 'Trạng thái', 'QUẬN/HUYỆN']
                    # Filter columns that actually exist
                    final_cols = [c for c in display_cols if c in msg["results"].columns]
                    st.dataframe(
                        msg["results"][final_cols],
                        column_config={
                            "Tên hàng hóa": st.column_config.TextColumn("Tên hàng hóa"),
                            "Từ serial": st.column_config.TextColumn("Từ serial"),
                            "NHÂN VIÊN NHẬN": st.column_config.TextColumn("NHÂN VIÊN NHẬN"),
                            "Trạng thái": st.column_config.TextColumn("Trạng thái"),
                            "QUẬN/HUYỆN": st.column_config.TextColumn("QUẬN/HUYỆN"),
                        },
                        hide_index=True
                    )

        # Chat Input
        if prompt := st.chat_input("🔍 Nhập Serial, Tên hàng, hoặc Tên nhân viên..."):
            # User message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)

            # Assistant processing
            with st.chat_message("assistant", avatar="🤖"):
                # Intent Detection
                clean_prompt = prompt.lower().strip()
                greetings = ["xin chào", "hello", "hi", "chào"]
                identity_words = ["bạn là ai", "là ai", "làm gì", "giới thiệu", "who are you"]
                help_words = ["hướng dẫn", "help", "cách dùng", "làm sao"]
                
                response_text = ""
                results_df = None
                
                if any(g == clean_prompt for g in greetings):
                    response_text = "**👋 Xin chào! Tôi là Trợ Lý Kho AI.**\n\nTôi ở đây để giúp bạn tra cứu thông tin tài sản, hàng hóa và nhân viên một cách nhanh nhất. Sếp cần tìm gì cứ bảo em nhé! 🚀"
                elif any(i in clean_prompt for i in identity_words):
                    response_text = """**🤖 Tôi là Trợ Lý Ảo Quản Lý Kho (AI Inventory Expert).**
                    
    Nhiệm vụ của tôi là:
    - 🕵️ **Tra cứu siêu tốc:** Tìm hàng hóa theo Serial, Tên hoặc Người giữ.
    - 📱 **Hỗ trợ đa nền tảng:** Hoạt động mượt mà trên cả Điện thoại và Máy tính.
    - 💡 **Hướng dẫn thông minh:** Gợi ý khi bạn tìm không thấy.
    
    *Hãy thử nhập **"IP952"** hoặc tên một nhân viên xem tôi làm được gì nhé!*"""
                elif any(h in clean_prompt for h in help_words):
                     response_text = """**💡 Mẹo tìm kiếm:**
    - Nhập **Serial** để tìm chính xác.
    - Nhập **Tên hàng** (ví dụ: `Camera`) để xem danh sách.
    - Nhập **Tên người** để xem tài sản họ đang giữ."""
                     st.markdown(response_text)
                else:
                    with st.spinner("🔍 Đang quét dữ liệu..."):
                        # Perform search
                        results, message = search_inventory(prompt, df)
                        
                        st.markdown(message)
                        response_text = message
                        
                        if not results.empty:
                            results_df = results
                            # Show limited columns for clarity
                            display_cols = ['Tên hàng hóa', 'Từ serial', 'NHÂN VIÊN NHẬN', 'Trạng thái', 'QUẬN/HUYỆN']
                            # Filter columns that actually exist
                            final_cols = [c for c in display_cols if c in results_df.columns]
                            st.dataframe(
                                results_df[final_cols],
                                column_config={
                                    "Tên hàng hóa": st.column_config.TextColumn("Tên hàng hóa"),
                                    "Từ serial": st.column_config.TextColumn("Từ serial"),
                                    "NHÂN VIÊN NHẬN": st.column_config.TextColumn("NHÂN VIÊN NHẬN"),
                                    "Trạng thái": st.column_config.TextColumn("Trạng thái"),
                                    "QUẬN/HUYỆN": st.column_config.TextColumn("QUẬN/HUYỆN"),
                                },
                                hide_index=True
                            )

            # Save assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response_text, "results": results_df})
else:
    # If not authenticated, we just show a friendly message or nothing (sidebar handles the error)
    st.markdown("### 🔒 Khu vực hạn chế\nVui lòng nhập mật khẩu chính xác bên thanh điều hướng để truy cập dữ liệu này.")
