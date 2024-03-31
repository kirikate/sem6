import numpy as np
from numpy.linalg import inv
from Lab2 import main_phase


def correction_func(vector: np.array, matrix: np.matrix):
    print(f"b: ", vector)
    print(f"Length of b: ", len(vector))
    for i in range(len(vector)):
        if vector[i] < 0:
            vector[i] *= -1
            matrix[i] *= -1
    return


def start_phase(int_n: int, int_m: int, matrix_a: np.matrix, vector_b: np.array):
    print("Step #1 Start")
    correction_func(vector_b, matrix_a)
    print("Step #1 Completed")
    print("matrix_a = \n", matrix_a)
    print("vector_b = \n", vector_b)

    print("Step #2 Start")
    vector_c_wave = np.array(np.zeros((1, int_n)))[0]
    vector_c_wave = np.append(vector_c_wave, np.full((1, int_m), -1))

    matrix_a_wave = np.matrix(np.concatenate((matrix_a, np.identity(int_m)), axis=1))
    print("Step #2 Completed")
    print("matrix_a_wave = \n", matrix_a_wave)
    print("vector_c_wave = \n", vector_c_wave)

    print("Step #3 Start")
    current_plan_wave = np.array(np.zeros((1, int_n)))[0]
    current_plan_wave = np.append(current_plan_wave, vector_b)
    index_list = np.arange(int_n + 1, int_n + int_m + 1)
    print("Step #3 Completed")
    print("current_plan_wave = \n", current_plan_wave)
    print("index_list = \n", index_list)

    print("Step #4 Start")
    main_phase(
        int_n, int_m, matrix_a_wave, vector_c_wave, current_plan_wave, index_list
    )
    print("Step #4 Completed")
    print("current_plan_wave = \n", current_plan_wave)
    print("index_list = \n", index_list)

    print("Step #5 Start")
    for i in range(int_n, int_n + int_m):
        if current_plan_wave[i] != 0:
            print("Задача несовместна")
            return
    print("Step #5 Completed")

    print("Step #6 Start")
    current_plan = np.split(current_plan_wave, [int_n, int_m])[0]
    print("Step #6 Completed")
    print("current_plan = \n", current_plan)

    while True:
        print("Step #7-8 Start")
        max_index = -1
        int_k = -1
        for i in range(0, len(index_list)):
            if index_list[i] > int_n and index_list[i] > max_index:
                max_index = index_list[i]
                int_k = i + 1

        if max_index == -1:
            print("Искомый план:", current_plan)
            return
        print("Step #7-8 Completed")
        print("max_index = \n", max_index)
        print("int_k = \n", int_k)

        print("Step #9-10 Start")
        basic_matrix = np.matrix(np.zeros((int_m, len(index_list))))
        for i in range(int_m):
            for j in range(len(index_list)):
                basic_matrix.itemset((i, j), matrix_a_wave.item(i, index_list[j] - 1))
        inverse_basic_matrix = inv(basic_matrix)

        all_zeros = True
        for j in range(1, int_n + 1):
            print("is j in B = \n", np.isin(index_list, j)[0])
            if not np.isin(index_list, j)[0]:
                vector_l = (
                    inverse_basic_matrix * matrix_a_wave.transpose()[j - 1].transpose()
                )
                print("j = \n", j)
                print("vector_l = \n", vector_l)
                if vector_l[int_k - 1] != 0:
                    index_list[int_k - 1] = j
                    print("j = \n", j)
                    all_zeros = False
                    break
        print("Step #9-10 Completed")

        print("Step #11 Start")
        print("all_zeros = \n", all_zeros)
        print("max_index = \n", max_index)
        if all_zeros:
            matrix_a = np.matrix(np.delete(matrix_a, max_index - int_n - 1, 0))
            vector_b = np.delete(vector_b, max_index - int_n - 1)
            index_list = np.delete(index_list, int_k - 1)
            matrix_a_wave = np.matrix(
                np.delete(matrix_a_wave, max_index - int_n - 1, 0)
            )
        print("Step #11 Completed")
        print("matrix_a_wave = \n", matrix_a_wave)
        print("matrix_a = \n", matrix_a)
        print("vector_b = \n", vector_b)
        print("index_list = \n", index_list)
    return


def main():

    int_m = 2
    int_n = 3

    matrix_a: np.matrix = np.matrix([[1, 1, 1], [2, 2, 2]])
    vector_b = np.array([-1, 0])

    start_phase(int_n, int_m, matrix_a, vector_b)
    return


if __name__ == "__main__":
    main()
