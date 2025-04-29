import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("bicycles_stat_2009.csv")

df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
df["Місяць"] = df["Date"].dt.month

# Отримуємо список усіх числових колонок і виключаємо з нього "Місяць"
numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
exclude_cols = ["Місяць"]
usage_cols = [col for col in numeric_cols if col not in exclude_cols]

# Обчислюємо для кожного рядка суму значень по числових колонках
df["Загальна кількість"] = df[usage_cols].sum(axis=1)

# Групуємо дані за місяцями: загальна кількість використань
monthly_total = df.groupby("Місяць")["Загальна кількість"].sum()

# Групуємо дані за місяцями окремо для кожного стовпця з usage_cols
monthly_usage_individual = {}
for col in usage_cols:
    monthly_usage_individual[col] = df.groupby("Місяць")[col].sum()

# Створюємо DataFrame з підсумковими даними по місяцях
df_visits = monthly_total.to_frame(name="Загальна кількість")
for col in usage_cols:
    df_visits[col] = monthly_usage_individual[col]

print("Датафрейм з кількістю відвідування велодоріжок по місяцях:")
print(df_visits)

plt.figure(figsize=(14, 8))
plt.plot(monthly_total.index, monthly_total.values, marker='o', linestyle='-', linewidth=2,
         color='black', label="Загальна кількість")

# Підписуємо кожну точку на графіку лінії загальної кількості
for x, y in zip(monthly_total.index, monthly_total.values):
    plt.text(x, y, str(y), fontsize=9, ha='center', va='bottom', color='black')

colors = ['blue', 'green', 'red', 'orange']
for i, col in enumerate(usage_cols):
    monthly_data = monthly_usage_individual[col]
    plt.plot(monthly_data.index, monthly_data.values, linestyle='-', label=col, color=colors[i % len(colors)])

plt.title("Використання велодоріжок за місяцями (2009)")
plt.xlabel("Місяць")
plt.ylabel("Кількість використань")
plt.grid()
plt.xticks(monthly_total.index)
plt.legend()
plt.tight_layout()
plt.show()