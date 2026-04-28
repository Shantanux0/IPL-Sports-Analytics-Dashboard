# Data Cleaning Guide (Excel)

This document outlines the step-by-step process for cleaning and preprocessing the raw IPL dataset (`matches.csv` and `deliveries.csv`) using Microsoft Excel.

## 1. Handling Missing Values
Raw datasets often contain missing or null values that can skew analysis.
* **City Column (`matches.csv`)**:
  * **Issue**: Some matches played in Dubai or Sharjah might have a blank `city` column.
  * **Solution**: Apply a filter on the `venue` column. Select venues like 'Dubai International Cricket Stadium' and update the blank `city` cells to 'Dubai'.
* **Winner Column**:
  * **Issue**: Matches with no result (e.g., due to rain) might have blank `winner` fields.
  * **Solution**: Replace blanks with `No Result` using the **Find & Select > Go To Special > Blanks** feature, then type `No Result` and press `Ctrl + Enter`.

## 2. Standardizing Team Names
Over the years, some IPL franchises have changed their names. It's crucial to standardize these to avoid splitting a single team's data.
* **Action**: Use `Find and Replace` (Ctrl + H) to map old names to new names.
  * *Replace* `Delhi Daredevils` *with* `Delhi Capitals`
  * *Replace* `Deccan Chargers` *with* `Sunrisers Hyderabad` (or keep them separate depending on analysis needs, but standardizing helps in franchise-wise analysis)
  * *Replace* `Kings XI Punjab` *with* `Punjab Kings`
  * *Replace* `Rising Pune Supergiant` *with* `Rising Pune Supergiants` (Fixing typos)

## 3. Removing Duplicates
Ensure there are no duplicate rows which could inflate match counts or run totals.
* **Action**: 
  1. Select the entire dataset.
  2. Go to **Data > Remove Duplicates**.
  3. For `matches.csv`, check based on `match_id`.
  4. For `deliveries.csv`, check based on `match_id`, `inning`, `over`, and `ball`.

## 4. Creating Calculated Columns
We need new metrics to enrich our Power BI dashboard and SQL analysis. Add these columns in the respective sheets:

### In `deliveries.csv`
* **Is Wicket?**:
  * Formula: `=IF(OR(ISBLANK(dismissal_kind), dismissal_kind=""), 0, 1)`
  * *Explanation*: Converts text-based dismissal entries into a binary 1/0 for easy aggregation.

### In Aggregated Player Stats (Pivot Tables in Excel)
If you are doing preliminary analysis in Excel using Pivot Tables, you can create Calculated Fields:
* **Strike Rate (Batsman)**:
  * Formula: `= (SUM(Batsman_Runs) / COUNT(Ball)) * 100`
* **Economy Rate (Bowler)**:
  * Formula: `= (SUM(Total_Runs) / (COUNT(Ball)/6))`

## 5. Formatting Dates
* **Action**: Ensure the `date` column in `matches.csv` is consistently formatted. Select the column, go to **Home > Number Format**, and choose `Short Date` (e.g., DD-MM-YYYY) to prevent Power BI from misinterpreting text strings as dates.

## 6. Saving Cleaned Files
* Save the finalized files as `matches_cleaned.csv` and `deliveries_cleaned.csv`. These will be the source files imported into Power BI and your SQL database.
