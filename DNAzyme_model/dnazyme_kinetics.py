import matplotlib.pyplot as plt
import numpy as np

plt.plot([6, 10, 20, 60, 180], [21, 29, 45, 67, 87], 'ro')
plt.axis([0, 200, 0, 120])

plt.ylabel('RFU/s')
plt.xlabel('Bacterial ECM Concentration (nM)')

x = np.arange(0, 200, 0.1)
y = (100 * x)/(28 + x)

plt.plot(x,y)

plt.plot((0, 200), (100, 100), 'k--')
plt.plot((28, 28), (0, 50), 'k--')
plt.plot((0, 28), (50, 50), 'k--')

plt.annotate('Km = 28 nM', xy=(28, 0), xytext=(29, 1),)
plt.annotate('1/2 Vmax = 50 RFU/s', xy=(0, 50), xytext=(1, 51),)
plt.annotate('Vmax = 100 RFU/s', xy=(0, 100), xytext=(1, 101),)

plt.show()