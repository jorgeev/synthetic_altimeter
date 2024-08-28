#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 10:32:57 2024

@author: jevz
"""

from lib.mask_functions import parsenames
import numpy as np

path = '/home/jevz/swot_simulator/karin/'
date = np.datetime64("2024-09-01")
targets = parsenames(path, date)
print(targets)



