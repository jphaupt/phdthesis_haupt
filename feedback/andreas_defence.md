> right, the frontpage should be updated. 🙂
Done.

> And the "argon" example should indeed be adapted, as "18 nuclei" reads really strange at this point.
Maybe do 100x100x100 grid, 1 nucleus, so 10^(6*(18+1))=10^114
indeed, the schroedinger equation (1.2) already has the nuclei interpreted as point particles.


> I found a few more points that require attention:

> * The statement after eq. 1.3 is not fully correct, as \Psi_elec matter-of-factly depends (parametrically) on the nuclear coordinates (but only weakly). The nuclear kinetic energy operator then leads to non-adiabatic coupling terms.

This is a good point. Maybe just drop the statement altogether for a more intuitive explanation? Solve at every instant.

> * Eq. 1.9 is not consistent with its later use in 2.32/2.33.

I think I was confusing chemist/physicist notation here, should definitely change here

> * In 1.3 it would be better to explicitly require that the spectrum of H must be bounded  from below, otherwise the variation method does not work (e.g. Dirac operator).

Do you mean the relativist one-electron Hamiltonian and the fermi sea? I'm not sure what is meant by "better", are we replacing something? My understanding is that Hermiticity and boundedness are both required. Do you mean to just introduce it as a sentence at the start of the section?

* Page 8: I do not get to 10^23 (only 10^22) ... pls check

(10 choose 20) for number of possible configurations
^2 for spin
^2 for square matrix
x8 for double precision
= 9.28e22 bytes or ~10 zettabytes. You are right.


* After 1.32 the line-break could be adapted (note that this use of V is consistent with eq. 1.9, but not with the later 2.32).

Put into its own equation (and fix the indexing...). Not sure why I changed notation when moving to the next chapter.

* Page 22, end of Section 2.1: The last paragraph reads as if the use of Gaussians was the main problem, but it is not. As mentioned in the exam, the convergence of Gaussian with respect to Slater type functions is roughly exponential and thus not a big problem (for energies). The main problem is the expansion of electron correlation in terms of products of one-particle functions, leading to the slow N^-1 convergence of the correlation energy.

Good point. Not sure how to adjust the discussion though.

* Pls. Check the signs in the argument of eq. 2.3

They look correct to me, could you clarify? I also checked them against this review: https://pubs.acs.org/doi/10.1021/cr200204r (equation 50) as well as the original paper https://journals.aps.org/pr/pdf/10.1103/PhysRev.31.333 (bottom of page 341) and my expression seems to be the same.

* Eq. 2.34 has indices I and J on the rhs with no counterpart on the lhs.

I forgot the sum over nuclear indices I and J. Should add. (these are not on the lhs)

* End of 2.5.2: In how far is F12 additive? In CC-F12 it enters the wavefunction as exp(T1+T2+F12)|0> = exp(F12)exp(T1+T2)|0> (F12 is the F12-dependent extra set of amplitudes).

Good point. I was thinking of it as additive since you have (1+tQ_{12}F_{12})\Psi in the early formulation, but I think it would be more accurate to mention F12 is a modification on the level of the wavefunction whereas TC is a modification on the level of the Hamiltonian.

* Page 51 (bottom line): I think that "results" of sth. like this misses after "chemcially accurate"

Yes, added.

* Page 64: "... simultaneous interaction of three electrons is unlikely ..." (should not be formulated this way, as 1/r means that interaction is unavoidable and we for sure know that there are important terms beyond CCSD.

Maybe best to just change how this was formulated in the paper

* Same page: "Reduction factors obtains ..." should be "... obtained ..."

Indeed, done.

* Table 4.7: To be precise, these are the electronic contributions to the Total Atomisation Energy, sometimes called eTAE. The TAE is significantly different due to ZPE.

okay, good point. should change a little

* Page 89 (and possibly other places): Ref 285 is not the correct one for HEAT

woops!! *Definitely* need to change that. The citation key is correct, might have been a build issue with latex. Try again!

* Figure 6.1: Pls check the upper two graphics. To me they look absolutely similar.

They are very similar, but it does look like I made a mistake here in the image. They were different when I compared them in two different plots, but when making the combined plots evidently used the same variable twice by mistake. They differ by a few mHa but on this scale it is hard to see (just in the atom it's easier because the values go crazy).

and yes fix up references:

* References: (62) Layout

  - (70) Title

  - (225) Journal Title

  - (234)/(234) Check completeness of references
> do you mean 234/235? 233?

  - (269)/(270) Check references

  - (283) Journal Title

  - (306) Reference incomplete
