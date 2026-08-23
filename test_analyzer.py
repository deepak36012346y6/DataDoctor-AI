import pandas as pd

from utils.analyzer import (
    generate_insights,
    correlation_insights,
    generate_summary,
    recommend_visualizations,
    cleaning_recommendations
)

# Load test dataset
df = pd.read_csv("data/test_messy_dataset.csv")

print("=" * 60)
print("🩺 DATADOCTOR AI - TEST")
print("=" * 60)

print("\n🔍 BASIC INSIGHTS")
print("-" * 40)

for result in generate_insights(df):
    print(result)

print("\n🔗 CORRELATION INSIGHTS")
print("-" * 40)

for result in correlation_insights(df):
    print(result)

print("\n📊 STATISTICAL SUMMARY")
print("-" * 40)

for result in generate_summary(df):
    print(result)

print("\n📈 VISUALIZATION RECOMMENDATIONS")
print("-" * 40)

for result in recommend_visualizations(df):
    print(result)

print("\n🧹 CLEANING RECOMMENDATIONS")
print("-" * 40)

for result in cleaning_recommendations(df):
    print(result)

print("\n" + "=" * 60)
print("✅ DATADOCTOR TEST COMPLETED")
print("=" * 60)