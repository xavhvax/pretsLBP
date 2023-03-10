# pretsLBP
Les prêts bancaires dépendent de 4 paramètres, qui sont liés entre eux
```
r : reste (en€)
q :taux
m : mensualité (en €)
n : durée (en mois)
r_0 : montant initial (en €)
r_k : montant restant au mois k (en €)

r_0=M
r_1=r_0\cdot (1+q) - m 
r_2=r_1\cdot (1+q) - m = r_0\cdot (1+q)^2 - m\cdot (1+(1+q)) 
r_n=r_0\cdot (1+q)^n - m\cdot (1+(1+q)+...+(1+q)^{n-1}) = r_0\cdot (1+q)^n - m\cdot \sum_{k=0}^n(1+q)^k
                                                        = r_0\cdot (1+q)^n - m\cdot \frac{(1+q)^{n-1}-1}{(1+q)-1}

```