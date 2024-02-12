import numpy.linalg as la
import numpy as np


N: int = 3
A: np.matrix = np.matrix([[1, -1, 0], [0, 1, 0], [0, 0, 1]])
x: np.matrix = np.matrix([1, 0, 1]).transpose()
i: int = 3
i = i - 1


Ainv: np.matrix = la.inv(A)
print(f"A=\n{A}\n A-=\n{Ainv}\n")

print(f"x=\n{x}")

newA = A.copy()

for row in range(0, N):
    newA.itemset((row, i), x.item(row))

l: np.matrix = Ainv * x
# print(f"l=\n{l}")
if l.item(i) == 0:
    print("Матрица необратима")
    quit(0)

li = l.item(i)
l.itemset(i, -1)

l = (-1 / li) * l
# print(f"lf=\n{l}")

Q: np.matrix = np.matrix(np.identity(3))

for row in range(0, N):
    Q.itemset((row, i), l.item(row))

# print(f"Q=\n{Q}")

newAinv: np.matrix = Q * Ainv

print(f"result =\n {newAinv}")
print(f"through numpy =\n {la.inv(newA)}")
