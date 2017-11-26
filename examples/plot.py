# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 12:22:54 2017

@author: CXY
"""
import xlrd
import numpy as np
import matplotlib.pyplot as plt

from graph_lib.plot.plot import scatter2d, plot2d, polyfit2d

# ----------------------scatter2d+polyfit2d-----------------------------
book = xlrd.open_workbook('example_data/xy.xls')
sheet = book.sheets()[0]
# get columns
x, y = sheet.col_values(ord('A') - ord('A')), sheet.col_values(ord('B') - ord('A'))
# get information from columns
x_label, y_label = x.pop(0), y.pop(0)
scatter2d(x, y)
polyfit2d(x, y, 1, label='male',
          xlabel=x_label, ylabel=y_label, title='test')

# ----------------------plot2d-----------------------------
x = range(10)
y = np.random.rand(10)
x_label = 'Here is x!'
y_label = 'Here is y!'
plt.figure()
plot2d(x, y, xlabel=x_label, ylabel=y_label, ls='--', marker='*', c='r', grid=True)

plt.show()
