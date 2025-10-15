import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 頁面配置
st.set_page_config(
    page_title="規劃配置建議書",
    page_icon="🏞️",
    layout="wide"
)

# 樣式設置
st.markdown("""
<style>
    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 2rem;
        gap: 1rem;
    }
    .logo-bottom-left {
        position: fixed;
        bottom: 20px;
        left: 20px;
        z-index: 999;
    }
    .title-container {
        text-align: center;
    }
    .main-title {
        font-size: 1.5rem;
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
    .highlight-box {
        background-color: #f0f8f0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E8B57;
        margin: 1rem 0;
    }
    .discount-text {
        color: #FF4444;
        font-weight: bold;
    }
    .installment-info {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #2E8B57;
        margin: 1rem 0;
    }
    .installment-item {
        font-size: 1.1rem;
        margin: 0.5rem 0;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

class GreenGardenProposal:
    def __init__(self):
        self.cemetery_products = self._init_cemetery_products()
        self.memorial_products = self._init_memorial_products()
        self.payment_terms = self._init_payment_terms()
    
    def _init_cemetery_products(self):
        return {
            "澤茵園": {
                "單人位": {"定價": 460000, "預購-現金價": 276000, "分期價": 292560, "馬上使用-現金價": 552000, "分期期數": 24, "管理費": 100400},
                "貴族2人": {"定價": 620000, "預購-現金價": 372000, "分期價": 394320, "馬上使用-現金價": 372000, "分期期數": 24, "管理費": 67700},
                "家福4人": {"定價": 950000, "預購-現金價": 570000, "分期價": 598500, "馬上使用-現金價": 570000, "分期期數": 24, "管理費": 103700},
                "家族6人": {"定價": 1300000, "預購-現金價": 780000, "分期價": 819000, "馬上使用-現金價": 780000, "分期期數": 24, "管理費": 142000}
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
            "天地": {
                "合人2人": {"定價": 800000, "預購-現金價": 416000, "分期價": 440960, "馬上使用-現金價": 640000, "分期期數": 24, "管理費": 87300},
                "圓融8人": {"定價": 1800000, "預購-現金價": 936000, "分期價": 982800, "馬上使用-現金價": 1440000, "分期期數": 24, "管理費": 196400},
                "福澤12人": {"定價": 2800000, "預購-現金價": 1456000, "分期價": 1528800, "馬上使用-現金價": 2240000, "分期期數": 36, "管理費": 305500}
            },
            "恩典園一期": {
                "安然2人": {"定價": 350000, "預購-現金價": 210000, "分期價": 226800, "馬上使用-現金價": 280000, "分期期數": 24, "管理費": 38200},
                "安然4人": {"定價": 700000, "預購-現金價": 406000, "分期價": 430360, "馬上使用-現金價": 560000, "分期期數": 24, "管理費": 76400},
                "安然特區4人": {"定價": 848000, "預購-現金價": 614800, "分期價": 645540, "馬上使用-現金價": 678400, "分期期數": 24, "管理費": 115700},
                "晨星2人": {"定價": 200000, "預購-現金價": 120000, "分期價": 128000, "馬上使用-現金價": 160000, "分期期數": 18, "管理費": 21900}
            }
        }
    
    def _init_memorial_products(self):
        return {
            "普羅廳": {
                "1、2、15、16": {"定價": 120000, "加購-現金價": 50000, "單購-現金價": 66000, "分期價": None, "分期期數": None, "管理費": 23000},
                "3、5、12、13": {"定價": 140000, "加購-現金價": 60000, "單購-現金價": 77000, "分期價": None, "分期期數": None, "管理費": 23000},
                "6、7、10、11": {"定價": 160000, "加購-現金價": 70000, "單購-現金價": 88000, "分期價": None, "分期期數": None, "管理費": 23000},
                "8、9": {"定價": 190000, "加購-現金價": 85000, "單購-現金價": 99000, "分期價": None, "分期期數": None, "管理費": 23000}
            },
            "彌陀廳": {
                "1、2、12、13": {"定價": 160000, "加購-現金價": 70000, "單購-現金價": 88000, "分期價": None, "分期期數": None, "管理費": 23000},
                "3、5、10、11": {"定價": 190000, "加購-現金價": 85000, "單購-現金價": 99000, "分期價": None, "分期期數": None, "管理費": 23000},
                "6、9": {"定價": 220000, "加購-現金價": 100000, "單購-現金價": 132000, "分期價": 143000, "分期期數": 24, "管理費": 23000},
                "7、8": {"定價": 240000, "加購-現金價": 110000, "單購-現金價": 144000, "分期價": 156000, "分期期數": 24, "管理費": 23000}
            },
            "大佛廳": {
                "1、2、10、11": {"定價": 220000, "加購-現金價": 100000, "單購-現金價": 132000, "分期價": 143000, "分期期數": 24, "管理費": 23000},
                "3、5、8、9": {"定價": 260000, "加購-現金價": 120000, "單購-現金價": 156000, "分期價": 169000, "分期期數": 24, "管理費": 23000},
                "6、7": {"定價": 290000, "加購-現金價": 135000, "單購-現金價": 174000, "分期價": 188500, "分期期數": 24, "管理費": 23000}
            }
        }
    
    def _init_payment_terms(self):
        return {
            "18期": {"頭款比例": 0.3},
            "24期": {"頭款比例": 0.3},
            "36期": {"頭款比例": 0.25},
            "42期": {"頭款比例": 0.2}
        }
    
    def calculate_installment_payment(self, product_price, management_fee, installment_terms):
        if not installment_terms:
            return 0, 0
        
        terms_info = self.payment_terms.get(f"{installment_terms}期", {"頭款比例": 0.3})
        down_payment_ratio = terms_info["頭款比例"]
        
        total_price = product_price + management_fee
        down_payment = total_price * down_payment_ratio
        monthly_payment = (total_price - down_payment) / installment_terms
        
        return down_payment, monthly_payment
    
    def calculate_total(self, selected_products):
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
            
            price_key_map = {
                'cash': '預購-現金價',
                'installment': '分期價',
                'immediate_cash': '馬上使用-現金價',
                'additional': '加購-現金價',
                'single': '單購-現金價'
            }
            
            price_key = price_key_map[price_type]
            product_price = product_data[price_key]
            
            management_fee_per_unit = product_data.get('管理費', 0)
            management_fee = management_fee_per_unit * quantity
            
            total_original += product_data['定價'] * quantity
            total_discounted += product_price * quantity
            total_management_fee += management_fee
            
            installment_terms = product_data.get('分期期數')
            
            product_details.append({
                'category': product['category'],
                'spec': product['spec'],
                'quantity': quantity,
                'price_type': price_key,
                'original_price': product_data['定價'],
                'product_price': product_price,
                'management_fee_per_unit': management_fee_per_unit,
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

def format_currency(amount):
    if pd.isna(amount) or amount is None:
        return "0"
    return f"{amount:,.0f}"

def main():
    # 顯示標題和圖檔
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    
    try:
        image_url = "https://raw.githubusercontent.com/m9606286/green-garden-app/main/my_app/綠金園.png"
        st.image(image_url, width=120)
    except:
        st.markdown("""
        <div style="width: 120px; height: 120px; background: #2E8B57; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 16px;">
            綠金園
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="title-container">
        <h1 class="main-title">規劃配置建議書</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # 初始化提案系統
    proposal_system = GreenGardenProposal()
    
    # 側邊欄 - 客戶信息
    st.sidebar.header("客戶資訊")
    client_name = st.sidebar.text_input("客戶姓名", value="")
    consultant_name = st.sidebar.text_input("專業顧問", value="")
    contact_phone = st.sidebar.text_input("聯絡電話", value="")
    proposal_date = st.sidebar.date_input("日期", value=datetime.now())
    
    # 初始化 session state
    if 'selected_products' not in st.session_state:
        st.session_state.selected_products = []
    
    # 主內容區域 - 合併為一頁
    st.markdown('<div class="section-header">產品選擇</div>', unsafe_allow_html=True)
    
    # 產品選擇
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("墓園產品")
        cemetery_type = st.selectbox("選擇墓園類型", 
            ["請選擇", "澤茵園", "寶祥家族", "聚賢閣", "永願", "天地", "恩典園一期"])
        
        if cemetery_type != "請選擇":
            spec = st.selectbox("規格", list(proposal_system.cemetery_products[cemetery_type].keys()))
            quantity = st.number_input("座數", min_value=1, max_value=10, value=1, key=f"{cemetery_type}_quantity")
            price_type = st.radio("購買方式", ["預購-現金價", "分期價", "馬上使用-現金價"], key=f"{cemetery_type}_price")
            
            if st.button(f"加入{cemetery_type}", key=f"add_{cemetery_type}"):
                price_type_map = {
                    "預購-現金價": "cash",
                    "分期價": "installment",
                    "馬上使用-現金價": "immediate_cash"
                }
                new_product = {
                    "category": cemetery_type,
                    "spec": spec,
                    "quantity": quantity,
                    "price_type": price_type_map[price_type],
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
            
            if spec in ["6、9", "7、8"]:
                price_options = ["加購-現金價", "單購-現金價", "單購分期價"]
            else:
                price_options = ["加購-現金價", "單購-現金價"]
            
            price_type = st.radio("購買方式", price_options, key=f"{memorial_type}_price")
            
            if st.button(f"加入{memorial_type}", key=f"add_{memorial_type}"):
                price_type_map = {
                    "加購-現金價": "additional",
                    "單購-現金價": "single",
                    "單購分期價": "installment"
                }
                new_product = {
                    "category": memorial_type,
                    "spec": spec,
                    "quantity": quantity,
                    "price_type": price_type_map[price_type],
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
                    price_type_display = {
                        'immediate_cash': '馬上使用-現金價',
                        'cash': '預購-現金價',
                        'installment': '分期價',
                        'additional': '加購-現金價',
                        'single': '單購-現金價'
                    }
                    st.write(f"**{product['category']}** - {product['spec']}")
                    st.write(f"座數: {product['quantity']} | 方式: {price_type_display[product['price_type']]}")
                with col_b:
                    if st.button("刪除", key=f"delete_{i}"):
                        st.session_state.selected_products.pop(i)
                        st.rerun()
            
            if st.button("清空所有產品"):
                st.session_state.selected_products = []
                st.rerun()
        else:
            st.info("尚未選擇任何產品")
    
    # 方案詳情
    if st.session_state.selected_products:
        st.markdown('<div class="section-header">方案詳情</div>', unsafe_allow_html=True)
        
        totals = proposal_system.calculate_total(st.session_state.selected_products)
        
        # 價格總覽
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(label="購買總定價", value=f"{format_currency(totals['total_original'])}")
        with col2:
            # 自定義折扣顯示
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 0.8rem; color: #666; margin-bottom: 0.5rem;">折扣後總價</div>
                <div style="font-size: 1.5rem; font-weight: bold; margin-bottom: 0.5rem;">{format_currency(totals['total_discounted'])}</div>
                <div class="discount-text">折扣 {totals['discount_rate']*100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.metric(label="總管理費", value=f"{format_currency(totals['total_management_fee'])}")
        with col4:
            st.metric(label="最終總額", value=f"{format_currency(totals['final_total'])}")
        
        # 產品明細
        st.markdown("**產品明細**")
        product_data = []
        for detail in totals['product_details']:
            product_data.append({
                '產品類型': '墓園' if any(p['category'] == detail['category'] and p['type'] == 'cemetery' for p in st.session_state.selected_products) else '牌位',
                '產品名稱': detail['category'],
                '規格': detail['spec'],
                '座數': detail['quantity'],
                '購買方式': detail['price_type'],
                '定價': format_currency(detail['original_price']),
                '購買價': format_currency(detail['product_price']),
                '管理費': format_currency(detail['management_fee']),
                '分期期數': f"{detail['installment_terms']}期" if detail['installment_terms'] else "無分期",
                '小計': format_currency(detail['subtotal'])
            })
        
        df = pd.DataFrame(product_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # 分期資訊
        total_down_payment = 0
        total_monthly_payment = 0
        max_installment_terms = 0
        
        installment_products = []
        for product in st.session_state.selected_products:
            if product['price_type'] == 'installment':
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
                    
                    total_down_payment += down_payment
                    total_monthly_payment += monthly_payment
                    max_installment_terms = max(max_installment_terms, installment_terms)
                    installment_products.append(product)
        
        if installment_products:
            st.markdown("**分期資訊**")
            st.markdown('<div class="installment-info">', unsafe_allow_html=True)
            st.markdown(f'<div class="installment-item">頭期款 {format_currency(total_down_payment)}</div>', unsafe_allow_html=True)
            
            # 根據不同期數顯示分期資訊
            if max_installment_terms <= 24:
                st.markdown(f'<div class="installment-item">1~{max_installment_terms}期 {format_currency(total_monthly_payment)}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="installment-item">1~24期 {format_currency(total_monthly_payment)}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="installment-item">25~{max_installment_terms}期 {format_currency(total_monthly_payment)}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 投資價值分析
        st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
        st.subheader("投資價值分析")
        savings = totals['total_original'] - totals['total_discounted']
        discount_rate = totals['discount_rate'] * 100
        st.write(f"""
        **「早規劃、早安心，現在購買最划算」**
        
        因應通膨，商品價格將依階段逐步調漲至定價，另外管理費亦會隨商品價格按比例同步調漲。若您現在購買，不僅可提前鎖定目前優惠，立即節省{format_currency(savings)}元 (相當於{discount_rate:.1f}%的折扣)，更能同時享有未來價格上漲的增值潛力，對日後轉售亦具明顯效益。
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.info("請先選擇產品以查看方案詳情")
    
    # 底部信息與晨暉logo
    st.markdown("---")
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.write(f"**專業顧問:** {consultant_name} | **聯絡電話:** {contact_phone} | **日期:** {proposal_date.strftime('%Y/%m/%d')}")
    
    with col_right:
        try:
            morning_logo_url = "https://raw.githubusercontent.com/m9606286/green-garden-app/main/my_app/晨暉logo.png"
            st.image(morning_logo_url, width=180)  # 放大1.5倍
        except:
            st.markdown("""
            <div style="width: 180px; height: 180px; background: #FF6B35; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 16px; text-align: center;">
                晨暉資產
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()