from dataclasses import dataclass
import numpy as np
import keypoints
from scipy import ndimage
from math import trunc


@dataclass
class BodyAngles:
    """Содержит в себе результаты вычислений углов """
    time: np.ndarray = None
    """Номера кадров 32212 """

    left_ankle: np.ndarray = None
    """ Угол в левой ладышке """
    right_ankle: np.ndarray = None
    """ Угол в правой ладышке """
    left_knee: np.ndarray = None
    """ Угол в левом колене """
    right_knee: np.ndarray = None
    """ Угол в правом колене """
    left_hip: np.ndarray = None
    """ Угол в связке левым плечо - левое бедро - левое колено """
    right_hip: np.ndarray = None
    """ Угол в правом бедре"""

    between_legs: np.ndarray = None
    """ Угол между левой и правой ногами """
    body_lean: np.ndarray = None
    """ Угол наклона туловища """


def calculate_angles(data) -> BodyAngles:
    ret = BodyAngles()

    ret.time = data[keypoints.LEFT_KNEE].xvalues

    ret.left_ankle = calc_tpoints(
        data[keypoints.LEFT_FOOT_INDEX].yvalues,
        data[keypoints.LEFT_ANKLE].yvalues,
        data[keypoints.LEFT_KNEE].yvalues
    )

    ret.right_ankle = calc_tpoints(
        data[keypoints.RIGHT_FOOT_INDEX].yvalues,
        data[keypoints.RIGHT_ANKLE].yvalues,
        data[keypoints.RIGHT_KNEE].yvalues
    )
    
    ret.left_knee = calc_tpoints(
        data[keypoints.LEFT_ANKLE].yvalues,
        data[keypoints.LEFT_KNEE].yvalues,
        data[keypoints.LEFT_HIP].yvalues
    )
    
    ret.right_knee = calc_tpoints(
        data[keypoints.RIGHT_ANKLE].yvalues,
        data[keypoints.RIGHT_KNEE].yvalues,
        data[keypoints.RIGHT_HIP].yvalues
    )
    
    ret.left_hip = calc_tpoints(
        data[keypoints.LEFT_SHOULDER].yvalues,
        data[keypoints.LEFT_HIP].yvalues,
        data[keypoints.LEFT_KNEE].yvalues
    )
    
    ret.right_hip = calc_tpoints(
        data[keypoints.RIGHT_SHOULDER].yvalues,
        data[keypoints.RIGHT_HIP].yvalues,
        data[keypoints.RIGHT_KNEE].yvalues
    )
    
    ret.between_legs = calc_fpoints(
        data[keypoints.RIGHT_HIP].yvalues,
        data[keypoints.RIGHT_KNEE].yvalues,
        data[keypoints.LEFT_HIP].yvalues,
        data[keypoints.LEFT_KNEE].yvalues
    )
    
    ret.body_lean = calc_fpoints(
        data[keypoints.RIGHT_HIP].yvalues,
        data[keypoints.RIGHT_SHOULDER].yvalues,
        np.tile(np.array([0,0]),(ret.time.shape[0],1)),
        np.tile(np.array([1,0]),(ret.time.shape[0],1))
    )
    
    return ret


def calc_fpoints(
        point1: np.ndarray,
        point2: np.ndarray,
        point3: np.ndarray,
        point4: np.ndarray):
    """Считает угол в радианах по 4 точкам, 1-2 вектор, 3-4 вектор"""
    
    vec1 = point2 - point1
    vec2 = point4 - point3
    cos = np.sum(vec1*vec2, axis=1) / np.linalg.norm(vec1, axis=1) / np.linalg.norm(vec2, axis=1) 
    
    return np.arccos(cos) *180 / 3.1415926


def calc_tpoints(
        point1: np.ndarray,
        point2: np.ndarray,
        point3: np.ndarray):
    
    angle = calc_fpoints(
        point1,
        point2,
        point3,
        point2)
    
    return angle

    
def mov_ave_median(a, n=3, m=3):
    if (n % 2 == 0):
        n += 1
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    ans = ret[n - 1:] / n

    for i in range(trunc(n/2)):
        ans = np.append(a[i], ans)

    for i in range(len(ans) - trunc(n/2) + 1, len(ans) + 1):
        ans = np.append(ans, a[i])
    ans = ndimage.median_filter(ans, m)
    return ans
