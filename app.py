import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.search_engine import search_inventory

# Page Config
st.set_page_config(page_title="Trợ Lý Kho AI", page_icon="🤖", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stChatFloatingInputContainer {bottom: 20px !important;}
    .block-container {padding-top: 2rem;}
</style>
""", unsafe_allow_html=True)

# Application Title
st.title("🤖 Trợ Lý AI Tra Cứu Hàng Hóa")
st.caption("Tra cứu thông tin theo Serial, Tên hàng, hoặc Nhân viên.")

# Sidebar - Configuration
with st.sidebar:
    # Hardcoded Data Source
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQYR3SYVD4hk4BasVIySZs9RPfVr4ijl0q2B7TUIwxN5oPQ7EKDziLCqLc11juIe5Zs6b-iJhEg6gIk/pub?gid=1456104723&single=true&output=csv"
    
    # st.header("⚙️ Cấu hình") 
    # Hidden for public view - Data auto-refreshes every 10 minutes
    
    st.markdown("**Hướng dẫn:**")
    st.markdown("1. Nhập **Serial** để tìm chính xác.")
    st.markdown("2. Nhập **Tên hàng** (ví dụ: 'Camera').")
    st.markdown("3. Nhập **Tên nhân viên** để xem tài sản họ giữ.")
    st.markdown("---")
    st.caption("Dữ liệu tự động cập nhật 10 phút/lần.")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Chào bạn! Tôi có thể giúp gì cho bạn hôm nay? (Hãy nhập Serial hoặc Tên hàng hóa)"}]

# Load Data
with st.spinner("Đang tải dữ liệu từ Google Sheet..."):
    df = load_data(sheet_url)

if df.empty:
    st.error("Không thể tải dữ liệu. Vui lòng kiểm tra đường link.")
else:
    # Display Chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            # Check if there are results to display
            if "results" in msg and msg["results"] is not None and not msg["results"].empty:
                 # Show limited columns for clarity
                display_cols = ['Tên hàng hóa', 'Từ serial', 'NHÂN VIÊN NHẬN', 'Trạng thái', 'QUẬN/HUYỆN']
                # Filter columns that actually exist
                final_cols = [c for c in display_cols if c in msg["results"].columns]
                st.dataframe(msg["results"][final_cols], use_container_width=True, hide_index=True)


    # Chat Input
    if prompt := st.chat_input("Nhập thông tin tra cứu..."):
        # User message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Assistant processing
        with st.chat_message("assistant"):
            with st.spinner("Đang tìm kiếm..."):
                
                # Simple Intent Detection
                clean_prompt = prompt.lower().strip()
                greetings = ["xin chào", "hello", "hi", "chào"]
                help_words = ["hướng dẫn", "help", "cách dùng"]
                
                response_text = ""
                results_df = None
                
                if any(g in clean_prompt for g in greetings):
                    response_text = "Chào bạn! Tôi là Trợ lý Kho AI. Hãy nhập Serial, Tên hàng hóa, hoặc Tên nhân viên để tôi tìm kiếm giúp bạn nhé."
                elif any(h in clean_prompt for h in help_words):
                     response_text = """**Hướng dẫn sử dụng:**
1. **Tìm theo Serial:** Nhập chính xác số Serial (ví dụ: `CN12345`).
2. **Tìm theo Tên hàng:** Nhập tên sản phẩm (ví dụ: `Camera`, `Switch`).
3. **Tìm theo Nhân viên:** Nhập tên nhân viên để xem tài sản họ đang giữ.
"""
                else:
                    # Perform search
                    results, message = search_inventory(prompt, df)
                    
                    st.markdown(message)
                    
                    if not results.empty:
                        results_df = results
                        # Add result count to history message
                        response_text = f"{message}\n\nTìm thấy **{len(results)}** kết quả."
                    else:
                        response_text = message

                if response_text:
                    st.markdown(response_text)
                    if results_df is not None:
                         # Show limited columns for clarity
                        display_cols = ['Tên hàng hóa', 'Từ serial', 'NHÂN VIÊN NHẬN', 'Trạng thái', 'QUẬN/HUYỆN']
                        # Filter columns that actually exist
                        final_cols = [c for c in display_cols if c in results_df.columns]
                        st.dataframe(results_df[final_cols], use_container_width=True, hide_index=True)

        # Save assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response_text, "results": results_df})
