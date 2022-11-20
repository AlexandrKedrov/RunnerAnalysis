from deartifacter import deartifacter
import keypoints
from mp_extractor import discrete_data_from_mp_json
import matplotlib.pyplot as plt
import numpy as np
import json
import angle_calculator
from scipy import signal



if __name__ == '__main__':

    path = 'D:/RunnerAnalysis/data/1.json'
    # TODO

    with open(path, 'r') as read_file:
        data = discrete_data_from_mp_json((json.loads(read_file.read())))

    pair_keys = [(keypoints.LEFT_FOOT_INDEX, keypoints.RIGHT_FOOT_INDEX),  # 0
                 (keypoints.LEFT_ANKLE, keypoints.RIGHT_ANKLE),            # 1
                 (keypoints.LEFT_KNEE, keypoints.RIGHT_KNEE),              # 2
                 (keypoints.LEFT_HIP, keypoints.RIGHT_HIP),                # 3
                 (keypoints.LEFT_SHOULDER, keypoints.RIGHT_SHOULDER)]      # 4
    
    q1 = 5 #Параметры для сглаживаний
    q2 = 5
    p1 = 7
    p2 = 5
    
    '''
    left_key, right_key = pair_keys[1]

    plt.figure()
    plt.plot(data[right_key].xvalues,
            data[left_key].yvalues[:, 1], label='Old y left')
    plt.plot(data[right_key].xvalues,
            data[right_key].yvalues[:, 1], label='Old y right')
    plt.legend(loc = 3)

    plt.figure()
    plt.plot(data[right_key].xvalues,
            data[left_key].yvalues[:, 0], label='Old x left')
    plt.plot(data[right_key].xvalues,
            data[right_key].yvalues[:, 0], label='Old x right')
    plt.legend(loc = 3)

    coord_l, coord_r = deartifacter(
        data[left_key].yvalues, data[right_key].yvalues)

    plt.figure()
    plt.plot(data[right_key].xvalues,
            coord_l[:, 1], label='New y left')
    plt.plot(data[right_key].xvalues,
            coord_r[:, 1], label='New y right')
    plt.legend(loc = 3)

    plt.figure()
    plt.plot(data[right_key].xvalues,
            coord_l[:, 0], label='New x left')
    plt.plot(data[right_key].xvalues,
            coord_r[:, 0], label='New x right')
    plt.legend(loc = 3)
    '''
    
    for k in range(len(pair_keys)): # Уничтожение смены ног из data
        left_key, right_key = pair_keys[k]
        coord_l, coord_r = deartifacter(
            data[left_key].yvalues, data[right_key].yvalues)

        data[left_key].yvalues = coord_l
        data[right_key].yvalues = coord_r

    bodyangles = angle_calculator.calculate_angles(data)

    ''' Графики углов 1 видоса до сглаживания
    plt.figure()
    plt.plot(bodyangles.time, bodyangles.between_legs, label='between_legs')
    plt.plot(bodyangles.time, bodyangles.body_lean, label='body_lean')
    plt.plot(bodyangles.time, bodyangles.left_ankle, label='left_ankle')
    plt.plot(bodyangles.time, bodyangles.right_ankle, label='right_ankle')
    plt.legend(loc = 3)

    plt.figure()
    plt.plot(bodyangles.time, bodyangles.left_knee, label='left_knee')
    plt.plot(bodyangles.time, bodyangles.right_knee, label='right_knee')
    plt.plot(bodyangles.time, bodyangles.left_hip, label='left_hip')
    plt.plot(bodyangles.time, bodyangles.right_hip, label='right_hip')
    plt.legend(loc = 3)
    '''
    
    bodyangles.between_legs = angle_calculator.mov_ave_median(bodyangles.between_legs, q1, q2)
    bodyangles.body_lean = angle_calculator.mov_ave_median(bodyangles.body_lean, q1, q2)
    bodyangles.left_ankle = angle_calculator.mov_ave_median(bodyangles.left_ankle, q1, q2)
    bodyangles.right_ankle = angle_calculator.mov_ave_median(bodyangles.right_ankle, q1, q2)
    
    bodyangles.left_knee = angle_calculator.mov_ave_median(bodyangles.left_knee, 5, 5)
    bodyangles.right_knee = angle_calculator.mov_ave_median(bodyangles.right_knee, 5, 5)
    bodyangles.left_hip = angle_calculator.mov_ave_median(bodyangles.left_hip, 5, 5)
    bodyangles.right_hip = angle_calculator.mov_ave_median(bodyangles.right_hip, 5, 5)

    if True:
        plt.figure()
        plt.plot(bodyangles.time, bodyangles.between_legs, label='new between_legs')
        plt.plot(bodyangles.time, bodyangles.body_lean, label='new body_lean')
        plt.plot(bodyangles.time, bodyangles.left_ankle, label='new left_ankle')
        plt.plot(bodyangles.time, bodyangles.right_ankle, label='new right_ankle')
        plt.legend(loc = 3)

        plt.figure()
        plt.plot(bodyangles.time, bodyangles.left_knee, label='new left_knee')
        plt.plot(bodyangles.time, bodyangles.right_knee, label='new right_knee')
        plt.plot(bodyangles.time, bodyangles.left_hip, label='new left_hip')
        plt.plot(bodyangles.time, bodyangles.right_hip, label='new right_hip')
        plt.legend(loc = 3)

    path = 'D:/RunnerAnalysis/data/2.json'
    # TODO

    with open(path, 'r') as read_file:
        data2 = discrete_data_from_mp_json((json.loads(read_file.read())))
    
    for k in range(len(pair_keys)):
        left_key, right_key = pair_keys[k]
        coord_l, coord_r = deartifacter(
            data2[left_key].yvalues, data2[right_key].yvalues)

        data2[left_key].yvalues = coord_l
        data2[right_key].yvalues = coord_r

    bodyangles2 = angle_calculator.calculate_angles(data2)

    ''' Графики углов 2 видоса до сглаживания
    plt.figure()
    plt.plot(bodyangles2.time, bodyangles2.between_legs, label='2between_legs')
    plt.plot(bodyangles2.time, bodyangles2.body_lean, label='body_lean')
    plt.plot(bodyangles2.time, bodyangles2.left_ankle, label='left_ankle')
    plt.plot(bodyangles2.time, bodyangles2.right_ankle, label='right_ankle')
    plt.legend(loc = 3)

    plt.figure()
    plt.plot(bodyangles2.time, bodyangles2.left_knee, label='2left_knee')
    plt.plot(bodyangles2.time, bodyangles2.right_knee, label='right_knee')
    plt.plot(bodyangles2.time, bodyangles2.left_hip, label='left_hip')
    plt.plot(bodyangles2.time, bodyangles2.right_hip, label='right_hip')
    plt.legend(loc = 3)
    '''
    
    bodyangles2.between_legs = angle_calculator.mov_ave_median(bodyangles2.between_legs, p1, p2)
    bodyangles2.body_lean = angle_calculator.mov_ave_median(bodyangles2.body_lean, p1, p2)
    bodyangles2.left_ankle = angle_calculator.mov_ave_median(bodyangles2.left_ankle, p1, p2)
    bodyangles2.right_ankle = angle_calculator.mov_ave_median(bodyangles2.right_ankle, p1, p2)
    
    bodyangles2.left_knee = angle_calculator.mov_ave_median(bodyangles2.left_knee, p1, p2)
    bodyangles2.right_knee = angle_calculator.mov_ave_median(bodyangles2.right_knee, p1, p2)
    bodyangles2.left_hip = angle_calculator.mov_ave_median(bodyangles2.left_hip, p1, p2)
    bodyangles2.right_hip = angle_calculator.mov_ave_median(bodyangles2.right_hip, p1, p2)

    if True:
        plt.figure()
        plt.plot(bodyangles2.time, bodyangles2.between_legs, label='2new between_legs')
        plt.plot(bodyangles2.time, bodyangles2.body_lean, label='new body_lean')
        plt.plot(bodyangles2.time, bodyangles2.left_ankle, label='new left_ankle')
        plt.plot(bodyangles2.time, bodyangles2.right_ankle, label='new right_ankle')
        plt.legend(loc = 3)

        plt.figure()
        plt.plot(bodyangles2.time, bodyangles2.left_knee, label='2new left_knee')
        plt.plot(bodyangles2.time, bodyangles2.right_knee, label='new right_knee')
        plt.plot(bodyangles2.time, bodyangles2.left_hip, label='new left_hip')
        plt.plot(bodyangles2.time, bodyangles2.right_hip, label='new right_hip')
        plt.legend(loc = 3)
    
    if False:
        corr = signal.correlate(bodyangles.between_legs, bodyangles2.between_legs, mode='same')
        if len(bodyangles.time) < len(bodyangles2.time):
            ordinata = bodyangles.time
        else:
            ordinata = bodyangles2.time
            
        plt.figure()
        plt.plot(ordinata, corr, label='Corr between_legs')
        plt.legend(loc = 3)
    
    # addtime = 0
    
    # plt.figure()
    # plt.plot(bodyangles.time, bodyangles.between_legs, label='1new+ between_legs')
    # plt.plot(bodyangles2.time + addtime, bodyangles2.between_legs, label='2new+ between_legs')
    # plt.legend(loc = 3)
    
    plt.show()
