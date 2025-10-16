import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

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
    }
    .dataframe tbody td {
        text-align: right !important;
    }
    .dataframe tbody td:first-child {
        text-align: left !important;
    }
    .client-info-footer {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-top: 2rem;
        border-left: 4px solid #2E8B57;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


# ======================================================
# 主類別：綠金園建議書邏輯
# ======================================================
class GreenGardenProposal:
    def __init__(self):
        self.cemetery_products = self._init_cemetery_products()
        self.memorial_products = self._init_memorial_products()
        self.down_payments = self._init_down_payments()
        self.management_down_payments = self._init_management_down_payments()

    # --- 各產品資料初始化 ---
    def _init_cemetery_products(self):
        return {
            "恩典園一期": {
                "晨星2人": {
                    "定價": 200000, "團購-現金價": 105430, "團購-分期價": 111000,
                    "預購-現金價": 120000, "分期價": 128000,
                    "馬上使用-現金價": 160000, "分期期數": 18,
                    "管理費": 21900, "團購-管理費": 16470
                }
            }
        }

    def _init_memorial_products(self):
        return {
            "彌陀廳": {
                "6、9": {"定價": 220000, "單購-現金價": 132000, "分期價": 143000, "分期期數": 24, "管理費": 23000},
                "7、8": {"定價": 240000, "單購-現金價": 144000, "分期價": 156000, "分期期數": 24, "管理費": 23000}
            }
        }

    def _init_down_payments(self):
        return {
            "恩典園一期": {"晨星2人": {"團購-分期價": 21000, "預購-分期價": 38000}},
            "彌陀廳": {"6、9": {"單購-分期價": 42920}, "7、8": {"單購-分期價": 46800}}
        }

    def _init_management_down_payments(self):
        return {
            "恩典園一期": {"晨星2人": {"團購-分期價": 6600, "預購-分期價": 6600}},
            "彌陀廳": {"6、9": {"單購-分期價": 23000}, "7、8": {"單購-分期價": 23000}}
        }

    # --- 頭款 ---
    def get_down_payment(self, category, spec, price_type, product_price, management_fee):
        try:
            price_type_map = {
                'installment': '預購-分期價',
                'single_installment': '單購-分期價',
                'group_installment': '團購-分期價'
            }
            mapped_price_type = price_type_map.get(price_type, price_type)
            if (category in self.down_payments and
                spec in self.down_payments[category] and
                mapped_price_type in self.down_payments[category][spec]):
                return self.down_payments[category][spec][mapped_price_type]
            else:
                return 0
        except:
            return 0

    def get_management_down_payment(self, category, spec, price_type, product_price, management_fee):
        try:
            price_type_map = {
                'installment': '預購-分期價',
                'single_installment': '單購-分期價',
                'group_installment': '團購-分期價'
            }
            mapped_price_type = price_type_map.get(price_type, price_type)
            if (category in self.management_down_payments and
                spec in self.management_down_payments[category] and
                mapped_price_type in self.management_down_payments[category][spec]):
                return self.management_down_payments[category][spec][mapped_price_type]
            else:
                return 0
        except:
            return 0

    # --- 分期計算 ---
    def calculate_total(self, selected_products):
        total_original = 0
        total_discounted = 0
        total_management_fee = 0
        total_down_payment = 0
        total_management_down_payment = 0
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
                'single': '單購-現金價',
                'group_cash': '團購-現金價',
                'group_installment': '團購-分期價'
            }

            price_key = price_key_map[price_type]
            product_price = product_data.get(price_key, 0) * quantity

            # 晨星2人團購管理費特例
            if product['category'] == "恩典園一期" and product['spec'] == "晨星2人" and price_type == "group_cash":
                management_fee_per_unit = product_data.get("團購-管理費", 0)
            else:
                management_fee_per_unit = product_data.get("管理費", 0)

            management_fee = management_fee_per_unit * quantity

            installment_terms = product_data.get("分期期數", 0)
            down_payment = self.get_down_payment(product['category'], product['spec'], price_type, product_price, management_fee)
            management_down_payment = self.get_management_down_payment(product['category'], product['spec'], price_type, product_price, management_fee)

            total_original += product_data.get("定價", 0) * quantity
            total_discounted += product_price
            total_management_fee += management_fee
            total_down_payment += down_payment
            total_management_down_payment += management_down_payment

            product_details.append({
                "類型": product['category'],
                "項目": product['spec'],
                "購買方式": price_key,
                "數量": quantity,
                "產品金額": f"{product_price:,.0f}",
                "管理費": f"{management_fee:,.0f}",
                "分期期數": installment_terms,
                "產品頭款": f"{down_payment:,.0f}",
                "管理費頭款": f"{management_down_payment:,.0f}"
            })

        total_summary = {
            "原價總計": total_original,
            "優惠後總價": total_discounted,
            "管理費總計": total_management_fee,
            "產品頭款總計": total_down_payment,
            "管理費頭款總計": total_management_down_payment,
            "應繳頭款合計": total_down_payment + total_management_down_payment
        }

        return pd.DataFrame(product_details), total_summary


# ======================================================
# Streamlit 主畫面
# ======================================================
st.title("📋 綠金園規劃配置建議書")

proposal = GreenGardenProposal()

# 模擬選擇資料
selected_products = [
    {"type": "cemetery", "category": "恩典園一期", "spec": "晨星2人", "price_type": "group_cash", "quantity": 2},
    {"type": "memorial", "category": "彌陀廳", "spec": "7、8", "price_type": "single", "quantity": 1},
]

df, summary = proposal.calculate_total(selected_products)

st.subheader("商品明細")
st.dataframe(df, use_container_width=True)

st.subheader("總計資訊")
st.write(f"原價總計：{summary['原價總計']:,}")
st.write(f"優惠後總價：{summary['優惠後總價']:,}")
st.write(f"管理費總計：{summary['管理費總計']:,}")
st.write(f"應繳頭款合計：{summary['應繳頭款合計']:,}")
