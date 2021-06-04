import json
import os
import stat
from subprocess import PIPE, Popen
import sys
from types import ModuleType
from mfg_setup import mfg_setup



class RobotCalibrator():
    def __init__(self):
        pass

    def set_model(self, model: str):
        if model not in mfg_setup.get_models():
            raise ValueError(
                "Invalid robot model %s. Cannot calibrate model %s" % (model, model))
        self.model = model

        raise ValueError('this function is not yet implemented')

    def run_calibration(self, model):
        raise ValueError('this function is not yet implemented')

    def get_calibration_file(self):
        raise ValueError('this function is not yet implemented')