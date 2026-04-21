import os
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs("data", exist_ok=True)
os.makedirs("database", exist_ok=True)
os.makedirs("sql", exist_ok=True)

df = pd.read_csv("C:/Users/crudr/Desktop/StudentsPerformance.csv")

print("🚀 Start")
print("✅ File Loaded Successfully")
print(df.head())

df.columns = df.columns.str.replace(" ", "_")

df["total_score"] = df["math_score"] + df["reading_score"] + df["writing_score"]
df["avg_score"] = df["total_score"] / 3

def risk_level(score):
    if score < 50:
        return "High Risk"
    elif score < 65:
        return "Moderate Risk"
    elif score < 80:
        return "Low Risk"
    else:
        return "Top Performer"

df["risk_level"] = df["avg_score"].apply(risk_level)

def performance_band(score):
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 50:
        return "Average"
    else:
        return "Poor"

df["performance_band"] = df["avg_score"].apply(performance_band)

def generate_insight(row):
    if row["risk_level"] == "High Risk":
        return "Needs immediate academic support"
    elif row["risk_level"] == "Moderate Risk":
        return "Needs improvement with guidance"
    elif row["risk_level"] == "Low Risk":
        return "Stable performance"
    else:
        return "Excellent student - can mentor others"

df["recommendation"] = df.apply(generate_insight, axis=1)

plt.figure()
sns.countplot(x="risk_level", data=df)
plt.savefig("data/risk_distribution.png")
plt.close()

plt.figure()
sns.countplot(x="performance_band", data=df)
plt.savefig("data/performance_band.png")
plt.close()

plt.figure()
sns.barplot(x="gender", y="avg_score", data=df)
plt.savefig("data/gender_performance.png")
plt.close()

plt.figure()
sns.barplot(x="lunch", y="avg_score", data=df)
plt.savefig("data/lunch_impact.png")
plt.close()

df.to_csv("data/students_final.csv", index=False)

conn = sqlite3.connect("database/students.db")

df.to_sql("students_final", conn, if_exists="replace", index=False)
print("✅ Data inserted into SQLite DB")

print("🚀 Running SQL script...")
with open("../sql/final_script.sql", "r") as file:
    conn.executescript(file.read())
print("✅ SQL script executed successfully")

result = pd.read_sql("SELECT COUNT(*) as total FROM students_final", conn)
print(result)

final_df = pd.read_sql("SELECT * FROM students_final", conn)
final_df.to_csv("data/students_final_updated.csv", index=False)

conn.close()

print("🚀 COMPLETE PIPELINE EXECUTED SUCCESSFULLY")