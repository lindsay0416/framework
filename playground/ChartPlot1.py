import matplotlib.pyplot as plt
import numpy as np


# plt.plot([1, 2, 3, 4])
# plt.ylabel('some numbers')
# plt.show()


def f(t):
    return np.exp(-t) * np.cos(2 * np.pi * t)


def e(t):
    return (1 - np.exp(-t)) / (1 - np.exp(-1))


def s(t):
    return -1 / (1 + np.exp(-t + 30)) + 1


def decay(t):
    return np.exp(-t * 0.1)


t1 = np.arange(0.5, 7.0, 0.1)
t2 = np.arange(0.0, 5.0, 0.02)

t3 = np.arange(0, 60, 0.02)

t_x = np.arange(0, 50, 0.1)


plt.figure(1)
plt.subplot(211)
# plt.plot(t_x, decay(t_x), 'r--')
plt.plot(t_x,  np.exp(-t_x * 0.01), 'r--')
plt.plot(t_x, np.exp(-t_x * 0.02), 'r--')
plt.plot(t_x, np.exp(-t_x * 0.03))
plt.plot(t_x, np.exp(-t_x * 0.04))
plt.plot(t_x, np.exp(-t_x * 0.05))
plt.plot(t_x, np.exp(-t_x * 0.06))
plt.plot(t_x, np.exp(-t_x * 0.07))
plt.plot(t_x, np.exp(-t_x * 0.08))
plt.plot(t_x, np.exp(-t_x * 0.09))
plt.plot(t_x, np.exp(-t_x * 0.1))

plt.show()

print(np.exp(1))

# plt.figure(1)
# plt.subplot(211)
# plt.plot(t1, f(t1), 'bo', t2, f(t2), 'k')
#
# plt.subplot(212)
# plt.plot(t2, np.cos(2 * np.pi * t2), 'r--')
# plt.show()
