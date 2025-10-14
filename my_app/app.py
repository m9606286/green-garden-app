import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 頁面配置
st.set_page_config(
    page_title="綠金園規劃配置建議書",
    page_icon="🏞️",
    layout="wide"
)

# 樣式設置
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2E8B57;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #2E8B57;
        padding-bottom: 0.5rem;
    }
    .highlight-box {
        background-color: #f0f8f0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E8B57;
        margin: 1rem 0;
    }
    .product-item {
        background-color: #f9f9f9;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
        border: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

class GreenGardenProposal:
    def __init__(self):
        # 初始化產品數據（從您的Excel中提取）
        self.cemetery_products = self._init_cemetery_products()
        self.memorial_products = self._init_memorial_products()
        self.payment_terms = self._init_payment_terms()
    
    def _init_cemetery_products(self):
        """初始化墓園產品數據"""
        return {
            "澤茵園": {
                "單人位": {"定價": 920000, "現金價": 552000, "分期價": 292560, "分期期數": 24, "管理費": 100400},
                "貴族2人": {"定價": 620000, "現金價": 372000, "分期價": 394320, "分期期數": 24, "管理費": 67700},
                "家福4人": {"定價": 950000, "現金價": 570000, "分期價": 598500, "分期期數": 24, "管理費": 103700},
                "家族6人": {"定價": 1300000, "現金價": 780000, "分期價": 819000, "分期期數": 24, "管理費": 142000}
            },
            "聚賢閣": {
                "12人": {"定價": 3200000, "現金價": 1888000, "分期價": 1982400, "分期期數": 42, "管理費": 349000},
                "18人": {"定價": 3800000, "現金價": 2356000, "分期價": 2473800, "分期期數": 42, "管理費": 415000}
            },
            "寶祥家族": {
                "6人": {"定價": 2200000, "現金價": 1166000, "分期價": 1224300, "分期期數": 36, "管理費": 240000},
                "9人": {"定價": 3200000, "現金價": 1696000, "分期價": 1780800, "分期期數": 42, "管理費": 350000},
                "15人": {"定價": 4000000, "現金價": 2120000, "分期價": 2226000, "分期期數": 42, "管理費": 436400}
            },
            "永願": {
                "2人": {"定價": 420000, "現金價": 252000, "分期價": 272160, "分期期數": 24, "管理費": 45900}
            },
            "天地": {
                "合人2人": {"定價": 800000, "現金價": 416000, "分期價": 440960, "分期期數": 24, "管理費": 87300},
                "圓融8人": {"定價": 1800000, "現金價": 936000, "分期價": 982800, "分期期數": 24, "管理費": 196400},
                "福澤12人": {"定價": 2800000, "現金價": 1456000, "分期價": 1528800, "分期期數": 36, "管理費": 305500}
            },
            "恩典園一期": {
                "安然2人": {"定價": 350000, "現金價": 210000, "分期價": 226800, "分期期數": 24, "管理費": 38200},
                "安然4人": {"定價": 700000, "現金價": 406000, "分期價": 430360, "分期期數": 24, "管理費": 76400},
                "安然特區4人": {"定價": 848000, "現金價": 614800, "分期價": 645540, "分期期數": 24, "管理費": 115700},
                "晨星2人": {"定價": 200000, "現金價": 120000, "分期價": 128000, "分期期數": 18, "管理費": 21900}
            }
        }
    
    def _init_memorial_products(self):
        """初始化牌位產品數據"""
        return {
            "普羅廳": {
                "1、2、15、16": {"定價": 120000, "加購現金價": 50000, "單購現金價": 66000, "分期價": None, "分期期數": None, "管理費": 23000},
                "3、5、12、13": {"定價": 140000, "加購現金價": 60000, "單購現金價": 77000, "分期價": None, "分期期數": None, "管理費": 23000},
                "6、7、10、11": {"定價": 160000, "加購現金價": 70000, "單購現金價": 88000, "分期價": None, "分期期數": None, "管理費": 23000},
                "8、9": {"定價": 190000, "加購現金價": 85000, "單購現金價": 99000, "分期價": None, "分期期數": None, "管理費": 23000}
            },
            "彌陀廳": {
                "1、2、12、13": {"定價": 160000, "加購現金價": 70000, "單購現金價": 88000, "分期價": None, "分期期數": None, "管理費": 23000},
                "3、5、10、11": {"定價": 190000, "加購現金價": 85000, "單購現金價": 99000, "分期價": None, "分期期數": None, "管理費": 23000},
                "6、9": {"定價": 220000, "加購現金價": 100000, "單購現金價": 132000, "分期價": 143000, "分期期數": 24, "管理費": 23000},
                "7、8": {"定價": 240000, "加購現金價": 110000, "單購現金價": 144000, "分期價": 156000, "分期期數": 24, "管理費": 23000}
            },
            "大佛廳": {
                "1、2、10、11": {"定價": 220000, "加購現金價": 100000, "單購現金價": 132000, "分期價": 143000, "分期期數": 24, "管理費": 23000},
                "3、5、8、9": {"定價": 260000, "加購現金價": 120000, "單購現金價": 156000, "分期價": 169000, "分期期數": 24, "管理費": 23000},
                "6、7": {"定價": 290000, "加購現金價": 135000, "單購現金價": 174000, "分期價": 188500, "分期期數": 24, "管理費": 23000}
            }
        }
    
    def _init_payment_terms(self):
        """初始化分期方案頭款比例"""
        return {
            "18期": {"頭款比例": 0.3},
            "24期": {"頭款比例": 0.3},
            "36期": {"頭款比例": 0.25},
            "42期": {"頭款比例": 0.2}
        }
    
    def get_installment_terms(self, product_type, category, spec):
        """根據產品類型獲取分期期數"""
        if product_type == "cemetery":
            product_data = self.cemetery_products[category][spec]
        else:
            product_data = self.memorial_products[category][spec]
        
        return product_data.get("分期期數")
    
    def calculate_installment_payment(self, product_price, management_fee, installment_terms):
        """計算分期付款金額"""
        if not installment_terms:
            return 0, 0
        
        terms_info = self.payment_terms.get(f"{installment_terms}期", {"頭款比例": 0.3})
        down_payment_ratio = terms_info["頭款比例"]
        
        # 頭款（產品價格 + 管理費）
        total_price = product_price + management_fee
        down_payment = total_price * down_payment_ratio
        
        # 月繳期款
        monthly_payment = (total_price - down_payment) / installment_terms
        
        return down_payment, monthly_payment
    
    def calculate_total(self, selected_products):
        """計算總價"""
        total_original = 0
        total_discounted = 0
        total_management_fee = 0
        product_details = []
        
        for product in selected_products:
            if product['type'] == 'cemetery':
                product_data = self.cemetery_products[product['category']][product['spec']]
            else:
                product_data = self.memorial_products[product['category']][product['spec']]
            
            quantity = product['quantity']
            price_type = product['price_type']
            
            if price_type == 'cash':
                price_key = '現金價'
                product_price = product_data[price_key]
            elif price_type == 'installment':
                price_key = '分期價'
                product_price = product_data[price_key]
            elif price_type == 'additional':
                price_key = '加購現金價'
                product_price = product_data[price_key]
            else:  # single
                price_key = '單購現金價'
                product_price = product_data[price_key]
            
            # 管理費
            management_fee = product_data.get('管理費', 0) * quantity
            
            total_original += product_data['定價'] * quantity
            total_discounted += product_price * quantity
            total_management_fee += management_fee
            
            # 分期期數
            installment_terms = product_data.get('分期期數')
            
            product_details.append({
                'category': product['category'],
                'spec': product['spec'],
                'quantity': quantity,
                'price_type': price_key,
                'original_price': product_data['定價'],
                'product_price': product_price,
                'management_fee': management_fee,
                'installment_terms': installment_terms,
                'subtotal': product_price * quantity + management_fee
            })
        
        discount_rate = (total_original - total_discounted) / total_original if total_original > 0 else 0
        final_total = total_discounted + total_management_fee
        
        return {
            "total_original": total_original,
            "total_discounted": total_discounted,
            "total_management_fee": total_management_fee,
            "discount_rate": discount_rate,
            "final_total": final_total,
            "product_details": product_details
        }

def main():
    st.markdown('<div class="main-header">🏞️ 綠金園規劃配置建議書</div>', unsafe_allow_html=True)
    
    # 初始化提案系統
    proposal_system = GreenGardenProposal()
    
    # 側邊欄 - 客戶信息
    st.sidebar.header("客戶資訊")
    client_name = st.sidebar.text_input("客戶姓名", value="莊聖賢")
    consultant_name = st.sidebar.text_input("專業顧問", value="王大明")
    contact_phone = st.sidebar.text_input("聯絡電話", value="0917888888")
    proposal_date = st.sidebar.date_input("日期", value=datetime.now())
    
    # 初始化 session state 來儲存選擇的產品
    if 'selected_products' not in st.session_state:
        st.session_state.selected_products = []
    
    # 主內容區域
    tab1, tab2, tab3 = st.tabs(["📋 產品選擇", "💰 價格總覽", "📊 方案詳情"])
    
    with tab1:
        st.markdown('<div class="section-header">墓園產品選擇</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("澤茵園")
            if st.checkbox("選擇澤茵園", key="zy_check"):
                spec = st.selectbox("規格", list(proposal_system.cemetery_products["澤茵園"].keys()), key="zy_spec")
                quantity = st.number_input("座數", min_value=1, max_value=10, value=1, key="zy_quantity")
                price_type = st.radio("購買方式", ["現金價", "分期價"], key="zy_price")
                
                if st.button("加入澤茵園", key="add_zy"):
                    new_product = {
                        "category": "澤茵園",
                        "spec": spec,
                        "quantity": quantity,
                        "price_type": "cash" if price_type == "現金價" else "installment",
                        "type": "cemetery"
                    }
                    # 檢查是否已存在相同產品
                    if new_product not in st.session_state.selected_products:
                        st.session_state.selected_products.append(new_product)
                        st.success(f"已加入 {spec} x{quantity}")
                    else:
                        st.warning("此產品已存在於清單中")
        
        with col2:
            st.subheader("寶祥家族")
            if st.checkbox("選擇寶祥家族", key="bx_check"):
                spec = st.selectbox("規格", list(proposal_system.cemetery_products["寶祥家族"].keys()), key="bx_spec")
                quantity = st.number_input("座數", min_value=1, max_value=10, value=1, key="bx_quantity")
                price_type = st.radio("購買方式", ["現金價", "分期價"], key="bx_price")
                
                if st.button("加入寶祥家族", key="add_bx"):
                    new_product = {
                        "category": "寶祥家族",
                        "spec": spec,
                        "quantity": quantity,
                        "price_type": "cash" if price_type == "現金價" else "installment",
                        "type": "cemetery"
                    }
                    if new_product not in st.session_state.selected_products:
                        st.session_state.selected_products.append(new_product)
                        st.success(f"已加入 {spec} x{quantity}")
                    else:
                        st.warning("此產品已存在於清單中")
        
        with col3:
            st.subheader("其他墓園")
            cemetery_type = st.selectbox("墓園類型", ["聚賢閣", "永願", "天地", "恩典園一期"], key="other_cemetery")
            if st.checkbox(f"選擇{cemetery_type}", key=f"{cemetery_type}_check"):
                spec = st.selectbox("規格", list(proposal_system.cemetery_products[cemetery_type].keys()), key=f"{cemetery_type}_spec")
                quantity = st.number_input("座數", min_value=1, max_value=10, value=1, key=f"{cemetery_type}_quantity")
                price_type = st.radio("購買方式", ["現金價", "分期價"], key=f"{cemetery_type}_price")
                
                if st.button(f"加入{cemetery_type}", key=f"add_{cemetery_type}"):
                    new_product = {
                        "category": cemetery_type,
                        "spec": spec,
                        "quantity": quantity,
                        "price_type": "cash" if price_type == "現金價" else "installment",
                        "type": "cemetery"
                    }
                    if new_product not in st.session_state.selected_products:
                        st.session_state.selected_products.append(new_product)
                        st.success(f"已加入 {spec} x{quantity}")
                    else:
                        st.warning("此產品已存在於清單中")
        
        st.markdown('<div class="section-header">牌位產品選擇</div>', unsafe_allow_html=True)
        
        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.subheader("普羅廳")
            if st.checkbox("選擇普羅廳", key="pl_check"):
                spec = st.selectbox("層別", list(proposal_system.memorial_products["普羅廳"].keys()), key="pl_spec")
                quantity = st.number_input("座數", min_value=1, max_value=10, value=1, key="pl_quantity")
                
                # 根據規格決定可用的購買方式
                available_price_types = ["加購現金價", "單購現金價"]
                price_type = st.radio("購買方式", available_price_types, key="pl_price")
                
                if st.button("加入普羅廳", key="add_pl"):
                    new_product = {
                        "category": "普羅廳",
                        "spec": spec,
                        "quantity": quantity,
                        "price_type": "additional" if price_type == "加購現金價" else "single",
                        "type": "memorial"
                    }
                    if new_product not in st.session_state.selected_products:
                        st.session_state.selected_products.append(new_product)
                        st.success(f"已加入 {spec} x{quantity}")
                    else:
                        st.warning("此產品已存在於清單中")
        
        with col5:
            st.subheader("彌陀廳")
            if st.checkbox("選擇彌陀廳", key="mt_check"):
                spec = st.selectbox("層別", list(proposal_system.memorial_products["彌陀廳"].keys()), key="mt_spec")
                quantity = st.number_input("座數", min_value=1, max_value=10, value=1, key="mt_quantity")
                
                # 根據規格決定可用的購買方式
                if spec in ["6、9", "7、8"]:
                    available_price_types = ["加購現金價", "單購現金價", "單購分期價"]
                else:
                    available_price_types = ["加購現金價", "單購現金價"]
                
                price_type = st.radio("購買方式", available_price_types, key="mt_price")
                
                if st.button("加入彌陀廳", key="add_mt"):
                    price_type_map = {
                        "加購現金價": "additional",
                        "單購現金價": "single", 
                        "單購分期價": "installment"
                    }
                    new_product = {
                        "category": "彌陀廳",
                        "spec": spec,
                        "quantity": quantity,
                        "price_type": price_type_map[price_type],
                        "type": "memorial"
                    }
                    if new_product not in st.session_state.selected_products:
                        st.session_state.selected_products.append(new_product)
                        st.success(f"已加入 {spec} x{quantity}")
                    else:
                        st.warning("此產品已存在於清單中")
        
        with col6:
            st.subheader("大佛廳")
            if st.checkbox("選擇大佛廳", key="df_check"):
                spec = st.selectbox("層別", list(proposal_system.memorial_products["大佛廳"].keys()), key="df_spec")
                quantity = st.number_input("座數", min_value=1, max_value=10, value=1, key="df_quantity")
                
                # 根據規格決定可用的購買方式
                available_price_types = ["加購現金價", "單購現金價", "單購分期價"]
                price_type = st.radio("購買方式", available_price_types, key="df_price")
                
                if st.button("加入大佛廳", key="add_df"):
                    price_type_map = {
                        "加購現金價": "additional",
                        "單購現金價": "single",
                        "單購分期價": "installment"
                    }
                    new_product = {
                        "category": "大佛廳",
                        "spec": spec,
                        "quantity": quantity,
                        "price_type": price_type_map[price_type],
                        "type": "memorial"
                    }
                    if new_product not in st.session_state.selected_products:
                        st.session_state.selected_products.append(new_product)
                        st.success(f"已加入 {spec} x{quantity}")
                    else:
                        st.warning("此產品已存在於清單中")
        
        # 顯示已選擇的產品
        if st.session_state.selected_products:
            st.markdown('<div class="section-header">已選擇產品</div>', unsafe_allow_html=True)
            for i, product in enumerate(st.session_state.selected_products):
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**{product['category']}** - {product['spec']}")
                with col2:
                    st.write(f"座數: {product['quantity']}")
                with col3:
                    if st.button("刪除", key=f"delete_{i}"):
                        st.session_state.selected_products.pop(i)
                        st.rerun()
        
        # 清空所有選擇的按鈕
        if st.session_state.selected_products:
            if st.button("清空所有產品"):
                st.session_state.selected_products = []
                st.rerun()
    
    with tab2:
        st.markdown('<div class="section-header">價格總覽</div>', unsafe_allow_html=True)
        
        if st.session_state.selected_products:
            totals = proposal_system.calculate_total(st.session_state.selected_products)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="購買總定價",
                    value=f"NT$ {totals['total_original']:,.0f}"
                )
            
            with col2:
                st.metric(
                    label="折扣後總價",
                    value=f"NT$ {totals['total_discounted']:,.0f}",
                    delta=f"-{totals['discount_rate']*100:.1f}%"
                )
            
            with col3:
                st.metric(
                    label="總管理費",
                    value=f"NT$ {totals['total_management_fee']:,.0f}"
                )
            
            with col4:
                st.metric(
                    label="最終總額",
                    value=f"NT$ {totals['final_total']:,.0f}"
                )
            
            # 顯示產品明細
            st.markdown('<div class="section-header">產品明細</div>', unsafe_allow_html=True)
            
            product_data = []
            for detail in totals['product_details']:
                product_data.append({
                    '產品類型': '墓園' if any(p['category'] == detail['category'] and p['type'] == 'cemetery' for p in st.session_state.selected_products) else '牌位',
                    '產品名稱': detail['category'],
                    '規格': detail['spec'],
                    '座數': detail['quantity'],
                    '購買方式': detail['price_type'],
                    '定價': detail['original_price'],
                    '購買價': detail['product_price'],
                    '管理費': detail['management_fee'],
                    '分期期數': f"{detail['installment_terms']}期" if detail['installment_terms'] else "無分期",
                    '小計': detail['subtotal']
                })
            
            df = pd.DataFrame(product_data)
            st.dataframe(df, use_container_width=True)
            
            # 顯示節省金額
            st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
            st.subheader("💰 節省金額分析")
            savings = totals['total_original'] - totals['total_discounted']
            st.write(f"**立即節省金額:** NT$ {savings:,.0f}")
            st.write(f"**折扣幅度:** {totals['discount_rate']*100:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            st.info("請先在「產品選擇」標籤頁選擇產品")
    
    with tab3:
        st.markdown('<div class="section-header">分期方案詳情</div>', unsafe_allow_html=True)
        
        if st.session_state.selected_products:
            totals = proposal_system.calculate_total(st.session_state.selected_products)
            
            # 顯示每個產品的分期方案
            for i, product in enumerate(st.session_state.selected_products):
                if product['price_type'] == 'installment':
                    st.markdown(f'<div class="product-item">', unsafe_allow_html=True)
                    st.subheader(f"{product['category']} - {product['spec']}")
                    
                    # 獲取產品數據
                    if product['type'] == 'cemetery':
                        product_data = proposal_system.cemetery_products[product['category']][product['spec']]
                    else:
                        product_data = proposal_system.memorial_products[product['category']][product['spec']]
                    
                    product_price = product_data['分期價'] * product['quantity']
                    management_fee = product_data.get('管理費', 0) * product['quantity']
                    installment_terms = product_data.get('分期期數')
                    
                    if installment_terms:
                        down_payment, monthly_payment = proposal_system.calculate_installment_payment(
                            product_price, management_fee, installment_terms
                        )
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric(
                                label="頭期款 (含管理費)",
                                value=f"NT$ {down_payment:,.0f}"
                            )
                        
                        with col2:
                            st.metric(
                                label=f"月繳期款 ({installment_terms}期)",
                                value=f"NT$ {monthly_payment:,.0f}"
                            )
                        
                        with col3:
                            st.metric(
                                label="總期數",
                                value=installment_terms
                            )
                        
                        # 分期付款明細表
                        st.markdown("**分期付款明細**")
                        installment_data = []
                        for period in range(installment_terms):
                            payment_type = "頭期款 + 首期" if period == 0 else "月繳期款"
                            installment_data.append({
                                '期數': period + 1,
                                '應繳金額': f"NT$ {monthly_payment:,.0f}",
                                '備註': payment_type
                            })
                        
                        installment_df = pd.DataFrame(installment_data)
                        st.dataframe(installment_df, use_container_width=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # 如果沒有分期產品，顯示提示
            if not any(p['price_type'] == 'installment' for p in st.session_state.selected_products):
                st.info("當前選擇的產品中沒有使用分期付款方式的產品")
            
            # 投資價值說明
            st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
            st.subheader("📈 投資價值分析")
            st.write("""
            **「早規劃、早安心，現在購買最划算」**
            
            - 因應通膨，商品價格將依階段逐步調漲至定價
            - 管理費亦會隨商品價格按比例同步調漲
            - 現在購買可提前鎖定目前優惠，立即節省資金
            - 享有未來價格上漲的增值潛力
            - 對日後轉售亦具明顯效益
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            st.info("請先在「產品選擇」標籤頁選擇產品")
    
    # 底部信息
    st.markdown("---")
    st.write(f"**專業顧問:** {consultant_name} | **聯絡電話:** {contact_phone} | **日期:** {proposal_date.strftime('%Y/%m/%d')}")
    st.write("**晨暉資產股份有限公司**")

if __name__ == "__main__":
    main()