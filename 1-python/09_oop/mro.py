class A:
    label = "A: Base class"


class B(A):
    label = "VB: Masal blend"


class C(A):
    label = "C: Herbal blend"


class D(B, C):
    pass


cup = D()
print(cup.label)
print(D.__mro__)
