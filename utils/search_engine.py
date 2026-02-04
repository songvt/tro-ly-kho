from thefuzz import process, fuzz
import pandas as pd

def search_inventory(query, df):
    """
    Search inventory by Serial, Product Name, or Employee Name.
    Prioritizes Exact/Substring matches over Fuzzy matching.
    """
    if df.empty or query.strip() == "":
        return pd.DataFrame(), "Chưa có dữ liệu tìm kiếm."

    query = query.strip()
    query_lower = query.lower()
    
    # 1. EXACT SEARCH: Serial Number (Highest Priority)
    serial_match = df[df['Từ serial'].str.lower() == query_lower]
    if not serial_match.empty:
        return serial_match, f"Tìm thấy theo Serial: {query}"
        
    # 2. SUBSTRING SEARCH: Product Name (High Priority)
    # Finds "IP952" in "ATV_HISENSE_IP952..."
    prod_contain = df[df['Tên hàng hóa'].str.contains(query, case=False, na=False)]
    
    # 3. SUBSTRING SEARCH: Employee Name
    emp_contain = pd.DataFrame()
    if 'NHÂN VIÊN NHẬN' in df.columns:
        emp_contain = df[df['NHÂN VIÊN NHẬN'].str.contains(query, case=False, na=False)]

    # 4. SUBSTRING SEARCH: Product Code (Mã hàng hóa)
    code_contain = pd.DataFrame()
    if 'Mã hàng hóa' in df.columns:
        code_contain = df[df['Mã hàng hóa'].str.contains(query, case=False, na=False)]

    # 4b. SUBSTRING SEARCH: Unit/Warehouse (Kho đơn vị)
    unit_contain = pd.DataFrame()
    possible_unit_cols = ['QUẬN/HUYỆN', 'LOẠI KHO']
    for col in possible_unit_cols:
        if col in df.columns:
            matches = df[df[col].astype(str).str.contains(query, case=False, na=False)]
            if not matches.empty:
                unit_contain = pd.concat([unit_contain, matches])
    
    if not unit_contain.empty:
        unit_contain = unit_contain.drop_duplicates()

    # 5. SUBSTRING SEARCH: Serial (Fallback for partial serials)
    serial_contain = df[df['Từ serial'].str.contains(query, case=False, na=False)]

    # 6. COMBINED KEYWORD SEARCH (AND Logic)
    # Allows "42x Võ Minh Nhật" -> Finds items with "42x" AND "Võ Minh Nhật" in any field
    tokens = query.split()
    if len(tokens) > 1:
        # Start with all True
        full_mask = pd.Series([True] * len(df))
        
        # For each word, it must exist in AT LEAST ONE of the columns
        for token in tokens:
            token_mask = (
                df['Tên hàng hóa'].str.contains(token, case=False, na=False) |
                df['Từ serial'].str.contains(token, case=False, na=False)
            )
            if 'NHÂN VIÊN NHẬN' in df.columns:
                token_mask |= df['NHÂN VIÊN NHẬN'].str.contains(token, case=False, na=False)
            if 'Mã hàng hóa' in df.columns:
                 token_mask |= df['Mã hàng hóa'].str.contains(token, case=False, na=False)
            if 'Trạng thái' in df.columns:
                 token_mask |= df['Trạng thái'].str.contains(token, case=False, na=False)
            
            # Add Unit Search to Combined Logic
            possible_unit_cols = ['QUẬN/HUYỆN', 'LOẠI KHO']
            for col in possible_unit_cols:
                if col in df.columns:
                    token_mask |= df[col].astype(str).str.contains(token, case=False, na=False)

            # Combine with AND: The row must satisfy THIS token too
            full_mask = full_mask & token_mask

        combined_results = df[full_mask]
        if not combined_results.empty:
             return combined_results, f"Tìm thấy {len(combined_results)} kết quả tổng hợp cho: '{query}'"

    # COMBINE RESULTS
    # Priority: Product Name > Product Code > Employee > Serial
    
    if not prod_contain.empty:
        return prod_contain, f"Tìm thấy {len(prod_contain)} sản phẩm có tên chứa: '{query}'"
        
    if not code_contain.empty:
        return code_contain, f"Tìm thấy {len(code_contain)} sản phẩm có mã chứa: '{query}'"
    
    if not emp_contain.empty:
        return emp_contain, f"Tìm thấy {len(emp_contain)} tài sản của nhân viên: '{query}'"

    if not unit_contain.empty:
        # Group by Unit if possible for better message
        found_units = unit_contain['QUẬN/HUYỆN'].unique() if 'QUẬN/HUYỆN' in unit_contain.columns else []
        unit_str = ", ".join(str(u) for u in found_units[:3])
        return unit_contain, f"Tìm thấy {len(unit_contain)} kết quả tại kho/đơn vị: {unit_str}..."
        
    if not serial_contain.empty:
        return serial_contain, f"Tìm thấy Serial chứa: '{query}'"

    return pd.DataFrame(), """**🤔 Hmm, tôi không tìm thấy thông tin nào cho từ khóa này.**
    
Là **Trợ lý Kho chuyên nghiệp**, tôi gợi ý bạn:
1.  🔍 **Kiểm tra Serial:** Đảm bảo nhập đúng chính xác (vd: `21200...`).
2.  📦 **Tên sản phẩm:** Thử nhập tên ngắn gọn (vd: `Switch` thay vì `Switch 8 cổng...`).
3.  👤 **Tên nhân viên:** Nhập tên không dấu nếu có dấu không ra kết quả.

*Bạn hãy thử lại xem sao nhé!* 👇"""
