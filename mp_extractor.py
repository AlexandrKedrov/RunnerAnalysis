import json
import numpy as np
from discrete_data import DiscreteData
import keypoints


class MpExtractor:
    array = ([11, keypoints.LEFT_SHOULDER], [12, keypoints.RIGHT_SHOULDER], [23, keypoints.LEFT_HIP], [24, keypoints.RIGHT_HIP],
             [27, keypoints.LEFT_ANKLE], [28, keypoints.RIGHT_ANKLE], [25, keypoints.LEFT_KNEE], [26, keypoints.RIGHT_KNEE],
             [31, keypoints.LEFT_FOOT_INDEX], [32, keypoints.RIGHT_FOOT_INDEX])
    

    def __init__(self, ind):
        self.id = self.array[ind][0]
        self.name = self.array[ind][1]
        self.points = []
        self.frames = []
        self.dd = {}

    def decoder(self, data):
        for i in range(len(data)):
            self.frames.append(data[i]['frame'])
            self.points.append([data[i]['points'][self.id]['x'],
                                data[i]['points'][self.id]['y']])

        self.dd = {self.name: {'frames': self.frames, 'points': self.points}}


def discrete_data_from_mp_json(data):
    discrete_data = dict()

    for index, (_, key) in enumerate(MpExtractor.array):
        k = MpExtractor(index)
        k.decoder(data)
        discrete_data[key] = DiscreteData(np.array(k.dd[key]['frames']), np.array(k.dd[key]['points'])) 

    return discrete_data

if __name__ == '__main__':

    with open('D:/RunnerAnalysis/data/1.json') as f:
        data = json.loads(f.read())

    discrete_data = {}
    for index, (_, key) in enumerate(MpExtractor.array):
        k = MpExtractor(index)
        k.decoder(data)
        discrete_data = {**discrete_data, **k.dd}

    with open('D:/RunnerAnalysis/data/newOut.json', 'w') as g:
        json.dump(discrete_data, g, indent=4)
