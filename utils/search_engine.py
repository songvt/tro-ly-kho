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

    # 5. SUBSTRING SEARCH: Serial (Fallback for partial serials)
    serial_contain = df[df['Từ serial'].str.contains(query, case=False, na=False)]

    # COMBINE RESULTS
    # Priority: Product Name > Product Code > Employee > Serial
    
    if not prod_contain.empty:
        return prod_contain, f"Tìm thấy {len(prod_contain)} sản phẩm có tên chứa: '{query}'"
        
    if not code_contain.empty:
        return code_contain, f"Tìm thấy {len(code_contain)} sản phẩm có mã chứa: '{query}'"
    
    if not emp_contain.empty:
        return emp_contain, f"Tìm thấy {len(emp_contain)} tài sản của nhân viên: '{query}'"
        
    if not serial_contain.empty:
        return serial_contain, f"Tìm thấy Serial chứa: '{query}'"

    return pd.DataFrame(), f"Không tìm thấy thông tin nào cho từ khóa: '{query}'"
