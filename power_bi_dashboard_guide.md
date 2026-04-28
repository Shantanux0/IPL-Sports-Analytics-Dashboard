# Power BI Dashboard Building Guide

This guide provides the instructions, DAX formulas, and visual layouts required to build the "IPL Sports Analytics Dashboard" in Power BI.

## 1. Data Import & Modeling
1. **Import Data**: Load `matches_cleaned.csv` and `deliveries_cleaned.csv` into Power BI via **Get Data > Text/CSV**.
2. **Data Modeling**:
   * Go to the Model View.
   * Create a **One-to-Many relationship** between `matches[match_id]` (One) and `deliveries[match_id]` (Many).
3. **Calendar Table (Optional but Recommended)**:
   * Create a new Date table for time-intelligence functions:
     `DateTable = CALENDAR(MIN(matches[date]), MAX(matches[date]))`
   * Link `DateTable[Date]` to `matches[date]`.

## 2. DAX Measures (Calculated Metrics)
Create a new table (e.g., `_Measures`) to store all your explicit DAX measures for a clean model.

**KPI Measures:**
```dax
Total Matches = COUNT(matches[match_id])

Total Runs = SUM(deliveries[total_runs])

Total Wickets = SUM(deliveries[is_wicket])

Total Sixes = CALCULATE(COUNT(deliveries[batsman_runs]), deliveries[batsman_runs] = 6)

Total Fours = CALCULATE(COUNT(deliveries[batsman_runs]), deliveries[batsman_runs] = 4)
```

**Performance Measures:**
```dax
Batting Strike Rate = 
DIVIDE(
    SUM(deliveries[batsman_runs]) * 100, 
    COUNT(deliveries[ball]), 
    0
)

Bowling Economy = 
DIVIDE(
    SUM(deliveries[total_runs]) * 6, 
    COUNT(deliveries[ball]), 
    0
)

Win Percentage = 
DIVIDE(
    CALCULATE(COUNT(matches[match_id]), matches[winner] <> "No Result"),
    [Total Matches],
    0
)
```

## 3. Dashboard Layout & Visualizations

Design the dashboard with a dark, premium theme (e.g., Dark Blue/Black background with neon/accent colors like Gold or Orange for IPL vibe).

### Section 1: Top Navigation & Filters
* **Slicers**: 
  * `Season` (Dropdown)
  * `Team` (Dropdown)
  * `Venue` (Dropdown)

### Section 2: KPI Scorecard (Top Row)
Use **Card Visuals** or **Multi-row Cards** to display:
* Total Matches
* Total Runs
* Total Wickets
* Total Sixes
* Total Fours

### Section 3: Main Visualizations
1. **Win Percentage by Team**
   * **Visual**: Clustered Bar Chart or Donut Chart.
   * **Axis/Legend**: `matches[winner]`
   * **Values**: `[Total Matches]` or `[Win Percentage]`
   * **Insight**: Easily identify the most dominant franchises over the years.

2. **Top Run Scorers (Orange Cap Contenders)**
   * **Visual**: Clustered Column Chart.
   * **Axis**: `deliveries[batter]`
   * **Values**: `[Total Runs]`
   * **Filter**: Top N (Top 10 by Total Runs).

3. **Top Wicket Takers (Purple Cap Contenders)**
   * **Visual**: Clustered Column Chart.
   * **Axis**: `deliveries[bowler]`
   * **Values**: `[Total Wickets]`
   * **Filter**: Top N (Top 10 by Total Wickets).

4. **Toss Decision vs. Match Result**
   * **Visual**: 100% Stacked Bar Chart.
   * **Axis**: `matches[toss_decision]` (Bat vs Field)
   * **Legend**: Won Match? (Create a calculated column: `If([toss_winner] = [winner], "Won", "Lost")`)
   * **Insight**: Shows whether chasing or defending is statistically better.

5. **Venue Analytics**
   * **Visual**: Scatter Plot or Matrix.
   * **Scatter Plot**: 
     * X-Axis: Average 1st Innings Score
     * Y-Axis: Win % for Chasing Teams
     * Details: `matches[venue]`

### Section 4: Tooltips & Drill-through
* Create a custom tooltip page showing a player's historical timeline (Runs/Wickets per season) when hovering over their name in the Top Scorers/Wicket Takers charts.
