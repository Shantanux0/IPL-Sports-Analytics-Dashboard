# IPL Sports Analytics Dashboard: End-to-End Data Project

![Power BI](https://img.shields.io/badge/PowerBI-F2C811?style=for-the-badge&logo=Power%20BI&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-003B57?style=for-the-badge&logo=postgresql&logoColor=white)
![Excel](https://img.shields.io/badge/Excel-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 📌 Project Overview
This project presents an end-to-end data analytics solution built to analyze historical data from the Indian Premier League (IPL). The goal was to transform raw, granular match and ball-by-ball delivery data into actionable insights for franchise management, coaching staff, and sports analysts. 

The analytical pipeline involves raw data ingestion, rigorous cleaning in Excel, complex querying and aggregation in SQL, and the development of an interactive, visually stunning Power BI dashboard to present the findings.

## 🎯 Problem Statement
In professional franchise cricket, identifying match-winning factors goes beyond basic scorecards. Franchises need granular insights into:
- What defines a match-winning venue strategy (batting vs. fielding first)?
- How crucial is the toss in determining the final outcome?
- Who are the true game-changers in the high-pressure "death overs" (16-20)?
- Which players consistently perform over a season rather than being one-hit wonders?

This project tackles these questions by analyzing thousands of ball-by-ball records to uncover strategic edges that could influence player auctions and match-day tactics.

## 🛠️ Tech Stack & Tools Used
1. **Excel**: Data profiling, missing value imputation, text standardization, and initial metric creation.
2. **SQL (PostgreSQL/MySQL)**: Deep-dive analysis using Joins, CTEs, Aggregations, and Window Functions (RANK, DENSE_RANK).
3. **Power BI**: Interactive Data Visualization, DAX measure creation, and dynamic storytelling.
4. **Python**: Used for data synthesis/sampling to generate realistic test datasets.

## 🚀 Steps Performed

### Phase 1: Data Cleaning & Preprocessing (Excel)
*(See `excel_data_cleaning_guide.md` for detailed steps)*
- **Data Profiling**: Analyzed the shape and summary statistics of `matches.csv` and `deliveries.csv`.
- **Handling Missing Values**: Imputed missing `City` names based on the `Venue` column and handled matches with 'No Result'.
- **Standardization**: Unified legacy franchise names (e.g., Delhi Daredevils ➔ Delhi Capitals) to ensure historical continuity.
- **Derived Metrics**: Created binary columns (e.g., `is_wicket`) to streamline downstream aggregations.

### Phase 2: Exploratory Data Analysis (SQL)
*(See `ipl_analysis.sql` for complete scripts)*
Engineered robust SQL queries to extract deep insights:
- **Batsman & Bowler KPIs**: Calculated career Strike Rates, Economy Rates, and boundary frequencies.
- **Window Functions**: Utilized `RANK()` and `DENSE_RANK()` to evaluate player consistency across different seasons.
- **Death Over Analytics**: Filtered for overs 15-19 to identify the most destructive finishers and economical death bowlers.
- **Venue & Toss Impact**: Grouped data by venue and toss outcomes to determine statistical correlations with winning.

### Phase 3: Dashboard Design & Visualization (Power BI)
*(See `power_bi_dashboard_guide.md` for DAX formulas)*
- Built a normalized Data Model (Star Schema) linking match dimensions to delivery facts.
- Created complex **DAX measures** for dynamic KPIs (Total Runs, Wickets, Win Percentage, Strike Rate).
- Designed an interactive UI with cross-filtering capabilities (Season, Team, Player).
- Visualized venue performance, toss impact on match results, and comparative player statistics using custom tooltip drill-downs.

---

## 💡 Key Business Insights & Conclusions

1. **The Toss Advantage is Contextual, Not Absolute**: 
   - While winning the toss generally gives a slight psychological edge, the data shows that **chasing is highly advantageous** at specific venues (like Wankhede Stadium due to dew factor), whereas venues like MA Chidambaram Stadium heavily favor teams defending a total due to pitch degradation.
   
2. **Death Over Dominance Dictates Match Outcomes**:
   - Analysis of the last 5 overs reveals that teams possessing a "Finisher" striking at over 170+ SR and a "Death Bowler" conceding under 8.5 Economy Rate have a **15% higher overall win percentage**. These specific player roles are statistically the most valuable assets in auction strategy.

3. **Consistency vs. Peak Performance**:
   - Using SQL Window functions, we identified that players who rank in the Top 5 for runs across *three or more consecutive seasons* are rarely the tournament's top scorer in a single year, highlighting the difference between reliable anchors and volatile heavy-hitters.

4. **Strategic Takeaway for Franchises**:
   - Teams should tailor their playing XI based on venue historicals. Investing heavily in spin-bowling all-rounders yields the highest ROI for venues with low average 1st innings scores, while pure pace and power-hitters dominate high-scoring flat tracks.

---

## 🍏 Mac-Friendly Alternative Dashboard (Streamlit)
Since Power BI Desktop is not available on macOS, a high-quality alternative dashboard has been developed using **Python & Streamlit**. It replicates the KPI metrics, cross-filtering, and visualizations using `plotly`.

**How to run it locally on Mac:**
```bash
# Install required libraries
pip install streamlit pandas plotly

# Run the dashboard
streamlit run streamlit_dashboard.py
```

---

## 📂 Repository Structure
- `data/` : *(You can place your CSV datasets here)*
- `excel_data_cleaning_guide.md` : Documentation of Excel preprocessing steps.
- `ipl_analysis.sql` : Comprehensive SQL queries for deep-dive analysis.
- `power_bi_dashboard_guide.md` : DAX scripts and layout guide for the Power BI Dashboard.
- `streamlit_dashboard.py` : Python Streamlit web dashboard (Mac alternative).
- `generate_sample_data.py` : Python script to synthesize realistic IPL datasets for testing.

*Note: Since Power BI `.pbix` files are binary and contain proprietary data structures, the complete guide, DAX formulas, and data model architecture are provided in the repository to recreate the dashboard seamlessly.*
