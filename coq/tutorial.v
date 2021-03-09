(* Instructions for OSX

1. `brew install coq` 2. follow instructions linked at
https://mdnahas.github.io/doc/nahas_tutorial

this gives you the basic coqtop.  For groupoid (instead of setoid)
based reasoning, use the HoTT version of coqtop:

3. if in emacs, add the line `(setq proof-prog-name-ask 1)` to
`~/.emacs` 4. clone hott library repo:

`git clone https://github.com/HoTT/HoTT.git`

5. install to system

``` cd HoTT ./autogen.sh ./configure make ```

6. Add `hoqtop` to your path, e.g.

`export PATH=$PATH:/path/to/hoqtop`

7. At the top of a file you want to use HoTT tools:

`Require Import HoTT.`

For more, see: https://github.com/HoTT/HoTT/blob/master/INSTALL.md

Notes on HoTT: 
 -- you need to include bullets when (- + *, -- ++ **, etc) when using subgoals

*)
Require Import HoTT.

(* True -> True *)
Theorem my_first_proof : (forall A : Prop, A -> A).
Proof.
  intros A. (*intros ~ assume*)
  intros proof_of_A.
  exact proof_of_A. (* If the subgoal matches an hypothesis, Then use tactic "exact" *)
Qed.

(* example Props:
(forall x : nat, (x < 5) -> (x < 6))
(forall x y : nat, x + y = y + x)
(forall A : Prop, A -> A)
*)


Theorem modus_poenens : (forall A B : Prop, A -> (A->B) -> B).
Proof.
  intros A.
  intros B.
  intros pA.
  intros AimpB.
  pose (pB := AimpB pA). (* order: function composition *)
  exact pB. (* could also say "A_implies_B proof_of_A*)
Qed.

(* dont seem to be able to indent subgoals in emacs :( *)
Theorem mpmp_back : (forall A B C : Prop, A -> (A->B) -> (A->B->C) -> C).
Proof.
  intros A B C.
  intros pA AiB AiBiC.
  refine (AiBiC _ _).
  - exact pA.
  - refine (AiB _).
    + exact pA.
Show Proof.
Qed.
(* these bullets -,+ are good formatting practice, but required in HoTT/Coq 
http://prl.ccs.neu.edu/blog/2017/02/21/bullets-are-good-for-your-coq-proofs/
*)



  
(* 
stopped at "true and false vs. True and False" 
https://mdnahas.github.io/doc/nahas_tutorial
*)
