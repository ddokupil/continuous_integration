# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import sys
import pytest
import logging
import numpy as np


class test_gpu_model_jetson:
    """
    test_gpu_model_jetson
    Args:
    Returns:
    """
    def __init__(self, model_name):
        """
        __init__
        Args:
            model_name: name of test model
        Returns:
            name(str): e.g. resnet50
        """
        logging.info("test model is:" + model_name)
        self.model_name = model_name

    def test_comb_model_path(self, path):
        """
        find combine model path
        Args:
            path: model save class path
        Returns:
            model_path: model save path
            params_path: paramse save path
        """
        project_path = os.environ.get("project_path")
        path = os.path.join(project_path, "Data", path, self.model_name)
        model_path = os.path.join(path, "model.pdmodel")
        params_path = os.path.join(path, "model.pdiparams")
        return model_path, params_path

    def test_uncomb_model_path(self, path):
        """
        find uncombine model path
        Args:
            path: model save class path
        Returns:
            model_path: model save path
        """
        project_path = os.environ.get("project_path")
        model_path = os.path.join(project_path, "Data", path, self.model_name)
        return model_path

    def npy_result_path(self, path):
        """
        load numpy result path
        Args:
            path: npy result save name
        Returns:
            npy result: npy result save path
        """
        project_path = os.environ.get("project_path")
        npy_result = os.path.join(
            project_path, "Data", path, self.model_name, self.model_name) + ".npy"
        npy_result = np.load(npy_result)
        return npy_result

    def test_readdata(self, path, data_name):
        """
        check model path
        Args:
            path: data save name
            data_name: data name
        Returns:
            data_path: data path
        """
        project_path = os.environ.get("project_path")
        data_path = os.path.join(project_path, "Data", path, data_name)
        return data_path

    def test_diff(self, without_lr_data, with_lr_data, diff_standard):
        """
        get native and analysis infer results
        Args:
            without_lr_data(numpy array): switch_ir_optim is False
            with_lr_data(numpy array): switch_ir_optim is True
            diff_standard: e.g 1e-6
        Returns:
            None
            """
        assert np.array(without_lr_data).shape == pytest.approx(np.array(with_lr_data).shape), \
            "output shape:" + str(np.array(without_lr_data).shape) + " and " + \
            str(np.array(with_lr_data).shape) + "not equal"
        max_diff = np.max(np.abs(without_lr_data - with_lr_data))
        assert max_diff < diff_standard or max_diff == diff_standard, \
            self.model_name + " output data diff is:" + str(max_diff)
        logging.info(self.model_name + 'gpu_test down')
