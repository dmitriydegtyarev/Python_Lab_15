import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("bicycles_stat_2009.csv")
df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
df["Місяць"] = df["Date"].dt.month

numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
exclude_cols = ["Місяць"]
usage_cols = [col for col in numeric_cols if col not in exclude_cols]

# Обчислюємо для кожного рядка суму значень усіх використаних колонок
df["Загальна кількість"] = df[usage_cols].sum(axis=1)

# Групуємо дані за місяцями та підраховуємо суму загального використання
monthly_total = df.groupby("Місяць")["Загальна кількість"].sum()

# Групуємо дані за місяцями окремо для кожного стовпця, що входить до usage_cols
monthly_usage_individual = {}
for col in usage_cols:
    monthly_usage_individual[col] = df.groupby("Місяць")[col].sum()

plt.figure(figsize=(14, 8))
plt.plot(monthly_total.index, monthly_total.values, marker='o', linestyle='-',
         linewidth=2, color='black', label="Загальна кількість")

# Підписуємо кожну точку лінії загальної кількості
for x, y in zip(monthly_total.index, monthly_total.values):
    plt.text(x, y, str(y), fontsize=9, ha='center', va='bottom', color='black')

colors = ['blue', 'green', 'red', 'orange']
for i, col in enumerate(usage_cols):
    monthly_data = monthly_usage_individual[col]
    plt.plot(monthly_data.index, monthly_data.values, linestyle='-',
             label=col, color=colors[i % len(colors)])

plt.title("Використання велодоріжок за місяцями (2009)")
plt.xlabel("Місяць")
plt.ylabel("Кількість використань")
plt.grid()
plt.xticks(monthly_total.index)
plt.legend()
plt.tight_layout()
plt.show()