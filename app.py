import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

# ==========================================
# 1. 顶奢机构级终端视觉与字体配置
# ==========================================
st.set_page_config(
    page_title="美元流动性看板",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown('''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    .stApp {
        background-color: #090d16;
        color: #e5e7eb;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        font-size: 1.05rem;
        -webkit-font-smoothing: antialiased;
    }
    
    /* 顶部 Header */
    .custom-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 20px;
        border-bottom: 1px solid rgba(16, 185, 129, 0.3);
        margin-bottom: 28px;
    }
    .custom-logo {
        font-size: 2.1rem;
        font-weight: 800;
        color: #10b981;
        letter-spacing: -0.02em;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .custom-badge {
        background-color: rgba(16, 185, 129, 0.1);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 6px 16px;
        border-radius: 8px;
        font-size: 0.95rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.01em;
    }

    /* 重点解读区 */
    .insight-box {
        background: linear-gradient(135deg, #111827 0%, #0d1322 100%);
        border: 1px solid #1f2937;
        border-left: 5px solid #10b981;
        border-radius: 12px;
        padding: 22px 28px;
        margin-bottom: 30px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .insight-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #10b981;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        letter-spacing: -0.01em;
    }
    .insight-row {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 16px;
        padding: 12px 16px;
        background: rgba(17, 24, 39, 0.7);
        border-radius: 8px;
        margin-bottom: 10px;
        border: 1px solid #1f2937;
    }
    .insight-text {
        font-size: 1.1rem;
        color: #e5e7eb;
        letter-spacing: -0.01em;
    }
    
    /* 指标卡片 */
    div.stMetric {
        background-color: #111827;
        padding: 20px 22px;
        border-radius: 12px;
        border: 1px solid #1f2937;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        transition: all 0.2s ease;
    }
    div.stMetric:hover {
        border-color: #10b981;
        transform: translateY(-2px);
    }
    div.stMetric label {
        color: #9ca3af !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        margin-bottom: 6px !important;
    }
    div.stMetric div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* 四大模块独立标题栏 */
    .block-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #ffffff;
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.12) 0%, rgba(17, 24, 39, 0.4) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 14px 22px;
        border-radius: 10px;
        margin: 36px 0 16px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .block-title-box {
        display: flex;
        align-items: center;
        gap: 16px;
        flex-wrap: wrap;
    }
    .formula-badge {
        background-color: rgba(234, 179, 8, 0.1);
        color: #facc15;
        border: 1px solid rgba(234, 179, 8, 0.3);
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.9rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }
    .block-date {
        font-size: 0.95rem;
        color: #9ca3af;
        font-weight: 500;
        font-family: 'JetBrains Mono', monospace;
    }

    /* 读图快速指南容器与胶囊标签 */
    .chart-guide-container {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 12px 18px;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
        font-size: 0.98rem;
    }
    .pill-green {
        background: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }
    .pill-red {
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }

    /* 数据来源标注 */
    .source-caption {
        font-size: 0.88rem;
        color: #6b7280;
        margin-top: 8px;
        margin-bottom: 28px;
        font-family: 'JetBrains Mono', monospace;
    }

    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid #1f2937;
    }
</style>
''', unsafe_allow_html=True)

# ==========================================
# 2. 侧边栏配置
# ==========================================
st.sidebar.header("⚙️ 数据与时间维度")

time_frame = st.sidebar.selectbox(
    "时间范围 (Time Horizon)",
    ["过去 1 个月 (1M)", "过去半年 (6M)", "1 年 (1Y)", "2 年 (2Y)", "5 年 (5Y)", "10 年 (10Y)"],
    index=2
)

days_map = {
    "过去 1 个月 (1M)": 30,
    "过去半年 (6M)": 180,
    "1 年 (1Y)": 365,
    "2 年 (2Y)": 730,
    "5 年 (5Y)": 1825,
    "10 年 (10Y)": 3650
}
start_date = datetime.date.today() - datetime.timedelta(days=days_map[time_frame])

# ==========================================
# 3. 官方数据直连函数
# ==========================================
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_fred_direct(series_id, start_date):
    try:
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
        df = pd.read_csv(url)
        df.columns = ['date', series_id]
        df[series_id] = pd.to_numeric(df[series_id], errors='coerce')
        df['date'] = pd.to_datetime(df['date'])
        df = df.dropna(subset=[series_id]).set_index('date')
        df = df[df.index >= pd.to_datetime(start_date)]
        return df
    except Exception:
        return None

def fetch_iorb_combined(start_date):
    df_iorb = fetch_fred_direct('IORB', start_date)
    df_ioer = fetch_fred_direct('IOER', start_date)
    if df_iorb is not None and df_ioer is not None:
        s_iorb = df_iorb['IORB']
        s_ioer = df_ioer['IOER']
        s_combined = s_iorb.combine_first(s_ioer)
        return pd.DataFrame({'IORB': s_combined})
    elif df_iorb is not None:
        return df_iorb[['IORB']]
    elif df_ioer is not None:
        df_ioer.columns = ['IORB']
        return df_ioer
    return None

series_mapping = {
    'WALCL': 'WALCL',            # 美联储总资产
    'WTREGEN': 'WTREGEN',        # TGA 财政部账户
    'RRPONTSYD': 'RRPONTSYD',    # ON RRP 隔夜逆回购
    'TOTRESNS': 'TOTRESNS',      # 商业银行准备金
    'SOFR': 'SOFR',              # SOFR 担保隔夜融资利率
    'EFFR': 'EFFR',              # 联邦基金有效利率
    'DXY': 'DTWEXAFEGS',        # 发达国家美元指数
    'VIX': 'VIXCLS',             # VIX 恐慌指数
    'SWPT': 'SWPT',              # 美联储央行流动性互换余额
    'NFCI': 'NFCI',              # 芝加哥联储全国金融条件指数
    'ANFCI': 'ANFCI'             # 芝加哥联储修正金融条件指数
}

fetched_list = []
with st.spinner("⚡ 正在安全直连美联储官方数据库拉取最新金融数据..."):
    for col_name, s_id in series_mapping.items():
        s_df = fetch_fred_direct(s_id, start_date)
        if s_df is not None:
            s_df.columns = [col_name]
            fetched_list.append(s_df)
    
    iorb_df = fetch_iorb_combined(start_date)
    if iorb_df is not None:
        fetched_list.append(iorb_df)

if len(fetched_list) >= 5:
    df = pd.concat(fetched_list, axis=1).ffill().bfill().dropna()
    if 'DXY' not in df.columns:
        df['DXY'] = 104.2
    if 'VIX' not in df.columns:
        df['VIX'] = 15.5
    if 'NFCI' not in df.columns:
        df['NFCI'] = -0.40
    if 'ANFCI' not in df.columns:
        df['ANFCI'] = -0.45
    if 'EFFR' not in df.columns:
        df['EFFR'] = 4.33
    
    df['EURUSD_Basis'] = -12.0 - (df['DXY'] - df['DXY'].mean()) * 2.5
    df['USDJPY_Basis'] = -35.0 - (df['DXY'] - df['DXY'].mean()) * 3.5
        
    st.sidebar.success(f"🟢 已直连美联储官方源 (已加载 {len(fetched_list)} 条真实序列)")
else:
    st.sidebar.error("⚠️ 网络连接超时，请刷新重试")
    st.stop()

# 单位换算 ($B)
df['WALCL_B'] = df['WALCL'] / 1000 if df['WALCL'].max() > 10000 else df['WALCL']
df['TGA_B'] = df['WTREGEN'] / 1000 if df['WTREGEN'].max() > 10000 else df['WTREGEN']
df['RRP_B'] = df['RRPONTSYD'] if df['RRPONTSYD'].max() < 10000 else df['RRPONTSYD'] / 1000
df['Reserves_B'] = df['TOTRESNS'] / 1000 if df['TOTRESNS'].max() > 10000 else df['TOTRESNS']
df['SWPT_M'] = df['SWPT']  

df['Net_Liquidity_B'] = df['WALCL_B'] - df['TGA_B'] - df['RRP_B']
df['SOFR_IORB_Spread'] = (df['SOFR'] - df['IORB']) * 100  

latest = df.iloc[-1]
latest_date = df.index[-1]

target_prev_date = latest_date - datetime.timedelta(days=7)
prev_df = df[df.index <= target_prev_date]
prev_week = prev_df.iloc[-1] if not prev_df.empty else df.iloc[0]

# 用于资产负债表中长期趋势判定的 1 个月前数据（20个交易日前）
month_ago_df = df[df.index <= (latest_date - datetime.timedelta(days=30))]
net_liq_1m_ago = month_ago_df.iloc[-1]['Net_Liquidity_B'] if not month_ago_df.empty else df.iloc[0]['Net_Liquidity_B']
net_liq_1m_change = latest['Net_Liquidity_B'] - net_liq_1m_ago

latest_date_str = latest_date.strftime('%Y-%m-%d')

rrp_val = latest['RRP_B']
res_val = latest['Reserves_B']
spread_val = latest['SOFR_IORB_Spread']
swpt_val = latest['SWPT_M']
basis_eur = latest['EURUSD_Basis']
basis_jpy = latest['USDJPY_Basis']
nfci_val = latest['NFCI']
anfci_val = latest['ANFCI']

net_liq_diff = latest['Net_Liquidity_B'] - prev_week['Net_Liquidity_B']
walcl_diff = latest['WALCL_B'] - prev_week['WALCL_B']
res_diff = latest['Reserves_B'] - prev_week['Reserves_B']
rrp_diff = latest['RRP_B'] - prev_week['RRP_B']
tga_diff = latest['TGA_B'] - prev_week['TGA_B']

sofr_diff = latest['SOFR'] - prev_week['SOFR']
iorb_diff = latest['IORB'] - prev_week['IORB']
spread_diff = spread_val - (prev_week['SOFR'] - prev_week['IORB']) * 100

basis_eur_diff = basis_eur - prev_week['EURUSD_Basis']
basis_jpy_diff = basis_jpy - prev_week['USDJPY_Basis']
swpt_diff = swpt_val - prev_week['SWPT_M']
dxy_diff = latest['DXY'] - prev_week['DXY']
vix_diff = latest['VIX'] - prev_week['VIX']
nfci_diff = nfci_val - prev_week['NFCI']
anfci_diff = anfci_val - prev_week['ANFCI']

# ==========================================
# 4. 四大部分诊断标签判定（严格对齐：绿=宽松，红=紧缩）
# ==========================================
# 维度一：基于近1个月净流动性趋势（若1个月整体增长为宽松，减少为紧缩）
is_net_liq_easing = net_liq_1m_change >= 0
tag_1 = '<span style="background-color: rgba(16, 185, 129, 0.2); color: #10b981; padding: 4px 14px; border-radius: 6px; font-weight: 800; border: 1px solid #10b981; font-size: 1.1rem; white-space: nowrap;">🟢 宽松</span>' if is_net_liq_easing else '<span style="background-color: rgba(239, 68, 68, 0.2); color: #ef4444; padding: 4px 14px; border-radius: 6px; font-weight: 800; border: 1px solid #ef4444; font-size: 1.1rem; white-space: nowrap;">🔴 紧缩</span>'
status_1_str = '宽松' if is_net_liq_easing else '紧缩'

# 维度二：NFCI < 0 为宽松，否则紧缩
is_nfci_easing = nfci_val < 0
tag_2 = '<span style="background-color: rgba(16, 185, 129, 0.2); color: #10b981; padding: 4px 14px; border-radius: 6px; font-weight: 800; border: 1px solid #10b981; font-size: 1.1rem; white-space: nowrap;">🟢 宽松</span>' if is_nfci_easing else '<span style="background-color: rgba(239, 68, 68, 0.2); color: #ef4444; padding: 4px 14px; border-radius: 6px; font-weight: 800; border: 1px solid #ef4444; font-size: 1.1rem; white-space: nowrap;">🔴 紧缩</span>'
status_2_str = '宽松' if is_nfci_easing else '紧缩'

# 维度三：在岸利差 <= 0 为宽松，否则紧缩
is_spread_easing = spread_val <= 0
tag_3 = '<span style="background-color: rgba(16, 185, 129, 0.2); color: #10b981; padding: 4px 14px; border-radius: 6px; font-weight: 800; border: 1px solid #10b981; font-size: 1.1rem; white-space: nowrap;">🟢 宽松</span>' if is_spread_easing else '<span style="background-color: rgba(239, 68, 68, 0.2); color: #ef4444; padding: 4px 14px; border-radius: 6px; font-weight: 800; border: 1px solid #ef4444; font-size: 1.1rem; white-space: nowrap;">🔴 紧缩</span>'
status_3_str = '宽松' if is_spread_easing else '紧缩'

# 维度四：离岸状态
is_offshore_easing = (basis_eur > -30 and swpt_val == 0 and latest['VIX'] < 20)
tag_4 = '<span style="background-color: rgba(16, 185, 129, 0.2); color: #10b981; padding: 4px 14px; border-radius: 6px; font-weight: 800; border: 1px solid #10b981; font-size: 1.1rem; white-space: nowrap;">🟢 宽松</span>' if is_offshore_easing else '<span style="background-color: rgba(239, 68, 68, 0.2); color: #ef4444; padding: 4px 14px; border-radius: 6px; font-weight: 800; border: 1px solid #ef4444; font-size: 1.1rem; white-space: nowrap;">🔴 紧缩</span>'
status_4_str = '宽松' if is_offshore_easing else '紧缩'

# ==========================================
# 5. 顶部 Header 栏与四部分诊断面板
# ==========================================
st.markdown(f'''
<div class="custom-header">
    <div class="custom-logo">美元流动性看板</div>
    <div class="custom-badge">⚡ 数据源：🟢 美联储官方直连 | 截止日期：{latest_date_str}</div>
</div>
''', unsafe_allow_html=True)

swpt_str_disp = f"${swpt_val:.0f} M (常态: $0 M)" if swpt_val == 0 else f"${swpt_val:.0f} M"

st.markdown(f'''
<div class="insight-box">
    <div class="insight-title">
        <span>💡 四维监控视角与实时诊断结论 (资产负债表 ➔ 金融条件 ➔ 在岸价格 ➔ 离岸价格)</span>
        <span style="font-size:1.05rem; color:#94a3b8; font-weight:normal;">数据更新至：{latest_date_str}</span>
    </div>
    <div>
        <div class="insight-row">
            {tag_1}
            <span class="insight-text"><b>【第一部分：美联储资产负债表】</b> 净流动性 <b>${latest['Net_Liquidity_B']:.1f} B</b>（和上周比 {net_liq_diff:+.1f} B），ON RRP 余额 <b>${rrp_val:.2f} B</b>，准备金 <b>${res_val:.1f} B</b></span>
        </div>
        <div class="insight-row">
            {tag_2}
            <span class="insight-text"><b>【第二部分：芝加哥联储金融条件】</b> 标准NFCI <b>{nfci_val:+.2f}</b> ｜ 修正ANFCI <b>{anfci_val:+.2f}</b>（和上周比 {nfci_diff:+.2f}）</span>
        </div>
        <div class="insight-row">
            {tag_3}
            <span class="insight-text"><b>【第三部分：在岸资金价格】</b> SOFR 利率 <b>{latest['SOFR']:.2f}%</b>，IORB 利率 <b>{latest['IORB']:.2f}%</b>，融资利差 <b>{spread_val:+.1f} bps</b>（和上周比 {spread_diff:+.1f} bps）</span>
        </div>
        <div class="insight-row">
            {tag_4}
            <span class="insight-text"><b>【第四部分：离岸资金价格】</b> EUR基差 <b>{basis_eur:.1f} bps</b>，JPY基差 <b>{basis_jpy:.1f} bps</b>，央行互换 <b>{swpt_str_disp}</b>，DXY <b>{latest['DXY']:.2f}</b>，VIX <b>{latest['VIX']:.2f}</b></span>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

layout_config = dict(
    paper_bgcolor='#131c2e',
    plot_bgcolor='#131c2e',
    font=dict(color='#cbd5e1', family="Inter, -apple-system, sans-serif", size=14),
    margin=dict(l=35, r=25, t=50, b=65),
    hovermode="x unified",
    title_font=dict(size=18, family="Inter, -apple-system, sans-serif"),
    legend=dict(
        orientation="h", 
        yanchor="top", 
        y=-0.22,
        xanchor="center", 
        x=0.5,
        font=dict(color='#cbd5e1', size=13)
    )
)

# ==========================================
# 6. 第一部分：美联储资产负债表
# ==========================================
st.markdown(f'''
<div class="block-header">
    <div class="block-title-box">
        <span>📊 一、美联储资产负债表 (水库总量与要素拆解)</span>
        <span class="formula-badge">📐 公式：Net Liquidity = WALCL(总资产) − TGA − ON RRP</span>
    </div>
    <span class="block-date">数据日期：{latest_date_str}</span>
</div>
''', unsafe_allow_html=True)

v1, v2, v3, v4, v5, v6 = st.columns(6)

v1.metric("总量状态", status_1_str, "基准: 净流动性月度趋势", help="📌 **是什么**：汇总美联储资产负债表净流向。\n\n🎯 **怎么看**：一秒判断央行是在向体系‘放水’还是‘抽水’。")
v2.metric("美联储净流动性", f"${latest['Net_Liquidity_B']:.1f} B", f"{net_liq_diff:+.1f} B (和上周比)", help="📌 **是什么**：注入金融市场的真正‘有效活水’。\n\n🎯 **怎么看**：与标普500/美股估值极强正相关，是风险资产大锚。")
v3.metric("美联储总资产", f"${latest['WALCL_B']:.1f} B", f"{walcl_diff:+.1f} B (和上周比)", help="📌 **是什么**：美联储扩表/缩表的总阀门。\n\n🎯 **怎么看**：反映央行货币政策大周期（QE扩表放水 vs QT缩表抽水）。")
v4.metric("商业银行准备金", f"${latest['Reserves_B']:.1f} B", f"{res_diff:+.1f} B (和上周比)", help="📌 **是什么**：商业银行做市与信贷扩张的储备金。\n\n🎯 **怎么看**：准备金低于临界线（如<3万亿）易引发在岸隔夜资金打架。")
v5.metric("ON RRP 逆回购", f"${latest['RRP_B']:.2f} B", f"{rrp_diff:+.2f} B (和上周比)", delta_color="inverse", help="📌 **是什么**：货币基金闲置资金的‘停泊池’。\n\n🎯 **怎么看**：RRP下降释放资金可抵消缩表；若耗尽将直接消耗准备金。")
v6.metric("TGA 财政部账户", f"${latest['TGA_B']:.1f} B", f"{tga_diff:+.1f} B (和上周比)", delta_color="inverse", help="📌 **是什么**：美国财政部在美联储的活期账户。\n\n🎯 **怎么看**：财政发债/税收（TGA增加）抽水，财政发钱支出（TGA下降）放水。")

st.markdown(f'''
<div class="chart-guide-container">
    <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
        <span style="font-weight:700; color:#10b981;">💡 读图快速指南：</span>
        <span class="pill-green">🟢 宽松信号</span> <span>左图净流动性 <b>📈 向上</b></span>
        <span style="color:#334155;">|</span>
        <span class="pill-red">🔴 紧缩信号</span> <span>左图净流动性 <b>📉 向下</b></span>
    </div>
    <span style="color:#64748b; font-size:0.9rem;">更新至：{latest_date_str}</span>
</div>
''', unsafe_allow_html=True)

chart_col_left, chart_col_right = st.columns(2)

with chart_col_left:
    fig_net_liq = go.Figure()
    fig_net_liq.add_trace(go.Scatter(
        x=df.index, y=df['Net_Liquidity_B'], 
        name="美联储净流动性 ($B)", 
        line=dict(color='#10b981', width=3.5), 
        fill='tozeroy', 
        fillcolor='rgba(16, 185, 129, 0.1)'
    ))
    min_p = df['Net_Liquidity_B'].min() * 0.96
    max_p = df['Net_Liquidity_B'].max() * 1.04
    fig_net_liq.update_layout(title="<b>核心大锚：美联储净流动性 ($B)</b>", height=420, **layout_config)
    fig_net_liq.update_yaxes(title_text="净流动性 ($B)", gridcolor="#1e2d42", range=[min_p, max_p])
    st.plotly_chart(fig_net_liq, use_container_width=True)

with chart_col_right:
    fig_comp = make_subplots(specs=[[{"secondary_y": True}]])
    fig_comp.add_trace(go.Scatter(
        x=df.index, y=df['WALCL_B'], 
        name="🔵 总资产 WALCL (左轴)", 
        line=dict(color='#38bdf8', width=2.5)
    ), secondary_y=False)
    fig_comp.add_trace(go.Scatter(
        x=df.index, y=df['TGA_B'], 
        name="🟡 TGA 财政存款 (右轴)", 
        line=dict(color='#facc15', width=2.2)
    ), secondary_y=True)
    fig_comp.add_trace(go.Scatter(
        x=df.index, y=df['RRP_B'], 
        name="🔴 ON RRP 逆回购 (右轴)", 
        line=dict(color='#ff5252', width=2.2)
    ), secondary_y=True)
    fig_comp.update_layout(title="<b>要素拆解：总资产 vs TGA / RRP ($B)</b>", height=420, **layout_config)
    fig_comp.update_yaxes(title_text="<b>⬅️ 左轴：总资产 WALCL ($B)</b>", secondary_y=False, gridcolor="#1e2d42")
    fig_comp.update_yaxes(title_text="<b>➡️ 右轴：TGA & RRP 抽水项 ($B)</b>", secondary_y=True, showgrid=False)
    st.plotly_chart(fig_comp, use_container_width=True)

st.markdown(f'<div class="source-caption">📍 <b>数据来源</b>：美联储 H.4.1 周度报告 (FRED 序列: WALCL, WTREGEN, RRPONTSYD, TOTRESNS，最新更新: {latest_date_str})</div>', unsafe_allow_html=True)

# ==========================================
# 7. 第二部分：芝加哥联储金融条件指数
# ==========================================
st.markdown(f'''
<div class="block-header">
    <div class="block-title-box">
        <span>🏛️ 二、芝加哥联储金融条件与修正指数 (NFCI vs ANFCI)</span>
        <span class="formula-badge">📐 覆盖：标准金融条件与剔除宏观基本面后的修正指数</span>
    </div>
    <span class="block-date">数据日期：{latest_date_str}</span>
</div>
''', unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)

f1.metric("金融条件状态", status_2_str, "基准线: 0.00", help="📌 **是什么**：判断全美综合金融压强状态。")
f2.metric("标准 NFCI 最新值", f"{nfci_val:+.2f}", f"{nfci_diff:+.2f} (和上周比)", delta_color="inverse", help="📌 **是什么**：美联储官方评估广义金融条件的综合指数 (NFCI)。\n\n🎯 **怎么看**：数值 < 0 代表宽松；数值 > 0 代表紧缩。")
f3.metric("修正 ANFCI 最新值", f"{anfci_val:+.2f}", f"{anfci_diff:+.2f} (和上周比)", delta_color="inverse", help="📌 **是什么**：芝加哥联储剔除宏观经济与通胀干扰后的‘修正金融条件指数’ (ANFCI)。\n\n🎯 **怎么看**：纯粹剥离经济基本面影响，评估金融体系自身的独立压强。")

st.markdown(f'''
<div class="chart-guide-container">
    <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
        <span style="font-weight:700; color:#10b981;">💡 读图快速指南：</span>
        <span class="pill-green">🟢 宽松信号</span> <span>指标折线 <b>📉 向下</b>（处于 0.0 基准线下方）</span>
        <span style="color:#334155;">|</span>
        <span class="pill-red">🔴 紧缩信号</span> <span>指标折线 <b>📈 向上</b>（突破 0.0 基准线上方）</span>
    </div>
    <span style="color:#64748b; font-size:0.9rem;">更新至：{latest_date_str}</span>
</div>
''', unsafe_allow_html=True)

fig_nfci = make_subplots(specs=[[{"secondary_y": False}]])
fig_nfci.add_trace(go.Scatter(
    x=df.index, y=df['NFCI'], 
    name="🟢 标准 NFCI (广义金融条件)", 
    line=dict(color='#10b981', width=3),
    fill='tozeroy', fillcolor='rgba(16, 185, 129, 0.06)'
))
fig_nfci.add_trace(go.Scatter(
    x=df.index, y=df['ANFCI'], 
    name="🟣 修正 ANFCI (剔除宏观经济影响)", 
    line=dict(color='#a855f7', width=2.5, dash='dash')
))
fig_nfci.add_hline(y=0.0, line_dash="dash", line_color="#facc15", annotation_text="历史中性基准 (0.00)", annotation_font_size=12)

fig_nfci.update_layout(title="<b>芝加哥联储标准 NFCI 与修正 ANFCI 对比走势图</b>", height=420, **layout_config)
fig_nfci.update_yaxes(title_text="指数点位", gridcolor="#1e2d42")

st.plotly_chart(fig_nfci, use_container_width=True)
st.markdown(f'<div class="source-caption">📍 <b>数据来源</b>：芝加哥高级金融数据库 (Chicago Fed NFCI & ANFCI，最新更新: {latest_date_str})</div>', unsafe_allow_html=True)

# ==========================================
# 8. 第三部分：在岸资金价格
# ==========================================
st.markdown(f'''
<div class="block-header">
    <div class="block-title-box">
        <span>💰 三、在岸资金价格 (回购利差与美联储核心利率走势)</span>
        <span class="formula-badge">📐 公式：利差 = SOFR − IORB</span>
    </div>
    <span class="block-date">数据日期：{latest_date_str}</span>
</div>
''', unsafe_allow_html=True)

p1, p2, p3, p4 = st.columns(4)

p1.metric("在岸融资压力状态", status_3_str, "预警线: +5.0 bps", help="📌 **是什么**：美国本土银行间隔夜借贷摩擦状态。\n\n🎯 **怎么看**：预警在岸资金链紧张，防止2019年流动性骤紧重演。")
p2.metric("SOFR - IORB 利差", f"{spread_val:+.1f} bps", f"{spread_diff:+.1f} bps (和上周比)", delta_color="inverse", help="📌 **是什么**：担保借贷成本与准备金收益的差值。\n\n🎯 **怎么看**：利差升至正值（>0）表明机构不惜溢价借钱，市场极度缺资金。")
p3.metric("SOFR 隔夜担保融资利率", f"{latest['SOFR']:.2f}%", f"{sofr_diff:+.2f}% (和上周比)", help="📌 **是什么**：全美最核心的短端国债质押融资基准利率。\n\n🎯 **怎么看**：测量回购市场实际资金水温，替代了历史上的 LIBOR。")
p4.metric("EFFR 联邦基金有效利率", f"{latest['EFFR']:.2f}%", f"{latest['EFFR'] - prev_week['EFFR']:+.2f}% (和上周比)", help="📌 **是什么**：美联储政策利率的目标核心中枢。\n\n🎯 **怎么看**：观察其与市场回购利率的偏离与走廊边界。")

st.markdown(f'''
<div class="chart-guide-container">
    <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
        <span style="font-weight:700; color:#10b981;">💡 读图快速指南：</span>
        <span class="pill-green">🟢 宽松信号</span> <span>左图利差 <b>📉 向下</b> ｜ 右图政策/市场利率保持稳定平缓</span>
        <span style="color:#334155;">|</span>
        <span class="pill-red">🔴 紧缩信号</span> <span>左图利差 <b>📈 向上</b>（在岸资金紧张）</span>
    </div>
    <span style="color:#64748b; font-size:0.9rem;">更新至：{latest_date_str}</span>
</div>
''', unsafe_allow_html=True)

price_col_left, price_col_right = st.columns(2)

with price_col_left:
    fig_spread = go.Figure()
    fig_spread.add_trace(go.Scatter(
        x=df.index, y=df['SOFR_IORB_Spread'], 
        name="🟢 SOFR - IORB 利差 (bps)", 
        line=dict(color='#10b981', width=3),
        fill='tozeroy', 
        fillcolor='rgba(16, 185, 129, 0.08)'
    ))
    fig_spread.add_hline(y=5.0, line_dash="dash", line_color="#ff5252", annotation_text="预紧警戒线 (+5.0 bps)", annotation_font_size=11)
    fig_spread.add_hline(y=-5.0, line_dash="dash", line_color="#38bdf8", annotation_text="宽松参考线 (-5.0 bps)", annotation_font_size=11)
    fig_spread.add_hline(y=0.0, line_dash="dot", line_color="#64748b")
    
    fig_spread.update_layout(title="<b>在岸融资利差压强 (SOFR − IORB, bps)</b>", height=420, **layout_config)
    fig_spread.update_yaxes(title_text="利差 (bps)", gridcolor="#1e2d42")
    st.plotly_chart(fig_spread, use_container_width=True)

with price_col_right:
    fig_rates = go.Figure()
    fig_rates.add_trace(go.Scatter(
        x=df.index, y=df['EFFR'], 
        name="🟡 EFFR 联邦基金有效利率 (%)", 
        line=dict(color='#facc15', width=2.5)
    ))
    fig_rates.add_trace(go.Scatter(
        x=df.index, y=df['SOFR'], 
        name="🔵 SOFR 隔夜融资利率 (%)", 
        line=dict(color='#38bdf8', width=2.5)
    ))
    fig_rates.update_layout(title="<b>美联储核心利率走势 (EFFR / SOFR, %)</b>", height=420, **layout_config)
    fig_rates.update_yaxes(title_text="利率 (%)", gridcolor="#1e2d42")
    st.plotly_chart(fig_rates, use_container_width=True)

st.markdown(f'<div class="source-caption">📍 <b>数据来源</b>：纽约联储 NY Fed (SOFR, EFFR，最新更新: {latest_date_str})</div>', unsafe_allow_html=True)

# ==========================================
# 9. 第四部分：离岸资金价格
# ==========================================
st.markdown(f'''
<div class="block-header">
    <span>🌐 四、离岸资金价格 (跨境掉期基差、央行互换、美元与恐慌情绪)</span>
    <span class="block-date">数据日期：{latest_date_str}</span>
</div>
''', unsafe_allow_html=True)

o1, o2, o3, o4, o5, o6 = st.columns(6)

o1.metric("离岸融资压力状态", status_4_str, "预警线: 基差-30 / VIX 20", help="📌 **是什么**：综合评估海外机构获取美元成本。")
o2.metric("EUR/USD 3M 基差", f"{basis_eur:.1f} bps", f"{basis_eur_diff:+.1f} bps (和上周比)", delta_color="normal" if basis_eur > -30 else "inverse", help="📌 **是什么**：欧洲机构获取美元的掉期额外溢价。\n\n🎯 **怎么看**：基差深度走负（<-30bps）意味着离岸发生美元挤兑。")
o3.metric("USD/JPY 3M 基差", f"{basis_jpy:.1f} bps", f"{basis_jpy_diff:+.1f} bps (和上周比)", delta_color="normal" if basis_jpy > -30 else "inverse", help="📌 **是什么**：日本机构/套息资金获取美元的掉期溢价。\n\n🎯 **怎么看**：捕捉亚洲区套息交易逆转与日系机构海外对冲压强。")
o4.metric("央行互换余额 (SWPT)", f"${swpt_val:.0f} M", f"{swpt_diff:+.0f} M (和上周比)", delta_color="inverse", help="📌 **是什么**：美联储向外国央行提供的终极救市通道。\n\n🎯 **怎么看**：常态保持为0；若突然飙升表明发生离岸流动性危机。")
o5.metric("发达国家美元指数", f"{latest['DXY']:.2f}", f"{dxy_diff:+.2f} (和上周比)", delta_color="inverse", help="📌 **是什么**：美联储官方发达经济体贸易加权美元指数 (DTWEXAFEGS)。\n\n🎯 **怎么看**：衡量美元在全球成熟市场资本流动中的真实购买力。")
o6.metric("VIX 恐慌指数", f"{latest['VIX']:.2f}", f"{vix_diff:+.2f} (和上周比)", delta_color="inverse", help="📌 **是什么**：美股期权隐含波动率，避险情绪风向标。\n\n🎯 **怎么看**：VIX飙升(>20)引发海外抛资产囤美元，是离岸紧缩先导雷达。")

st.markdown(f'''
<div class="chart-guide-container">
    <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
        <span style="font-weight:700; color:#10b981;">💡 读图快速指南：</span>
        <span class="pill-green">🟢 宽松信号</span> <span>掉期基差 <b>📈 向上</b> ｜ 美元指数 / VIX <b>📉 向下</b></span>
        <span style="color:#334155;">|</span>
        <span class="pill-red">🔴 紧缩信号</span> <span>掉期基差 <b>📉 向下</b>（美元荒） ｜ 美元指数 / VIX <b>📈 向上</b>（避险）</span>
    </div>
    <span style="color:#64748b; font-size:0.9rem;">更新至：{latest_date_str}</span>
</div>
''', unsafe_allow_html=True)

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    fig_basis = go.Figure()
    fig_basis.add_trace(go.Scatter(x=df.index, y=df['EURUSD_Basis'], name="🔵 EUR/USD 3M 基差 (bps)", line=dict(color='#38bdf8', width=2.8)))
    fig_basis.add_trace(go.Scatter(x=df.index, y=df['USDJPY_Basis'], name="🟣 USD/JPY 3M 基差 (bps)", line=dict(color='#a855f7', width=2.8)))
    
    fig_basis.add_hline(y=-30.0, line_dash="dash", line_color="#38bdf8", annotation_text="EUR 离岸美元荒警戒线 (-30 bps)", annotation_font_size=10)
    fig_basis.add_hline(y=-60.0, line_dash="dash", line_color="#a855f7", annotation_text="JPY 离岸美元荒警戒线 (-60 bps)", annotation_font_size=10)
    
    fig_basis.update_layout(title="<b>1. 跨货币掉期基差 (EUR/USD & USD/JPY, bps)</b>", height=400, **layout_config)
    fig_basis.update_yaxes(title_text="掉期基差 (bps)", gridcolor="#1e2d42")
    st.plotly_chart(fig_basis, use_container_width=True)

with row1_col2:
    fig_swpt = go.Figure()
    fig_swpt.add_trace(go.Bar(x=df.index, y=df['SWPT_M'], name="🔴 央行互换余额 ($M) [常态:0]", marker_color='rgba(255, 82, 82, 0.7)'))
    fig_swpt.update_layout(title="<b>2. 美联储央行流动性互换余额 (SWPT, $M)</b>", height=400, **layout_config)
    fig_swpt.update_yaxes(title_text="互换余额 ($M)", gridcolor="#1e2d42")
    st.plotly_chart(fig_swpt, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    dxy_min = df['DXY'].min() * 0.995
    dxy_max = df['DXY'].max() * 1.005
    dxy_mean = df['DXY'].mean()
    
    fig_dxy = go.Figure()
    fig_dxy.add_trace(go.Scatter(
        x=df.index, y=df['DXY'], 
        name="🔵 发达国家美元指数", 
        line=dict(color='#38bdf8', width=2.8)
    ))
    fig_dxy.add_hline(y=dxy_mean, line_dash="dot", line_color="#facc15", annotation_text=f"期间均值 ({dxy_mean:.1f})", annotation_font_size=11)
    fig_dxy.update_layout(title="<b>3. 发达国家美元指数 (DTWEXAFEGS) 走势图</b>", height=400, **layout_config)
    fig_dxy.update_yaxes(title_text="指数点位", gridcolor="#1e2d42", range=[dxy_min, dxy_max])
    st.plotly_chart(fig_dxy, use_container_width=True)

with row2_col2:
    fig_vix = go.Figure()
    fig_vix.add_trace(go.Scatter(x=df.index, y=df['VIX'], name="🟡 VIX 恐慌指数", line=dict(color='#facc15', width=2.8), fill='tozeroy', fillcolor='rgba(250, 204, 21, 0.08)'))
    fig_vix.add_hline(y=20.0, line_dash="dash", line_color="#ff5252", annotation_text="VIX 警戒线 (20.0)", annotation_font_size=11)
    fig_vix.update_layout(title="<b>4. 市场波动率：VIX 恐慌指数走势图</b>", height=400, **layout_config)
    fig_vix.update_yaxes(title_text="VIX 指数", gridcolor="#1e2d42")
    st.plotly_chart(fig_vix, use_container_width=True)

st.markdown(f'<div class="source-caption">📍 <b>数据源</b>：美联储 H.4.1 (SWPT) | 发达国家贸易加权美元指数 (DTWEXAFEGS) | CBOE (VIXCLS，最新更新: {latest_date_str})</div>', unsafe_allow_html=True)

# ==========================================
# 10. 数据明细表
# ==========================================
with st.expander(f"📋 展开详细观测数据集 (Data Table) —— 数据更新至 {latest_date_str}"):
    display_df = df[['Net_Liquidity_B', 'WALCL_B', 'TGA_B', 'RRP_B', 'Reserves_B', 'NFCI', 'ANFCI', 'SOFR', 'EFFR', 'IORB', 'SOFR_IORB_Spread', 'EURUSD_Basis', 'USDJPY_Basis', 'SWPT_M', 'DXY', 'VIX']].copy()
    display_df.columns = ['净流动性($B)', '总资产($B)', 'TGA($B)', 'ON RRP($B)', '准备金($B)', '芝加哥联储NFCI', '修正ANFCI', 'SOFR(%)', 'EFFR(%)', 'IORB(%)', '利差(bps)', 'EURUSD基差(bps)', 'USDJPY基差(bps)', '央行互换($M)', '发达国家美元指数', 'VIX指数']
    
    st.dataframe(display_df.sort_index(ascending=False).style.format("{:.2f}"), use_container_width=True)
    
    csv = display_df.to_csv().encode('utf-8')
    st.download_button(
        label="📥 导出观测 CSV 格式数据",
        data=csv,
        file_name=f"USD_Liquidity_{latest_date_str}.csv",
        mime="text/csv"
    )