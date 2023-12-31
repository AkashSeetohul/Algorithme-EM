import numpy as np
import math as math
from scipy.stats import uniform
from scipy.stats import rv_discrete

class loi_melange_viellisement:

  def __init__(self, alpha, beta):
    self.alpha = alpha
    self.beta = beta
    # la classe contient aussi la distribution marginale des machines - chaque élément de alpha représente le probabililité de chaque classe.
    self.distribution_Z = rv_discrete(a=0, b=len(alpha), values=(np.arange(len(alpha)),alpha))

  # methode pour renvoyer une array d'échantillon d'un taille donné
  def echantilloner(self, taille):
    # L'échantillon z déterminera la valeur de beta_j utilisée, grâce à la présence de l'indicatrice dans chaque terme de l'expression
    z = self.distribution_Z.rvs(size=taille)

    x_echantillon = np.zeros(shape = taille)

    for indice in range(taille):
      realization_Z = z[indice]
      beta_j = self.beta[realization_Z]
      # on simule une réalization aléatoire "unif" de la distribution uniforme avec paramètre 0 et 1
      # L'échantillon X est le quantile de "unif" de la fonction de répartition de h(x; beta=beta_j; alpha = realization_Z)
      unif = uniform.rvs(size=1)
      x_echantillon[indice] = math.exp(math.log(1-unif) / -beta_j)

    return x_echantillon

# on simule des données pour l'algorithme
alpha_vrai = [0.15, 0.25, 0.2, 0.1, 0.3]
beta_vrai = [5, 7, 2, 9, 8]

# on génère des échantillons/observations
loi_melange = loi_melange_viellisement(alpha=alpha_vrai, beta=beta_vrai)
x_echantillon = loi_melange.echantilloner(taille=1000)
ln_x_echantillon = [math.log(x) for x in x_echantillon]

# les paramètres initiales
alpha_estime = [0.10, 0.20, 0.3, 0.15, 0.25]
beta_estime = [10,2, 20, 5, 12 ]

# une fonction qui calcule f(x, beta_j)
# Paramètres: une réalisation de X, alpha_j, et beta_j
def f(alpha_j, beta_j, x):
    return alpha_j * beta_j * (x **(-beta_j-1))

# On définit nos critère d'arrêt
max_iterations = 2001
tolerance = 0.0001

# initialization des variables pour la boucle while
nombre_iterations = 0
difference = 1000

# on initialize une boucle avec les conditions d'arrêt - tolerance et nombre maximale d'itérations
while (nombre_iterations < max_iterations) and (difference > tolerance):
  # arrays pour les prochains paramètres
  nouveau_alpha = np.zeros(len(alpha_estime))
  nouveau_beta = np.zeros(len(beta_estime))

  # on initialise la matrice H
  H = np.zeros((len(x_echantillon), len(alpha_estime)))

  # on calcule les valeurs de H_ij basée sur les formules du Section ....
  for i in range(len(x_echantillon)):
    for j in range(len(alpha_estime)):

        # on calcule f(x_i,alpha) pour chaque alpha - le somme est le denominateur de H_ij
        denom = np.zeros(len(alpha_estime))
        for indice in range(len(alpha_estime)):
          denom[indice] = f(alpha_j=alpha_estime[indice], beta_j=beta_estime[indice], x=x_echantillon[i])

        H[i,j] = f(alpha_j=alpha_estime[j], beta_j=beta_estime[j], x=x_echantillon[i]) / np.sum(denom)

  # on calcule les prochaines estimations basées sur les formules du Section 6.1.2
  for index in range(len(alpha_estime)):
    nouveau_alpha[index] = np.sum(H[:, index])/len(x_echantillon)
    nouveau_beta[index] = np.sum(H[:, index])/np.dot(np.transpose(ln_x_echantillon),H[:, index])

  # mise à jour des variables pour le critère d'arrêt
  nombre_iterations += 1
  difference = np.sqrt(math.dist(nouveau_alpha,alpha_estime) + math.dist(nouveau_beta,beta_estime))

  # mise à jour de nos parametres
  alpha_estime = nouveau_alpha
  beta_estime = nouveau_beta

  if nombre_iterations==250 or nombre_iterations==500 or nombre_iterations==750 or nombre_iterations==1000:
      print(nombre_iterations)
      print(alpha_estime)
      print(beta_estime)
