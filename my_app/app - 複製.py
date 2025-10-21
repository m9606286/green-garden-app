import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import requests
import io

# 頁面配置
st.set_page_config(
    page_title="規劃配置建議書",
    page_icon="📋",
    layout="wide"
)

# 樣式設置
st.markdown("""
<style>
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 2rem;
        position: relative;
    }
    .title-container {
        text-align: center;
        flex-grow: 1;
    }
    .main-title {
        font-size: 1.2rem;
        color: #2E8B57;
        font-weight: bold;
        margin: 0;
    }
    .section-header {
        font-size: 1.3rem;
        color: #2E8B57;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #2E8B57;
        padding-bottom: 0.5rem;
    }
    .discount-text {
        color: #FF4444;
        font-weight: bold;
    }
    .installment-item {
        font-size: 1.1rem;
        margin: 0.5rem 0;
        font-weight: bold;
        padding: 0.5rem;
        background-color: #f8f9fa;
        border-radius: 0.3rem;
    }
    .dataframe thead th {
        text-align: center !important;
        font-size: 0.9rem;
        white-space: nowrap;
    }
    .dataframe tbody td {
        text-align: right !important;
        font-size: 0.85rem;
    }
    .dataframe tbody td:first-child {
        text-align: left !important;
    }
    .logo-top-right {
        position: absolute;
        top: 0;
        right: 0;
    }
    .client-info-content {
        font-size: 1rem;
        line-height: 1.6;
    }
    .analysis-title {
        font-size: 1.3rem;
        color: #2E8B57;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-align: left;
    }
    .analysis-content {
        font-size: 1rem;
        line-height: 1.4;
        text-align: left;
    }
    .disclaimer {
        font-size: 0.9rem;
        color: #666;
        text-align: center;
        margin: 1rem 0;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        border-left: 4px solid #2E8B57;
    }
    .compact-table {
        font-size: 0.7rem;
    }
    .compact-table th {
        padding: 3px 4px !important;
        font-size: 0.65rem;
    }
    .compact-table td {
        padding: 3px 4px !important;
        font-size: 0.65rem;
    }
    .half-width-table {
        width: 50% !important;
        margin: 0 auto;
    }
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 2rem;
        border: 1px solid #ddd;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

class AuthorizationSystem:
    def __init__(self, excel_url=None):
        # 預設的Excel檔案URL（放在GitHub上）
        self.excel_url = excel_url or "https://raw.githubusercontent.com/m9606286/green-garden-app/main/my_app/在職業務名單.xlsx"
        self.authorized_agents = self.load_authorized_agents()
    
    def load_authorized_agents(self):
        """從Git上的Excel檔案載入授權的業務員資料"""
        # 下載Excel檔案
        response = requests.get(self.excel_url)
        response.raise_for_status()
            
        # 讀取Excel檔案
        df = pd.read_excel(io.BytesIO(response.content))
            
        # 直接處理資料，不檢查欄位
        authorized_dict = {}
        for _, row in df.iterrows():
            agent_id = str(row['業務身份證字號']).strip().upper()
            agent_name = str(row['業務姓名']).strip()
            office = str(row['營業處']).strip()
            
            authorized_dict[agent_id] = {
                'name': agent_name,
                'office': office,
                'status': 'active'
            }
        return authorized_dict
    
    def verify_agent(self, agent_id):
        """驗證業務員身份證字號"""
        agent_id = str(agent_id).strip().upper()
        if agent_id in self.authorized_agents:
            agent_info = self.authorized_agents[agent_id]
            if agent_info.get('status') == 'active':
                return agent_info
        return None
    
    def display_login_page(self):
        """顯示登入頁面"""
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # 標題和logo
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            try:
                st.image("https://raw.githubusercontent.com/m9606286/green-garden-app/main/my_app/綠金園.png", width=100)
            except:
                st.markdown("""
                <div style="width: 100px; height: 100px; background: #2E8B57; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; margin: 0 auto;">
                    綠金園
                </div>
                """, unsafe_allow_html=True)
        
        st.title("🔐 業務系統登入")
        st.markdown('<p style="color: #666;">請輸入身份證字號進行驗證</p>', unsafe_allow_html=True)
        
        # 登入表單
        with st.form("login_form"):
            id_number = st.text_input(
                "身份證字號", 
                placeholder="請輸入您的身份證字號",
                help="請輸入完整的身份證字號（英文字母大寫）"
            )
            submit_button = st.form_submit_button("登入系統", use_container_width=True)
            
            if submit_button:
                if id_number:
                    agent_info = self.verify_agent(id_number)
                    if agent_info:
                        st.session_state.authorized = True
                        st.session_state.agent_id = id_number.upper()
                        st.session_state.agent_info = agent_info
                        st.success(f"✅ 驗證成功！歡迎 {agent_info['name']}")
                        st.rerun()
                    else:
                        st.error("❌ 身份證字號未授權，請聯繫管理員")
                else:
                    st.warning("⚠️ 請輸入身份證字號")
               
        # 使用說明
        with st.expander("💡 使用說明"):
            st.markdown("""
            **登入說明：**
            1. 請輸入您的身份證字號（英文字母請大寫）
            2. 系統會自動驗證您的授權狀態
            3. 驗證成功後即可使用系統功能
            
            **遇到問題？**
            - 確認身份證字號輸入正確
            - 確認英文字母為大寫
            - 如持續無法登入，請聯繫系統管理員
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

# 其餘的 GreenGardenProposal 類別保持不變...
class GreenGardenProposal:
    def __init__(self):
        self.cemetery_products = self._init_cemetery_products()
        self.memorial_products = self._init_memorial_products()
        self.down_payments = self._init_down_payments()
        self.management_down_payments = self._init_management_down_payments()

    def _init_cemetery_products(self):
        return {
            "澤茵園": {
                "單人位": {"定價": 460000, "預購-現金價": 276000, "分期價": 292560, "馬上使用-現金價": 368000, "分期期數": 24, "管理費": 50200},
                "貴族2人": {"定價": 620000, "預購-現金價": 372000, "分期價": 394320, "馬上使用-現金價": 496000, "分期期數": 24, "管理費": 67700},
                "家福4人": {"定價": 950000, "預購-現金價": 570000, "分期價": 598500, "馬上使用-現金價": 760000, "分期期數": 24, "管理費": 103700},
                "家族6人": {"定價": 1300000, "預購-現金價": 780000, "分期價": 819000, "馬上使用-現金價": 1040000, "分期期數": 24, "管理費": 142000}
            },
            "聚賢閣": {
                "12人": {"定價": 3200000, "預購-現金價": 1888000, "分期價": 1982400, "馬上使用-現金價": 2560000, "分期期數": 42, "管理費": 349000},
                "18人": {"定價": 3800000, "預購-現金價": 2356000, "分期價": 2473800, "馬上使用-現金價": 3040000, "分期期數": 42, "管理費": 415000}
            },
            "寶祥家族": {
                "6人": {"定價": 2200000, "預購-現金價": 1166000, "分期價": 1224300, "馬上使用-現金價": 1760000, "分期期數": 36, "管理費": 240000},
                "9人": {"定價": 3200000, "預購-現金價": 1696000, "分期價": 1780800, "馬上使用-現金價": 2560000, "分期期數": 42, "管理費": 350000},
                "15人": {"定價": 4000000, "預購-現金價": 2120000, "分期價": 2226000, "馬上使用-現金價": 3200000, "分期期數": 42, "管理費": 436400}
            },
            "永願": {
                "2人": {"定價": 420000, "預購-現金價": 252000, "分期價": 272160, "馬上使用-現金價": 336000, "分期期數": 24, "管理費": 45900}
            },
             "永念": {
                "2人": {"定價": 200000, "預購-現金價": 120000, "分期價": 128000, "馬上使用-現金價": 160000, "分期期數": 18, "管理費": 21900}
            },
            "天地": {
                "合人2人": {"定價": 800000, "預購-現金價": 416000, "分期價": 440960, "馬上使用-現金價": 640000, "分期期數": 24, "管理費": 87300},
                "圓融8人": {"定價": 1800000, "預購-現金價": 936000, "分期價": 982800, "馬上使用-現金價": 1440000, "分期期數": 24, "管理費": 196400},
                "福澤12人": {"定價": 2800000, "預購-現金價": 1456000, "分期價": 1528800, "馬上使用-現金價": 2240000, "分期期數": 36, "管理費": 305500}
            },
            "恩典園一期": {
                "安然2人": {"定價": 350000, "預購-現金價": 210000, "分期價": 226800, "馬上使用-現金價": 280000, "分期期數": 24, "管理費": 38200},
                "安然4人": {"定價": 700000, "預購-現金價": 406000, "分期價": 430360, "馬上使用-現金價": 560000, "分期期數": 24, "管理費": 76400},
                "安然特區4人": {"定價": 848000, "預購-現金價": 614800, "分期價": 645540, "馬上使用-現金價": 678400, "分期期數": 24, "管理費": 115700},
                "晨星2人": {"定價": 200000, "團購-現金價": 105430, "團購-分期價": 111000, "預購-現金價": 120000, "分期價": 128000, "馬上使用-現金價": 160000, "分期期數": 18, "管理費": 21900,"團購-管理費": 16470}
            }
        }

    # ... 其餘的 GreenGardenProposal 類別方法保持不變 ...

def format_currency(amount):
    if pd.isna(amount) or amount is None:
        return "0"
    return f"{amount:,.0f}"

def main():
    # 初始化授權系統
    auth_system = AuthorizationSystem()
    
    # 檢查授權狀態
    if 'authorized' not in st.session_state:
        st.session_state.authorized = False
    
    # 如果未授權，顯示登入頁面
    if not st.session_state.authorized:
        auth_system.display_login_page()
    
    # 以下為授權成功後的內容
    # 移除左邊的用戶資訊區塊，直接顯示基本資訊
    with st.sidebar:
        # 基本資訊
        st.header("基本資訊")
        client_name = st.text_input("客戶姓名", value="")
        
        # 自動填入專業顧問資訊（營業處 + 姓名）
        agent_info = st.session_state.agent_info
        office_name = agent_info.get('office', '')
        consultant_display = f"{office_name}營業處-專業顧問：{agent_info['name']}"
        st.text_input("專業顧問", value=consultant_display, disabled=True)
        
        contact_phone = st.text_input("聯絡電話", value="")
        proposal_date = st.date_input("日期", value=datetime.now())
        
        # 登出按鈕放在底部
        st.markdown("---")
        if st.button("🚪 登出系統", use_container_width=True):
            for key in ['authorized', 'agent_id', 'agent_info']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    # 顯示標題和圖檔
    st.markdown('<div class="header-container">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        try:
            image_url = "https://raw.githubusercontent.com/m9606286/green-garden-app/main/my_app/綠金園.png"
            st.image(image_url, width=120)
        except:
            st.markdown("""
            <div style="width: 120px; height: 120px; background: #2E8B57; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 16px;">
                綠金園
            </div>
            """, unsafe_allow_html=True)

    with col2:
        if client_name:
            page_title = f"客戶{client_name}-規劃配置建議書"
        else:
            page_title = "規劃配置建議書"

        st.markdown(f"""
        <div class="title-container">
            <h1 class="main-title" style="font-size: 1.5rem;">{page_title}</h1>
        </div>
        """, unsafe_allow_html=True)

    # 初始化提案系統
    proposal_system = GreenGardenProposal()

    # 初始化 session state
    if 'selected_products' not in st.session_state:
        st.session_state.selected_products = []

    # 主內容區域 - 兩個標籤頁
    tab1, tab2 = st.tabs(["🛒 產品選擇", "📋 方案詳情"])

    with tab1:
        # 產品選擇
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("墓園產品")
            cemetery_type = st.selectbox("選擇墓園類型",
                ["請選擇", "澤茵園", "寶祥家族", "聚賢閣", "永願","永念", "天地", "恩典園一期"])

            if cemetery_type != "請選擇":
                spec = st.selectbox("規格", list(proposal_system.cemetery_products[cemetery_type].keys()))
                quantity = st.number_input("座數", min_value=1, max_value=10, value=1, key=f"{cemetery_type}_quantity")

                # 根據產品類型設定購買方式選項
                if cemetery_type == "恩典園一期" and spec == "晨星2人":
                    price_options = ["預購-現金價", "分期價", "馬上使用-現金價", "團購-現金價", "團購-分期價"]
                else:
                    price_options = ["預購-現金價", "分期價", "馬上使用-現金價"]

                price_type = st.radio("購買方式", price_options, key=f"{cemetery_type}_price")

                if st.button(f"加入{cemetery_type}", key=f"add_{cemetery_type}"):
                    new_product = {
                        "category": cemetery_type,
                        "spec": spec,
                        "quantity": quantity,
                        "price_type": price_type,
                        "type": "cemetery"
                    }
                    if new_product not in st.session_state.selected_products:
                        st.session_state.selected_products.append(new_product)
                        st.success(f"已加入 {cemetery_type} - {spec} x{quantity}")
                    else:
                        st.warning("此產品已存在於清單中")

        with col2:
            st.subheader("牌位產品")
            memorial_type = st.selectbox("選擇牌位類型",
                ["請選擇", "普羅廳", "彌陀廳", "大佛廳"])

            if memorial_type != "請選擇":
                spec = st.selectbox("層別", list(proposal_system.memorial_products[memorial_type].keys()), key=f"{memorial_type}_spec")
                quantity = st.number_input("座數", min_value=1, max_value=10, value=1, key=f"{memorial_type}_quantity")

                if memorial_type == '大佛廳' or (memorial_type == '彌陀廳' and spec in ["6、9", "7、8"]):
                    price_options = ["加購-現金價", "單購-現金價", "單購-分期價"]
                else:
                    price_options = ["加購-現金價", "單購-現金價"]

                price_type = st.radio("購買方式", price_options, key=f"{memorial_type}_price")

                if st.button(f"加入{memorial_type}", key=f"add_{memorial_type}"):
                    new_product = {
                        "category": memorial_type,
                        "spec": spec,
                        "quantity": quantity,
                        "price_type": price_type,
                        "type": "memorial"
                    }
                    if new_product not in st.session_state.selected_products:
                        st.session_state.selected_products.append(new_product)
                        st.success(f"已加入 {memorial_type} - {spec} x{quantity}")
                    else:
                        st.warning("此產品已存在於清單中")

        with col3:
            st.subheader("已選擇產品")
            if st.session_state.selected_products:
                for i, product in enumerate(st.session_state.selected_products):
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.write(f"**{product['category']}** - {product['spec']}")
                        st.write(f"座數: {product['quantity']} | 購買方式: {product['price_type']}")
                    with col_b:
                        if st.button("刪除", key=f"delete_{i}"):
                            st.session_state.selected_products.pop(i)
                            st.rerun()

                if st.button("清空所有產品"):
                    st.session_state.selected_products = []
                    st.rerun()
            else:
                st.info("尚未選擇任何產品")

    with tab2:
        if st.session_state.selected_products:
            totals = proposal_system.calculate_total(st.session_state.selected_products)

            # 價格總覽
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(label="總定價", value=f"{format_currency(totals['total_original'])}")
            with col2:
                st.markdown(f"""
                 <div style="text-align: left;">
                    <div style="font-size: 1rem">折扣後總價</div>
                    <div style="font-size: 2.3rem; font-weight: bold; color: #FF4444;">{format_currency(totals['total_discounted'])}</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #FF4444;">折扣 {totals['discount_rate']*100:.0f}%</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.metric(label="總管理費", value=f"{format_currency(totals['total_management_fee'])}")
            with col4:
                st.metric(label="折扣後總價+總管理費", value=f"{format_currency(totals['final_total'])}")

            # 產品明細
            st.markdown('<div style="margin-bottom: -3rem; font-weight: bold;">產品明細</div>', unsafe_allow_html=True)

            simple_product_data = []
            for detail in totals['product_details']:
                simple_product_data.append({
                    '產品': f"{detail['category']} {detail['spec']}",
                    '座數': detail['quantity'],
                    '購買方式': detail['price_type'],
                    '定價': format_currency(detail['original_price']),
                    '優惠價': format_currency(detail['product_price']),
                    '管理費': format_currency(detail['management_fee'])
                })

            simple_df = pd.DataFrame(simple_product_data)
            st.markdown('<div class="compact-table half-width-table">', unsafe_allow_html=True)
            st.dataframe(simple_df, use_container_width=False, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # 產品分期明細（如果有分期產品）
            installment_details = []
            for detail in totals['product_details']:
                if detail['installment_terms']:
                    installment_details.append({
                        '產品': f"{detail['category']}\n{detail['spec']}",
                        '座數': detail['quantity'],
                        '期數': f"{detail['installment_terms']}期",
                        '產品頭款': format_currency(detail['product_down_payment']),
                        '產品期款': format_currency(detail['product_monthly_payment']),
                        '管理費頭款': format_currency(detail['management_down_payment']),
                        '管理費期款': format_currency(detail['management_monthly_payment'])
                    })

            if installment_details:
                st.markdown('<div style="margin-bottom: -3rem; font-weight: bold;">產品分期明細</div>', unsafe_allow_html=True)
                installment_df = pd.DataFrame(installment_details)
                st.markdown('<div class="compact-table half-width-table">', unsafe_allow_html=True)
                st.dataframe(installment_df, use_container_width=False, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # 分期總結
                st.markdown('<div style="margin-bottom: -2rem; font-weight: bold;">分期總結</div>', unsafe_allow_html=True)

                total_down_payment = totals['total_down_payment']
                total_management_down_payment = totals['total_management_down_payment']
                st.markdown(f'<div class="installment-item">頭期款：{format_currency(total_down_payment + total_management_down_payment)} (產品 {format_currency(total_down_payment)}、管理費 {format_currency(total_management_down_payment)})</div>', unsafe_allow_html=True)

                # 計算月繳總額
                payment_schedule = {}
                product_payment_schedule = {}
                management_payment_schedule = {}

                all_terms = []
                for detail in totals['product_details']:
                    if detail['installment_terms']:
                        all_terms.append(detail['installment_terms'])

                if all_terms:
                    max_term = max(all_terms)

                    for term in range(1, max_term + 1):
                        payment_schedule[term] = 0
                        product_payment_schedule[term] = 0
                        management_payment_schedule[term] = 0

                    for detail in totals['product_details']:
                        if detail['installment_terms']:
                            terms = detail['installment_terms']
                            product_monthly = detail['product_monthly_payment']
                            management_monthly = detail['management_monthly_payment']
                            total_monthly = product_monthly + management_monthly

                            for term in range(1, terms + 1):
                                payment_schedule[term] += total_monthly
                                product_payment_schedule[term] += product_monthly
                                management_payment_schedule[term] += management_monthly

                    current_total = payment_schedule[1]
                    current_product = product_payment_schedule[1]
                    current_management = management_payment_schedule[1]
                    start_period = 1

                    for term in range(2, max_term + 2):
                        if term > max_term or (payment_schedule.get(term, current_total) != current_total):
                            if start_period == term - 1:
                                st.markdown(f'<div class="installment-item">第{start_period}期：每期 {format_currency(current_total)} (產品{format_currency(current_product)}、管理費 {format_currency(current_management)})</div>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<div class="installment-item">第{start_period}~{term-1}期：每期 {format_currency(current_total)} (產品{format_currency(current_product)}、管理費 {format_currency(current_management)})</div>', unsafe_allow_html=True)

                            if term <= max_term:
                                start_period = term
                                current_total = payment_schedule[term]
                                current_product = product_payment_schedule[term]
                                current_management = management_payment_schedule[term]

            # 規劃配置分析
            st.markdown('<div class="analysis-title">「早規劃、早安心，現在購買最划算」</div>', unsafe_allow_html=True)
            savings = totals['total_original'] - totals['total_discounted']
            discount_rate = totals['discount_rate'] * 100
            st.markdown(f"""
            <div class="analysis-content">
            因應通膨，商品價格將依階段逐步調漲至定價，另外管理費亦會隨商品價格按比例同步調漲。若您現在購買，不僅可提前鎖定目前優惠，立即節省{format_currency(savings)}元 (相當於{discount_rate:.0f}%的折扣)，更能同時享有未來價格上漲的增值潛力，對日後轉售亦具明顯效益。
            <br><br>
            本建議書提供客戶七日審閱期，建議價格自本建議書日期起七天內有效，實際成交價格仍以公司最新公告為準。
            <br><br>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.info("請先在「產品選擇」標籤頁選擇產品")

        # 基本資訊顯示在建議書最下方
        col1, col2 = st.columns([1, 4])
        with col1:
            morning_logo_url = "https://raw.githubusercontent.com/m9606286/green-garden-app/main/my_app/晨暉logo.png"
            st.image(morning_logo_url, width=200)

        col1, col2, col3 = st.columns(3)
        with col1:
           st.markdown(f'<div class="client-info-content"><strong>專業顧問：</strong>{consultant_display}</div>', unsafe_allow_html=True)
        with col2:
           st.markdown(f'<div class="client-info-content"><strong>聯絡電話：</strong>{contact_phone if contact_phone else ""}</div>', unsafe_allow_html=True)
        with col3:
           st.markdown(f'<div class="client-info-content"><strong>日期：</strong>{proposal_date.strftime("%Y-%m-%d")}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
