
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

df = pd.read_csv(r"C:\Users\navee\OneDrive\Desktop\Task-2\Cleaned_Electric_Vehicle_Data.csv")

print("="*50)
print("DATASET OVERVIEW")
print("="*50)

print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nSummary Statistics:")
print(df.describe())

year_trend = df["Model Year"].value_counts().sort_index()

plt.figure(figsize=(10,5))
plt.plot(year_trend.index, year_trend.values, marker='o')
plt.title("EV Adoption Trend by Model Year")
plt.xlabel("Model Year")
plt.ylabel("Number of Vehicles")
plt.grid(True)
plt.tight_layout()
plt.savefig("01_EV_Adoption_Trend.png", dpi=300)
plt.close()

top_cities = df["City"].value_counts().head(10)

plt.figure(figsize=(10,6))
top_cities.sort_values().plot(kind="barh")
plt.title("Top 10 Cities by EV Registrations")
plt.xlabel("Number of Vehicles")
plt.ylabel("City")
plt.tight_layout()
plt.savefig("02_Top_Cities.png", dpi=300)
plt.close()

top_counties = df["County"].value_counts().head(10)

plt.figure(figsize=(10,6))
top_counties.plot(kind="bar")
plt.title("Top 10 Counties by EV Registrations")
plt.xlabel("County")
plt.ylabel("Number of Vehicles")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("03_Top_Counties.png", dpi=300)
plt.close()

plt.figure(figsize=(10,5))
plt.hist(df["Electric Range"], bins=30)
plt.title("Electric Range Distribution")
plt.xlabel("Electric Range")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("04_Range_Distribution.png", dpi=300)
plt.close()

plt.figure(figsize=(10,6))
plt.scatter(
    df["Vehicle Age"],
    df["Electric Range"],
    alpha=0.4
)

plt.title("Vehicle Age vs Electric Range")
plt.xlabel("Vehicle Age")
plt.ylabel("Electric Range")
plt.tight_layout()
plt.savefig("05_Age_vs_Range.png", dpi=300)
plt.close()

cafv = df["Clean Alternative Fuel Vehicle (CAFV) Eligibility"].value_counts()

plt.figure(figsize=(8,8))
plt.pie(
    cafv,
    labels=cafv.index,
    autopct="%1.1f%%"
)

plt.title("CAFV Eligibility Distribution")
plt.tight_layout()
plt.savefig("06_CAFV_Distribution.png", dpi=300)
plt.close()

utilities = df["Electric Utility"].value_counts().head(10)

plt.figure(figsize=(10,6))
utilities.sort_values().plot(kind="barh")

plt.title("Top 10 Electric Utilities")
plt.xlabel("Number of Vehicles")
plt.ylabel("Utility")
plt.tight_layout()
plt.savefig("07_Top_Utilities.png", dpi=300)
plt.close()


models = df["Model"].value_counts().head(10)

plt.figure(figsize=(8,8))

plt.pie(
    models,
    labels=models.index,
    autopct="%1.1f%%"
)

centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.title("Top 10 EV Models")
plt.tight_layout()
plt.savefig("08_Top_Models_Donut.png", dpi=300)
plt.close()


top_brands = df["Make"].value_counts().head(5).index

box_data = [
    df[df["Make"] == brand]["Electric Range"]
    for brand in top_brands
]

plt.figure(figsize=(10,6))
plt.boxplot(box_data, labels=top_brands)

plt.title("Electric Range Distribution by Top Brands")
plt.ylabel("Electric Range")
plt.tight_layout()
plt.savefig("09_Boxplot_Range_By_Brand.png", dpi=300)
plt.close()

numeric_cols = [
    "Model Year",
    "Electric Range",
    "Legislative District",
    "Vehicle Age"
]

corr = df[numeric_cols].corr()

plt.figure(figsize=(8,6))
plt.imshow(corr)

plt.colorbar()

plt.xticks(
    range(len(corr.columns)),
    corr.columns,
    rotation=45
)

plt.yticks(
    range(len(corr.columns)),
    corr.columns
)

plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("10_Correlation_Heatmap.png", dpi=300)
plt.close()

print("\nTop Manufacturer:")
print(df["Make"].value_counts().head(1))

print("\nTop City:")
print(df["City"].value_counts().head(1))

print("\nTop County:")
print(df["County"].value_counts().head(1))

print("\nMost Popular Model:")
print(df["Model"].value_counts().head(1))

print("\nAverage Electric Range:")
print(round(df["Electric Range"].mean(), 2))

print("\nAll 10 charts saved successfully as PNG files!")

print("\n" + "="*60)
print("SQL BUSINESS ANALYSIS")
print("="*60)

# Create SQLite Database
conn = sqlite3.connect("ev_data.db")

# Create Table from DataFrame
df.to_sql(
    "EV_DATA",
    conn,
    if_exists="replace",
    index=False
)

print("\nDatabase Created Successfully!")
print("Table Name: EV_DATA")

queries = {

    "Q1. Top 10 EV Manufacturers": """
    SELECT Make,
           COUNT(*) AS Total_Vehicles
    FROM EV_DATA
    GROUP BY Make
    ORDER BY Total_Vehicles DESC
    LIMIT 10;
    """,

    "Q2. Top 10 Cities by EV Adoption": """
    SELECT City,
           COUNT(*) AS Total_EVs
    FROM EV_DATA
    GROUP BY City
    ORDER BY Total_EVs DESC
    LIMIT 10;
    """,

    "Q3. EV Adoption Trend by Model Year": """
    SELECT "Model Year",
           COUNT(*) AS Total_EVs
    FROM EV_DATA
    GROUP BY "Model Year"
    ORDER BY "Model Year";
    """,

    "Q4. Manufacturers with Highest Average Range": """
    SELECT Make,
           ROUND(AVG("Electric Range"),2) AS Average_Range
    FROM EV_DATA
    GROUP BY Make
    ORDER BY Average_Range DESC
    LIMIT 10;
    """,

    "Q5. Electric Vehicle Type Distribution": """
    SELECT "Electric Vehicle Type",
           COUNT(*) AS Total_Vehicles
    FROM EV_DATA
    GROUP BY "Electric Vehicle Type";
    """,

    "Q6. Top Electric Utility Providers": """
    SELECT "Electric Utility",
           COUNT(*) AS Total_Customers
    FROM EV_DATA
    GROUP BY "Electric Utility"
    ORDER BY Total_Customers DESC
    LIMIT 10;
    """,

    "Q7. CAFV Eligibility Distribution": """
    SELECT "Clean Alternative Fuel Vehicle (CAFV) Eligibility",
           COUNT(*) AS Total_Vehicles
    FROM EV_DATA
    GROUP BY "Clean Alternative Fuel Vehicle (CAFV) Eligibility";
    """
}

for title, query in queries.items():

    print("\n" + "="*60)
    print(title)
    print("="*60)

    try:
        result = pd.read_sql_query(query, conn)
        print(result)

    except Exception as e:
        print("Error:", e)

# Close Database
conn.close()

print("\nSQL Analysis Completed Successfully!")
print("Total Records:", df.shape[0])
print("Total Columns:", df.shape[1])