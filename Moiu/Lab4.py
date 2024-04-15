import numpy as np
from numpy.linalg import inv


def double_simplex(int_m: int, int_n: int, matrix_a: np.matrix, vector_c: np.array,
                   vector_b: np.array, index_list: np.array):
    while True:
        print("Step #1 Start")
        basic_matrix = np.matrix(np.zeros((int_m, len(index_list))))
        for i in range(int_m):
            for j in range(len(index_list)):
                basic_matrix.itemset((i, j), matrix_a.item(i, index_list[j] - 1))
        inverse_basic_matrix = inv(basic_matrix)
        print("Step #1 Completed")
        print(f"basic_matrix: \n{basic_matrix}")
        print(f"inverse_basic_matrix: \n{inverse_basic_matrix}")

        print("Step #2 Start")
        basic_c = np.array([[vector_c.item(j - 1)] for j in index_list])
        print("Step #2 Completed")
        print(f"basic_c: \n{basic_c}")

        print("Step #3 Start")
        current_y = basic_c.transpose() * inverse_basic_matrix
        print("Step #3 Completed")
        print(f"current_y: \n{current_y}")

        print("Step #4,6 Start")
        vector_kappa = np.zeros(int_n)
        int_j: int = 0
        int_k: int = 0
        pseudo_vector = inverse_basic_matrix * np.matrix(vector_b).transpose()
        is_positive = True
        print(f"pseudo_vector: \n{pseudo_vector}")
        for i in index_list:
            vector_kappa[i - 1] = pseudo_vector[int_j]
            if pseudo_vector[int_j] < 0:
                is_positive = False
                int_k = np.argwhere(index_list == i)[0][0] + 1
            int_j += 1
        print("Step #4,6 Completed")
        print(f"vector_kappa: \n{vector_kappa}")
        print(f"int_k: \n{int_k}")  

        print("Step #5 Start")
        if is_positive:
            print("Optimal plan: \n", vector_kappa)
            break
        print("Step #5 Completed")

        anti_index_list = np.array([i for i in range(1, int_n + 1) if not np.isin(i, index_list)], int)

        print("Step #7 Start")
        delta_y = inverse_basic_matrix[int_k - 1]
        print(f"delta_y: \n{delta_y}")
        vector_mu = np.zeros(int_n)
        all_positive = False
        for j in range(1, int_n + 1):
            if np.isin(j, anti_index_list):
                print(f"столбец: \n{np.matrix(matrix_a.transpose()[j - 1]).transpose()}")
                vector_mu[j - 1] = delta_y * np.matrix(matrix_a.transpose()[j - 1]).transpose()
                if vector_mu[j - 1] < 0:
                    all_positive = False
        print("Step #7 Completed")
        print(f"vector_mu: \n{vector_mu}")

        print("Step #8 Start")
        if all_positive:
            print("Прямая задача несовместна\n")
            break
        print("Step #8 Completed")

        print("Step #9 Start")
        vector_sigma = np.zeros(int_n)
        print(f"current_y: \n{current_y}")
        for j in range(1, int_n + 1):
            if np.isin(j, anti_index_list) and vector_mu[j - 1] < 0:
                vector_sigma[j - 1] = ((vector_c[j - 1] - np.matrix(matrix_a.transpose()[j - 1]) * current_y.transpose()) /
                                       vector_mu[j - 1])
        print("Step #9 Completed")
        print(f"vector_sigma: \n{vector_sigma}")

        print("Step #10 Start")
        sigma_min = vector_sigma[anti_index_list[0] - 1]
        j_0 = anti_index_list[0]
        print(f"anti_index_list: {anti_index_list}")
        for j in range(1, int_n + 1):
            if (np.isin(j, anti_index_list) and
                    sigma_min > vector_sigma[anti_index_list[np.argwhere(anti_index_list == j)[0][0]] - 1]):
                sigma_min = vector_sigma[anti_index_list[np.argwhere(anti_index_list == j)[0][0]] - 1]
                j_0 = j
        print("Step #10 Completed")
        print(f"sigma_min: {sigma_min}")
        print(f"j_0: {j_0}")

        print("Step #11 Start")
        index_list[int_k - 1] = j_0
        print("Step #11 Completed")
        print(f"int_k: {int_k}")
        print(f"index_list: \n{index_list}")
    return


def main():

    int_m = 2
    int_n = 5
    matrix_a: np.matrix = np.matrix(
        [[-2, -1, -4, 1, 0], [-2, -2, -2, 0, 1]]
    )
    vector_c = np.array([-4, -3, -7, 0, 0])
    vector_b = np.array([-1, -1.5])
    index_list = np.array([4, 5], int)

    double_simplex(int_m, int_n, matrix_a, vector_c, vector_b, index_list)

    return


if __name__ == "__main__":
    main()
