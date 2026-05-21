import numpy as np
import pandas as pd
from pathlib import Path


def generate_marketing_data(n_rows=500, export_excel=True, excel_path="data/marketing_data.xlsx"):
    """Generate a realistic marketing dataset and optionally export to Excel."""
    np.random.seed(42)

    platforms = ["Meta", "Google", "LinkedIn"]
    audience_segments = [
        "Tech Bros 25-34",
        "Soccer Moms",
        "Fitness Enthusiasts",
        "Luxury Shoppers",
        "Eco Buyers",
        "Small Business Owners",
        "Freelance Creators",
        "Health Advocates",
        "Urban Commuters",
        "Budget Travelers",
    ]
    creatives = [
        "Bold Launch",
        "Summer Value",
        "Growth Story",
        "Trust Builder",
        "Limited Offer",
        "Experience Now",
        "Performance Boost",
        "Fresh Perspective",
        "Smart Choice",
        "Feel Great",
    ]

    rows = []
    for i in range(n_rows):
        campaign_id = f"CMP-{1000 + i}"
        platform = np.random.choice(platforms, p=[0.45, 0.4, 0.15])
        segment = np.random.choice(audience_segments)
        creative = np.random.choice(creatives)
        spend = np.round(np.random.uniform(600, 8000), 2)

        # Baseline performance distributions
        impressions = int(np.random.normal(120000, 22000))
        impressions = max(20000, impressions)
        ctr = np.clip(np.random.normal(0.015, 0.006), 0.003, 0.05)
        clicks = int(impressions * ctr)
        clicks = max(5, clicks)
        conversion_rate = np.clip(np.random.normal(0.08, 0.03), 0.01, 0.21)
        conversions = max(1, int(clicks * conversion_rate))

        rows.append(
            {
                "Campaign ID": campaign_id,
                "Platform": platform,
                "Audience Segment": segment,
                "Ad Creative Name": creative,
                "Spend ($)": spend,
                "Impressions": impressions,
                "Clicks": clicks,
                "Conversions": conversions,
            }
        )

    df = pd.DataFrame(rows)

    # Inject 2-3 intentionally bad segments to create obvious underperformers
    bad_segments = ["Budget Travelers", "Soccer Moms", "Urban Commuters"]
    bad_mask = df["Audience Segment"].isin(bad_segments)
    df.loc[bad_mask, "Clicks"] = (df.loc[bad_mask, "Impressions"] * np.random.uniform(0.002, 0.004, size=bad_mask.sum())).astype(int)
    df.loc[bad_mask, "Conversions"] = (df.loc[bad_mask, "Clicks"] * np.random.uniform(0.02, 0.05, size=bad_mask.sum())).astype(int)
    df.loc[bad_mask, "Spend ($)"] = df.loc[bad_mask, "Spend ($)"].clip(lower=2000, upper=9000)
    df.loc[bad_mask, "Clicks"] = df.loc[bad_mask, "Clicks"].clip(lower=3)
    df.loc[bad_mask, "Conversions"] = df.loc[bad_mask, "Conversions"].clip(lower=1)

    # Derived metrics
    df["CTR"] = (df["Clicks"] / df["Impressions"]).round(4)
    df["CPA ($)"] = (df["Spend ($)"] / df["Conversions"]).replace([np.inf, np.nan], 0).round(2)
    df["ROAS"] = ((df["Conversions"] * np.random.uniform(30, 140, size=len(df))) / df["Spend ($)"]).round(2)

    if export_excel:
        output_path = Path(excel_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(output_path, index=False)

    return df


if __name__ == "__main__":
    df = generate_marketing_data(n_rows=500, export_excel=True)
    print(f"Generated {len(df)} rows and exported to data/marketing_data.xlsx")
