import matplotlib.pyplot as plt
import numpy as np


# plt.plot([1, 2, 3, 4])
# plt.ylabel('some numbers')
# plt.show()


def e(t):
    return 1/ np.exp(-2 * t)


t_x = np.arange(0, 1, 0.1)

plt.figure(1)
plt.subplot(211)
# plt.plot(t_x, decay(t_x), 'r--')

plt.plot(t_x,  e(t_x), 'r--')


plt.show()

print(np.exp(1))

# plt.figure(1)
# plt.subplot(211)
# plt.plot(t1, f(t1), 'bo', t2, f(t2), 'k')
#
# plt.subplot(212)
# plt.plot(t2, np.cos(2 * np.pi * t2), 'r--')
# plt.show()
