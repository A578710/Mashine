import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Функція для розрахунку моменту
def calculate_moment(s, R2, X2, omega_s):
    return (3 / omega_s) * (R2 / s) / ((R2 / s)**2 + X2**2) * 1000  # Переведення в Н·м

# Інтерфейс Streamlit
st.title("Симулятор залежності електромагнітного моменту від ковзання")
st.sidebar.header("Параметри двигуна")
R2 = st.sidebar.slider("Активний опір ротора R2 (Ом)", 0.1, 2.0, 0.5, 0.1)
X2 = st.sidebar.slider("Індуктивний опір ротора X2 (Ом)", 0.1, 2.0, 1.0, 0.1)
f = st.sidebar.slider("Частота живлення f (Гц)", 10, 60, 50, 1)
p = st.sidebar.slider("Кількість пар полюсів p", 1, 4, 2, 1)

# Розрахунок синхронної кутової швидкості
omega_s = 2 * np.pi * f / p

# Генерація значень ковзання
s_values = np.linspace(-0.5, 1, 500)
moment_values = np.array([calculate_moment(s, R2, X2, omega_s) if s != 0 else np.nan for s in s_values])

# Вибір точок для відображення
num_points = st.sidebar.slider("Кількість точок для позначення", 2, 20, 11)
s_points = np.linspace(-0.5, 1, num_points)
moment_points = np.array([calculate_moment(s, R2, X2, omega_s) if s != 0 else np.nan for s in s_points])

# Побудова графіка
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(s_values, moment_values, label="M = f(s)", color="blue")
ax.scatter(s_points, moment_points, color="red", label="Обрані точки", zorder=5)
ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
ax.set_title("Залежність електромагнітного моменту від ковзання", fontsize=14)
ax.set_xlabel("Ковзання, s", fontsize=12)
ax.set_ylabel("Електромагнітний момент, M (Н·м)", fontsize=12)
ax.grid(True)

# Додавання текстових підписів для точок
for i, s in enumerate(s_points):
    if not np.isnan(moment_points[i]):
        ax.annotate(f"s={s:.2f}\nM={moment_points[i]:.2f} Н·м", 
                    (s, moment_points[i]), 
                    textcoords="offset points", 
                    xytext=(-10, 10), 
                    ha='center', color='red')

ax.legend()

# Виведення графіка
st.pyplot(fig)
