# -*- coding: utf-8 -*-
"""Plot Densité Viellisement.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rKvRfJz_o1vKuY9RQdtRNmayLj0A_UNZ
"""

from scipy.stats import expon
import numpy as np
import matplotlib.pyplot as plt

# fonction pour calculer f(x) pour la densité du modèle de viellisement
def calcul_densite(alpha, beta, x):
  f = np.zeros(len(x))

  for point in range(len(x)):
    for index in range(len(alpha)):
        f[point] += alpha[index] * beta[index] * (x[point] **(-beta[index]-1))
  return f

alpha_vrai =[0.15, 0.25, 0.2, 0.1, 0.3]
beta_vrai = [5, 7, 2, 9, 8]

alpha_0= [0.10, 0.20, 0.3, 0.15, 0.25]
beta_0=[10,2, 20, 5, 12 ]

alpha_1000 = [0.11858998, 0.2319159,  0.24283876, 0.12997089, 0.27668447]
beta_1000 = [8.43933757, 2.1321403,  8.43991654, 4.03137739, 8.43947494]

support = np.linspace(start=1, stop=8, num=100)

f_true = calcul_densite(alpha=alpha_vrai, beta=beta_vrai, x=support)
f_0 = calcul_densite(alpha=alpha_0, beta=beta_0, x=support)
f_1000 = calcul_densite(alpha=alpha_1000, beta=beta_1000, x=support)

plt.plot(support, f_true, label='Vraie densité des machines', linewidth=1.0)
plt.plot(support, f_0, label='Densité initiale sans itération', ls='dotted',linewidth=1.0)
plt.plot(support, f_1000, label='Densité après 1000 itérations', ls='--', linewidth=1.0)

plt.legend()
plt.show()