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
    (thx Mike Shulman)

*)
Require Import HoTT.
Require Import Bool.

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

(* seems odd you dont provide a term of type A->B *)
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
False is more like "Unprovable"
True is "Provable"
false is a boolean
true is a boolean
 *)

Inductive False : Prop := .

Inductive True : Prop := I : True.

Inductive bool : Set :=
| true : bool
| false : bool.


(* proving True allows us to use I *)

Theorem True_can_be_proven : True.
  exact I.
Qed.

(* proving "not False" uses an empty case *)

Theorem Not_False : ~False.
Proof.
  intros proof_of_False.
  case proof_of_False.
Qed.

(* 
in HoTT/Coq ~ maps to Empty... if you need the traditional Coq usage,
try "A -> False" instead of ~A
*)

Theorem Not_TiF : (True -> False) -> False.
Proof.
  intros TiF.
  refine (TiF _).
  - exact I.
Qed.


(* beware "reducto ad absurdum" *)

Theorem absurd : forall A B : Prop, A -> ~A -> B.
Proof.
  intros A B.
  intros pA pNotA.
  pose (pFalse := pNotA pA).
  case pFalse.
Qed.


(* *)


(* 
https://mdnahas.github.io/doc/nahas_tutorial
*)










Theorem modus_poenens : (forall A B : Prop, A -> (A->B) -> B).
  intros A B



