import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# 1. PREMIUM PAGE CONFIGURATION & INTERFACE THEME
# =====================================================
st.set_page_config(
    page_title="LPG 3KG Distribution & Supply Chain Analytics",
    layout="wide"
)

# Injeksi CSS Kustom Tingkat Tinggi: Animasi, Neumorphism Grid, & Gaya Canvas Power BI
st.markdown("""
    <style>
    /* Animasi Keyframes untuk Efek Fade-In Saat Halaman Dimuat */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    html, body, [class*="css"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #F8FAFC;
    }
    
    /* Mengatur Gaya Navigasi Komponen Tab Ritel */
    .stTabs [data-baseweb="tab"] {
        font-size: 15px;
        font-weight: 600;
        color: #64748B;
        padding: 14px 28px;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #0052CC;
    }
    .stTabs [aria-selected="true"] {
        color: #0052CC !important;
        border-bottom: 3px solid #0052CC !important;
    }
    
    /* Struktur Kotak Grid KPI Komersial */
    .metric-card {
        background-color: #FFFFFF;
        padding: 22px 18px;
        border-radius: 6px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.03);
        margin-bottom: 20px;
        animation: fadeIn 0.6s ease-out;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
        border-color: #CBD5E1;
    }
    .metric-title {
        font-size: 11px;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #0F172A;
    }
    
    /* Pembungkus Kanvas Grafik Pro (Chart Wrapper Card) */
    .chart-wrapper {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 6px;
        border: 1px solid #E2E8F0;
        margin-bottom: 25px;
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Customisasi Tampilan Tabel Dataframe */
    div.stDataFrame {
        border: 1px solid #E2E8F0;
        border-radius: 6px;
    }
    </style>
    """, unsafe_allow_html=True)

# Kode Spektrum Warna Tunggal Selaras (Corporate Navy & Soft Blue)
HEX_DARK_NAVY = "#0A2540"
HEX_ROYAL_BLUE = "#0052CC"
HEX_CYAN_BLUE = "#2085EC"
HEX_MUTED_SLATE = "#475569"
HEX_BORDER_GRAY = "#94A3B8"
PALETTE_GAS_COMPREHENSIVE = ["#0A2540", "#0052CC", "#2085EC", "#38BDF8", "#64748B", "#CBD5E1"]

# =====================================================
# 2. DATA PIPELINE (CLEANING, PARSING, & CACHING)
# =====================================================
@st.cache_data
def load_data():
    df = pd.read_excel("Penjualan tabung gas.xlsx", sheet_name="Transaksi")
    df["Tanggal"] = pd.to_datetime(df["Tanggal"])

    numeric_cols = ["Gas Keluar", "Omzet", "Modal", "Laba", "Sisa Tabung"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

df = load_data()

# Komputasi Algoritma Penyamaran Identitas Pelanggan (Anonymization Module)
unique_buyers = df["Pembeli"].dropna().unique()
buyer_mapping = {buyer: f"Client ID-{i+1:02d}" for i, buyer in enumerate(unique_buyers)}
df["Pembeli_Anonim"] = df["Pembeli"].map(buyer_mapping)

# =====================================================
# 3. INTERACTIVE FILTER INTERFACE (SIDEBAR CONTROL)
# =====================================================
st.sidebar.markdown("### Operational Controls")

min_date = df["Tanggal"].min()
max_date = df["Tanggal"].max()

date_range = st.sidebar.date_input("Rentang Monitoring", [min_date, max_date])
buyer_list = ["Semua Klien"] + sorted(df["Pembeli_Anonim"].dropna().unique())
selected_buyer = st.sidebar.selectbox("Identitas Pembeli (Teranonim)", buyer_list)

# Eksekusi Filter Logika Array
filtered_df = df.copy()

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["Tanggal"] >= pd.to_datetime(start_date)) &
        (filtered_df["Tanggal"] <= pd.to_datetime(end_date))
    ]

if selected_buyer != "Semua Klien":
    filtered_df = filtered_df[filtered_df["Pembeli_Anonim"] == selected_buyer]

# =====================================================
# 4. MATRIKS AGREGASI FINANSIAL & LOGISTIK GLOBAL
# =====================================================
total_omzet = filtered_df["Omzet"].sum()
total_modal = filtered_df["Modal"].sum()
total_laba = filtered_df["Laba"].sum()
total_tabung = filtered_df["Gas Keluar"].sum()
total_transaksi = len(filtered_df)

total_piutang = filtered_df[filtered_df["Status"] != "Lunas"]["Omzet"].sum() if "Status" in filtered_df.columns else 0
margin = (total_laba / total_omzet) * 100 if total_omzet > 0 else 0
sisa_tabung = filtered_df["Sisa Tabung"].dropna().iloc[-1] if "Sisa Tabung" in filtered_df.columns and not filtered_df["Sisa Tabung"].dropna().empty else 0

# Aggregation Klien Teratas Guna Kebutuhan Grafik & Algoritma
top_buyer_volume = filtered_df.groupby("Pembeli_Anonim", as_index=False)["Gas Keluar"].sum().sort_values(by="Gas Keluar", ascending=False).head(5)
top_buyer_profit = filtered_df.groupby("Pembeli_Anonim", as_index=False)["Laba"].sum().sort_values(by="Laba", ascending=False).head(5)

top_client_name = top_buyer_volume.iloc[0]["Pembeli_Anonim"] if not top_buyer_volume.empty else "N/A"
top_client_qty = top_buyer_volume.iloc[0]["Gas Keluar"] if not top_buyer_volume.empty else 0

# =====================================================
# 5. MAIN HEADER APPLICATION CANVAS
# =====================================================
st.title("LPG 3KG Distribution & Supply Chain Analytics")
st.markdown("Arsitektur manajemen Business Intelligence untuk memantau ritme perputaran logistik tabung gas, audit piutang berjalan, dan kapasitas pergudangan.")
st.markdown("---")

# Mengatur Struktur Multi-Tab Modular (Termasuk Predictive Analytics Baru)
tab1, tab2, tab3, tab4 = st.tabs([
    "Commercial Trends & Revenue", 
    "Client Distribution Analytics", 
    "Inventory Control & Receivables",
    "Predictive Logistics & Planning"
])

# -----------------------------------------------------
# TAB 1: COMMERCIAL TRENDS & REVENUE
# -----------------------------------------------------
with tab1:
    # Komponen Grid Neumorphism KPI Cards Row 1
    kpi_cols = st.columns(6)
    
    with kpi_cols[0]:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Gross Revenue</div><div class="metric-value">Rp {total_omzet:,.0f}</div></div>', unsafe_allow_html=True)
    with kpi_cols[1]:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Net Profit</div><div class="metric-value">Rp {total_laba:,.0f}</div></div>', unsafe_allow_html=True)
    with kpi_cols[2]:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Volume Distribusi</div><div class="metric-value">{total_tabung:,.0f} Pcs</div></div>', unsafe_allow_html=True)
    with kpi_cols[3]:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Total Ledger</div><div class="metric-value">{total_transaksi:,}</div></div>', unsafe_allow_html=True)
    with kpi_cols[4]:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Outstanding Debt</div><div class="metric-value">Rp {total_piutang:,.0f}</div></div>', unsafe_allow_html=True)
    with kpi_cols[5]:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Warehouse Stock</div><div class="metric-value">{sisa_tabung:,.0f} Pcs</div></div>', unsafe_allow_html=True)

    # Indikator Keamanan Kapasitas Gudang (Stock Alert Banner)
    if sisa_tabung <= 20:
        st.error(f"**STOCK CRITICAL WARNING:** Sisa persediaan di gudang hanya tersisa {sisa_tabung:.0f} unit tabung. Segera ajukan Purchase Order (PO) ke agen utama.")
    elif sisa_tabung <= 50:
        st.warning(f"**STOCK BUFFER NOTICE:** Persediaan menipis pada level {sisa_tabung:.0f} unit tabung. Lakukan pemantauan ketat pada laju keluar harian.")
    else:
        st.success(f"**STOCK SECURITY SAFE:** Persediaan gudang terpantau prima pada posisi {sisa_tabung:.0f} unit tabung. Operasional aman.")

    st.markdown("<br>", unsafe_allow_html=True)

    # PERBAIKAN UTAMA GRAFIK 1: SINGLE-AXIS GROUPED BAR CHART (OMZET VS LABA)
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown("#### Analisis Komparasi Akurasi Batang Sumbu Tunggal: Omzet vs Laba Bersih Harian")
    
    financial_trend = filtered_df.groupby("Tanggal", as_index=False)[["Omzet", "Laba"]].sum().sort_values("Tanggal")
    
    # Membangun grafik batang berdampingan (Grouped Bar) dalam satu skala Y agar gap margin terlihat jelas
    fig_grouped_financial = go.Figure()
    
    fig_grouped_financial.add_trace(go.Bar(
        x=financial_trend["Tanggal"],
        y=financial_trend["Omzet"],
        name="Gross Omzet",
        marker_color=HEX_CYAN_BLUE,
        opacity=0.9
    ))
    
    fig_grouped_financial.add_trace(go.Bar(
        x=financial_trend["Tanggal"],
        y=financial_trend["Laba"],
        name="Net Laba Bersih",
        marker_color=HEX_DARK_NAVY,
        opacity=1.0
    ))
    
    fig_grouped_financial.update_layout(
        barmode='group', # Membuat posisi batang berdampingan kiri-kanan
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=20, t=20, b=40),
        height=380,
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", title="Nilas Finansial (Rp)"), # Hanya satu sumbu Y
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_grouped_financial, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # GRAFIK 2: INTERACTIVE INDIGO SMOOTH AREA CHART (VARIASI BARU)
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown("#### Tren Fluktuasi Kebutuhan Alokasi Kas Arus Modal Kerja")
    capital_trend = filtered_df.groupby("Tanggal", as_index=False)["Modal"].sum().sort_values("Tanggal")
    
    fig_capital = go.Figure()
    fig_capital.add_trace(go.Scatter(
        x=capital_trend["Tanggal"], y=capital_trend["Modal"],
        mode='lines',
        line=dict(color="#6366F1", width=2.5, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(99, 102, 241, 0.08)'
    ))
    fig_capital.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=40, r=20, t=10, b=40), height=260,
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9"), yaxis=dict(showgrid=True, gridcolor="#F1F5F9")
    )
    st.plotly_chart(fig_capital, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------
# TAB 2: CLIENT DISTRIBUTION ANALYTICS
# -----------------------------------------------------
with tab2:
    st.markdown("### Automated Client Segmentation Insights")
    insight_col1, insight_col2 = st.columns(2)
    
    with insight_col1:
        st.markdown(f"""
        <div style="background-color: #F0FDF4; padding: 20px; border-radius: 6px; border-left: 5px solid #16A34A; height: 100%; border-top: 1px solid #E2E8F0; border-right: 1px solid #E2E8F0; border-bottom: 1px solid #E2E8F0;">
            <h4 style="color: #16A34A; margin-top:0; font-size:14.5px; font-weight:700;">Kluster Kontributor Alokasi Volume Utama</h4>
            <p style="font-size:13.5px; line-height:1.5; color:#1F2937; margin-bottom:8px;">Entitas pelanggan dengan label <b>{top_client_name}</b> terdeteksi sebagai jangkar serapan pasokan terbesar pada kluster ini dengan total penyerapan mencapai <b>{top_client_qty:,.0f} Pcs</b> tabung gas.</p>
            <ul style="font-size:13px; color:#374151; padding-left:18px; margin:0;">
                <li><b>Rekomendasi Operasional:</b> Kunci entitas ini ke dalam kontrak distribusi prioritas tetap guna menjamin stabilitas volume kuota bulanan.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with insight_col2:
        st.markdown(f"""
        <div style="background-color: #F8FAFC; padding: 20px; border-radius: 6px; border-left: 5px solid #475569; height: 100%; border-top: 1px solid #E2E8F0; border-right: 1px solid #E2E8F0; border-bottom: 1px solid #E2E8F0;">
            <h4 style="color: #475569; margin-top:0; font-size:14.5px; font-weight:700;">Siklus Efisiensi Logistik Mingguan</h4>
            <p style="font-size:13.5px; line-height:1.5; color:#1F2937; margin-bottom:8px;">Berdasarkan pola rekam jejak mingguan harian, pergerakan armada pengiriman gas terbukti mengalami puncak kepadatan rute distribusi pada hari-hari tertentu.</p>
            <ul style="font-size:13px; color:#374151; padding-left:18px; margin:0;">
                <li><b>Rekomendasi Operasional:</b> Lakukan penjadwalan perawatan berkala kendaraan operasional (*delivery fleet maintenance*) di hari yang memiliki volume transaksi terendah.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # VARIETAS VIEW GRAFIK (HORIZONTAL BAR & FUNNEL)
    col_client_l, col_client_r = st.columns(2)
    
    with col_client_l:
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        st.markdown("#### Top 5 Klien Berdasarkan Kapasitas Volume Serapan (Horizontal View)")
        fig_buyer_v = px.bar(
            top_buyer_volume, x="Gas Keluar", y="Pembeli_Anonim", text_auto=True,
            orientation='h', color_discrete_sequence=[HEX_CYAN_BLUE]
        )
        fig_buyer_v.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=40, r=20, t=10, b=40), height=320,
            xaxis=dict(title="Tabung Keluar (Pcs)"), yaxis=dict(title=None, categoryorder='total ascending')
        )
        st.plotly_chart(fig_buyer_v, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_client_r:
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        st.markdown("#### Top 5 Klien Berdasarkan Kontribusi Profit Bersih (Funnel Hierarchy)")
        fig_buyer_f = px.funnel(
            top_buyer_profit, x="Laba", y="Pembeli_Anonim",
            color_discrete_sequence=[HEX_ROYAL_BLUE]
        )
        fig_buyer_f.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=40, r=20, t=10, b=40), height=320,
            yaxis=dict(title=None)
        )
        st.plotly_chart(fig_buyer_f, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # GRAFIK 3: SIKLUS HARI PENJUALAN
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown("#### Matriks Konsolidasi Volume Perputaran Dagang Berdasarkan Siklus Hari")
    filtered_df["Hari"] = filtered_df["Tanggal"].dt.day_name()
    hari_sales = filtered_df.groupby("Hari", as_index=False)["Omzet"].sum()
    
    urutan_hari = {
        "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
        "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
    }
    hari_sales["Hari"] = hari_sales["Hari"].map(urutan_hari)
    hari_sales["Hari"] = pd.Categorical(
        hari_sales["Hari"], 
        categories=["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], ordered=True
    )
    hari_sales = hari_sales.sort_values("Hari")

    fig_hari = px.bar(
        hari_sales, x="Hari", y="Omzet", text_auto=".2s",
        color_discrete_sequence=[HEX_DARK_NAVY]
    )
    fig_hari.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=40, r=20, t=10, b=40), height=320,
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", title="Total Pemasukan (Rp)"), xaxis=dict(title=None)
    )
    st.plotly_chart(fig_hari, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------
# TAB 3: INVENTORY CONTROL & RECEIVABLES
# -----------------------------------------------------
with tab3:
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown("#### Rekam Jejak Kapasitas Laju Distribusi Tabung Harian (Warehouse Output Tracking)")
    qty_trend = filtered_df.groupby("Tanggal", as_index=False)["Gas Keluar"].sum()
    
    fig_qty = px.bar(
        qty_trend, x="Tanggal", y="Gas Keluar", text_auto=True,
        color_discrete_sequence=[HEX_MUTED_SLATE]
    )
    fig_qty.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=40, r=20, t=10, b=40), height=280,
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", title="Kuantitas Keluar (Pcs)"), xaxis=dict(title="Siklus Kalender")
    )
    st.plotly_chart(fig_qty, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # DONUT CHART STATUS PEMBAYARAN KLIEN
    if "Status" in filtered_df.columns:
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        st.markdown("#### Proporsi Rasio Status Likuiditas Pembayaran Transaksi (Donut View)")
        payment_status = filtered_df.groupby("Status", as_index=False)["Omzet"].sum()
        
        fig_payment = px.pie(
            payment_status, names="Status", values="Omzet", hole=0.5,
            color_discrete_sequence=PALETTE_GAS_COMPREHENSIVE
        )
        fig_payment.update_layout(margin=dict(t=30, b=30, l=10, r=10), height=340)
        st.plotly_chart(fig_payment, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("#### Buku Besar Pemantauan Rasio Piutang Macet Per Klien (Outstanding Accounts Receivable)")
        hutang = filtered_df[filtered_df["Status"] != "Lunas"]
        
        if not hutang.empty:
            hutang_customer = hutang.groupby("Pembeli_Anonim", as_index=False).agg({"Omzet": "sum", "Gas Keluar": "sum"}).sort_values(by="Omzet", ascending=False)
            hutang_customer.columns = ["Kode Identitas Klien", "Total Nominal Piutang (Rp)", "Volume Tabung Tertahan (Pcs)"]
            st.dataframe(hutang_customer, use_container_width=True, hide_index=True)
        else:
            st.info("Seluruh catatan pembukuan pada jangka waktu filter terpantau bersih dari piutang tertahan (100% Liquidity Safe).")

    st.markdown("---")
    st.markdown("#### Konsolidasi Rekam Jejak Detail Riwayat Transaksi (Raw Data Audit Trail)")
    display_df = filtered_df.drop(columns=["Pembeli", "Hari", "Barang_Clean"], errors="ignore")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Export Audited Dataset Pack (CSV)",
        data=csv,
        file_name="dashboard_lpg_audited_export.csv",
        mime="text/csv"
    )

# -----------------------------------------------------
# TAB 4: PREDICTIVE LOGISTICS & PLANNING 
# -----------------------------------------------------
with tab4:
    st.markdown("### Advanced Predictive Logistics & Safety Stock Forecast")
    st.markdown("Seksi analitik komputasi tingkat lanjut menggunakan operasi matriks **Linear Regression via NumPy** untuk meramal titik aman stok gudang.")
    st.markdown("---")

    daily_inventory = filtered_df.groupby("Tanggal", as_index=False).agg({"Gas Keluar": "sum", "Omzet": "sum"})
    
    if len(daily_inventory) > 2:
        daily_inventory = daily_inventory.sort_values("Tanggal").reset_index(drop=True)
        daily_inventory["X_Indeks"] = daily_inventory.index
        
        X_matrix = daily_inventory["X_Indeks"].values
        Y_volume = daily_inventory["Gas Keluar"].values
        
        slope_v, intercept_v = np.polyfit(X_matrix, Y_volume, 1)
        daily_inventory["Garis_Tren_Logistik"] = slope_v * X_matrix + intercept_v
        
        future_range = 7
        last_x_indeks = X_matrix[-1]
        array_future_x = np.array([last_x_indeks + i for i in range(1, future_range + 1)])
        
        last_calendar_date = daily_inventory["Tanggal"].max()
        array_future_dates = pd.date_range(start=last_calendar_date + pd.Timedelta(days=1), periods=future_range)
        
        prediction_volume_future = slope_v * array_future_x + intercept_v
        prediction_volume_future = np.clip(prediction_volume_future, a_min=0, a_max=None)
        
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        st.markdown("#### Analisis Linear Regression Linimasa Volume Distribusi")
        
        fig_predictive_line = go.Figure()
        fig_predictive_line.add_trace(go.Scatter(x=daily_inventory["Tanggal"], y=Y_volume, mode='markers', name='Actual Output (Pcs)', marker=dict(color=HEX_DARK_NAVY, size=6)))
        fig_predictive_line.add_trace(go.Scatter(x=daily_inventory["Tanggal"], y=daily_inventory["Garis_Tren_Logistik"], mode='lines', name='Regression Line Trend', line=dict(color=HEX_ROYAL_BLUE, width=3, dash='dash')))
        
        fig_predictive_line.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=40, r=20, t=10, b=40), height=320,
            xaxis=dict(showgrid=True, gridcolor="#F1F5F9"), yaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_predictive_line, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("#### Estimasi Kebutuhan Alokasi Tabung Gas - 7 Hari Kedepan")
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        df_future_forecast = pd.DataFrame({"Tanggal Masa Depan": array_future_dates, "Proyeksi Kebutuhan Gas (Pcs)": prediction_volume_future})
        
        fig_forecast_bar = px.bar(df_future_forecast, x="Tanggal Masa Depan", y="Proyeksi Kebutuhan Gas (Pcs)", text_auto=".1f", color_discrete_sequence=[HEX_CYAN_BLUE])
        fig_forecast_bar.update_layout(plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=40, r=20, t=10, b=40), height=280, yaxis=dict(showgrid=True, gridcolor="#F1F5F9"))
        st.plotly_chart(fig_forecast_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### What-If Analysis: Manajemen Buffer Stock & Safety Stock Simulator")
        st.markdown("Geser kontrol parameter di bawah untuk mensimulasikan penambahan kuota cadangan pengaman (Safety Stock Ratio) guna mengantisipasi keterlambatan pasokan pasokan agen.")
        
        st.markdown('<div class="chart-card" style="background-color:#FFFFFF; padding:20px; border-radius:6px; border:1px solid #E2E8F0;">', unsafe_allow_html=True)
        average_daily_output = Y_volume.mean() if len(Y_volume) > 0 else 0
        
        safety_ratio_slider = st.slider("Tentukan Batas Cadangan Pengaman (Hari Konsumsi)", min_value=1, max_value=10, value=3, step=1)
        
        calculated_safety_stock = average_daily_output * safety_ratio_slider
        optimal_restock_point = calculated_safety_stock + average_daily_output
        
        sim_col_g1, sim_col_g2 = st.columns(2)
        with sim_col_g1:
            st.metric(label="Safety Stock Required", value=f"{calculated_safety_stock:.1f} Pcs Tabung", delta=f"Proteksi {safety_ratio_slider} Hari Operasional")
        with sim_col_g2:
            st.metric(label="Re-Order Point (ROP) Threshold", value=f"Sisa {optimal_restock_point:.0f} Tabung Di Gudang")
            
        st.markdown(f"""
        <p style="font-size:13.5px; color:#475569; margin-top:15px; line-height:1.5;">
            💡 <b>Rekomendasi Kebijakan Logistik:</b> Berdasarkan rata-rata laju pengeluaran historis sebesar <b>{average_daily_output:.1f} unit tabung per hari</b>, 
            apabila Anda menetapkan faktor toleransi risiko pengaman selama <b>{safety_ratio_slider} hari kalender</b>, maka gudang Anda wajib mempertahankan **Safety Stock** minimal di level <b>{calculated_safety_stock:.1f} Pcs</b>. 
            Sistem menetapkan perintah isi ulang (Re-Order Point) wajib otomatis diterbitkan ke agen ketika jumlah fisik sisa tabung di gudang menyentuh angka **{optimal_restock_point:.0f} Pcs**.
        </p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.warning("Basis baris data harian terlalu tipis untuk merumuskan kalkulasi matriks Regresi Statistik. Silakan perluas rentang tanggal analisis Anda pada panel filter.")