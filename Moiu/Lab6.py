import numpy as np
from numpy.linalg import inv


def quadratic_method(int_m: int, int_n: int, matrix_a: np.matrix, matrix_d: np.matrix,
                     vector_c: np.array, current_plan: np.array, index_list: np.array, index_list_star: np.array):
    while True:
        print("Step #1 Start")
        basic_matrix = np.matrix(np.zeros((int_m, len(index_list))))
        for i in range(int_m):
            for j in range(len(index_list)):
                basic_matrix.itemset((i, j), matrix_a.item(i, index_list[j] - 1))
        inverse_basic_matrix = inv(basic_matrix)
        print(f"basic_matrix: \n{basic_matrix}")
        print(f"inverse_basic_matrix: \n{inverse_basic_matrix}")
        vector_cx = np.matrix(vector_c).transpose() + matrix_d * np.matrix(current_plan).transpose()
        basic_cx = np.array([[vector_cx.item(j - 1)] for j in index_list])
        print(f"basic_cx: \n{basic_cx}")
        vector_ux = - basic_cx.transpose() * inverse_basic_matrix
        vector_deltax = np.squeeze(np.asarray(vector_ux * matrix_a + np.array(vector_cx.transpose())))
        print("Step #1 Completed")
        print(f"vector_cx: \n{vector_cx}")
        print(f"vector_ux: \n{vector_ux}")
        print(f"vector_deltax: \n{vector_deltax}")

        print("Step #2-3 Start")
        j_0 = -1
        for i in vector_deltax:
            if i < 0:
                j_0 = np.argwhere(vector_deltax == i)[0][0] + 1
                break
        if j_0 == -1:
            print("Step #2-3 Completed")
            print("Optimal plan: \n", current_plan)
            break
        print("Step #2-3 Completed")
        print(f"j_0: {j_0}")

        print("Step #4 Start")
        # anti_index_list_star = np.array([i for i in range(1, int_n + 1) if not np.isin(i, index_list_star)], int)
        vector_l = np.zeros(int_n)
        vector_l[j_0 - 1] = 1

        args = index_list_star - np.full(len(index_list_star), 1)
        sub_d = matrix_d[np.ix_(args, args)]

        basic_matrix_star = np.matrix(np.zeros((int_m, len(index_list_star))))
        for i in range(int_m):
            for j in range(len(index_list_star)):
                basic_matrix_star.itemset((i, j), matrix_a.item(i, index_list_star[j] - 1))

        matrix_h_upper = np.concatenate((sub_d, basic_matrix_star.transpose()), 1)
        matrix_h_lower = np.concatenate((basic_matrix_star, np.zeros((int_m, int_m))), 1)
        matrix_h = np.concatenate((matrix_h_upper, matrix_h_lower), axis=0)
        matrix_h_inverse = inv(matrix_h)

        b_star = np.zeros(1)
        for j in index_list_star:
            b_star = np.append(b_star, matrix_d.transpose().item(j_0 - 1, j - 1))
        for j in range(int_m):
            b_star = np.append(b_star, matrix_a.transpose().item(j_0 - 1, j))
        b_star = np.delete(b_star, 0)

        vector_x = - matrix_h_inverse * np.matrix(b_star).transpose()

        for j in range(len(index_list_star)):
            vector_l[index_list_star[j] - 1] = vector_x[j]
        print("Step #4 Completed")
        print(f"vector_l: \n{vector_l}")

        print("Step #5 Start")
        vector_theta = np.array([(None if vector_l.item(j - 1) >= 0 else -current_plan[j - 1] / vector_l.item(j - 1))
                                 for j in index_list_star])
        delta = float(vector_l * matrix_d * np.matrix(vector_l).transpose())
        theta_j_0 = None if delta == 0 else np.abs(vector_deltax[j_0 - 1]) / delta
        theta_0 = theta_j_0
        j_star = j_0
        int_k: int = -1
        for i in range(len(vector_theta)):
            if vector_theta.item(i) is not None:
                if theta_0 is None or vector_theta.item(i) < theta_0:
                    theta_0 = vector_theta.item(i)
                    int_k = i
        if theta_0 is None:
            print("Целевая функция задачи неограничена снизу на мн-ве допустимых планов")
            break
        if int_k >= 0:
            j_star = index_list_star[int_k]
        print("Step #5 Completed")
        print(f"theta_j_0: \n{theta_j_0}")
        print(f"vector_theta: \n{vector_theta}")
        print(f"theta_0: \n{theta_0}")
        print(f"j_star: \n{j_star}")

        print("Step #6 Start")
        current_plan += theta_0 * vector_l

        if j_star == j_0:
            print("Case #1")
            index_list_star = np.append(index_list_star, j_star)
            index_list_star.sort()
        elif np.isin(j_star, index_list_star) and not np.isin(j_star, index_list):
            print("Case #2")
            index_list_star = np.delete(index_list_star, np.argwhere(index_list_star == j_star)[0][0])
        elif np.isin(j_star, index_list):
            int_s = np.argwhere(index_list == j_star)
            j_plus = -1
            for j in index_list_star:
                if not np.isin(j, index_list):
                    vector = inverse_basic_matrix * np.matrix(matrix_a.transpose().item(j - 1)).transpose()
                    if vector.item(int_s) != 0:
                        j_plus = j
                        break
            if j_plus != -1:
                print("Case #3")
                index_list[int_s] = j_plus
                index_list.sort()
                index_list_star = np.delete(index_list_star, np.argwhere(index_list_star == j_star)[0][0])
            if j_plus == -1 or index_list == index_list_star:
                print("Case #4")
                index_list[int_s] = j_0
                index_list.sort()
                index_list_star[int_s] = j_0
                index_list_star.sort()
        print("Step #6 Completed")
        print(f"current_plan: \n{current_plan}")
        print(f"index_list_star: \n{index_list_star}")
        print(f"index_list: \n{index_list}\n")
    return


def main():

    int_m = 2
    int_n = 4
    matrix_a: np.matrix = np.matrix(
        [[1, 0, 2, 1], [0, 1, -1, 2]]
    )
    matrix_d: np.matrix = np.matrix(
        [[2, 1, 1, 0], [1, 1, 0, 0], [1, 0, 1, 0], [0, 0, 0, 0]]
    )
    vector_c = np.array([-8, -6, -4, -6])
    vector_x = np.array([2, 3, 0, 0], float)
    index_list = np.array([1, 2], int)
    index_list_star = np.array([1, 2], int)

    quadratic_method(int_m, int_n, matrix_a, matrix_d, vector_c, vector_x, index_list, index_list_star)
    return


if __name__ == "__main__":
    main()
