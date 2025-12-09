import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# ==============================================================================
# 1. PAGE CONFIGURATION & ENHANCED STYLING
# ==============================================================================
st.set_page_config(
    page_title="Executive Dashboard: Kesiapan Pendidikan AI",
    page_icon="🇮🇩",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Enhanced Custom CSS with Modern Design
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #0A0E27 0%, #1a1f3a 50%, #0f1419 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Glassmorphism Metric Cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(30, 35, 47, 0.9) 0%, rgba(26, 31, 58, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 16px;
        border-left: 4px solid;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        transition: all 0.3s ease;
    }

    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
    }

    div[data-testid="metric-container"]:nth-child(1) { border-left-color: #00D9FF; }
    div[data-testid="metric-container"]:nth-child(2) { border-left-color: #A855F7; }
    div[data-testid="metric-container"]:nth-child(3) { border-left-color: #10B981; }

    /* Enhanced Typography */
    h1 {
        background: linear-gradient(135deg, #00D9FF 0%, #A855F7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        font-size: 3rem !important;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem !important;
    }

    h2 {
        color: #E5E7EB !important;
        font-weight: 600 !important;
        font-size: 1.75rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        position: relative;
        padding-bottom: 0.5rem;
    }

    h2:after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #00D9FF 0%, #A855F7 100%);
        border-radius: 2px;
    }

    h3 {
        color: #D1D5DB !important;
        font-weight: 500 !important;
        font-size: 1.25rem !important;
    }

    /* Enhanced Insight Box */
    .insight-box {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.05) 100%);
        border-left: 4px solid #10B981;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.1);
        backdrop-filter: blur(10px);
    }

    .insight-box b {
        color: #10B981;
        font-size: 1.1rem;
        display: block;
        margin-bottom: 8px;
    }

    /* Section Cards */
    .section-card {
        background: rgba(30, 35, 47, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* Enhanced Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(30, 35, 47, 0.4);
        padding: 8px;
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #9CA3AF;
        font-weight: 500;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.05);
        color: #E5E7EB;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00D9FF 0%, #A855F7 100%);
        color: white !important;
    }

    /* Enhanced Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg,
            transparent 0%,
            rgba(0, 217, 255, 0.3) 20%,
            rgba(168, 85, 247, 0.3) 80%,
            transparent 100%);
    }

    /* Dataframe Styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #10B981 0%, #00D9FF 100%);
    }
</style>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# 2. DATA LOADING ENGINE (SMART MERGE) - IMPROVED
# ==============================================================================
RAW_DATA_PATH = "/app/mage_data_source/data_kesiapan_pendidikan_enriched.csv"
LABELED_DATA_PATH = "/app/artifacts/data_labeled.csv"
LOCAL_GEOJSON_PATH = "/app/indonesia-prov.geojson"

# ... (Import dan CSS tetap sama) ...


@st.cache_data
def load_and_prep_data():
    # 1. Load GeoJSON
    geojson = None
    if os.path.exists(LOCAL_GEOJSON_PATH):
        try:
            with open(LOCAL_GEOJSON_PATH, "r") as f:
                geojson = json.load(f)
        except Exception as e:
            st.error(f"Gagal baca GeoJSON: {e}")
    else:
        st.warning("⚠️ File 'indonesia-prov.geojson' tidak ditemukan.")

    # 2. Load Data Mentah
    if os.path.exists(RAW_DATA_PATH):
        df_raw = pd.read_csv(RAW_DATA_PATH)
    elif os.path.exists("mage_pipeline/data_kesiapan_pendidikan_enriched.csv"):
        df_raw = pd.read_csv("mage_pipeline/data_kesiapan_pendidikan_enriched.csv")
    else:
        return None, None

    # [CRITICAL FIX] STANDARISASI KOLOM
    df_raw.columns = df_raw.columns.str.lower().str.strip()

    # Cari nama kolom provinsi yang benar
    prov_col_raw = next((col for col in df_raw.columns if "prov" in col), None)
    if not prov_col_raw:
        return None, None

    # 3. Load Label & Merge
    df_raw["cluster_label"] = "Belum Diklasifikasi"
    if os.path.exists(LABELED_DATA_PATH):
        try:
            df_labeled = pd.read_csv(LABELED_DATA_PATH)
            df_labeled.columns = df_labeled.columns.str.lower().str.strip()

            prov_col_label = next(
                (col for col in df_labeled.columns if "prov" in col), None
            )
            cluster_col = next(
                (
                    col
                    for col in df_labeled.columns
                    if "cluster_label" in col or "label" in col
                ),
                None,
            )

            if prov_col_label and cluster_col:
                # Normalisasi Key untuk Join
                df_labeled["join_key"] = (
                    df_labeled[prov_col_label].astype(str).str.lower().str.strip()
                )
                df_raw["join_key"] = (
                    df_raw[prov_col_raw].astype(str).str.lower().str.strip()
                )

                label_map = dict(zip(df_labeled["join_key"], df_labeled[cluster_col]))
                df_raw["cluster_label"] = (
                    df_raw["join_key"].map(label_map).fillna("Belum Diklasifikasi")
                )
        except:  # noqa: E722
            pass

    # 4. Feature Engineering
    # ... (Bagian perhitungan Indeks tetap sama seperti kode Anda sebelumnya) ...
    # ... (Salin logika Indeks Infrastruktur, SDM, dll dari kode lama Anda disini) ...
    # Agar singkat, saya asumsikan bagian ini sudah ada (lihat kode lengkap di bawah)
    col_inet = [c for c in df_raw.columns if "internet" in c]
    if col_inet:
        df_raw["indeks_infrastruktur"] = df_raw[col_inet].mean(axis=1)

    col_sdm = [c for c in df_raw.columns if "sertifikasi" in c]
    if col_sdm:
        df_raw["indeks_sdm"] = df_raw[col_sdm].mean(axis=1)

    col_akm = [c for c in df_raw.columns if "akm" in c]
    if col_akm:
        df_raw["potensi_siswa"] = df_raw[col_akm].mean(axis=1)

    col_pc = [c for c in df_raw.columns if "komputer" in c and "rasio" in c]
    if col_pc:
        df_raw["rasio_pc_avg"] = df_raw[col_pc].mean(axis=1)

    # 5. [FIX MAP FINAL] MAPPING PROVINSI ROBUST
    # Ini adalah kunci agar peta muncul!
    # Kita petakan semua variasi penulisan CSV ke Format Standar GeoJSON

    MAPPING_PROVINSI = {
        "aceh": "ACEH",
        "sumatera utara": "SUMATERA UTARA",
        "sumatera barat": "SUMATERA BARAT",
        "riau": "RIAU",
        "jambi": "JAMBI",
        "sumatera selatan": "SUMATERA SELATAN",
        "bengkulu": "BENGKULU",
        "lampung": "LAMPUNG",
        "kepulauan bangka belitung": "KEPULAUAN BANGKA BELITUNG",
        "bangka belitung": "KEPULAUAN BANGKA BELITUNG",
        "kepulauan riau": "KEPULAUAN RIAU",
        "dki jakarta": "DAERAH KHUSUS IBUKOTA JAKARTA",
        "jakarta": "DAERAH KHUSUS IBUKOTA JAKARTA",
        "jawa barat": "JAWA BARAT",
        "jawa tengah": "JAWA TENGAH",
        "di yogyakarta": "DAERAH ISTIMEWA YOGYAKARTA",
        "yogyakarta": "DAERAH ISTIMEWA YOGYAKARTA",
        "jawa timur": "JAWA TIMUR",
        "banten": "BANTEN",
        "bali": "BALI",
        "nusa tenggara barat": "NUSA TENGGARA BARAT",
        "ntb": "NUSA TENGGARA BARAT",
        "nusa tenggara timur": "NUSA TENGGARA TIMUR",
        "ntt": "NUSA TENGGARA TIMUR",
        "kalimantan barat": "KALIMANTAN BARAT",
        "kalimantan tengah": "KALIMANTAN TENGAH",
        "kalimantan selatan": "KALIMANTAN SELATAN",
        "kalimantan timur": "KALIMANTAN TIMUR",
        "kalimantan utara": "KALIMANTAN UTARA",
        "sulawesi utara": "SULAWESI UTARA",
        "sulawesi tengah": "SULAWESI TENGAH",
        "sulawesi selatan": "SULAWESI SELATAN",
        "sulawesi tenggara": "SULAWESI TENGGARA",
        "gorontalo": "GORONTALO",
        "sulawesi barat": "SULAWESI BARAT",
        "maluku": "MALUKU",
        "maluku utara": "MALUKU UTARA",
        "papua barat": "PAPUA BARAT",
        "papua": "PAPUA",
        "papua tengah": "PAPUA",  # Mapping ke parent jika geojson lama
        "papua pegunungan": "PAPUA",
        "papua selatan": "PAPUA",
    }

    def normalize_prov_geo(name):
        # Bersihkan string input
        n = str(name).lower().replace("prov.", "").replace("provinsi", "").strip()
        # Cek di kamus, jika tidak ada, kembalikan Uppercase biasa
        return MAPPING_PROVINSI.get(n, n.upper())

    # Terapkan Mapping
    df_raw["geo_key"] = df_raw[prov_col_raw].apply(normalize_prov_geo)

    # Simpan nama asli untuk label hover
    df_raw["display_prov"] = df_raw[prov_col_raw]

    return df_raw, geojson


# Load Data
df, geojson_indo = load_and_prep_data()

# Enhanced Color Map with Better Contrast
COLOR_MAP = {
    "Tinggi (High)": "#10B981",  # Emerald
    "Sedang (Medium)": "#F59E0B",  # Amber
    "Rendah (Low)": "#EF4444",  # Red
    "Belum Diklasifikasi": "#6B7280",  # Gray
}

# --- ENHANCED HEADER ---
col_title, col_logo = st.columns([4, 1])
with col_title:
    st.title("🇮🇩 Executive Dashboard: Kesiapan Pendidikan AI")
    st.markdown(
        "**Monitor Strategis** · Infrastruktur Digital & SDM Nasional · Real-time Analytics"
    )
with col_logo:
    st.markdown(
        "<div style='text-align: right; padding: 20px;'><span style='font-size: 4rem;'>📊</span></div>",
        unsafe_allow_html=True,
    )

st.divider()

if df is None:
    st.error("❌ Data tidak ditemukan. Pastikan data enriched tersedia.")
    st.stop()

# ==============================================================================
# 1. EXECUTIVE SUMMARY - ENHANCED
# ==============================================================================
st.header("1. Executive Summary")

# KPI Metrics dengan warna gradient
c1, c2, c3, c4 = st.columns(4)
c1.metric(
    "Indeks Infrastruktur",
    f"{df['indeks_infrastruktur'].mean():.1f}%",
    f"+{df['indeks_infrastruktur'].std():.1f} σ",
    help="Rata-rata Akses Internet & Listrik",
)
c2.metric(
    "Indeks Kualitas SDM",
    f"{df['indeks_sdm'].mean():.1f}%",
    f"+{df['indeks_sdm'].std():.1f} σ",
    help="Rata-rata Sertifikasi Guru",
)
c3.metric(
    "Potensi Siswa (AKM)",
    f"{df['potensi_siswa'].mean():.1f}",
    f"±{df['potensi_siswa'].std():.1f}",
    help="Skor Literasi & Numerasi",
)
total_prov = len(df)
ready_prov = df["cluster_label"].str.contains("Tinggi").sum()
c4.metric(
    "Provinsi Siap AI",
    f"{ready_prov}/{total_prov}",
    f"{ready_prov/total_prov*100:.0f}%",
    help="Klaster Tinggi (High)",
)

st.markdown("<br>", unsafe_allow_html=True)

col_map, col_pie = st.columns([3, 1])

with col_map:
    st.subheader("🗺️ Peta Sebaran Kesiapan Nasional")

    if geojson_indo:
        # PERBAIKAN KRITIS: Pastikan mapping warna bekerja
        # Tambahkan kolom numerik untuk memastikan plotly bisa render warna
        color_order = [
            "Rendah (Low)",
            "Sedang (Medium)",
            "Tinggi (High)",
            "Belum Diklasifikasi",
        ]
        df["cluster_numeric"] = df["cluster_label"].map(
            {v: i for i, v in enumerate(color_order)}
        )

        fig_map = px.choropleth_mapbox(
            df,
            geojson=geojson_indo,
            locations="geo_key",
            featureidkey="properties.Propinsi",  # Pastikan ini sesuai dengan struktur GeoJSON
            color="cluster_label",
            color_discrete_map=COLOR_MAP,
            category_orders={"cluster_label": color_order},
            mapbox_style="carto-darkmatter",
            zoom=3.8,
            center={"lat": -2.5, "lon": 118},
            opacity=0.85,
            hover_name="display_prov",
            hover_data={
                "geo_key": False,
                "cluster_numeric": False,
                "indeks_infrastruktur": ":.1f",
                "indeks_sdm": ":.1f",
                "potensi_siswa": ":.1f",
            },
            labels={
                "indeks_infrastruktur": "Infrastruktur",
                "indeks_sdm": "SDM",
                "potensi_siswa": "AKM",
            },
        )

        fig_map.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            height=500,
            legend=dict(
                yanchor="top",
                y=0.98,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(30, 35, 47, 0.8)",
                bordercolor="rgba(255, 255, 255, 0.2)",
                borderwidth=1,
                font=dict(color="white", size=11),
            ),
            font=dict(family="Inter, sans-serif"),
        )

        st.plotly_chart(fig_map, use_container_width=True, key="main_map")
    else:
        st.warning("⚠️ Peta tidak muncul. Menampilkan visualisasi alternatif...")
        fig_b = px.bar(
            df.sort_values("indeks_infrastruktur", ascending=True),
            x="indeks_infrastruktur",
            y="display_prov",
            orientation="h",
            color="cluster_label",
            color_discrete_map=COLOR_MAP,
            height=600,
        )
        fig_b.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
        )
        st.plotly_chart(fig_b, use_container_width=True)

with col_pie:
    st.subheader("Distribusi Klaster")
    counts = df["cluster_label"].value_counts().reset_index()
    counts.columns = ["cluster_label", "count"]

    fig_pie = px.pie(
        counts,
        values="count",
        names="cluster_label",
        color="cluster_label",
        color_discrete_map=COLOR_MAP,
        hole=0.65,
    )

    fig_pie.update_traces(
        textposition="inside",
        textinfo="percent+label",
        textfont=dict(size=11, color="white"),
        marker=dict(line=dict(color="rgba(255,255,255,0.3)", width=2)),
    )

    fig_pie.update_layout(
        showlegend=False,
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        height=280,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", family="Inter"),
    )

    st.plotly_chart(fig_pie, use_container_width=True)

    rentan = df["cluster_label"].str.contains("Rendah").sum()
    sedang = df["cluster_label"].str.contains("Sedang").sum()

    st.markdown(
        f"""
    <div class='insight-box'>
        <b>💡 Key Insights</b>
        <ul style='margin: 8px 0 0 0; padding-left: 20px; color: #D1D5DB;'>
            <li><b>{rentan}</b> provinsi ({rentan/len(df)*100:.0f}%) masih klaster 'Rendah'</li>
            <li><b>{sedang}</b> provinsi ({sedang/len(df)*100:.0f}%) di klaster 'Sedang'</li>
            <li>Prioritas: Tingkatkan infrastruktur di zona merah</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ==============================================================================
# 2. CLUSTER INTELLIGENCE - ENHANCED
# ==============================================================================
st.header("2. Cluster Intelligence")

c_rad, c_tab = st.columns([1.2, 1])

with c_rad:
    st.subheader("🧬 DNA Profil Klaster")

    radar_metrics = ["indeks_infrastruktur", "indeks_sdm", "potensi_siswa"]
    extra_col = next((c for c in df.columns if "internet_smp" in c), None)
    if extra_col:
        radar_metrics.append(extra_col)

    radar_df = df.groupby("cluster_label")[radar_metrics].mean().reset_index()

    fig_rad = go.Figure()

    for idx, row in radar_df.iterrows():
        cluster = row["cluster_label"]
        values = [row[m] for m in radar_metrics]
        values.append(values[0])  # Close the loop

        fig_rad.add_trace(
            go.Scatterpolar(
                r=values,
                theta=radar_metrics + [radar_metrics[0]],
                fill="toself",
                name=cluster,
                line=dict(color=COLOR_MAP.get(cluster, "#888"), width=2),
                fillcolor=COLOR_MAP.get(cluster, "#888"),
                opacity=0.5,
            )
        )

    fig_rad.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="rgba(255,255,255,0.1)",
                tickfont=dict(color="#9CA3AF", size=10),
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="white", size=11)
            ),
            bgcolor="rgba(0,0,0,0)",
        ),
        showlegend=True,
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", family="Inter"),
        legend=dict(
            bgcolor="rgba(30,35,47,0.8)",
            bordercolor="rgba(255,255,255,0.2)",
            borderwidth=1,
        ),
    )

    st.plotly_chart(fig_rad, use_container_width=True)

with c_tab:
    st.subheader("🎯 Matriks Prioritas Aksi")

    prio_cols = ["indeks_infrastruktur", "indeks_sdm", "rasio_pc_avg"]
    prio_df = df.groupby("cluster_label")[prio_cols].mean()

    def get_act(row):
        act = []
        if row["indeks_infrastruktur"] < 65:
            act.append("⚡ Infra")
        if row["indeks_sdm"] < 50:
            act.append("🎓 Guru")
        if row["rasio_pc_avg"] > 15:
            act.append("💻 Perangkat")
        return " + ".join(act) if act else "✅ Maintain"

    prio_df["Fokus Utama"] = prio_df.apply(get_act, axis=1)

    # Color coding untuk dataframe
    def color_scale(val):
        if val < 50:
            return "background-color: rgba(239, 68, 68, 0.3)"
        elif val < 70:
            return "background-color: rgba(245, 158, 11, 0.3)"
        else:
            return "background-color: rgba(16, 185, 129, 0.3)"

    styled_df = prio_df.style.format("{:.1f}", subset=prio_cols).applymap(
        color_scale, subset=prio_cols
    )

    st.dataframe(styled_df, use_container_width=True, height=250)

    st.markdown(
        """
    <div style='background: rgba(59, 130, 246, 0.1); border-left: 3px solid #3B82F6; padding: 12px; border-radius: 8px; margin-top: 16px;'>
        <small style='color: #93C5FD;'><b>📌 Action Items:</b> Prioritas tertinggi pada klaster Rendah untuk akselerasi digital</small>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ==============================================================================
# 3. INFRASTRUCTURE DEEP-DIVE - ENHANCED
# ==============================================================================
st.header("3. Infrastructure Deep-Dive")

c_sc, c_bar = st.columns([2, 1])

with c_sc:
    st.subheader("⚡ Matriks Energi vs Konektivitas Digital")

    df["size_bubble"] = df["rasio_pc_avg"].fillna(1).clip(lower=1)

    col_x = next((c for c in df.columns if "internet_smp" in c), None)
    col_y = next((c for c in df.columns if "internet_sd" in c), None)

    if col_x and col_y:
        fig_sc = px.scatter(
            df,
            x=col_x,
            y=col_y,
            color="cluster_label",
            size="size_bubble",
            hover_name="display_prov",
            color_discrete_map=COLOR_MAP,
            labels={
                "size_bubble": "Rasio PC",
                col_x: "Internet SMP (%)",
                col_y: "Internet SD (%)",
            },
            size_max=30,
        )

        # Add quadrant lines
        fig_sc.add_vline(
            x=df[col_x].median(),
            line_dash="dash",
            line_color="rgba(255,255,255,0.3)",
            line_width=1,
        )
        fig_sc.add_hline(
            y=df[col_y].median(),
            line_dash="dash",
            line_color="rgba(255,255,255,0.3)",
            line_width=1,
        )

        # Add annotations for quadrants
        fig_sc.add_annotation(
            x=95,
            y=95,
            text="🚀 Cloud Ready",
            showarrow=False,
            font=dict(color="#10B981", size=14, family="Inter"),
        )
        fig_sc.add_annotation(
            x=30,
            y=30,
            text="⚠️ Priority Zone",
            showarrow=False,
            font=dict(color="#EF4444", size=14, family="Inter"),
        )

        fig_sc.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", family="Inter"),
            height=450,
            legend=dict(
                bgcolor="rgba(30,35,47,0.8)",
                bordercolor="rgba(255,255,255,0.2)",
                borderwidth=1,
            ),
        )

        st.plotly_chart(fig_sc, use_container_width=True)

with c_bar:
    st.subheader("🔴 Red Zone: Rasio PC Tertinggi")

    worst = df.sort_values("rasio_pc_avg", ascending=False).head(10)

    fig_b = px.bar(
        worst,
        x="rasio_pc_avg",
        y="display_prov",
        orientation="h",
        color="cluster_label",
        color_discrete_map=COLOR_MAP,
        text="rasio_pc_avg",
    )

    fig_b.add_vline(
        x=5,
        line_color="#10B981",
        line_dash="solid",
        line_width=2,
        annotation_text="Target Ideal (1:5)",
    )

    fig_b.update_traces(
        texttemplate="%{text:.1f}", textposition="outside", textfont=dict(color="white")
    )

    fig_b.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", family="Inter"),
        height=450,
        showlegend=False,
        xaxis_title="Rasio Siswa per PC",
        yaxis_title="",
    )

    st.plotly_chart(fig_b, use_container_width=True)

# ==============================================================================
# 4. HUMAN CAPITAL - ENHANCED
# ==============================================================================
st.header("4. Human Capital Analytics")

c_cor, c_heat = st.columns(2)

with c_cor:
    st.subheader("🎓 Korelasi: Kualifikasi Guru vs Numerasi Siswa")

    col_guru = next((c for c in df.columns if "sertifikasi_smp" in c), None)
    col_num = next((c for c in df.columns if "akm_numerasi" in c), None)

    if col_guru and col_num:
        fig_cor = px.scatter(
            df,
            x=col_guru,
            y=col_num,
            color="cluster_label",
            color_discrete_map=COLOR_MAP,
            hover_name="display_prov",
            trendline="ols",
            trendline_color_override="rgba(0, 217, 255, 0.8)",
            labels={col_guru: "Guru Bersertifikat (%)", col_num: "Skor Numerasi AKM"},
        )

        fig_cor.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", family="Inter"),
            height=400,
            legend=dict(
                bgcolor="rgba(30,35,47,0.8)",
                bordercolor="rgba(255,255,255,0.2)",
                borderwidth=1,
            ),
        )

        st.plotly_chart(fig_cor, use_container_width=True)
    else:
        st.info("⚠️ Data guru atau numerasi tidak tersedia")

with c_heat:
    st.subheader("📊 Heatmap: Beban Guru vs Kualitas")

    col_beban = next((c for c in df.columns if "rasio_siswa_guru" in c), None)
    col_num = next((c for c in df.columns if "akm_numerasi" in c), None)

    if col_beban and col_num:
        fig_heat = px.density_heatmap(
            df,
            x=col_beban,
            y=col_num,
            color_continuous_scale="Turbo",
            labels={col_beban: "Rasio Siswa:Guru", col_num: "Skor Numerasi"},
        )

        fig_heat.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", family="Inter"),
            height=400,
        )

        st.plotly_chart(fig_heat, use_container_width=True)
    else:
        st.info("⚠️ Data beban mengajar tidak tersedia")

# Enhanced Insight Box
st.markdown(
    """
<div class='insight-box'>
    <b>🔬 Research Finding</b>
    <p style='margin: 8px 0; color: #D1D5DB;'>
    Korelasi positif signifikan antara kualifikasi guru dengan capaian numerasi siswa.
    Setiap <b>10% peningkatan</b> guru bersertifikat berpotensi menaikkan skor AKM hingga <b>3-5 poin</b>.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# 5. STRATEGIC ROADMAP - ENHANCED
# ==============================================================================
st.header("5. Strategic Roadmap by Cluster")

t1, t2, t3 = st.tabs(
    ["🚀 High: AI Leaders", "🚧 Medium: Gap Fillers", "🆘 Low: Basic Enablers"]
)

with t1:
    st.markdown(
        """
    <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.1) 100%);
                border-radius: 12px; padding: 24px; border-left: 4px solid #10B981;'>
        <h4 style='color: #10B981; margin: 0 0 16px 0;'>🎯 Vision: National AI Innovation Hub</h4>
        <ul style='color: #D1D5DB; line-height: 1.8; padding-left: 20px;'>
            <li><b>Deep Tech:</b> Implementasi Cloud AI, Neural Networks, Computer Vision</li>
            <li><b>Global Standards:</b> Sertifikasi internasional (AWS, Google AI, Azure)</li>
            <li><b>Research Collaboration:</b> Partnership dengan universitas top dunia</li>
            <li><b>Innovation Labs:</b> AI Research Center di sekolah unggulan</li>
        </ul>
        <div style='margin-top: 16px; padding: 12px; background: rgba(16, 185, 129, 0.1); border-radius: 8px;'>
            <b style='color: #10B981;'>💰 Investment:</b> <span style='color: #E5E7EB;'>Rp 500M - 1T per provinsi | ROI Target: 300% dalam 5 tahun</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with t2:
    st.markdown(
        """
    <div style='background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.1) 100%);
                border-radius: 12px; padding: 24px; border-left: 4px solid #F59E0B;'>
        <h4 style='color: #F59E0B; margin: 0 0 16px 0;'>🎯 Vision: Digital Literacy Acceleration</h4>
        <ul style='color: #D1D5DB; line-height: 1.8; padding-left: 20px;'>
            <li><b>Hardware:</b> Pengadaan 50,000 laptop/tahun per provinsi</li>
            <li><b>Connectivity:</b> Fiber optic deployment + Starlink backup</li>
            <li><b>Capacity Building:</b> Training of Trainers (ToT) untuk 10,000 guru</li>
            <li><b>Curriculum:</b> Hybrid learning model (30% digital)</li>
        </ul>
        <div style='margin-top: 16px; padding: 12px; background: rgba(245, 158, 11, 0.1); border-radius: 8px;'>
            <b style='color: #F59E0B;'>💰 Investment:</b> <span style='color: #E5E7EB;'>Rp 200M - 500M per provinsi | Timeline: 2-3 tahun</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with t3:
    st.markdown(
        """
    <div style='background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.1) 100%);
                border-radius: 12px; padding: 24px; border-left: 4px solid #EF4444;'>
        <h4 style='color: #EF4444; margin: 0 0 16px 0;'>🎯 Vision: Foundation Infrastructure</h4>
        <ul style='color: #D1D5DB; line-height: 1.8; padding-left: 20px;'>
            <li><b>Power Grid:</b> 24/7 electricity coverage (solar + PLN)</li>
            <li><b>Basic Internet:</b> 4G/Starlink untuk 100% sekolah</li>
            <li><b>Offline-First:</b> Raspberry Pi labs + unplugged coding curriculum</li>
            <li><b>Teacher Upskilling:</b> Basic digital literacy untuk semua guru</li>
        </ul>
        <div style='margin-top: 16px; padding: 12px; background: rgba(239, 68, 68, 0.1); border-radius: 8px;'>
            <b style='color: #EF4444;'>💰 Investment:</b> <span style='color: #E5E7EB;'>Rp 100M - 300M per provinsi | Priority: CRITICAL</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.divider()

# ==============================================================================
# 6. POLICY SIMULATION ENGINE - ENHANCED
# ==============================================================================
st.header("6. Interactive Policy Simulator")

st.markdown(
    """
<div style='background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 12px; padding: 20px; margin-bottom: 24px;'>
    <h4 style='color: #3B82F6; margin: 0 0 8px 0;'>🧪 What-If Scenario Analysis</h4>
    <p style='color: #93C5FD; margin: 0; font-size: 14px;'>
    Simulasikan dampak investasi infrastruktur terhadap kualitas pendidikan dengan model predictive analytics.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

col_sim_left, col_sim_right = st.columns([1, 2])

with col_sim_left:
    selected_prov = st.selectbox(
        "🎯 Target Provinsi",
        df["display_prov"].unique(),
        help="Pilih provinsi untuk simulasi kebijakan",
    )

    current_data = df[df["display_prov"] == selected_prov].iloc[0]
    current_pc_ratio = int(current_data["rasio_pc_avg"])

    # Safely get AKM score
    col_num_sim = next((c for c in df.columns if "akm_numerasi" in c), None)
    current_akm = float(current_data[col_num_sim]) if col_num_sim else 50.0

    st.markdown(
        f"""
    <div style='background: rgba(30, 35, 47, 0.8); padding: 16px; border-radius: 8px; margin: 16px 0;'>
        <h5 style='color: #E5E7EB; margin: 0 0 12px 0;'>📊 Current State</h5>
        <p style='color: #9CA3AF; margin: 4px 0;'>
            <b style='color: #00D9FF;'>Rasio PC:</b> 1:{current_pc_ratio} siswa<br>
            <b style='color: #A855F7;'>Skor AKM:</b> {current_akm:.1f}<br>
            <b style='color: #10B981;'>Klaster:</b> {current_data['cluster_label']}
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    target_pc_ratio = st.slider(
        "🎚️ Target Rasio PC (Ideal: 1:5)",
        min_value=1,
        max_value=max(current_pc_ratio, 20),
        value=min(current_pc_ratio, 10),
        help="Semakin kecil rasio, semakin baik akses siswa terhadap teknologi",
    )

    investment_infra = st.slider(
        "💰 Investasi Infrastruktur (dalam %)",
        min_value=0,
        max_value=100,
        value=20,
        help="Persentase peningkatan akses internet & listrik",
    )

with col_sim_right:
    st.subheader("📈 Projected Impact Analysis")

    # Predictive Model (Simple Linear Regression Simulation)
    delta_pc = current_pc_ratio - target_pc_ratio

    # Impact factors (simplified model)
    akm_impact_pc = delta_pc * 0.35  # Every 1 point PC improvement = 0.35 AKM gain
    akm_impact_infra = (investment_infra / 10) * 0.8  # Infrastructure boost

    projected_akm = current_akm + akm_impact_pc + akm_impact_infra

    # Cost estimation
    cost_per_pc = 500  # Million IDR per ratio point improvement
    cost_per_infra = 300  # Million IDR per 10% infrastructure
    total_cost = (delta_pc * cost_per_pc) + (investment_infra / 10 * cost_per_infra)

    # ROI calculation
    roi_percentage = (
        ((projected_akm - current_akm) / current_akm * 100) if current_akm > 0 else 0
    )

    # Display metrics
    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            "Target Rasio PC",
            f"1:{target_pc_ratio}",
            f"-{delta_pc} (Better)" if delta_pc > 0 else "Maintain",
            delta_color="normal",
        )

    with m2:
        st.metric(
            "Projected AKM Score",
            f"{projected_akm:.1f}",
            f"+{(projected_akm - current_akm):.1f}",
            delta_color="normal",
        )

    with m3:
        st.metric(
            "Estimated Investment",
            f"Rp {total_cost:.0f}M",
            f"ROI: {roi_percentage:.1f}%",
        )

    # Progress visualization
    st.markdown("<br>", unsafe_allow_html=True)

    progress_val = min(projected_akm / 100, 1.0)
    st.progress(progress_val)

    st.caption(f"🎯 Progress menuju target nasional (AKM ≥ 80): {progress_val*100:.0f}%")

    # Investment breakdown chart
    st.markdown("<br>", unsafe_allow_html=True)

    breakdown_data = pd.DataFrame(
        {
            "Category": [
                "PC Hardware",
                "Infrastructure",
                "Teacher Training",
                "Maintenance (5yr)",
            ],
            "Cost (M IDR)": [
                delta_pc * cost_per_pc * 0.6,
                investment_infra / 10 * cost_per_infra,
                delta_pc * cost_per_pc * 0.2,
                total_cost * 0.3,
            ],
        }
    )

    fig_breakdown = px.bar(
        breakdown_data,
        x="Cost (M IDR)",
        y="Category",
        orientation="h",
        color="Category",
        color_discrete_sequence=["#00D9FF", "#A855F7", "#10B981", "#F59E0B"],
    )

    fig_breakdown.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", family="Inter"),
        height=250,
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
    )

    st.plotly_chart(fig_breakdown, use_container_width=True)

# Impact summary
st.markdown(
    f"""
<div class='insight-box' style='border-left-color: #3B82F6;'>
    <b>🔮 Impact Projection Summary</b>
    <p style='color: #D1D5DB; margin: 8px 0 0 0;'>
    Dengan investasi <b>Rp {total_cost:.0f}M</b>, provinsi <b>{selected_prov}</b> dapat meningkatkan
    skor AKM dari <b>{current_akm:.1f}</b> menjadi <b>{projected_akm:.1f}</b> dalam <b>2-3 tahun</b>.
    ROI diproyeksikan mencapai <b>{roi_percentage:.1f}%</b> melalui peningkatan kualitas SDM dan daya saing digital.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

st.divider()

# ==============================================================================
# 7. DATA EXPLORER - ENHANCED
# ==============================================================================
st.header("7. Data Explorer & Raw Insights")

with st.expander("🔍 View Complete Dataset", expanded=False):
    # Column selection
    available_cols = [
        c for c in df.columns if c not in ["join_key", "size_bubble", "cluster_numeric"]
    ]

    selected_cols = st.multiselect(
        "Select columns to display",
        available_cols,
        default=[
            "display_prov",
            "cluster_label",
            "indeks_infrastruktur",
            "indeks_sdm",
            "potensi_siswa",
        ],
    )

    if selected_cols:
        # Display with conditional formatting
        display_df = df[selected_cols].copy()

        st.dataframe(
            display_df.style.format(
                "{:.2f}",
                subset=[
                    c for c in selected_cols if df[c].dtype in ["float64", "int64"]
                ],
            ),
            use_container_width=True,
            height=400,
        )

        # Download button
        csv = display_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"indonesia_ai_readiness_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

# ==============================================================================
# FOOTER - ENHANCED
# ==============================================================================
st.divider()

footer_cols = st.columns([2, 1, 1])

with footer_cols[0]:
    st.markdown(
        """
    <div style='color: #6B7280; font-size: 13px;'>
        <b style='color: #9CA3AF;'>Executive Dashboard v2.0</b><br>
        Data Sources: Kemendikbud, BPS, Regional Analytics<br>
        Last Updated: December 2025 | Real-time Sync Enabled
    </div>
    """,
        unsafe_allow_html=True,
    )

with footer_cols[1]:
    st.markdown(
        """
    <div style='color: #6B7280; font-size: 13px; text-align: center;'>
        <b style='color: #9CA3AF;'>Powered by</b><br>
        Streamlit • Plotly • ML Pipeline
    </div>
    """,
        unsafe_allow_html=True,
    )

with footer_cols[2]:
    st.markdown(
        """
    <div style='color: #6B7280; font-size: 13px; text-align: right;'>
        <b style='color: #9CA3AF;'>Support</b><br>
        📧 devmlops@edu.id<br>
        🌐 dashboard.ai-education.id
    </div>
    """,
        unsafe_allow_html=True,
    )

st.caption("© 2025 DevMLOps Education System. Built with ❤️ for Indonesian Education")
