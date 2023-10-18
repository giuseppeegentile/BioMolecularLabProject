# BioMolecularLabProject
Let $\mathcal P$ the space of proteins.<br>
Let $H_t : \mathcal P \rightarrow \mathcal P$ the map that describes the evolution of a protein following to heating.<br>
Let $\mathcal N : \mathcal P \rightarrow \mathscr P ( \mathcal P )$ a function that given a protein returns a set of admissible proteins that are "near" to that
(admissible mutation function)
<br>
The idea is to measure some kind of "topological affinity" among a protein at rest state and a protein after energy administration through heat. <br>
This topological affinity $a : \mathcal P \times \mathcal P \rightarrow [0,1]$  measures how much bonds are similar in the perturbed version of the protein. <br>
The objective of the project is to solve the following optimization problem
<br>
$\text{Given } p \in \mathcal P$ <br>
$\text{Find } p^* \in \mathcal N(p) \text{ such that } a(p^{\*},H_t(p^{\*})) \text{ is maximized} $
