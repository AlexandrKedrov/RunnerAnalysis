from dataclasses import dataclass
import numpy as np

@dataclass
class DiscreteData:
    xvalues: np.array
    yvalues: np.array

    def __iter__(self):
        return zip(self.xvalues, self.yvalues)

        