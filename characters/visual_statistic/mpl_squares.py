import matplotlib.pyplot as plt

squares = [1, 4, 9, 16, 25]
plt.plot(squares, linewidth=5)

# Назначение заголовка диаграммы и меток осей 
plt.title("Викли статс", fontsize=24)
plt.xlabel("Value", fontsize=14)
plt.show()