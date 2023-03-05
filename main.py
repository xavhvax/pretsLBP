# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
#np.set_printoptions(formatter=['float'],precision=2)
#np.format_float_positional(precision=2)

class pret:
    """
    Cette classe définit toutes les informations utiles pour déterminer l'échéancier d'un prêt bancaire
    """
    def __init__(self, montant_ini, taux, mensualite):
        """ (self) -> None
        self.mensualite: montant de la mensualité (en €)
        """
        self.montant_ini=montant_ini
        self.taux=taux # par an
        self.mensualite=mensualite
        self.nb_mois=0

        self.echeancier=np.array([montant_ini])
        self.update()

        return None

    def update(self):
        """" (self) -> None

        """
        self.nb_mois=0
        #reste[1]=reste[0]x(1+q)-mensualite
        #[...]
        #reste[n]=reste[n-1]x(1+q)-mensualite
        # par définition : 1+taux=(1+q)^12
        q=(1.+self.taux)**(1./12.)-1.
        while self.echeancier[-1]>0:
            self.echeancier=np.append(self.echeancier,self.echeancier[-1]*(1.+q)-self.mensualite)
            self.nb_mois+=1
        return None

    def determine_mensualite(self):
        """ (self) -> float
        self.determine_mensualite()
        :return: renvoie la mensualité pour rembourser le prêt en nb_mois
        """
        # q=self.taux/12.
        # par définition : 1+taux=(1+q)^12
        q=(1.+self.taux)**(1./12.)-1.
        n=self.nb_mois
        return self.montant_ini*(1+q)**n*q/((1+q)**n-1)

    def determine_duree(self):
        """ (self) -> float
        reste[0]x(1+q)^n = mensualite x ((1+q)^n-1)/q
        reste[0] x q / mensualite  = 1-1/(1+q)^n
        1 - reste[0] x q / mensualite  = 1/(1+q)^n
        ln(1 - reste[0] x q / mensualite)  = -n ln (1+q)
        :return: renvoie le nombre de mensualités nécessaire pour rembourser le prêt
        """
        # q = self.taux / 12.
        # par définition : 1+taux=(1+q)^12
        q=(1.+self.taux)**(1./12.)-1.

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
                                    n*(n-1)*(ratio/np.math.factorial(2)-(n-2)/np.math.factorial(3)),
                                    n*(n-1)*(n-2)*(ratio/np.math.factorial(3)-(n-3)/np.math.factorial(4))),
                                   symbol='q')
        #print(p.roots())
        # par définition : 1+taux=(1+q)^12
        return (1.+np.real(p.roots()[-1]))**12.-1. # taux par an

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # par définition : 1+taux=(1+q)^12
    pret190k = pret(montant_ini=190.e3,taux=(1.+((189009.93+1124.65)/190.e3-1.))**12.-1.,mensualite=1124.65)
    #pret190k = pret(montant_ini=190.e3, taux=0.0085, mensualite=1124.65)
    print(pret190k.echeancier)
    print("taux : " + str((1.+((189009.93+1124.65)/190.e3-1.))**12.-1.))

    print("taux estimé : "       +str(pret190k.determine_taux()))
    print("durée estimée : "     +str(pret190k.determine_duree()))
    print("mensualité estimée : "+str(pret190k.determine_mensualite()))
