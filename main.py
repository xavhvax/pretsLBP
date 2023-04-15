# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

np.set_printoptions(formatter={'float': '{:10.2f}'.format})
pd.options.display.float_format = "{:.2f}".format

# pd.set_option('display.max_rows', None) # print tout le pd.DataFrame, pas seulement un nb limité de lignes

class Pret:
    """
    Cette classe définit toutes les informations utiles pour déterminer l'échéancier d'un prêt bancaire
    """

    def __init__(self, montant_ini, taux, mensualite, nb_mois):
        """ (self) -> None
        :param self.mensualite: montant de la mensualité (en €)
        """
        self.montant_ini = montant_ini
        self.taux = taux  # par an

        if type(nb_mois) is list:
            assert (len(mensualite) == len(nb_mois)), \
                "il faut avoir autant de changement de mensualité que de changement de nb de mois"
            self.mensualite = mensualite
            self.nb_mois = nb_mois
        else:
            self.mensualite = [mensualite]
            self.nb_mois = [nb_mois]

        self.update()

        # on stocke le cout final du prêt dans une variable, pour mémoire
        cout_prets_ini=self.echeancier['intérêts cumulés'].values[-1]
        self.interets_cumules_tot_ini=pd.DataFrame([[cout_prets_ini, 100.*cout_prets_ini/self.montant_ini]],
                                                   columns=['cout_pret_ini (€)', 'cout_pret_ini (%)'])
        #self.interets_cumules_tot_ini.style.hide_index()
        print(self.interets_cumules_tot_ini)

    def update(self, cash=0, mois_du_cash=0, mensualite_variation=0.):
        """" (self) -> None
        :param self:
        :param cash:
        :param mois_du_cash:
        """
        assert(-0.1<mensualite_variation<0.1), \
            "La variation des mensualités doit être comprise entre -10% et +10%"
        # reste[1]=reste[0]x(1+q)-mensualite
        # [...]
        # reste[n]=reste[n-1]x(1+q)-mensualite
        # par définition : :math:`1+taux=(1+q)^{12}`
        # q=(1.+self.taux)**(1./12.)-
        q = self.taux / 12.

        # while self.echeancier[-1][0]>0:
        l=[[]]
        if hasattr(self,"echeancier"):
            #print(self.echeancier.loc[mois_du_cash,:].values.tolist())
            l = [(self.echeancier.loc[mois_du_cash,:].values-np.array([cash,0.,0.,0.])).tolist()]
        else:
            l = [[self.montant_ini, 0., 0., 0.]]

        k = mois_du_cash
        for m, n in zip(self.mensualite, self.nb_mois):
            while k < n:
                k += 1
                reste = l[-1][0]
                interet = reste * q
                capital = np.round(m*(1.+mensualite_variation) - interet,2) # en prenant en compte cet arrondi, on retrouve exactement l'échéancier de la banque
                interet_cumule = l[-1][-1] + interet
                l.append([reste - capital,
                          capital,
                          interet,
                          interet_cumule])

        if hasattr(self,"echeancier"):
            self.echeancier[mois_du_cash:] = pd.DataFrame(l, columns=['reste',
                                                                      'capital',
                                                                      'intérêts',
                                                                      'intérêts cumulés'])
        else:
            self.echeancier = pd.DataFrame(l, columns=['reste',
                                                       'capital',
                                                       'intérêts',
                                                       'intérêts cumulés'])

        # On supprime les derniers mois car on a fini de rembourser le prêt
        #cf. https://stackoverflow.com/questions/13851535/how-to-delete-rows-from-a-pandas-dataframe-based-on-a-conditional-expression
        self.echeancier.drop(self.echeancier[self.echeancier.reste < 0.].index[1:], inplace=True)
        interets_cumules_tot_new=np.round(self.echeancier['intérêts cumulés'].values[-1],2)
        if hasattr(self,"interets_cumules_tot_ini"):
            print("gain abs (€) & gain relatif (%)")
            print(self.interets_cumules_tot_ini.values[0][0]-interets_cumules_tot_new, 100.*interets_cumules_tot_new/self.montant_ini)
            return
        else:
            return

    def determine_mensualite(self):
        """ (self) -> float
        cette méthode permet d'évaluer le montant de la mensualité pour rembourser le prêt de self.montant_ini
        au taux de self.taux en self.nb_mois
        :param self:
        :return: renvoie la mensualité pour rembourser le prêt en nb_mois
        """
        if len(self.nb_mois) > 1:
            return "méthode non implémentée si changement de mensualité en cours de remboursement"

        # par définition : 1+taux=(1+q)^12
        # q=(1.+self.taux)**(1./12.)-1.
        q = self.taux / 12.
        n = self.nb_mois[0]
        # reste[0] x q / mensualite  = 1-1/(1+q)^n
        return np.round(self.montant_ini * (1. + q) ** n * q / ((1. + q) ** n - 1.),3)

    def determine_duree(self):
        """ (self) -> float
        reste[0]x(1+q)^n = mensualite x ((1+q)^n-1)/q
        reste[0] x q / mensualite  = 1-1/(1+q)^n
        1 - reste[0] x q / mensualite  = 1/(1+q)^n
        ln(1 - reste[0] x q / mensualite)  = -n ln (1+q)
        :return: renvoie le nombre de mensualités nécessaire pour rembourser le prêt
        """
        if len(self.nb_mois) > 1:
            return "méthode non implémentée si changement de mensualité en cours de remboursement"
        # par définition : 1+taux=(1+q)^12
        # q=(1.+self.taux)**(1./12.)-1.
        q = self.taux / 12.

        # ln(1 - reste[0] x q / mensualite)  = -n ln (1+q)
        return np.round(-np.log(1 - self.montant_ini * q / self.mensualite[0]) / np.log(1 + q), 2)

    def determine_taux(self):
        """ (self) -> float
        q=taux/12 => taux par mois # c'est une approximation
        reste[1]=reste[0]x(1+q)-mensualite
        reste[n]=reste[0]x(1+q)^n-mensualite x somme_k=0,n-1 (1+q)^k
                =reste[0]x(1+q)^n-mensualite x ((1+q)^n-1)/(1+q-1) # fonctionne pour reste[1]

        reste[n]=0 <=>
        reste[0]x(1+q)^n = mensualite x ((1+q)^n-1)/q
        reste[0] x q / mensualite  = 1-1/(1+q)^n
        1 - reste[0]/mensualite x q  = 1/(1+q)^n
        1/(1 - reste[0]/mensualite x q)  = (1+q)^n
        DL de (1+x)^n en 0 : (1+x)^n=1+nx+x^2 n(n-1)/2!+x^3 n(n-1)(n-2)/3!+o(x^3)
        (1+q)^n = 1 + nq + n(n-1)/2! q^2 + o(q^2)

        reste[0] x q x (1+q)^n = mensualite x ((1+q)^n-1)
        reste[0]/mensualite x q x (1 + nq+ n(n-1)/2!q^2+n(n-1)(n-2)/3!q^3+o(q^3)) = (nq+ n(n-1)/2!q^2+n(n-1)(n-2)/3!q^3+o(q^3))
        reste[0]/mensualite x (q + nq^2+ n(n-1)/2!q^3+n(n-1)(n-2)/3!q^4+o(q^4)) = (nq+ n(n-1)/2!q^2+n(n-1)(n-2)/3!q^3+o(q^3))
        :return:
        """
        if len(self.nb_mois) > 1:
            return "méthode non implémentée si changement de mensualité en cours de remboursement"

        ratio = self.montant_ini / self.mensualite[0]
        n = self.nb_mois[0]
        p = np.polynomial.Polynomial((0.,
                                      ratio - n,
                                      n * (ratio - (n - 1) / np.math.factorial(2)),
                                      n * (n - 1) * (ratio / np.math.factorial(2) - (n - 2) / np.math.factorial(3)),
                                      # ordre 3
                                      n * (n - 1) * (n - 2) * (
                                                  ratio / np.math.factorial(3) - (n - 3) / np.math.factorial(4)),
                                      # ordre 4
                                      # n*(n-1)*(n-2)*(n-3)*(ratio/np.math.factorial(4)-(n-4)/np.math.factorial(5)) # ordre 5
                                      ),
                                     symbol='q')
        # print(p.roots())
        return np.round(12. * np.real(p.roots()[-1]),5)  # taux par an
        # par définition : 1+taux=(1+q)^12
        # return (1.+np.real(p.roots()[-1]))**12.-1. # taux par an

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # par définition : 1+taux=(1+q)^12

    # Construction du 1er prêt, de 196k€
    # pret190k = pret(montant_ini=190.e3,taux=(1.+((189009.93+1124.65)/190.e3-1.))**12.-1.,mensualite=1124.65)
    pret190k = Pret(montant_ini=190.e3, taux=0.0085, mensualite=1124.65, nb_mois=180)

    print(pret190k.echeancier)
    # print("taux : " + str((1.+((189009.93+1124.65)/190.e3-1.))**12.-1.))
    print("taux : " + str(np.round(12. * ((189009.93 + 1124.65) / 190.e3 - 1.),5)))  # => 0.00849978947368335
    print("taux : " + str(0.0085))  # => indiqué dans les papiers de la banque

    # Quelques estimations et vérifications
    print("taux estimé : " + str(pret190k.determine_taux()))
    print("durée estimée : " + str(pret190k.determine_duree()))
    print("mensualité estimée : " + str(pret190k.determine_mensualite()))

    # Construction du 1er prêt, de 266k€
    pret266k = Pret(montant_ini=266.e3, taux=0.013, mensualite=[294.83 + 288.17, 1619.65 + 224.72], nb_mois=[180, 300])
    print(pret266k.echeancier)

    # Ajout de 50k€ de cash à 15 ans du 2ème prêt
    print("\nAjout de 50k€ de cash à 15 ans du 2ème prêt")
    pret266k.update(cash=50.e3,mois_du_cash=15*12)
    print(pret266k.echeancier)

    pret_tot = pret190k.echeancier.add(pret266k.echeancier, fill_value=0)

    # Quelques graphs
    exit()
    print(pret_tot)
    fig, ax1 = plt.subplots()
    plt.xlabel('mois')
    plt.ylabel('€')
    plt.plot(pret_tot[['reste', 'intérêts cumulés']], label=['reste', 'intérêts cumulés'], color='r')
    plt.legend()
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    plt.ylabel('€')
    plt.plot(pret_tot[['capital', 'intérêts']], label=['capital', 'intérêts'], color='b')
    plt.legend()
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
