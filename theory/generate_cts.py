#!/bin/python3
"""
USAGE: generate_cts.py N
N is the number of universes that need to be generated
"""


import sys


PUBLIC_SIG = """
(;---------- PUBLIC SIG ----------;)

(; Represents the type of sorts ;)
Sort: Type.

(; encoded versions of CTS type living in sort s ;)
Univ: s : Sort -> Type.	

(; `Term s A` is the encoded version of term living in type A ;)
def Term : s : Sort -> a : Univ s -> Type.


def UNat : Type.
def enum : UNat -> Sort.
def uzero : UNat.
def usucc : UNat -> UNat.

bool : Type.
eps : bool -> Type.
true : bool.

def Axiom : Sort -> Sort -> bool.
def Rule : Sort -> Sort -> Sort -> bool.
def Cumul : Sort -> Sort -> bool.
def SubType : s : Sort -> s' : Sort -> Univ s -> Univ s' -> bool.

def sinf : Sort.
def univ : s : Sort -> s' : Sort -> eps (Axiom s s') -> Univ s'.
def prod : s1 : Sort -> s2 : Sort -> s3 : Sort -> eps (Rule s1 s2 s3) -> a : Univ s1 -> b : (Term s1 a -> Univ s2) -> Univ s3.
def cast : s : Sort -> s' : Sort -> a : Univ s -> b : Univ s' -> eps (SubType s s' a b) -> Term s a -> Term s' b.


univ' (s : Sort) (s' : Sort) : Univ s'.
def prod' : s1 : Sort -> s2 : Sort -> s3 : Sort -> a : Univ s1 -> b : (Term s1 a -> Univ s2) -> Univ s3.
def cast' : s : Sort -> s' : Sort -> a : Univ s -> b : Univ s' -> Term s a -> Term s' b.
"""

PRIVATE_SIG = """
(;---------- PRIVATE SIG ----------;)
[s,s',p] univ s s' p --> univ' s s'.
[s1,s2,s3,p] prod s1 s2 s3 p --> prod' s1 s2 s3.
[s1,s2,a,b,t] cast s1 s2 a b _ t --> cast' s1 s2 a b t.

[s] Term _ (univ' s _) --> Univ s.
[s1,s2,a,b] Term _ (prod' s1 s2 _ a b) --> x : Term s1 a -> Term s2 (b x).
[s,a] Term _ (cast' _ _ (univ' s _) _ a) --> Term s a.

def forall : s : Sort -> a : Univ s -> (Term s a -> bool) -> bool.
[] forall _ _ (x => true) --> true.
I : eps true.

[s1, s2] SubType _ _ (univ' s1 _) (univ' s2 _ ) --> Cumul s1 s2
[s1,s2,s2',a,b,b'] SubType _ _ (prod' s1 s2 _ a b) (prod' _ s2' _ a b') --> forall s1 a (x => SubType s2 s2' (b x) (b' x)).
[a] SubType _ _ a a --> true.

[A,t] cast' _ _ A A t --> t.
[s, s', a, c, t] cast' _ s' _ c (cast' s _ a _ t) --> cast' s s' a c t.
[s1,s2,A,B,a] cast' _ s2 (cast' _ _ (univ' s1 _) _ A) B a --> cast' s1 s2 A B a.
[s1,s2,A,B,a] cast' s1 _ A (cast' _ _ (univ' s2 _) _ B) a --> cast' s1 s2 A B a.
[s1,s2,s3,s4,a,b] cast' _ _ (univ' _ _) (univ' s4 _) (prod' s1 s2 s3 a b) --> prod' s1 s2 s4 a b.
[s1,s2,s3, a, b] prod' _ s2 s3 (cast' _ _ (univ' s1 _) (univ' _ _) a) b --> prod' s1 s2 s3 a b.
[s1, s2, s3, a, b] prod' s1 _ s3 a (x => cast' _ _ (univ' s2 _) (univ' _ _) (b x)) --> prod' s1 s2 s3 a (x => b x).
[s1,s2,s3,A,B,C,b] cast' _ _ (prod' s1 s2 _ A B) (prod' s1 s3 _ A C) (x => b x) --> x : Term s1 A => cast' s2 s3 (B x) (C x) (b x).
[s1,s2,s3,A,B,C,b,a] cast' _ _ (prod' s1 s2 _ A B) (prod' s1 s3 _ A C) b a --> cast' s2 s3 (B a) (C a) (b a).
"""

STTFA_SPEC="""
(;---------- STTFA SPEC ----------;)
def triangle : Sort.
def diamond : Sort.
def box : Sort.
def star : Sort.
def ball : Sort.

[] Axiom star box --> true.
[] Axiom box triangle --> true.
[] Axiom diamond sinf --> true.
[] Axiom triangle sinf --> true.


[] Rule star star star --> true.
[] Rule box box box --> true.
[] Rule box star star --> true.
[] Rule triangle star star --> true. (; ? ;)
[] Rule triangle diamond diamond --> true. (; ? ;)
[] Rule triangle ball ball --> true.

[] Cumul box diamond --> true.
[] Cumul triangle ball --> true.
"""

def generateAgdaSpec(num_univ):
    ans = "(;---------- AGDA SPEC -----------;)\n"

    #def set2 : Sort.
    for i in range(0, num_univ):
        ans += f"def set{i} : Sort.\n"

    #[] Axiom seti setj --> true.
    for i in range(0, num_univ-1):
        ans += f"[] Axiom set{i} set{i+1} --> true.\n"

    #[] Rule seti setj setk --> true
    for i in range(0, num_univ):
        for j in range(0, num_univ):
            ans += f"[] Rule set{i} set{j} set{max(i,j)} --> true.\n"

    ans += "[a] Cumul a a --> true.\n"

    return ans

if __name__ == '__main__':
    # number of universes
    N = int(sys.argv[1])
    print(PUBLIC_SIG)
    print(PRIVATE_SIG)
    print(STTFA_SPEC)
    print(generateAgdaSpec(N))
