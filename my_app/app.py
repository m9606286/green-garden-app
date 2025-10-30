# ✅ 完整整合後程式碼（包含 easier selectbox 寫法）
# ⚠️ 此檔案僅示範 AgGrid + 編輯/刪除客戶資料

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from supabase import create_client

# ---------- ✅ Supabase Client ----------
url = st.secrets["supabase_url"]
key = st.secrets["supabase_key"]
supabase = create_client(url, key)

# ---------- ✅ Supabase CRUD function ----------
def update_customer(customer_id, update_data):
    supabase.table("customers").update(update_data).eq("id", customer_id).execute()

def delete_customer(customer_id):
    supabase.table("customers").delete().eq("id", customer_id).execute()

# ---------- ✅ 讀資料 ----------
response = supabase.table("customers").select("*").execute()
df = pd.DataFrame(response.data)

# ---------- ✅ AgGrid 設定 ----------
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination()
gb.configure_selection(selection_mode="single", use_checkbox=True)
gb.configure_default_column(resizable=True, filter=True, sortable=True)
gb.configure_column("client_name", pinned="left")  # 凍結姓名欄

grid_options = gb.build()

# ---------- ✅ 顯示表格 ----------
st.subheader("客戶清單")
grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    allow_unsafe_jscode=True,
    height=450,
)

selected_rows = grid_response["selected_rows"]

# ---------- ✅ 編輯 / 刪除 UI ----------
if selected_rows:

    selected_customer = selected_rows[0]
    st.markdown("---")
    st.subheader(f"操作客戶：{selected_customer['client_name']}")

    col1, col2 = st.columns([1, 1])

    # ======================== ✏️ 編輯客戶 =========================
    with col1:
        if st.button("✏️ 編輯客戶資料"):

            with st.form("edit_customer_form"):
                st.write("### 修改客戶資料")

                gender_options = ["男", "女"]
                current_gender = selected_customer.get("gender", "男")
                try:
                    gender_index = gender_options.index(current_gender)
                except ValueError:
                    gender_index = 0

                status_options = ["尚未聯絡", "已聯絡", "已成交", "拒絕"]
                current_status = selected_customer.get("current_status", "尚未聯絡")
                try:
                    status_index = status_options.index(current_status)
                except ValueError:
                    status_index = 0

                new_name = st.text_input("客戶姓名", value=selected_customer['client_name'])
                new_gender = st.selectbox("性別", gender_options, index=gender_index)
                new_relation = st.text_input("關係", value=selected_customer['relation'])

                new_birthday = st.date_input(
                    "生日", value=pd.to_datetime(selected_customer['birthday'])
                )
                new_address = st.text_input("居住地址", value=selected_customer['address'])
                new_phone = st.text_input("手機號碼", value=selected_customer['phone'])
                new_email = st.text_input("Email", value=selected_customer['email'])

                new_proposal_date = st.date_input(
                    "建議書日期",
                    value=pd.to_datetime(selected_customer['latest_proposal_date'])
                )

                new_proposal_amount = st.number_input(
                    "建議書金額(含管)",
                    value=selected_customer.get('latest_proposal_amount', 0)
                )

                new_status = st.selectbox(
                    "目前狀況", status_options, index=status_index
                )

                submitted_edit = st.form_submit_button("💾 存檔")
                if submitted_edit:
                    update_data = {
                        "client_name": new_name,
                        "gender": new_gender,
                        "relation": new_relation,
                        "birthday": new_birthday.strftime("%Y-%m-%d"),
                        "address": new_address,
                        "phone": new_phone,
                        "email": new_email,
                        "latest_proposal_date": new_proposal_date.strftime("%Y-%m-%d"),
                        "latest_proposal_amount": new_proposal_amount,
                        "current_status": new_status
                    }
                    update_customer(selected_customer['id'], update_data)
                    st.success("✅ 客戶資料已更新")
                    st.experimental_rerun()

    # ======================== 🗑️ 刪除客戶 =========================
    with col2:
        if st.button("🗑️ 刪除客戶"):
            confirm = st.checkbox("⚠️ 確認刪除？(不可恢復)")
            if confirm:
                delete_customer(selected_customer['id'])
                st.success("❌ 客戶已刪除！")
                st.experimental_rerun()

else:
    st.info("請在左側表格勾選客戶進行操作 ✅")
