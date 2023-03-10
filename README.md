# pretsLBP
Les prêts bancaires dépendent de 4 paramètres, qui sont liés entre eux
* $r_0$ : montant initial (en €)
* $q$ : taux
* $m$ : mensualité (en €)
* $N$ : durée (en mois)

Pour info, le taux des banques est donné par an, et pour passer au taux $q$ par mois, il suffit de diviser par 12 : $q=taux/12$
Cette approche est discutable, mais pas trop fausse et de toute façon c'est celle utilisée par ma banque.

Une alternative aurait été de définir $q$ de telle sorte que 
$$(1+taux)=(1+q)^{12}$$

A chaque mois, on peut établir :
* $r_n$ : montant restant au mois $n$ (en €)
* $i_n$ : intérêt au mois $n$
* $c_n$ : capital remboursé au mois $n$

```math
\begin{align}
r_1&=r_0\cdot (1+q) - m \\
r_2&=r_1\cdot (1+q) - m = r_0\cdot (1+q)^2 - m\cdot (1+(1+q)) = r_0\cdot (1+q)^2 - m\cdot ((1+q)^0+(1+q)^1) \\
r_n&=r_0\cdot (1+q)^n - m\cdot ((1+q)^0+(1+q)^1+...+(1+q)^{n-1}) \\
    &= r_0\cdot (1+q)^n - m\cdot \sum_{k=0}^{n-1}(1+q)^k\\
    &= r_0\cdot (1+q)^n - m\cdot \frac{(1+q)^{(n-1)+1}-1}{(1+q)-1}\\
i_n&=q\cdot r_{n-1} \\   
c_n&=m-i_k
\end{align}
```
Ensuite, comme les 4 paramètres sont liés, si on en fige 3, on peut en déduire le 4ème, plus ou moins directement.
Si le paramètre libre est la mensualité $m$, ça donne :
```math
\begin{align}
0&= r_0\cdot q\cdot (1+q)^N - m\cdot ((1+q)^N-1)\\
m&=r_0\cdot q\cdot \frac{(1+q)^N}{(1+q)^N-1} 
\end{align}
```
Au final, je retrouve au centime prêt le montant de la mensualité calculée par ma banque.

On peut ensuite faire la même chose avec comme paramètre libre la durée du prêt en mois
```math
\begin{align}
0&= r_0\cdot q\cdot (1+q)^N - m\cdot ((1+q)^N-1)\\
0&= r_0\cdot q - m\cdot \left(1-\frac{1}{(1+q)^N}\right)\\
\frac{1}{(1+q)^N}&=1-\frac{r_0\cdot q}{m}\\
-N\cdot \ln(1+q)&=\ln\left(1-\frac{r_0\cdot q}{m}\right)\\
N&=-\frac{\ln\left(1-\frac{r_0\cdot q}{m}\right)}{\ln(1+q)}\\\end{align}
```
Comme pour le calcul de la mensualité, avec cette formule on retrouve parfaitement la durée du prêt fourni par la banque.

Enfin, on peut chercher à évaluer le taux $q$, mais c'est un peu plus compliqué, car il est difficile d'isoler $q$ dans la formule ci-dessous
```math
\begin{align}
0&= r_0\cdot q\cdot (1+q)^N - m\cdot ((1+q)^N-1)\\
\end{align}
```
On peut s'en sortir en passant par des développements limités, ce qui fonctionne bien car $q$ est souvent beaucoup plus petit que $1$. SI on définit $\alpha = \frac{r_0}{m}$, on peut réécrire à l'ordre 3 
```math
\begin{align}
\alpha\cdot q\cdot \left(1+Nq+\frac{N(N-1)}{2!}q^2+\frac{N(N-1)(N-2)}{3!}q^3+o(q^3)\right) - \left(Nq+\frac{N(N-1)}{2!}q^2+\frac{N(N-1)(N-2)}{3!}q^3+o(q^3)\right)&=0\\
\left(\alpha q+\alpha Nq^2+\alpha\frac{N(N-1)}{2!}q^3+o(q^3)\right) - \left(Nq+\frac{N(N-1)}{2!}q^2+\frac{N(N-1)(N-2)}{3!}q^3+o(q^3)\right)&=0\\
(\alpha-N) q+N\left(\alpha -\frac{N-1}{2!}\right)q^2+N(N-1)\left(\frac{\alpha}{2!}-\frac{(N-2)}{3!}\right)q^3+o(q^3)&=0
\end{align}
```
Au final, on peut estimer assez finement le taux par mois $q$ (et donc le taux fourni par la banque $12\cdot q$ en trouvant les racines de ce polynôme d'ordre 3, par exemple à l'aide de numpy (method roots de np.polynomial.Polynomial). Sans difficulté on peut monter à l'ordre 4 ou 5.
