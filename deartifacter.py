import numpy as np


def deartifacter(arr1, arr2):
    coord_l = np.copy(arr1)
    coord_r = np.copy(arr2)

    for i in range(3, len(coord_l)):

        cur_dist_l = np.linalg.norm(coord_l[i-1] - coord_l[i])
        cur_dist_l_swapped = np.linalg.norm(coord_l[i-1] - coord_r[i])

        cur_dist_r = np.linalg.norm(coord_r[i-1] - coord_r[i])
        cur_dist_r_swapped = np.linalg.norm(coord_r[i-1] - coord_l[i])

        if cur_dist_l_swapped < cur_dist_l and cur_dist_r_swapped < cur_dist_r:
            # мы поменяли - всем лучше
            t = np.copy(coord_l[i])
            coord_l[i] = coord_r[i]
            coord_r[i] = t
        elif cur_dist_l_swapped > cur_dist_l and cur_dist_r_swapped > cur_dist_r:
            # мы оставили - всем лучше

            pass
        elif cur_dist_l < cur_dist_r_swapped:
            # если левой ближе до левой, чем правой до левой
            # тоже не трогаем
            pass
        elif cur_dist_l_swapped < cur_dist_r:
            t = np.copy(coord_l[i])
            coord_l[i] = coord_r[i]
            coord_r[i] = t

    return coord_l, coord_r
