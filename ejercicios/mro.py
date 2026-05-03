class A:
    pass

class F:
    def hablar(self):
        print("Hola desde F")
class B(A):
    pass

class C(F):
    pass
    
class D(B,C):
    pass

d = D()

d.hablar()
# d.mro() - esto es para ver como funciona esa mondaa