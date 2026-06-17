import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Entrepreneurial Intention Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv")

    # Derive IntentionStatus from entrepreneurial trait scores
    # A student is considered to have entrepreneurial intention
    # if they score above 3 in at least 3 of these 4 key traits
    key_traits = ["Perseverance", "SelfConfidence", "StrongNeedToAchieve", "DesireToTakeInitiative"]
    df["IntentionStatus"] = (
        (df[key_traits] > 3).sum(axis=1) >= 3
    ).astype(int)

    return df

df = load_data()

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.title("Filters")

if "Gender" in df.columns:
    gender_filter = st.sidebar.multiselect(
        "Gender",
        options=df["Gender"].unique(),
        default=df["Gender"].unique()
    )
    df = df[df["Gender"].isin(gender_filter)]

if "EducationSector" in df.columns:
    sector_filter = st.sidebar.multiselect(
        "Education Sector",
        options=df["EducationSector"].unique(),
        default=df["EducationSector"].unique()
    )
    df = df[df["EducationSector"].isin(sector_filter)]

if "City" in df.columns:
    city_filter = st.sidebar.multiselect(
        "City",
        options=df["City"].unique(),
        default=df["City"].unique()
    )
    df = df[df["City"].isin(city_filter)]

# =====================================================
# TITLE
# =====================================================

st.title("📊 Entrepreneurial Intention Dashboard")

st.markdown(
    """
    This dashboard analyzes entrepreneurial intention among university students
    and highlights key traits associated with entrepreneurial readiness.
    """
)

# =====================================================
# KPI SECTION
# =====================================================

total_students = len(df)

students_with_intention = len(df[df["IntentionStatus"] == 1])
students_without_intention = len(df[df["IntentionStatus"] == 0])

intention_rate = (
    students_with_intention / total_students * 100
    if total_students > 0
    else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Students", total_students)
col2.metric("With Intention", students_with_intention)
col3.metric("Without Intention", students_without_intention)
col4.metric("Intention Rate", f"{intention_rate:.2f}%")

st.divider()

# =====================================================
# INTENTION DISTRIBUTION
# =====================================================

st.subheader("Entrepreneurial Intention Distribution")

intention_labels = df["IntentionStatus"].map({1: "Has Intention", 0: "No Intention"})
fig1 = px.histogram(
    df.assign(Intention=intention_labels),
    x="Intention",
    color="Intention",
    text_auto=True,
    color_discrete_map={"Has Intention": "#2ecc71", "No Intention": "#e74c3c"}
)

st.plotly_chart(fig1, use_container_width=True)

# =====================================================
# GENDER DISTRIBUTION
# =====================================================

if "Gender" in df.columns:
    st.subheader("Gender Distribution")

    gender_counts = df["Gender"].value_counts().reset_index()
    gender_counts.columns = ["Gender", "Count"]

    fig2 = px.pie(
        gender_counts,
        names="Gender",
        values="Count"
    )

    st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# EDUCATION SECTOR
# =====================================================

if "EducationSector" in df.columns:
    st.subheader("Education Sector Distribution")

    sector_counts = df["EducationSector"].value_counts().reset_index()
    sector_counts.columns = ["EducationSector", "Count"]

    fig3 = px.bar(
        sector_counts,
        x="EducationSector",
        y="Count"
    )

    st.plotly_chart(fig3, use_container_width=True)

# =====================================================
# KEY TRAITS DISTRIBUTION
# =====================================================

if "KeyTraits" in df.columns:
    st.subheader("Key Traits Distribution")

    traits_counts = df["KeyTraits"].value_counts().reset_index()
    traits_counts.columns = ["KeyTrait", "Count"]

    fig_kt = px.bar(
        traits_counts,
        x="KeyTrait",
        y="Count",
        color="KeyTrait",
        text_auto=True
    )

    st.plotly_chart(fig_kt, use_container_width=True)

# =====================================================
# TRAIT ANALYSIS
# =====================================================

trait_columns = [
    "Perseverance",
    "DesireToTakeInitiative",
    "Competitiveness",
    "SelfReliance",
    "StrongNeedToAchieve",
    "SelfConfidence",
    "GoodPhysicalHealth"
]

available_traits = [col for col in trait_columns if col in df.columns]

if len(available_traits) > 0:
    st.subheader("Average Entrepreneurial Trait Scores")

    trait_means = df[available_traits].mean().reset_index()
    trait_means.columns = ["Trait", "Average Score"]

    fig4 = px.bar(
        trait_means,
        x="Trait",
        y="Average Score"
    )

    st.plotly_chart(fig4, use_container_width=True)

# =====================================================
# INTENTION COMPARISON
# =====================================================

if len(available_traits) > 0:
    st.subheader("Trait Comparison by Entrepreneurial Intention")

    comparison = (
        df.groupby("IntentionStatus")[available_traits]
        .mean()
        .T
        .reset_index()
    )

    comparison.columns = ["Trait", "No Intention", "Has Intention"]

    comparison_long = comparison.melt(
        id_vars="Trait",
        var_name="Group",
        value_name="Average Score"
    )

    fig5 = px.bar(
        comparison_long,
        x="Trait",
        y="Average Score",
        color="Group",
        barmode="group",
        color_discrete_map={"Has Intention": "#2ecc71", "No Intention": "#e74c3c"}
    )

    st.plotly_chart(fig5, use_container_width=True)

# =====================================================
# CORRELATION HEATMAP
# =====================================================

if len(available_traits) > 0:
    st.subheader("Correlation Matrix")

    corr = df[available_traits + ["IntentionStatus"]].corr()

    fig6 = px.imshow(
        corr,
        text_auto=True,
        aspect="auto"
    )

    st.plotly_chart(fig6, use_container_width=True)

# =====================================================
# KEY INSIGHTS
# =====================================================

st.subheader("Key Insights")

st.success(f"{intention_rate:.2f}% of students demonstrate entrepreneurial intention.")

st.info(
    "Students with entrepreneurial intention generally report higher entrepreneurial trait scores."
)

st.warning(
    "Universities should focus on initiative-building and confidence-building programs."
)

# =====================================================
# DATA TABLE
# =====================================================

with st.expander("View Dataset"):
    st.dataframe(df)
