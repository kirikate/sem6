import numpy as np
from numpy.linalg import inv


def specInv(int_m: int, int_n: int, inverse_matrix: np.matrix, new_matrix: np.matrix, i: int):
    x: np.array = (new_matrix.transpose()[i]).transpose()

    print(f"A-=\n{inverse_matrix}\n")

    print(f"x=\n{x}")

    l: np.matrix = inverse_matrix * x
    print(f"l=\n{l}")
    if l.item(i) == 0:
        print("Матрица необратима")
        quit(0)

    li = l.item(i)
    l.itemset(i, -1)

    l = (-1 / li) * l
    print(f"lf=\n{l}")
    Q: np.matrix = np.matrix(np.identity(int_m))

    for row in range(int_m):
        Q.itemset((row, i), l.item(row))

    # new_inverted: np.matrix = Q * inverse_matrix
    new_inverted = np.identity(int_m)
    for j in range(int_m):
        for k in range(int_m):
            new_inverted.itemset((j, k), Q.item(j, j) * inverse_matrix.item(j, k) +
                                 Q.item(j, i) * inverse_matrix.item(i, k))

    print(f"result =\n {new_inverted}")
    return new_inverted


def main_phase(int_n: int, int_m: int, matrix_a: np.matrix,
               vector_c: np.array, current_plan: np.array,
               index_list: np.array):

    flist = []
    for i in range(int_m):
        flist.append([])
        for j in range(int_n):
            flist[i].append(0)
    # print(flist)

    basic_matrix = np.matrix(np.zeros((int_m, len(index_list))))

    for i in range(int_m):
        for j in range(len(index_list)):
            basic_matrix.itemset((i, j), matrix_a.item(i, index_list[j] - 1))

    print(f"basic_matrix =\n {basic_matrix}")
    inverse_basic_matrix = inv(basic_matrix)

    while True:
        basic_c: np.matrix = np.matrix([[vector_c.item(j - 1)] for j in index_list])
        print(f"basic_c: {basic_c}")

        vector_u = basic_c.transpose() * inverse_basic_matrix
        print(f"vector_u: {vector_u}")

        vector_delta = vector_u * matrix_a - vector_c
        print(f"vector_delta:{vector_delta}")

        j_0 = -1
        for j in range(int_m):
            if vector_delta.item(j) < 0:
                j_0 = j
                break

        if j_0 == -1:
            print(f"The optimal plan is:\n{current_plan}")
            break

        print(f"first neg comp has index {j_0} and its {vector_delta.item(j_0)}")

        jcolumn = np.matrix([[matrix_a.item(i, j_0)] for i in range(matrix_a.shape[0])])

        print(f"invers basic:\n{inverse_basic_matrix}\n jcolumn: {jcolumn}")
        vector_z: np.matrix = (inverse_basic_matrix) * jcolumn
        print(f"vector_z:\n{vector_z}")

        vector_theta = np.matrix(
            [
                [
                    (
                        None
                        if vector_z.item(i) <= 0
                        else current_plan[index_list[i] - 1] / vector_z.item(i)
                    )
                    for i in range(int_m)
                ]
            ]
        )

        theta_0 = None
        int_k = 0
        for i in range(int_m):
            if vector_theta.item(i) is not None:
                if theta_0 is None or vector_theta.item(i) < theta_0:
                    theta_0 = vector_theta.item(i)
                    int_k = i

        j_star = index_list[int_k]
        index_list[int_k] = j_0 + 1

        if theta_0 is None:
            print(
                "Целевой функционал не ограничен сверху на множестве допустимых планов\n"
            )
            break

        for i in range(int_m):
            if i == int_k:
                current_plan[index_list[i] - 1] = theta_0
            else:
                current_plan[index_list[i] - 1] = current_plan[index_list[i] - 1] - theta_0 * vector_z.item(i)
        current_plan.itemset(j_star - 1, 0)

        print(f"base\n{basic_matrix}")
        print(f"index_list\n{index_list}")
        print(f"A\n{matrix_a}")

        initial_inverse_matrix = inverse_basic_matrix
        for j in range(len(index_list)):
            for i in range(int_m):
                # print(f"i={i} j={j}")
                basic_matrix.itemset((i, j), matrix_a.item(i, index_list[j] - 1))

        print(f"base\n{basic_matrix}")
        print(f"int_k=\t{int_k}")
        inverse_basic_matrix = specInv(int_m, int_n, inverse_basic_matrix, basic_matrix, int_k)

        print(f"current_plan {current_plan}")
        print("\n\n\n\n")
    return


def main():

    int_m = 3
    int_n = 5
    matrix_a: np.matrix = np.matrix(
        [[-1, 1, 1, 0, 0], [1, 0, 0, 1, 0], [0, 1, 0, 0, 1]]
    )
    vector_c = np.array([1, 1, 0, 0, 0])
    current_plan = np.array([0.0, 0.0, 1.0, 3.0, 2.0], float)
    index_list = np.array([3, 4, 5], int)

    main_phase(int_n, int_m, matrix_a, vector_c, current_plan, index_list)
    return


if __name__ == "__main__":
    main()
