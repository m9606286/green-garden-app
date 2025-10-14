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
                "單人位": {"定價": 460000, "現金價": 276000, "分期價": 292560},
                "貴族2人": {"定價": 620000, "現金價": 372000, "分期價": 394320},
                "家福4人": {"定價": 950000, "現金價": 570000, "分期價": 598500},
                "家族6人": {"定價": 1300000, "現金價": 780000, "分期價": 819000}
            },
            "聚賢閣": {
                "12人": {"定價": 3200000, "現金價": 1888000, "分期價": 1982400},
                "18人": {"定價": 3800000, "現金價": 2356000, "分期價": 2473800}
            },
            "寶祥家族": {
                "6人": {"定價": 2200000, "現金價": 1166000, "分期價": 1224300},
                "9人": {"定價": 3200000, "現金價": 1696000, "分期價": 1780800},
                "15人": {"定價": 4000000, "現金價": 2120000, "分期價": 2226000}
            },
            "永願": {
                "2人": {"定價": 420000, "現金價": 252000, "分期價": 272160}
            },
            "天地": {
                "合人2人": {"定價": 800000, "現金價": 416000, "分期價": 440960},
                "圓融8人": {"定價": 1800000, "現金價": 936000, "分期價": 982800},
                "福澤12人": {"定價": 2800000, "現金價": 1456000, "分期價": 1528800}
            },
            "恩典園一期": {
                "安然2人": {"定價": 350000, "現金價": 210000, "分期價": 226800},
                "安然4人": {"定價": 700000, "現金價": 406000, "分期價": 430360},
                "安然特區4人": {"定價": 848000, "現金價": 614800, "分期價": 645540},
                "晨星2人": {"定價": 200000, "現金價": 120000, "分期價": 128000}
            }
        }
    
    def _init_memorial_products(self):
        """初始化牌位產品數據"""
        return {
            "普羅廳": {
                "1、2、15、16": {"定價": 120000, "加購現金價": 50000, "單購現金價": 66000},
                "3、5、12、13": {"定價": 140000, "加購現金價": 60000, "單購現金價": 77000},
                "6、7、10、11": {"定價": 160000, "加購現金價": 70000, "單購現金價": 88000},
                "8、9": {"定價": 190000, "加購現金價": 85000, "單購現金價": 99000}
            },
            "彌陀廳": {
                "1、2、12、13": {"定價": 160000, "加購現金價": 70000, "單購現金價": 88000},
                "3、5、10、11": {"定價": 190000, "加購現金價": 85000, "單購現金價": 99000},
                "6、9": {"定價": 220000, "加購現金價": 100000, "單購現金價": 132000},
                "7、8": {"定價": 240000, "加購現金價": 110000, "單購現金價": 144000}
            },
            "大佛廳": {
                "1、2、10、11": {"定價": 220000, "加購現金價": 100000, "單購現金價": 132000},
                "3、5、8、9": {"定價": 260000, "加購現金價": 120000, "單購現金價": 156000},
                "6、7": {"定價": 290000, "加購現金價": 135000, "單購現金價": 174000}
            }
        }
    
    def _init_payment_terms(self):
        """初始化分期方案"""
        return {
            "24期": {"頭款比例": 0.3, "月繳期數": 24},
            "36期": {"頭款比例": 0.25, "月繳期數": 36},
            "42期": {"頭款比例": 0.2, "月繳期數": 42}
        }
    
    def calculate_total(self, selected_products):
        """計算總價"""
        total_original = 0
        total_discounted = 0
        management_fee = 0
        
        for product in selected_products:
            if product['type'] == 'cemetery':
                product_data = self.cemetery_products[product['category']][product['spec']]
            else:
                product_data = self.memorial_products[product['category']][product['spec']]
            
            quantity = product['quantity']
            price_type = product['price_type']
            
            if price_type == 'cash':
                price_key = '現金價'
            elif price_type == 'installment':
                price_key = '分期價'
            elif price_type == 'additional':
                price_key = '加購現金價'
            else:  # single
                price_key = '單購現金價'
            
            total_original += product_data['定價'] * quantity
            total_discounted += product_data[price_key] * quantity
            
            # 簡化管理費計算（實際應根據您的業務規則）
            management_fee += product_data[price_key] * quantity * 0.15
        
        discount_rate = (total_original - total_discounted) / total_original if total_original > 0 else 0
        
        return {
            "total_original": total_original,
            "total_discounted": total_discounted,
            "management_fee": management_fee,
            "discount_rate": discount_rate,
            "final_total": total_discounted + management_fee
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
    
    # 主內容區域
    tab1, tab2, tab3 = st.tabs(["📋 產品選擇", "💰 價格總覽", "📊 方案詳情"])
    
    with tab1:
        st.markdown('<div class="section-header">墓園產品選擇</div>', unsafe_allow_html=True)
        
        selected_cemetery_products = []
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("澤茵園")
            if st.checkbox("選擇澤茵園"):
                spec = st.selectbox("規格", list(proposal_system.cemetery_products["澤茵園"].keys()))
                quantity = st.number_input("座數", min_value=1, max_value=10, value=1, key="zy_quantity")
                price_type = st.radio("購買方式", ["現金價", "分期價"], key="zy_price")
                
                if st.button("加入澤茵園", key="add_zy"):
                    selected_cemetery_products.append({
                        "category": "澤茵園",
                        "spec": spec,
                        "quantity": quantity,
                        "price_type": "cash" if price_type == "現金價" else "installment",
                        "type": "cemetery"
                    })
                    st.success(f"已加入 {spec} x{quantity}")
        
        with col2:
            st.subheader("寶祥家族")
            if st.checkbox("選擇寶祥家族"):
                spec = st.selectbox("規格", list(proposal_system.cemetery_products["寶祥家族"].keys()))
                quantity = st.number_input("座數", min_value=1, max_value=10, value=1, key="bx_quantity")
                price_type = st.radio("購買方式", ["現金價", "分期價"], key="bx_price")
                
                if st.button("加入寶祥家族", key="add_bx"):
                    selected_cemetery_products.append({
                        "category": "寶祥家族",
                        "spec": spec,
                        "quantity": quantity,
                        "price_type": "cash" if price_type == "現金價" else "installment",
                        "type": "cemetery"
                    })
                    st.success(f"已加入 {spec} x{quantity}")
        
        with col3:
            st.subheader("其他墓園")
            cemetery_type = st.selectbox("墓園類型", ["聚賢閣", "永願", "天地", "恩典園一期"])
            if st.checkbox(f"選擇{cemetery_type}"):
                spec = st.selectbox("規格", list(proposal_system.cemetery_products[cemetery_type].keys()), key=f"{cemetery_type}_spec")
                quantity = st.number_input("座數", min_value=1, max_value=10, value=1, key=f"{cemetery_type}_quantity")
                price_type = st.radio("購買方式", ["現金價", "分期價"], key=f"{cemetery_type}_price")
                
                if st.button(f"加入{cemetery_type}", key=f"add_{cemetery_type}"):
                    selected_cemetery_products.append({
                        "category": cemetery_type,
                        "spec": spec,
                        "quantity": quantity,
                        "price_type": "cash" if price_type == "現金價" else "installment",
                        "type": "cemetery"
                    })
                    st.success(f"已加入 {spec} x{quantity}")
        
        st.markdown('<div class="section-header">牌位產品選擇</div>', unsafe_allow_html=True)
        
        selected_memorial_products = []
        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.subheader("普羅廳")
            if st.checkbox("選擇普羅廳"):
                spec = st.selectbox("層別", list(proposal_system.memorial_products["普羅廳"].keys()), key="pl_spec")
                quantity = st.number_input("座數", min_value=1, max_value=10, value=1, key="pl_quantity")
                price_type = st.radio("購買方式", ["加購現金價", "單購現金價"], key="pl_price")
                
                if st.button("加入普羅廳", key="add_pl"):
                    selected_memorial_products.append({
                        "category": "普羅廳",
                        "spec": spec,
                        "quantity": quantity,
                        "price_type": "additional" if price_type == "加購現金價" else "single",
                        "type": "memorial"
                    })
                    st.success(f"已加入 {spec} x{quantity}")
        
        with col5:
            st.subheader("彌陀廳")
            if st.checkbox("選擇彌陀廳"):
                spec = st.selectbox("層別", list(proposal_system.memorial_products["彌陀廳"].keys()), key="mt_spec")
                quantity = st.number_input("座數", min_value=1, max_value=10, value=1, key="mt_quantity")
                price_type = st.radio("購買方式", ["加購現金價", "單購現金價"], key="mt_price")
                
                if st.button("加入彌陀廳", key="add_mt"):
                    selected_memorial_products.append({
                        "category": "彌陀廳",
                        "spec": spec,
                        "quantity": quantity,
                        "price_type": "additional" if price_type == "加購現金價" else "single",
                        "type": "memorial"
                    })
                    st.success(f"已加入 {spec} x{quantity}")
        
        with col6:
            st.subheader("大佛廳")
            if st.checkbox("選擇大佛廳"):
                spec = st.selectbox("層別", list(proposal_system.memorial_products["大佛廳"].keys()), key="df_spec")
                quantity = st.number_input("座數", min_value=1, max_value=10, value=1, key="df_quantity")
                price_type = st.radio("購買方式", ["加購現金價", "單購現金價"], key="df_price")
                
                if st.button("加入大佛廳", key="add_df"):
                    selected_memorial_products.append({
                        "category": "大佛廳",
                        "spec": spec,
                        "quantity": quantity,
                        "price_type": "additional" if price_type == "加購現金價" else "single",
                        "type": "memorial"
                    })
                    st.success(f"已加入 {spec} x{quantity}")
    
    with tab2:
        st.markdown('<div class="section-header">價格總覽</div>', unsafe_allow_html=True)
        
        all_products = selected_cemetery_products + selected_memorial_products
        if all_products:
            totals = proposal_system.calculate_total(all_products)
            
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
                    value=f"NT$ {totals['management_fee']:,.0f}"
                )
            
            with col4:
                st.metric(
                    label="最終總額",
                    value=f"NT$ {totals['final_total']:,.0f}"
                )
            
            # 顯示產品明細
            st.markdown('<div class="section-header">產品明細</div>', unsafe_allow_html=True)
            
            product_data = []
            for product in all_products:
                if product['type'] == 'cemetery':
                    product_info = proposal_system.cemetery_products[product['category']][product['spec']]
                else:
                    product_info = proposal_system.memorial_products[product['category']][product['spec']]
                
                price_key_map = {
                    'cash': '現金價',
                    'installment': '分期價',
                    'additional': '加購現金價',
                    'single': '單購現金價'
                }
                
                product_data.append({
                    '產品類型': '墓園' if product['type'] == 'cemetery' else '牌位',
                    '產品名稱': product['category'],
                    '規格': product['spec'],
                    '座數': product['quantity'],
                    '購買方式': price_key_map[product['price_type']],
                    '定價': product_info['定價'],
                    '購買價': product_info[price_key_map[product['price_type']]],
                    '小計': product_info[price_key_map[product['price_type']]] * product['quantity']
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
        
        if selected_cemetery_products or selected_memorial_products:
            totals = proposal_system.calculate_total(all_products)
            
            installment_option = st.selectbox(
                "選擇分期方案",
                list(proposal_system.payment_terms.keys())
            )
            
            terms = proposal_system.payment_terms[installment_option]
            down_payment = totals['final_total'] * terms['頭款比例']
            monthly_payment = (totals['final_total'] - down_payment) / terms['月繳期數']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="頭期款",
                    value=f"NT$ {down_payment:,.0f}"
                )
            
            with col2:
                st.metric(
                    label=f"月繳期款 ({terms['月繳期數']}期)",
                    value=f"NT$ {monthly_payment:,.0f}"
                )
            
            with col3:
                st.metric(
                    label="總期數",
                    value=terms['月繳期數']
                )
            
            # 分期付款明細表
            st.markdown('<div class="section-header">分期付款明細</div>', unsafe_allow_html=True)
            
            installment_data = []
            for i in range(terms['月繳期數']):
                installment_data.append({
                    '期數': i + 1,
                    '應繳金額': f"NT$ {monthly_payment:,.0f}",
                    '備註': '月繳期款' if i > 0 else '頭期款 + 首期'
                })
            
            installment_df = pd.DataFrame(installment_data)
            st.dataframe(installment_df, use_container_width=True)
            
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