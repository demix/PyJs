#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil

def rm(target):
    """
    
    Arguments:
    - `target`:
    """
    if os.path.exists(target):
        if os.path.isfile(target):
            os.remove(target)
        elif os.path.isdir(target):
            shutil.rmtree(target)

    return True

