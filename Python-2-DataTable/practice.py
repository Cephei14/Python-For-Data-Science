import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [1, 2, 3], label="A")
plt.plot([1, 2, 3], [3, 2, 1], label="B")
plt.title("Demo")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()
