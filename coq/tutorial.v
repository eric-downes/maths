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
  pose (pB := AimpB pA). (* A_implies_B APPLIED_TO proof_of_A *) 
  exact pB. (* could also say "A_implies_B proof_of_A*)
Qed.

(* dont seem to be able to indent subgoals in emacs :( *)
Theorem mpmp_back : (forall A B C : Prop, A -> (A->B) -> (A->B->C) -> C).
Proof.
  intros A B C.
  intros pA AiB AiBiC.
  refine (AiBiC _ _).
    exact pA.
    refine (AiB _).
      exact pA.
Show Proof.
Qed.

(* 
stopped at "true and false vs. True and False" 
https://mdnahas.github.io/doc/nahas_tutorial
*)
