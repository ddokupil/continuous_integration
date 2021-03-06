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
import argparse
import logging
import struct
import six

import pytest
import nose
import numpy as np

sys.path.append("../..")
from src.test_case import Predictor

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


class TestModelInferenceTrtFp32(object):
    """
    TestModelInferenceTrtFp32
    Args:
    Returns:
    """

    def __init__(self,
                 data_path="Data/python-model-infer",
                 trt_dynamic_shape_info=None):
        """__init__
        """
        project_path = os.environ.get("project_path")
        self.model_root = os.path.join(project_path, data_path)
        self.trt_dynamic_shape_info = trt_dynamic_shape_info

    def check_data(self, result, expect, delta):
        """
        check result
        Args:
            result(list): list of result data
            expect(list): list of expect data
            delta(float): e.g. 0.001
        Returns:
            None
        """
        logger.info("current comparison delta is : {0}".format(delta))
        assert len(result) == pytest.approx(len(
            expect)), "output length not equal"
        for i in range(0, len(expect)):
            assert result[i] == pytest.approx(
                expect[i], rel=None, abs=delta), "output data not equal"

    def get_infer_results(self, model_path, data_path, min_subgraph_size=3):
        """
        get native and analysis infer results
        trt_fp32
        Args:
            model_path(string): parent path of __model__ file
            data_path(string): path of data.json
            min_subgraph_size(int): tensorrt subgraph size
        Returns:
            res(numpy array): analysis cf outputs
            exp(numpy array): native cfg outputs
        """
        AnalysisPredictor = Predictor(
            model_path,
            predictor_mode="Analysis",
            config_type="trt_fp32",
            min_subgraph_size=min_subgraph_size,
            trt_dynamic_shape_info=self.trt_dynamic_shape_info)

        res, ave_time = AnalysisPredictor.analysis_predict(
            data_path, repeats=10)
        logger.info(ave_time)

        NoIrPredictor = Predictor(
            model_path, predictor_mode="Analysis", config_type="gpu_no_ir")
        exp, ave_time = NoIrPredictor.analysis_predict(data_path)
        logger.info(ave_time)

        assert len(res) == pytest.approx(len(
            exp)), "num of output tensor not equal"

        return res, exp
