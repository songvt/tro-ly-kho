import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.search_engine import search_inventory
from utils.ui_components import inject_custom_css, render_asset_card, render_results_table, render_sidebar_stats

# Page Config
st.set_page_config(page_title="Trợ Lý Kho AI", page_icon="📦", layout="wide")

# Inject Enterprise CSS
inject_custom_css()

# Application Title
st.markdown("<div class='main-header'>🤖 Trợ Lý Kho AI</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Hệ thống tra cứu tài sản thông minh & chuyên nghiệp</div>", unsafe_allow_html=True)

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Cấu hình")
    
    # Data Source Selection
    source_option = st.radio("Nguồn dữ liệu", ["KHO NHÂN VIÊN", "KHO ĐƠN VỊ"], captions=["Dữ liệu công khai", "Dữ liệu nội bộ"])
    
    # URL Definitions
    public_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQYR3SYVD4hk4BasVIySZs9RPfVr4ijl0q2B7TUIwxN5oPQ7EKDziLCqLc11juIe5Zs6b-iJhEg6gIk/pub?gid=1456104723&single=true&output=csv"
    private_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQYR3SYVD4hk4BasVIySZs9RPfVr4ijl0q2B7TUIwxN5oPQ7EKDziLCqLc11juIe5Zs6b-iJhEg6gIk/pub?gid=1050267960&single=true&output=csv"
    
    selected_url = public_url
    is_authenticated = True

    if source_option == "KHO ĐƠN VỊ":
        password = st.text_input("🔒 Mật khẩu quản trị", type="password", placeholder="Nhập mật khẩu...")
        if password == "150590":
            st.success("Đã xác thực quyền truy cập")
            selected_url = private_url
            is_authenticated = True
        else:
            if password:
                st.error("Mật khẩu không đúng")
            is_authenticated = False
            st.info("Vui lòng nhập mật khẩu để xem dữ liệu kho đơn vị.")

    st.markdown("---")
    st.markdown("### 💡 Mẹo tìm kiếm")
    st.caption("""
    - **Tìm nhanh:** Nhập Serial (vd: `215...`)
    - **Tìm sản phẩm:** Nhập tên (vd: `Camera`)
    - **Tìm người:** Nhập tên nhân viên
    """)

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "👋 Xin chào! Tôi có thể giúp gì cho bạn hôm nay?"}]

# Main Application Logic
if is_authenticated:
    # Load Data
    with st.spinner("⏳ Đang đồng bộ dữ liệu..."):
        df = load_data(selected_url, is_private=(source_option == "KHO ĐƠN VỊ"))

    if df.empty:
        st.error("⚠️ Không thể tải dữ liệu. Vui lòng kiểm tra kết nối internet.")
    else:
        # Show stats in sidebar
        render_sidebar_stats(df)

        # Display Chat History
        for msg in st.session_state.messages:
            role_icon = "👤" if msg["role"] == "user" else "🤖"
            with st.chat_message(msg["role"], avatar=role_icon):
                st.markdown(msg["content"])
                
                # Render Results if they exist
                if "results" in msg and msg["results"] is not None and not msg["results"].empty:
                    results_df = msg["results"]
                    # If single result, show beautiful card
                    if len(results_df) == 1:
                        render_asset_card(results_df.iloc[0])
                    else:
                        render_results_table(results_df)

        # Chat Input
        if prompt := st.chat_input("🔍 Nhập thông tin cần tra cứu..."):
            # Display User Message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)

            # Assistant Processing
            with st.chat_message("assistant", avatar="🤖"):
                # Intent Detection
                clean_prompt = prompt.lower().strip()
                greetings = ["xin chào", "hello", "hi", "chào", "ola"]
                
                response_text = ""
                results_df = None
                
                if any(g == clean_prompt for g in greetings):
                    response_text = "Chào bạn! Tôi là trợ lý kho AI. Bạn cần tìm kiếm thông tin thiết bị hay nhân viên nào không? 🚀"
                    st.markdown(response_text)
                else:
                    with st.spinner("🔍 Đang tìm kiếm trong kho dữ liệu..."):
                        # Perform search
                        results, message = search_inventory(prompt, df)
                        
                        st.markdown(message)
                        response_text = message
                        
                        if not results.empty:
                            results_df = results
                            if len(results) == 1:
                                render_asset_card(results.iloc[0])
                            else:
                                render_results_table(results)

            # Save to history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response_text, 
                "results": results_df
            })

else:
    st.warning("⛔ Khu vực hạn chế. Vui lòng xác thực ở thanh bên trái.")

