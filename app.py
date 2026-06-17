import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Entrepreneurial Intention Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# CUSTOM CSS — Navy/Teal Design
# =====================================================

st.markdown("""
<style>
/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; padding-bottom: 2rem !important; max-width: 100% !important; }

/* ── Top header bar ── */
.dash-header {
    background: #0F2A3D;
    padding: 16px 32px;
    margin: -1rem -1rem 0 -1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-radius: 0;
}
.dash-header-title {
    color: #ffffff;
    font-size: 18px;
    font-weight: 600;
    letter-spacing: 0.01em;
}
.dash-header-title span {
    color: #1D9E75;
    margin-right: 10px;
}
.dash-header-meta {
    color: #9FC4C7;
    font-size: 13px;
}

/* ── Section labels ── */
.section-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #888780;
    margin: 1.5rem 0 0.6rem 0;
    padding-bottom: 6px;
    border-bottom: 0.5px solid #e0ddd6;
    font-weight: 500;
}

/* ── KPI cards ── */
[data-testid="metric-container"] {
    background: #f4f6f8;
    border-radius: 10px;
    padding: 16px 20px !important;
    border: none;
}
[data-testid="metric-container"] > div:first-child {
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #5F5E5A !important;
}
[data-testid="stMetricValue"] {
    font-size: 28px !important;
    font-weight: 600 !important;
    color: #0F2A3D !important;
}
[data-testid="stMetricDelta"] { display: none; }

/* ── KPI accent colours (applied via st.markdown wrappers) ── */
.kpi-accent [data-testid="stMetricValue"] { color: #0F6E56 !important; }
.kpi-danger  [data-testid="stMetricValue"] { color: #993C1D !important; }
.kpi-rate    [data-testid="stMetricValue"] { color: #185FA5 !important; }

/* ── Insight banners ── */
.insight-card {
    background: #E1F5EE;
    border-left: 3px solid #1D9E75;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    font-size: 13px;
    color: #085041;
    margin-bottom: 8px;
    line-height: 1.5;
}
.insight-card.warn {
    background: #FAEEDA;
    border-left-color: #EF9F27;
    color: #633806;
}
.insight-card.info {
    background: #E6F1FB;
    border-left-color: #378ADD;
    color: #0C447C;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0F2A3D !important;
}
[data-testid="stSidebar"] * {
    color: #d0e8e8 !important;
}
[data-testid="stSidebar"] .stMultiSelect > label {
    color: #9FC4C7 !important;
    font-size: 12px !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: #1D9E75 !important;
    color: #fff !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] {
    background: #1a3a50 !important;
    border-color: #2a5570 !important;
}
.sidebar-brand {
    color: #1D9E75;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.02em;
    padding: 0.5rem 0 1rem 0;
    border-bottom: 0.5px solid #1a3a50;
    margin-bottom: 1rem;
}

/* ── Chart containers ── */
.chart-wrap {
    background: #ffffff;
    border: 0.5px solid #e5e3dc;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
}
.chart-title {
    font-size: 13px;
    font-weight: 600;
    color: #0F2A3D;
    margin-bottom: 2px;
}
.chart-sub {
    font-size: 11px;
    color: #888780;
    margin-bottom: 12px;
}

/* ── Key trait tiles ── */
.trait-grid {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 4px;
}
.trait-tile {
    flex: 1;
    min-width: 100px;
    border-radius: 10px;
    padding: 14px 10px;
    text-align: center;
}
.trait-tile .t-label { font-size: 11px; font-weight: 600; margin-bottom: 6px; }
.trait-tile .t-count { font-size: 24px; font-weight: 700; }
.trait-tile .t-pct   { font-size: 11px; margin-top: 2px; opacity: 0.75; }

.tile-teal   { background: #E1F5EE; } .tile-teal   .t-label { color: #085041; } .tile-teal   .t-count { color: #0F6E56; } .tile-teal   .t-pct { color: #5DCAA5; }
.tile-blue   { background: #E6F1FB; } .tile-blue   .t-label { color: #0C447C; } .tile-blue   .t-count { color: #185FA5; } .tile-blue   .t-pct { color: #85B7EB; }
.tile-purple { background: #EEEDFE; } .tile-purple .t-label { color: #3C3489; } .tile-purple .t-count { color: #534AB7; } .tile-purple .t-pct { color: #AFA9EC; }
.tile-amber  { background: #FAEEDA; } .tile-amber  .t-label { color: #633806; } .tile-amber  .t-count { color: #854F0B; } .tile-amber  .t-pct { color: #EF9F27; }
.tile-coral  { background: #FAECE7; } .tile-coral  .t-label { color: #712B13; } .tile-coral  .t-count { color: #993C1D; } .tile-coral  .t-pct { color: #F0997B; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv")
    key_traits = ["Perseverance", "SelfConfidence", "StrongNeedToAchieve", "DesireToTakeInitiative"]
    df["IntentionStatus"] = (
        (df[key_traits] > 3).sum(axis=1) >= 3
    ).astype(int)
    return df

df = load_data()

# =====================================================
# SIDEBAR FILTERS
# =====================================================

with st.sidebar:
    st.markdown('<div class="sidebar-brand">📊 EI Dashboard</div>', unsafe_allow_html=True)

    if "Gender" in df.columns:
        gender_filter = st.multiselect(
            "Gender",
            options=df["Gender"].unique(),
            default=df["Gender"].unique()
        )
        df = df[df["Gender"].isin(gender_filter)]

    if "EducationSector" in df.columns:
        sector_filter = st.multiselect(
            "Education Sector",
            options=df["EducationSector"].unique(),
            default=df["EducationSector"].unique()
        )
        df = df[df["EducationSector"].isin(sector_filter)]

    if "City" in df.columns:
        city_filter = st.multiselect(
            "City",
            options=df["City"].unique(),
            default=df["City"].unique()
        )
        df = df[df["City"].isin(city_filter)]

# =====================================================
# HEADER BAR
# =====================================================

total_students = len(df)
students_with_intention = len(df[df["IntentionStatus"] == 1])
students_without_intention = len(df[df["IntentionStatus"] == 0])
intention_rate = (students_with_intention / total_students * 100) if total_students > 0 else 0

st.markdown(f"""
<div class="dash-header">
    <div class="dash-header-title"><span>◈</span> Entrepreneurial Intention Dashboard</div>
    <div class="dash-header-meta">{total_students} students · FYP 2025</div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# KPI CARDS
# =====================================================

st.markdown('<div class="section-label">Overview</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Students", f"{total_students:,}")
with col2:
    st.markdown('<div class="kpi-accent">', unsafe_allow_html=True)
    st.metric("With Intention", f"{students_with_intention:,}")
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="kpi-danger">', unsafe_allow_html=True)
    st.metric("Without Intention", f"{students_without_intention:,}")
    st.markdown('</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="kpi-rate">', unsafe_allow_html=True)
    st.metric("Intention Rate", f"{intention_rate:.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# TRAIT ANALYSIS + INTENTION SPLIT
# =====================================================

st.markdown('<div class="section-label">Trait Analysis</div>', unsafe_allow_html=True)

trait_columns = [
    "Perseverance", "DesireToTakeInitiative", "Competitiveness",
    "SelfReliance", "StrongNeedToAchieve", "SelfConfidence", "GoodPhysicalHealth"
]
available_traits = [col for col in trait_columns if col in df.columns]

col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Average trait scores</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">Mean score per entrepreneurial trait (1–5 scale)</div>', unsafe_allow_html=True)

    if available_traits:
        trait_means = df[available_traits].mean().sort_values(ascending=True).reset_index()
        trait_means.columns = ["Trait", "Average Score"]

        fig_traits = px.bar(
            trait_means,
            x="Average Score",
            y="Trait",
            orientation="h",
            color="Average Score",
            color_continuous_scale=["#9FE1CB", "#1D9E75", "#085041"],
            text=trait_means["Average Score"].round(2),
        )
        fig_traits.update_traces(textposition="outside", textfont_size=11)
        fig_traits.update_layout(
            coloraxis_showscale=False,
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=0, r=30, t=10, b=10),
            height=280,
            xaxis=dict(range=[0, 5], showgrid=True, gridcolor="#f0ede6", tickfont_size=11),
            yaxis=dict(tickfont_size=12),
            font_family="sans-serif",
        )
        st.plotly_chart(fig_traits, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Intention split</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">Students with vs without entrepreneurial intention</div>', unsafe_allow_html=True)

    fig_donut = go.Figure(go.Pie(
        labels=["Has Intention", "No Intention"],
        values=[students_with_intention, students_without_intention],
        hole=0.62,
        marker_colors=["#1D9E75", "#0F2A3D"],
        textinfo="label+percent",
        textfont_size=12,
        hovertemplate="%{label}: %{value} students<extra></extra>",
    ))
    fig_donut.update_layout(
        showlegend=False,
        paper_bgcolor="white",
        margin=dict(l=10, r=10, t=10, b=10),
        height=280,
        annotations=[dict(
            text=f"<b>{intention_rate:.1f}%</b><br>intention",
            x=0.5, y=0.5, font_size=14, showarrow=False,
            font_color="#0F2A3D"
        )],
        font_family="sans-serif",
    )
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# TRAIT COMPARISON BY INTENTION
# =====================================================

if available_traits:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Trait scores by intention group</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">Comparing average scores between students with and without entrepreneurial intention</div>', unsafe_allow_html=True)

    comparison = (
        df.groupby("IntentionStatus")[available_traits]
        .mean().T.reset_index()
    )
    comparison.columns = ["Trait", "No Intention", "Has Intention"]
    comparison_long = comparison.melt(id_vars="Trait", var_name="Group", value_name="Average Score")

    fig_compare = px.bar(
        comparison_long,
        x="Trait",
        y="Average Score",
        color="Group",
        barmode="group",
        color_discrete_map={"Has Intention": "#1D9E75", "No Intention": "#0F2A3D"},
        text_auto=".2f",
    )
    fig_compare.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=0, r=0, t=10, b=10),
        height=320,
        yaxis=dict(range=[0, 5], gridcolor="#f0ede6"),
        xaxis=dict(tickangle=-20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font_family="sans-serif",
    )
    st.plotly_chart(fig_compare, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# KEY TRAITS TILES + GENDER PIE
# =====================================================

st.markdown('<div class="section-label">Demographics & Key Traits</div>', unsafe_allow_html=True)

col_kt, col_gender = st.columns([3, 2])

with col_kt:
    if "KeyTraits" in df.columns:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Key trait distribution</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-sub">Dominant entrepreneurial trait per student</div>', unsafe_allow_html=True)

        tile_styles = ["tile-teal", "tile-blue", "tile-purple", "tile-amber", "tile-coral"]
        trait_counts = df["KeyTraits"].value_counts()
        tiles_html = '<div class="trait-grid">'
        for i, (trait, count) in enumerate(trait_counts.items()):
            pct = count / len(df) * 100
            style = tile_styles[i % len(tile_styles)]
            tiles_html += f"""
            <div class="trait-tile {style}">
                <div class="t-label">{trait.capitalize()}</div>
                <div class="t-count">{count}</div>
                <div class="t-pct">{pct:.1f}%</div>
            </div>"""
        tiles_html += '</div>'
        st.markdown(tiles_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col_gender:
    if "Gender" in df.columns:
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Gender distribution</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-sub">Split of respondents by gender</div>', unsafe_allow_html=True)

        gender_counts = df["Gender"].value_counts()
        fig_gender = go.Figure(go.Pie(
            labels=gender_counts.index.tolist(),
            values=gender_counts.values.tolist(),
            hole=0.5,
            marker_colors=["#1D9E75", "#0F2A3D", "#5DCAA5", "#9FE1CB"],
            textinfo="label+percent",
            textfont_size=12,
        ))
        fig_gender.update_layout(
            showlegend=False,
            paper_bgcolor="white",
            margin=dict(l=10, r=10, t=10, b=10),
            height=220,
            font_family="sans-serif",
        )
        st.plotly_chart(fig_gender, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# EDUCATION SECTOR
# =====================================================

if "EducationSector" in df.columns:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Students by education sector</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">Number of respondents per academic discipline</div>', unsafe_allow_html=True)

    sector_counts = df["EducationSector"].value_counts().reset_index()
    sector_counts.columns = ["EducationSector", "Count"]

    fig_sector = px.bar(
        sector_counts,
        x="EducationSector",
        y="Count",
        color="Count",
        color_continuous_scale=["#9FE1CB", "#1D9E75", "#085041"],
        text="Count",
    )
    fig_sector.update_traces(textposition="outside")
    fig_sector.update_layout(
        coloraxis_showscale=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=0, r=0, t=10, b=10),
        height=280,
        xaxis=dict(tickangle=-20),
        yaxis=dict(gridcolor="#f0ede6"),
        font_family="sans-serif",
    )
    st.plotly_chart(fig_sector, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# CORRELATION HEATMAP
# =====================================================

if available_traits:
    st.markdown('<div class="section-label">Correlation Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Correlation matrix</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-sub">Relationship between entrepreneurial traits and intention</div>', unsafe_allow_html=True)

    corr = df[available_traits + ["IntentionStatus"]].corr().round(2)

    fig_corr = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale=["#FAECE7", "#ffffff", "#E1F5EE"],
        zmin=-1, zmax=1,
    )
    fig_corr.update_layout(
        paper_bgcolor="white",
        margin=dict(l=0, r=0, t=10, b=10),
        height=380,
        font_family="sans-serif",
        coloraxis_colorbar=dict(tickfont_size=10),
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# KEY INSIGHTS
# =====================================================

st.markdown('<div class="section-label">Key Insights</div>', unsafe_allow_html=True)

col_i1, col_i2, col_i3 = st.columns(3)

with col_i1:
    st.markdown(f"""
    <div class="insight-card">
        📈 <strong>{intention_rate:.1f}%</strong> of students demonstrate entrepreneurial intention
        based on their trait scores.
    </div>""", unsafe_allow_html=True)

with col_i2:
    st.markdown("""
    <div class="insight-card info">
        🔍 Students <strong>with intention</strong> consistently score higher across
        all 7 entrepreneurial traits.
    </div>""", unsafe_allow_html=True)

with col_i3:
    st.markdown("""
    <div class="insight-card warn">
        🎓 Universities should prioritize <strong>initiative-building</strong> and
        <strong>confidence-building</strong> programs.
    </div>""", unsafe_allow_html=True)

# =====================================================
# DATA TABLE
# =====================================================

st.markdown('<div class="section-label">Dataset</div>', unsafe_allow_html=True)
with st.expander("View full dataset"):
    st.dataframe(df, use_container_width=True)
