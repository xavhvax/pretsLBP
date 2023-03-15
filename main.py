# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import pandas as pd
np.set_printoptions(formatter={'float':'{:10.2f}'.format})
pd.options.display.float_format = "{:.2f}".format

pd.DataFrame()
class pret:
    """
    Cette classe définit toutes les informations utiles pour déterminer l'échéancier d'un prêt bancaire
    """
    def __init__(self, montant_ini, taux, mensualite, nb_mois):
        """ (self) -> None
        :param self.mensualite: montant de la mensualité (en €)
        """
        self.montant_ini=montant_ini
        self.taux=taux # par an
        self.mensualite=mensualite
        self.nb_mois=nb_mois

        self.echeancier=np.array([[montant_ini, 0., 0., 0.]])
        self.update()

        return None

    def update(self):
        """" (self) -> None
        :param self:
        """
        #reste[1]=reste[0]x(1+q)-mensualite
        #[...]
        #reste[n]=reste[n-1]x(1+q)-mensualite
        # par définition : .. math:`1+taux=(1+q)^{12}`
        #q=(1.+self.taux)**(1./12.)-1.
        q=self.taux/12.

        #while self.echeancier[-1][0]>0:
        for mois in np.arange(self.nb_mois):
            #self.nb_mois += 1
            self.echeancier=np.concatenate((self.echeancier,
                                            [[self.echeancier[-1][0]*(1.+q)-self.mensualite,
                                              self.mensualite-self.echeancier[-1][0]*q,
                                              self.echeancier[-1][0]*q,
                                              self.echeancier[-1][-1]+self.echeancier[-1][0]*q]]))
        return None

    def determine_mensualite(self):
        """ (self) -> float
        cette méthode permet d'évaluer le montant de la mensualité pour rembourser le prêt de self.montant_ini
        au taux de self.taux en self.nb_mois
        :param self:
        :return: renvoie la mensualité pour rembourser le prêt en nb_mois
        """
        # par définition : 1+taux=(1+q)^12
        # q=(1.+self.taux)**(1./12.)-1.
        q = self.taux / 12.
        n=self.nb_mois
        # reste[0] x q / mensualite  = 1-1/(1+q)^n
        return self.montant_ini*(1.+q)**n*q/((1.+q)**n-1.)

    def determine_duree(self):
        """ (self) -> float
        reste[0]x(1+q)^n = mensualite x ((1+q)^n-1)/q
        reste[0] x q / mensualite  = 1-1/(1+q)^n
        1 - reste[0] x q / mensualite  = 1/(1+q)^n
        ln(1 - reste[0] x q / mensualite)  = -n ln (1+q)
        :return: renvoie le nombre de mensualités nécessaire pour rembourser le prêt
        """
        # par définition : 1+taux=(1+q)^12
        # q=(1.+self.taux)**(1./12.)-1.
        q = self.taux / 12.

        # ln(1 - reste[0] x q / mensualite)  = -n ln (1+q)
        return -np.log(1-self.montant_ini*q/self.mensualite)/np.log(1+q)


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
        ratio=self.montant_ini/self.mensualite
        n=self.nb_mois
        p=np.polynomial.Polynomial((0.,
                                    ratio-n,
                                    n*(ratio-(n-1)/np.math.factorial(2)),
                                    n*(n - 1)*(ratio/np.math.factorial(2)-(n-2)/np.math.factorial(3)), # ordre 3
                                    n*(n-1)*(n-2)*(ratio/np.math.factorial(3)-(n-3)/np.math.factorial(4)), # ordre 4
                                    #n*(n-1)*(n-2)*(n-3)*(ratio/np.math.factorial(4)-(n-4)/np.math.factorial(5)) # ordre 5
                                   ),
                                   symbol='q')
        #print(p.roots())
        return 12.*np.real(p.roots()[-1]) # taux par an
        # par définition : 1+taux=(1+q)^12
        # return (1.+np.real(p.roots()[-1]))**12.-1. # taux par an

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # par définition : 1+taux=(1+q)^12
    #pret190k = pret(montant_ini=190.e3,taux=(1.+((189009.93+1124.65)/190.e3-1.))**12.-1.,mensualite=1124.65)
    pret190k = pret(montant_ini=190.e3, taux=0.0085, mensualite=1124.65, nb_mois=180)

    print(pd.DataFrame(pret190k.echeancier,columns=['reste', 'capital', 'intérêts', 'intérêts cumulés']))
    #print("taux : " + str((1.+((189009.93+1124.65)/190.e3-1.))**12.-1.))
    print("taux : " + str(12.*((189009.93 + 1124.65) / 190.e3 - 1.))) # => 0.00849978947368335
    print("taux : " + str(0.0085)) # => indiqué dans les papiers de la banque

    print("taux estimé : "       +str(pret190k.determine_taux()))
    print("durée estimée : "     +str(pret190k.determine_duree()))
    print("mensualité estimée : "+str(pret190k.determine_mensualite()))
