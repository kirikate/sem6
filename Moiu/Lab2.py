import numpy as np
from numpy.linalg import inv


def main():

    int_m = 3
    int_n = 5

    matrix_a: np.matrix = np.matrix(
        [[-1, 1, 1, 0, 0], [1, 0, 0, 1, 0], [0, 1, 0, 0, 1]]
    )

    vector_c = np.matrix([[1, 1, 0, 0, 0]])
    print(vector_c)
    current_plan = np.array([0.0, 0.0, 1.0, 3.0, 2.0], float)

    index_list = np.array([2, 3, 4], int)

    basic_matrix = np.matrix(np.zeros((int_m, len(index_list))))

    for i in range(int_m):
        for j in range(len(index_list)):
            basic_matrix.itemset((i, j), matrix_a.item(i, index_list[j]))

    inverse_basic_matrix = inv(basic_matrix)

    while True:
        basic_c: np.matrix = np.matrix([[vector_c.item(j)] for j in index_list])
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

        print(f"first neg comp has index {j_0} and it's {vector_delta.item(j_0)}")

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
                        else current_plan[index_list[i]] / vector_z.item(i)
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
        index_list[int_k] = j_0

        if theta_0 is None:
            print(
                "Целевой функционал не ограничен сверху на множестве допустимых планов\n"
            )
            break

        # j_star = 0
        for i in range(int_m):
            if i == int_k:
                current_plan[index_list[i]] = theta_0
            else:
                current_plan[index_list[i]] = current_plan[
                    index_list[i]
                ] - theta_0 * vector_z.item(i)
        current_plan.itemset(j_star, 0)

        print(f"base\n{basic_matrix}")
        print(f"index_list\n{index_list}")
        print(f"A\n{matrix_a}")

        for j in range(len(index_list)):
            for i in range(int_m):
                # print(f"i={i} j={j}")
                basic_matrix.itemset((i, j), matrix_a.item(i, index_list[j]))

        print(f"base\n{basic_matrix}")
        inverse_basic_matrix = inv(basic_matrix)  # special_inverse

        print(f"current_plan {current_plan}")
        print("\n\n\n\n")
    return


if __name__ == "__main__":
    main()
