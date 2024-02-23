import matplotlib.pyplot as plt



x_days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
y_quan_reqls = [15, 43, 53, 23, 33, 55, 33]

fig, ax = plt.subplots()


bar_container = ax.bar(x_days, y_quan_reqls)
ax.set(title="Количество обращений")
ax.bar_label(bar_container)

plt.savefig("weekly_stats.png", bbox_inches="tight")
plt.show()
