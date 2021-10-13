#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


def generate(n_repeat=32,
             ):
    """
    Generate exp data.
    Returns the DataFrame contains the stimulus

    Parameters
    ----------
    n_repeat : int
        number of trials per condition
    Returns
    -------
    df : DataFrame
    """
    condition = ['Gain', 'Loss']
    pic = ['box_%s.png' % i for i in range(8)]
    np.random.shuffle(pic)
    df_gain = pd.DataFrame()
    df_loss = pd.DataFrame()
    df_gain['p_cond'] = [0.75]*n_repeat+[0.6]*n_repeat
    is_left = np.random.randint(0, 2, 2)
    df_gain['p_left'] = [0.75*is_left[0]+0.25*(1-is_left[0])]*n_repeat + [0.6*is_left[1]+0.4*(1-is_left[1])]*n_repeat
    df_gain['pic_left'] = np.repeat(pic[0:2], n_repeat)
    df_gain['pic_right'] = np.repeat(pic[2:4], n_repeat)
    df_gain['condition'] = 'Gain'

    df_loss['p_cond'] = [0.75]*n_repeat+[0.6]*n_repeat
    is_left = np.random.randint(0, 2, 2)
    df_loss['p_left'] = [0.75*is_left[0]+0.25*(1-is_left[0])]*n_repeat + [0.6*is_left[1]+0.4*(1-is_left[1])]*n_repeat
    df_loss['pic_left'] = np.repeat(pic[4:6], n_repeat)
    df_loss['pic_right'] = np.repeat(pic[6:], n_repeat)
    df_loss['condition'] = 'Loss'
    df = [df_gain, df_loss]
    np.random.shuffle(df)
    df = pd.concat(df)
    df.index = range(len(df))
    df['block'] = np.repeat([1, 2, 3, 4], n_repeat)
    return df


def generate_train(n=12,
             ):
    """
    Generate exp data.
    Returns the DataFrame contains the stimulus

    Parameters
    ----------
    n : int
        number of trials in train
    Returns
    -------
    df : DataFrame
    """
    pic = ['box_train%s.png' % i for i in range(2)]
    np.random.shuffle(pic)
    df = pd.DataFrame()
    df['p_cond'] = [0.5]*n
    df['p_left'] = [0.5]*n
    df['pic_left'] = np.repeat([pic[0]], n)
    df['pic_right'] = np.repeat([pic[1]], n)
    df['condition'] = 'Gain'
    return df
