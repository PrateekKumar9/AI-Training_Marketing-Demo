import streamlit as st
import pandas as pd
import plotly.express as px
from data.generate_data import generate_marketing_data

st.set_page_config(
    page_title="Agentic Campaign Optimization Engine",
    page_icon="🚀",
    layout="wide",
)

@st.cache_data(show_spinner=False)
def load_data():
    """Load or generate the marketing dataset."""
    df = generate_marketing_data(n_rows=500, export_excel=True)
    return df

# Load data once for the app
marketing_df = load_data()

st.title("Agentic Campaign Optimization Engine")
st.write(
    "Welcome to the marketing workshop demo. This app shows how an autonomous agent can analyze campaign performance, identify underperformers, rewrite ad copy, and reallocate budgets."
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Campaign Dashboard",
        "Anomaly Detection",
        "Agentic Creative Optimization",
        "Budget Reallocation Engine",
    ],
)

@st.cache_data
def aggregate_platform_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate spend and performance metrics by platform."""
    platform_summary = df.groupby("Platform").agg(
        {
            "Spend ($)": "sum",
            "Conversions": "sum",
            "CPA ($)": "mean",
            "CTR": "mean",
            "ROAS": "mean",
        }
    )
    platform_summary = platform_summary.reset_index()
    platform_summary["CPA ($)"] = platform_summary["CPA ($)"].round(2)
    platform_summary["CTR"] = (platform_summary["CTR"] * 100).round(2)
    return platform_summary

@st.cache_data
def aggregate_segment_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate spend and performance metrics by audience segment."""
    segment_summary = df.groupby("Audience Segment").agg(
        {
            "Spend ($)": "sum",
            "Impressions": "sum",
            "Clicks": "sum",
            "Conversions": "sum",
            "CPA ($)": "mean",
            "CTR": "mean",
            "ROAS": "mean",
        }
    )
    segment_summary = segment_summary.reset_index()
    segment_summary["CPA ($)"] = segment_summary["CPA ($)"].round(2)
    segment_summary["CTR"] = (segment_summary["CTR"] * 100).round(2)
    segment_summary["ROAS"] = segment_summary["ROAS"].round(2)
    return segment_summary

@st.cache_data
def identify_underperformers(segment_df: pd.DataFrame) -> pd.DataFrame:
    """Identify segments with high CPA or low CTR."""
    underperformers = segment_df[
        (segment_df["CPA ($)"] > 50) | (segment_df["CTR"] < 0.5)
    ].sort_values(by=["CPA ($)", "CTR"], ascending=[False, True])
    return underperformers

@st.cache_data
def recommend_budget_allocation(df: pd.DataFrame, underperformer_df: pd.DataFrame):
    """Create current and recommended budget allocations."""
    segment_df = aggregate_segment_metrics(df)
    top_segments = segment_df.sort_values(by=["ROAS", "CTR"], ascending=[False, False]).head(3).copy()
    top_segments["Recommended Budget ($)"] = top_segments["Spend ($)"].copy()

    total_cut = underperformer_df["Spend ($)"].sum() * 0.2
    if total_cut <= 0:
        total_cut = 0

    allocation_share = total_cut / len(top_segments)
    top_segments["Recommended Budget ($)"] += allocation_share

    current_allocation = segment_df[["Audience Segment", "Spend ($)", "Conversions", "CPA ($)", "CTR", "ROAS"]].copy()
    recommended_allocation = current_allocation.copy()
    recommended_allocation = recommended_allocation.merge(
        top_segments[["Audience Segment", "Recommended Budget ($)"]],
        on="Audience Segment",
        how="left",
    )
    recommended_allocation["Recommended Budget ($)"] = recommended_allocation[
        "Recommended Budget ($)"
    ].fillna(recommended_allocation["Spend ($)"])

    recommended_allocation["Recommended Budget ($)"] = recommended_allocation[
        "Recommended Budget ($)"].round(2)
    
    return current_allocation, recommended_allocation, total_cut, top_segments

@st.cache_data
def simulate_agent_copy(segment: str) -> tuple[str, list[dict[str, str]]]:
    """Simulate an AI agent response for creative optimization."""
    analysis = (
        f"The '{segment}' audience is underperforming because the current creative is too generic for their preferences. "
        "Low CTR and high CPA suggest the message is not resonating with the segment's values, timing, or emotional triggers. "
        "We need sharper targeting, stronger social proof, and a clearer benefit statement tailored to this audience."
    )

    variants = [
        {
            "Headline": f"{segment} Deserves Better Performance",
            "Primary Text": (
                f"Take control of your next campaign with a message built for {segment}. Highlight urgency, trust, and a clear path to results so this audience responds instantly."
            ),
        },
        {
            "Headline": "Turn Interest into Action with Precision Targeting",
            "Primary Text": (
                f"Show {segment} exactly how your product fits their lifestyle. Use real benefits, specific outcomes, and a confident ask to improve engagement and lower costs."
            ),
        },
        {
            "Headline": "Stop Wasting Spend on Generic Messaging",
            "Primary Text": (
                f"Deliver a sharper value proposition to {segment} by focusing on top pain points, fast results, and a simple next step that feels personal and relevant."
            ),
        },
    ]
    return analysis, variants

platform_metrics = aggregate_platform_metrics(marketing_df)
segment_metrics = aggregate_segment_metrics(marketing_df)
underperformer_segments = identify_underperformers(segment_metrics)

if page == "Campaign Dashboard":
    st.header("Campaign Dashboard")
    st.markdown(
        "This page visualizes the campaign data the agent is monitoring. Use it to explore spend, conversions, and platform performance."
    )

    with st.expander("View summary metrics"):
        platform_cols = st.columns(3)
        for idx, row in platform_metrics.iterrows():
            platform_cols[idx].metric(
                label=f"{row['Platform']} CPA",
                value=f"${row['CPA ($)']}",
                delta=f"{row['CTR']}% CTR",
            )

    spend_vs_conv = px.scatter(
        marketing_df,
        x="Spend ($)",
        y="Conversions",
        color="Platform",
        size="Impressions",
        hover_data=["Audience Segment", "CPA ($)", "CTR", "ROAS"],
        title="Spend vs Conversions by Campaign",
        template="plotly_white",
    )
    st.plotly_chart(spend_vs_conv, width="stretch")

    cpa_by_platform = px.bar(
        platform_metrics,
        x="Platform",
        y="CPA ($)",
        color="Platform",
        text="CPA ($)",
        title="Average CPA by Platform",
        template="plotly_white",
    )
    cpa_by_platform.update_traces(textposition="outside")
    st.plotly_chart(cpa_by_platform, width="stretch")

    roas_chart = px.bar(
        platform_metrics,
        x="Platform",
        y="ROAS",
        color="Platform",
        title="Average ROAS by Platform",
        template="plotly_white",
    )
    st.plotly_chart(roas_chart, width="stretch")

elif page == "Anomaly Detection":
    st.header("Anomaly Detection")
    st.markdown(
        "This page highlights underperforming segments with high CPA or low CTR so the agent can identify clear opportunities for improvement."
    )

    st.markdown(
        "### Underperforming segments detected"
    )
    st.dataframe(
        underperformer_segments,
    )

    if not underperformer_segments.empty:
        with st.container():
            st.markdown("### Worst offenders")
            offender_cols = st.columns(3)
            for slot, (_, row) in enumerate(underperformer_segments.head(3).iterrows()):
                offender_cols[slot].metric(
                    label=row["Audience Segment"],
                    value=f"CPA ${row['CPA ($)']}",
                    delta=f"CTR {row['CTR']}%",
                )

        st.markdown(
            "The agent flags these segments because they have either a CPA above $50 or a CTR below 0.5%. These patterns indicate ad creative and budget waste."
        )
    else:
        st.success("No underperforming segments found. All campaigns are performing within target thresholds.")

elif page == "Agentic Creative Optimization":
    st.header("Agentic Creative Optimization")
    st.markdown(
        "Select an underperforming segment and run the AI Agent to simulate a creative optimization briefing."
    )

    if underperformer_segments.empty:
        st.warning("No underperforming segments are available to optimize.")
    else:
        segment_choice = st.selectbox(
            "Choose an underperforming audience segment", underperformer_segments["Audience Segment"].tolist()
        )

        if st.button("Run AI Agent"):
            with st.spinner("Analyzing campaign performance and generating new copy..."):
                analysis, variants = simulate_agent_copy(segment_choice)

            st.success("Agent complete: creative recommendations generated.")
            st.markdown("### Agent analysis")
            st.info(analysis)

            for i, variant in enumerate(variants, start=1):
                with st.expander(f"Creative variant {i}"):
                    st.markdown(f"**Headline:** {variant['Headline']}")
                    st.markdown(f"**Primary Text:** {variant['Primary Text']}")

        else:
            st.info("Select a segment and click Run AI Agent to see targeted creative recommendations.")

elif page == "Budget Reallocation Engine":
    st.header("Budget Reallocation Engine")
    st.markdown(
        "This page shows the current budget allocation and the agent's recommended shift toward higher-performing segments."
    )

    current_allocation, recommended_allocation, total_cut, top_segments = recommend_budget_allocation(
        marketing_df, underperformer_segments
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Current Budget Allocation")
        st.dataframe(current_allocation.sort_values("Spend ($)", ascending=False).reset_index(drop=True))
    with col2:
        st.subheader("Agent Recommended Allocation")
        st.dataframe(recommended_allocation.sort_values("Recommended Budget ($)", ascending=False).reset_index(drop=True))

    projected_gain = int(total_cut * 0.18)
    projected_conversions = marketing_df["Conversions"].sum() + projected_gain
    st.metric("Budget shift moved", f"${total_cut:,.0f}", delta=f"Projected +{projected_gain} conversions")
    st.markdown(
        "The agent shifts 20% of spend from the underperforming segments into the top 3 highest-ROAS segments, projecting a measurable gain in overall campaign efficiency."
    )

    budget_chart = px.bar(
        recommended_allocation.sort_values("Recommended Budget ($)", ascending=False).head(10),
        x="Audience Segment",
        y=["Spend ($)", "Recommended Budget ($)"],
        title="Current vs Recommended Budget Allocation",
        template="plotly_white",
    )
    st.plotly_chart(budget_chart, width="stretch")
