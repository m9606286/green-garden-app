import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="綠金園建議書試算", layout="centered")
st.title("💼 綠金園商品建議書試算系統")

# 1️⃣ 客戶輸入
name = st.text_input("客戶姓名")
budget = st.number_input("預算（萬元）", min_value=0)
payment_method = st.selectbox("付款方式", ["單筆", "分期"])

# 2️⃣ 試算邏輯範例
if budget > 100:
    plan = "方案 A - 高階配置"
    total = budget * 1.05
else:
    plan = "方案 B - 標準配置"
    total = budget * 1.02

monthly = total / 12 if payment_method == "分期" else total

# 3️⃣ 顯示建議書結果
st.subheader("建議方案")
st.write(f"客戶姓名：{name}")
st.write(f"推薦方案：{plan}")
st.write(f"總價（含管理費）：{total:.2f} 萬元")
st.write(f"月繳金額：{monthly:.2f} 萬元")