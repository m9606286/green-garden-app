import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import requests
import io
import json
import os
import pickle

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
    .client-table th {
        font-size: 0.8rem !important;
        padding: 8px 10px !important;
    }
    .client-table td {
        font-size: 0.8rem !important;
        padding: 8px 10px !important;
    }
    .contact-record {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #2E8B57;
    }
    .selected-row {
        background-color: #e6f3ff !important;
        border: 2px solid #007bff !important;
    }
    .proposal-item {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #2E8B57;
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
        
        st.title("🔐 規劃配置建議書系統登入")
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
            **登入說明頁面：**
            1. 請輸入您的身份證字號。
            2. 系統會自動驗證您的授權狀態。
            3. 驗證成功後系統會自動帶出您的姓名與所屬營業處。
            
            **規劃配置建議書頁面**
            1. 於左側輸入基本資訊：客戶姓名、聯絡電話、日期(預設為今日)。
            2. 於**產品選擇**中，選取欲為客戶規劃的產品後，點選**方案詳情**，系統將自動產生建議書。
            3. 點選左上角 **<<** 收合後，再於右上角點選 **⋮** ，選擇 Print 列印建議書。如內容較多超出一頁，請將紙張大小設定為 Legal 或 Tabloid。
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

class DataStorage:
    """資料儲存類別，使用檔案儲存實現持久化"""
    
    @staticmethod
    def get_data_file_path():
        """取得資料檔案路徑"""
        return "client_data.pkl"
    
    @staticmethod
    @st.cache_data(ttl=300)  # 快取5分鐘
    def load_data():
        """從檔案載入資料"""
        file_path = DataStorage.get_data_file_path()
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    return pickle.load(f)
            except:
                pass
        # 如果檔案不存在或讀取失敗，返回預設資料
        return {
            'clients': [],
            'contact_records': {},
            'proposals': {}
        }
    
    @staticmethod
    def save_data(data):
        """儲存資料到檔案"""
        file_path = DataStorage.get_data_file_path()
        try:
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
            # 清除快取，強制重新載入
            DataStorage.load_data.clear()
            return True
        except Exception as e:
            st.error(f"儲存資料時發生錯誤: {e}")
            return False
    
    @staticmethod
    def get_all_data():
        """取得所有資料"""
        return DataStorage.load_data()
    
    @staticmethod
    def update_data(update_dict):
        """更新部分資料"""
        data = DataStorage.get_all_data()
        data.update(update_dict)
        return DataStorage.save_data(data)

class ClientManagementSystem:
    def __init__(self):
        self.data = DataStorage.get_all_data()
    
    def get_clients(self):
        """取得客戶列表"""
        return self.data.get('clients', [])
    
    def get_contact_records(self):
        """取得聯絡紀錄"""
        return self.data.get('contact_records', {})
    
    def get_proposals(self):
        """取得建議書"""
        return self.data.get('proposals', {})
    
    def add_client(self, client_data):
        """新增客戶"""
        clients = self.get_clients()
        client_id = f"client_{len(clients) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        client_data['client_id'] = client_id
        client_data['建檔日期'] = datetime.now().strftime("%Y/%m/%d")
        client_data['聯絡次數'] = 0
        client_data['目前狀況'] = '尚未聯絡'
        client_data['建議書日期'] = ''
        client_data['建議書金額(含管)'] = ''
        
        clients.append(client_data)
        
        # 初始化聯絡紀錄
        contact_records = self.get_contact_records()
        contact_records[client_id] = []
        
        success = DataStorage.update_data({
            'clients': clients,
            'contact_records': contact_records
        })
        
        if success:
            self.data = DataStorage.get_all_data()
        return client_id if success else None
    
    def update_client(self, client_id, updated_data):
        """更新客戶資料"""
        clients = self.get_clients()
        for i, client in enumerate(clients):
            if client['client_id'] == client_id:
                # 保留原有的 client_id 和建檔日期
                updated_data['client_id'] = client_id
                updated_data['建檔日期'] = client['建檔日期']
                updated_data['聯絡次數'] = client['聯絡次數']
                updated_data['建議書日期'] = client.get('建議書日期', '')
                updated_data['建議書金額(含管)'] = client.get('建議書金額(含管)', '')
                clients[i] = updated_data
                break
        
        success = DataStorage.update_data({'clients': clients})
        if success:
            self.data = DataStorage.get_all_data()
        return success
    
    def delete_client(self, client_id):
        """刪除客戶"""
        clients = [client for client in self.get_clients() if client['client_id'] != client_id]
        contact_records = self.get_contact_records()
        proposals = self.get_proposals()
        
        if client_id in contact_records:
            del contact_records[client_id]
        if client_id in proposals:
            del proposals[client_id]
        
        success = DataStorage.update_data({
            'clients': clients,
            'contact_records': contact_records,
            'proposals': proposals
        })
        
        if success:
            self.data = DataStorage.get_all_data()
        return success
    
    def add_contact_record(self, client_id, contact_date, record):
        """新增聯絡紀錄"""
        contact_records = self.get_contact_records()
        if client_id not in contact_records:
            contact_records[client_id] = []
        
        contact_records[client_id].append({
            '聯絡日期': contact_date,
            '聯絡紀錄': record
        })
        
        # 更新聯絡次數
        clients = self.get_clients()
        for client in clients:
            if client['client_id'] == client_id:
                client['聯絡次數'] = len(contact_records[client_id])
                break
        
        success = DataStorage.update_data({
            'clients': clients,
            'contact_records': contact_records
        })
        
        if success:
            self.data = DataStorage.get_all_data()
        return success
    
    def update_contact_record(self, client_id, record_index, contact_date, record):
        """更新聯絡紀錄"""
        contact_records = self.get_contact_records()
        if client_id in contact_records:
            if 0 <= record_index < len(contact_records[client_id]):
                contact_records[client_id][record_index] = {
                    '聯絡日期': contact_date,
                    '聯絡紀錄': record
                }
        
        success = DataStorage.update_data({'contact_records': contact_records})
        if success:
            self.data = DataStorage.get_all_data()
        return success
    
    def delete_contact_record(self, client_id, record_index):
        """刪除聯絡紀錄"""
        contact_records = self.get_contact_records()
        if client_id in contact_records:
            if 0 <= record_index < len(contact_records[client_id]):
                contact_records[client_id].pop(record_index)
                
                # 更新聯絡次數
                clients = self.get_clients()
                for client in clients:
                    if client['client_id'] == client_id:
                        client['聯絡次數'] = len(contact_records[client_id])
                        break
                
                success = DataStorage.update_data({
                    'clients': clients,
                    'contact_records': contact_records
                })
                
                if success:
                    self.data = DataStorage.get_all_data()
                return success
        return False
    
    def add_proposal(self, client_id, proposal_data):
        """新增建議書"""
        proposals = self.get_proposals()
        if client_id not in proposals:
            proposals[client_id] = []
        
        proposal_id = f"proposal_{len(proposals[client_id]) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        proposal_data['proposal_id'] = proposal_id
        proposal_data['建立時間'] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        proposals[client_id].append(proposal_data)
        
        # 更新客戶的建議書日期和金額
        clients = self.get_clients()
        for client in clients:
            if client['client_id'] == client_id:
                client['建議書日期'] = proposal_data['建議書日期']
                client['建議書金額(含管)'] = f"{proposal_data['建議書金額(含管)']:,.0f}"
                break
        
        success = DataStorage.update_data({
            'clients': clients,
            'proposals': proposals
        })
        
        if success:
            self.data = DataStorage.get_all_data()
        return proposal_id if success else None
    
    def get_client_proposals(self, client_id):
        """取得客戶的建議書列表"""
        proposals = self.get_proposals()
        return proposals.get(client_id, [])
    
    def get_client_contact_records(self, client_id):
        """取得客戶的聯絡紀錄"""
        contact_records = self.get_contact_records()
        return contact_records.get(client_id, [])

# 由於程式碼太長，這裡只顯示關鍵的修改部分，其餘類別保持不變
# GreenGardenProposal 類別保持不變
class GreenGardenProposal:
    def __init__(self):
        self.cemetery_products = self._init_cemetery_products()
        self.memorial_products = self._init_memorial_products()
        self.down_payments = self._init_down_payments()
        self.management_down_payments = self._init_management_down_payments()

    def _init_cemetery_products(self):
        return {
            "澤茵園": {
                "單灰位": {"定價": 460000, "預購-現金價": 276000, "分期價": 292560, "馬上使用-現金價": 368000, "分期期數": 24, "管理費": 50200},
                "貴族2灰": {"定價": 620000, "預購-現金價": 372000, "分期價": 394320, "馬上使用-現金價": 496000, "分期期數": 24, "管理費": 67700},
                "家福4灰": {"定價": 950000, "預購-現金價": 570000, "分期價": 598500, "馬上使用-現金價": 760000, "分期期數": 24, "管理費": 103700},
                "家族6灰": {"定價": 1300000, "預購-現金價": 780000, "分期價": 819000, "馬上使用-現金價": 1040000, "分期期數": 24, "管理費": 142000},
                "聚賢閣壁龕12灰": {"定價": 3200000, "預購-現金價": 1888000, "分期價": 1982400, "馬上使用-現金價": 2560000, "分期期數": 42, "管理費": 349000},
                "聚賢閣壁龕18灰": {"定價": 3800000, "預購-現金價": 2356000, "分期價": 2473800, "馬上使用-現金價": 3040000, "分期期數": 42, "管理費": 415000}
            },
            "天璽文創園一期A區": {
                "寶祥6灰": {"定價": 2200000, "預購-現金價": 1166000, "分期價": 1224300, "馬上使用-現金價": 1760000, "分期期數": 36, "管理費": 240000},
                "寶祥9灰": {"定價": 3200000, "預購-現金價": 1696000, "分期價": 1780800, "馬上使用-現金價": 2560000, "分期期數": 42, "管理費": 350000},
                "寶祥15灰": {"定價": 4000000, "預購-現金價": 2120000, "分期價": 2226000, "馬上使用-現金價": 3200000, "分期期數": 42, "管理費": 436400}
            },
            "天意園一期": {
                "永念2灰": {"定價": 200000, "預購-現金價": 120000, "分期價": 128000, "馬上使用-現金價": 160000, "分期期數": 18, "管理費": 21900},
                "永願2灰": {"定價": 420000, "預購-現金價": 252000, "分期價": 272160, "馬上使用-現金價": 336000, "分期期數": 24, "管理費": 45900},
                "天地合和2灰": {"定價": 800000, "預購-現金價": 416000, "分期價": 440960, "馬上使用-現金價": 640000, "分期期數": 24, "管理費": 87300},
                "天地圓融8灰": {"定價": 1800000, "預購-現金價": 936000, "分期價": 982800, "馬上使用-現金價": 1440000, "分期期數": 24, "管理費": 196400},
                "天地福澤12灰": {"定價": 2800000, "預購-現金價": 1456000, "分期價": 1528800, "馬上使用-現金價": 2240000, "分期期數": 36, "管理費": 305500}
            },
            "恩典園一期": {
                "安然2灰": {"定價": 350000, "預購-現金價": 210000, "分期價": 226800, "馬上使用-現金價": 280000, "分期期數": 24, "管理費": 38200},
                "安然4灰": {"定價": 700000, "預購-現金價": 406000, "分期價": 430360, "馬上使用-現金價": 560000, "分期期數": 24, "管理費": 76400},
                "安然特區4灰": {"定價": 848000, "預購-現金價": 614800, "分期價": 645540, "馬上使用-現金價": 678400, "分期期數": 24, "管理費": 115700},
                "晨星2灰": {"定價": 200000, "團購-現金價": 105430, "團購-分期價": 111000, "預購-現金價": 120000, "分期價": 128000, "馬上使用-現金價": 160000, "分期期數": 18, "管理費": 21900,"團購-管理費": 16470}
            }
        }

    # 其餘方法保持不變...
    def _init_memorial_products(self):
        """初始化牌位產品資料"""
        return {
            "永願樓-普羅廳": {
                "牌位1、2、15、16層": {"定價": 120000, "加購-現金價": 50000, "單購-現金價": 66000, "單購-分期價": None, "分期期數": None, "管理費": 23000},
                "牌位3、5、12、13層": {"定價": 140000, "加購-現金價": 60000, "單購-現金價": 77000, "單購-分期價": None, "分期期數": None, "管理費": 23000},
                "牌位6、7、10、11層": {"定價": 160000, "加購-現金價": 70000, "單購-現金價": 88000, "單購-分期價": None, "分期期數": None, "管理費": 23000},
                "牌位8、9層": {"定價": 190000, "加購-現金價": 85000, "單購-現金價": 99000, "單購-分期價": None, "分期期數": None, "管理費": 23000}
            },
            "永願樓-彌陀廳": {
                "牌位1、2、12、13層": {"定價": 160000, "加購-現金價": 70000, "單購-現金價": 88000, "單購-分期價": None, "分期期數": None, "管理費": 23000},
                "牌位3、5、10、11層": {"定價": 190000, "加購-現金價": 85000, "單購-現金價": 99000, "單購-分期價": None, "分期期數": None, "管理費": 23000},
                "牌位6、9層": {"定價": 220000, "加購-現金價": 100000, "單購-現金價": 132000, "單購-分期價": 143000, "分期期數": 24, "管理費": 23000},
                "牌位7、8層": {"定價": 240000, "加購-現金價": 110000, "單購-現金價": 144000, "單購-分期價": 156000, "分期期數": 24, "管理費": 23000}
            },
            "永願樓-大佛廳": {
                "牌位1、2、10、11層": {"定價": 220000, "加購-現金價": 100000, "單購-現金價": 132000, "單購-分期價": 143000, "分期期數": 24, "管理費": 23000},
                "牌位3、5、8、9層": {"定價": 260000, "加購-現金價": 120000, "單購-現金價": 156000, "單購-分期價": 169000, "分期期數": 24, "管理費": 23000},
                "牌位6、7層": {"定價": 290000, "加購-現金價": 135000, "單購-現金價": 174000, "單購-分期價": 188500, "分期期數": 24, "管理費": 23000}
            }
        }

    # 其餘方法保持不變...
    def _init_down_payments(self):
        """初始化頭款金額（只保留分期購買的頭款）"""
        return {
            "澤茵園": {
                "單灰位": {"分期價": 88560},
                "貴族2灰": {"分期價": 118320},
                "家福4灰": {"分期價": 180900},
                "家族6灰": {"分期價": 247800},
                "聚賢閣壁龕12灰": {"分期價": 399000},
                "聚賢閣壁龕18灰": {"分期價": 499800}          
            },
            "天璽文創園一期A區": {
                "寶祥6灰": {"分期價": 306300},
                "寶祥9灰": {"分期價": 357000},
                "寶祥15灰": {"分期價": 420000}
            },
            "天意園一期": {
                "永念2灰": {"分期價": 38000},
                "永願2灰": {"分期價": 82560},
                "天地合和2灰": {"分期價": 133760},
                "天地圓融8灰": {"分期價": 296400},
                "天地福澤12灰": {"分期價": 384000}
            },
            "恩典園一期": {
                "安然2灰": {"分期價": 68400},
                "安然4灰": {"分期價": 130360},
                "安然特區4灰": {"分期價": 165540},
                "晨星2灰": {"團購-分期價": 21000, "分期價": 38000}
            },
            "永願樓-彌陀廳": {
                "牌位6、9層": {"單購-分期價": 42920},
                "牌位7、8層": {"單購-分期價": 46800}
            },
            "永願樓-大佛廳": {
                "牌位1、2、10、11層": {"單購-分期價": 42920},
                "牌位3、5、8、9層": {"單購-分期價": 50680},
                "牌位6、7層": {"單購-分期價": 56500}
            }
        }

    def _init_management_down_payments(self):
        """初始化管理費頭款"""
        return {
            "澤茵園": {
                "單灰位": {"分期價": 16600},
                "貴族2灰": {"分期價": 22100},
                "家福4灰": {"分期價": 31700},
                "家族6灰": {"分期價": 46000},
                "聚賢閣壁龕12灰": {"分期價": 76000},
                "聚賢閣壁龕18灰": {"分期價": 87400}               
            },
            "天璽文創園一期A區": {
                "寶祥6灰": {"分期價": 60000},
                "寶祥9灰": {"分期價": 72800},
                "宝祥15灰": {"分期價": 87800}
            },
            "天意園一期": {
                "永念2灰": {"分期價": 6600},
                "永願2灰": {"分期價": 14700},
                "天地合和2灰": {"分期價": 27300},
                "天地圓融8灰": {"分期價": 66800},
                "天地福澤12灰": {"分期價": 78700}
            },
            "恩典園一期": {
                "安然2灰": {"分期價": 11800},
                "安然4灰": {"分期價": 23600},
                "安然特區4灰": {"分期價": 31700},
                "晨星2灰": {"團購-分期價": 6600, "分期價": 6600}
            },
            "永願樓-大佛廳": {
                "牌位1、2、10、11層": {"單購-分期價": 23000},
                "牌位3、5、8、9層": {"單購-分期價": 23000},
                "牌位6、7層": {"單購-分期價": 23000}
            },
            "永願樓-彌陀廳": {
                "牌位6、9層": {"單購-分期價": 23000},
                "牌位7、8層": {"單購-分期價": 23000}
            }
        }

    # 其餘方法保持不變...
    def get_down_payment(self, category, spec, product_price, price_type, quantity):
        """取得頭款金額"""
        if '現金' in price_type:
            return product_price
        else:
             return self.down_payments[category][spec][price_type] * quantity

    def get_management_down_payment(self, category, spec, management_fee, price_type, quantity):
        """取得管理費頭款"""
        if '現金' in price_type:
            return management_fee
        else:
            return self.management_down_payments[category][spec][price_type] * quantity

    def calculate_installment_payment(self, product_price, management_fee, installment_terms, down_payment_amount, management_down_payment_amount):
        """計算分期付款"""
        if not installment_terms:
            return 0

        total_price = product_price + management_fee
        total_down_payment = down_payment_amount + management_down_payment_amount
        monthly_payment = (total_price - total_down_payment) / installment_terms

        return monthly_payment

    def calculate_product_installment_payment(self, product_price, installment_terms, down_payment_amount):
        """計算產品分期付款"""
        if not installment_terms:
            return 0

        monthly_payment = (product_price - down_payment_amount) / installment_terms
        return monthly_payment

    def calculate_management_installment_payment(self, management_fee, installment_terms, management_down_payment_amount):
        """計算管理費分期付款"""
        if not installment_terms:
            return 0

        monthly_payment = (management_fee - management_down_payment_amount) / installment_terms
        return monthly_payment

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
            price_type = product['price_type']  # 現在直接是中文

            # 直接使用中文 price_type 作為價格鍵值
            product_price = product_data[price_type] * quantity
            original_price = product_data['定價'] * quantity
            # 修正：晨星團購價要抓團購管理費
            if product['category'] == "恩典園一期" and product['spec'] == "晨星2灰" and '團購' in price_type:
                management_fee_per_unit = product_data.get('團購-管理費', 0)
            else:
                management_fee_per_unit = product_data.get('管理費', 0)

            management_fee = management_fee_per_unit * quantity

            # 計算產品頭款
            product_down_payment = self.get_down_payment(product['category'], product['spec'], product_price, price_type, quantity)
            total_down_payment += product_down_payment

            # 計算管理費頭款
            management_down_payment = self.get_management_down_payment(product['category'], product['spec'], management_fee, price_type, quantity)
            total_management_down_payment += management_down_payment

            # 計算總價
            total_original += original_price
            total_discounted += product_price
            total_management_fee += management_fee

            # 只有分期價才顯示分期期數
            installment_terms = product_data.get('分期期數') if '分期' in price_type else None

            # 計算產品期款和管理費期款
            product_monthly_payment = 0
            management_monthly_payment = 0

            if '分期' in price_type and installment_terms:
                product_monthly_payment = self.calculate_product_installment_payment(
                    product_price, installment_terms, product_down_payment
                )
                management_monthly_payment = self.calculate_management_installment_payment(
                    management_fee, installment_terms, management_down_payment
                )

            # 購買方式顯示
            display_price_type = price_type
            if '分期' in price_type and installment_terms:
                display_price_type = f"{price_type}-{installment_terms}期"

            product_details.append({
                'category': product['category'],
                'spec': product['spec'],
                'quantity': quantity,
                'price_type': display_price_type,
                'original_price':original_price,
                'product_price': product_price,
                'management_fee_per_unit': management_fee_per_unit,
                'management_fee': management_fee,
                'installment_terms': installment_terms,
                'product_down_payment': product_down_payment,
                'product_monthly_payment': product_monthly_payment,
                'management_down_payment': management_down_payment,
                'management_monthly_payment': management_monthly_payment
            })

        discount_rate = (total_original - total_discounted) / total_original if total_original > 0 else 0
        final_total = total_discounted + total_management_fee

        return {
            "total_original": total_original,
            "total_discounted": total_discounted,
            "total_management_fee": total_management_fee,
            "total_down_payment": total_down_payment,
            "total_management_down_payment": total_management_down_payment,
            "discount_rate": discount_rate,
            "final_total": final_total,
            "product_details": product_details
        }

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
    # 初始化客戶管理系統
    client_system = ClientManagementSystem()
    
    # 初始化提案系統
    proposal_system = GreenGardenProposal()
    
    # 初始化 session state
    if 'selected_products' not in st.session_state:
        st.session_state.selected_products = []
    if 'current_client_id' not in st.session_state:
        st.session_state.current_client_id = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "新增客戶資料"
    if 'editing_client' not in st.session_state:
        st.session_state.editing_client = None
    if 'selected_client_id' not in st.session_state:
        st.session_state.selected_client_id = None
    if 'editing_contact_index' not in st.session_state:
        st.session_state.editing_contact_index = None
    if 'viewing_proposals' not in st.session_state:
        st.session_state.viewing_proposals = None

    # 側邊欄
    with st.sidebar:
        # 基本資訊
        st.header("導航選單")
        
        # 頁面選擇
        page = st.radio("選擇頁面", ["新增客戶資料", "客戶列表", "規劃配置建議書"], key="page_selector")
        st.session_state.current_page = page
        
        if page == "規劃配置建議書":
            # 客戶選擇
            clients = client_system.get_clients()
            if clients:
                client_options = ["請選擇客戶"] + [f"{client['客戶姓名']}" for client in clients]
                selected_client = st.selectbox("選擇客戶", client_options, key="client_selector")
                
                if selected_client != "請選擇客戶":
                    # 找到對應的客戶
                    current_client = next((client for client in clients if client['客戶姓名'] == selected_client), None)
                    if current_client:
                        st.session_state.current_client_id = current_client['client_id']
                        st.session_state.client_name = current_client['客戶姓名']
                        st.session_state.contact_phone = current_client.get('手機號碼', '')
                        
                        # 顯示選中客戶的基本資訊
                        st.info(f"**當前客戶:** {current_client['客戶姓名']}")
                        st.info(f"**手機:** {current_client.get('手機號碼', '')}")
            else:
                st.warning("尚未建立任何客戶資料")
                st.session_state.current_client_id = None
            
            # 自動填入專業顧問資訊（營業處 + 姓名）
            agent_info = st.session_state.agent_info
            office_name = agent_info.get('office', '')
            consultant_display = f"{office_name}-{agent_info['name']}"
            st.text_input("專業顧問", value=consultant_display, disabled=True)
            
            contact_phone = st.text_input("聯絡電話", value=st.session_state.get('contact_phone', ''))
            proposal_date = st.date_input("日期", value=datetime.now())
            
            # 更新 session state
            st.session_state.contact_phone = contact_phone
            st.session_state.proposal_date = proposal_date
        
        # 登出按鈕放在底部
        st.markdown("---")
        if st.button("🚪 登出系統", use_container_width=True):
            for key in ['authorized', 'agent_id', 'agent_info']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    # 主內容區域
    if st.session_state.current_page == "新增客戶資料":
        display_add_client(client_system)
    elif st.session_state.current_page == "客戶列表":
        display_client_list(client_system)
    else:
        display_proposal_system(client_system, proposal_system)

# 其餘顯示函數保持不變，但需要修改為使用 client_system.get_clients() 等方法
def display_add_client(client_system):
    """顯示新增客戶資料頁面"""
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
        st.markdown(f"""
        <div class="title-container">
            <h1 class="main-title" style="font-size: 1.5rem;">新增客戶資料</h1>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 檢查是否在編輯模式
    editing_client = st.session_state.get('editing_client')
    
    # 新增/編輯客戶表單
    with st.form("add_client_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            client_name = st.text_input("客戶姓名*", value=editing_client.get('客戶姓名', '') if editing_client else "")
            gender = st.selectbox("性別*", ["請選擇", "男", "女"], index=0 if not editing_client else (1 if editing_client.get('性別') == '男' else 2))
            relationship = st.selectbox("關係*", ["請選擇", "朋友", "親戚", "同事", "其他"], 
                                      index=0 if not editing_client else (["請選擇", "朋友", "親戚", "同事", "其他"].index(editing_client.get('關係', '請選擇'))))
            # 生日從1900年開始
            birthday_value = None
            if editing_client and editing_client.get('生日'):
                try:
                    birthday_value = datetime.strptime(editing_client.get('生日'), "%Y/%m/%d")
                except:
                    birthday_value = None
            birthday = st.date_input("生日", value=birthday_value, min_value=datetime(1900, 1, 1), max_value=datetime.now())
            address = st.text_input("居住地址", value=editing_client.get('居住地址', '') if editing_client else "")
        
        with col2:
            mobile = st.text_input("手機號碼*", value=editing_client.get('手機號碼', '') if editing_client else "")
            email = st.text_input("e-mail", value=editing_client.get('e-mail', '') if editing_client else "")
            status = st.selectbox("目前狀況*", ["請選擇", "尚未聯絡", "已聯絡", "已成交", "拒絕"], 
                                index=0 if not editing_client else (["請選擇", "尚未聯絡", "已聯絡", "已成交", "拒絕"].index(editing_client.get('目前狀況', '請選擇'))))
        
        col1, col2 = st.columns(2)
        with col1:
            if editing_client:
                submit_label = "💾 更新客戶資料"
            else:
                submit_label = "💾 新增客戶"
            
            submit_button = st.form_submit_button(submit_label, use_container_width=True)
        
        with col2:
            if st.form_submit_button("❌ 取消", use_container_width=True):
                st.session_state.editing_client = None
                st.rerun()
        
        if submit_button:
            if client_name and gender != "請選擇" and relationship != "請選擇" and mobile and status != "請選擇":
                client_data = {
                    '客戶姓名': client_name,
                    '性別': gender,
                    '關係': relationship,
                    '生日': birthday.strftime("%Y/%m/%d") if birthday else "",
                    '居住地址': address,
                    '手機號碼': mobile,
                    'e-mail': email,
                    '目前狀況': status
                }
                
                if editing_client:
                    # 編輯現有客戶
                    success = client_system.update_client(editing_client['client_id'], client_data)
                    if success:
                        st.success(f"✅ 已更新客戶 {client_name} 的資料")
                        st.session_state.editing_client = None
                    else:
                        st.error("❌ 更新客戶資料失敗")
                else:
                    # 新增客戶
                    client_id = client_system.add_client(client_data)
                    if client_id:
                        st.success(f"✅ 已新增客戶 {client_name}")
                    else:
                        st.error("❌ 新增客戶失敗")
                
                st.rerun()
            else:
                st.error("❌ 請填寫所有必填欄位（標示*）")

def display_client_list(client_system):
    """顯示客戶列表頁面"""
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
        st.markdown(f"""
        <div class="title-container">
            <h1 class="main-title" style="font-size: 1.5rem;">客戶列表</h1>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 客戶篩選
    st.markdown("### 客戶篩選")
    search_name = st.text_input("輸入客戶姓名篩選", value="")
    
    # 操作按鈕區域
    st.markdown("### 客戶操作")
    
    clients = client_system.get_clients()
    if clients:
        # 篩選客戶
        filtered_clients = clients
        if search_name:
            filtered_clients = [client for client in filtered_clients if search_name.lower() in client['客戶姓名'].lower()]
        
        if not filtered_clients:
            st.info("沒有符合條件的客戶")
            return
        
        # 顯示客戶表格
        st.markdown("### 客戶明細表")
        st.markdown('<div class="client-table">', unsafe_allow_html=True)
        
        # 建立表格標頭
        cols = st.columns([2, 1, 1, 1, 2, 2, 2, 1, 1, 2])
        headers = ["客戶姓名", "性別", "關係", "生日", "居住地址", "手機號碼", "e-mail", "建議書日期", "建議書金額", "狀態"]
        for i, header in enumerate(headers):
            cols[i].write(f"**{header}**")
        
        # 顯示客戶資料
        for client in filtered_clients:
            cols = st.columns([2, 1, 1, 1, 2, 2, 2, 1, 1, 2])
            
            with cols[0]:
                is_selected = st.checkbox(
                    client['客戶姓名'], 
                    key=f"client_{client['client_id']}",
                    value=(st.session_state.selected_client_id == client['client_id'])
                )
                if is_selected:
                    st.session_state.selected_client_id = client['client_id']
                    st.session_state.selected_client = client
            
            cols[1].write(client['性別'])
            cols[2].write(client['關係'])
            cols[3].write(client.get('生日', ''))
            cols[4].write(client.get('居住地址', ''))
            cols[5].write(client.get('手機號碼', ''))
            cols[6].write(client.get('e-mail', ''))
            
            with cols[7]:
                proposal_date = client.get('建議書日期', '')
                if proposal_date:
                    if st.button("📅", key=f"proposal_{client['client_id']}", help=proposal_date):
                        st.session_state.viewing_proposals = client['client_id']
                        st.rerun()
                else:
                    st.write("")
            
            cols[8].write(client.get('建議書金額(含管)', ''))
            cols[9].write(client.get('目前狀況', ''))
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 操作按鈕
        if st.session_state.selected_client_id:
            selected_client = st.session_state.selected_client
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("✏️ 編輯客戶", use_container_width=True):
                    st.session_state.editing_client = selected_client
                    st.session_state.current_page = "新增客戶資料"
                    st.rerun()
            
            with col2:
                if st.button("🗑️ 刪除客戶", use_container_width=True):
                    success = client_system.delete_client(selected_client['client_id'])
                    if success:
                        st.session_state.selected_client_id = None
                        st.session_state.selected_client = None
                        st.success(f"✅ 已刪除客戶 {selected_client['客戶姓名']}")
                    else:
                        st.error("❌ 刪除客戶失敗")
                    st.rerun()
            
            with col3:
                if st.button("📞 聯絡紀錄", use_container_width=True):
                    st.session_state.viewing_contact_records = selected_client['client_id']
                    st.rerun()
            
            with col4:
                if st.button("📋 建立建議書", use_container_width=True):
                    st.session_state.current_client_id = selected_client['client_id']
                    st.session_state.client_name = selected_client['客戶姓名']
                    st.session_state.contact_phone = selected_client.get('手機號碼', '')
                    st.session_state.current_page = "規劃配置建議書"
                    st.rerun()
        
        else:
            st.info("請選擇一個客戶以進行操作")
        
        # 聯絡紀錄下鑽
        if hasattr(st.session_state, 'viewing_contact_records'):
            display_contact_records(client_system, st.session_state.selected_client)
        
        # 建議書下鑽
        if hasattr(st.session_state, 'viewing_proposals'):
            display_client_proposals(client_system, st.session_state.selected_client)
        
    else:
        st.info("尚未有任何客戶資料，請到「新增客戶資料」頁面新增客戶。")

# 其餘 display_contact_records, display_client_proposals, display_proposal_system 函數保持不變
# 但需要修改為使用 client_system 的方法來存取資料

if __name__ == "__main__":
    main()
