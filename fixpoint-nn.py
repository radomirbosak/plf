#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from plf import PiecewiseLinearFunction
from division import Division

from numpy import linspace

from matplotlib import pyplot
from math import tanh

POINTS = 101

stddiv = Division(linspace(0, 1, POINTS))

def convolution(fun, aparam):
	newdiv = Division(linspace(-aparam + fun.range_left, fun.range_right + aparam, POINTS)) + fun.division
	values = [fun.quad(x - aparam, x + aparam) / (2*aparam) for x in newdiv]
	values[0], values[-1] = 0, 0
	return PiecewiseLinearFunction(newdiv, values)





ITERATIONS = 4
a = 1/2
b = 1/3

#X = PiecewiseLinearFunction([0, 0.5, 1], [0, 2, 0])
def doforab(a, b, X):
	for it in range(ITERATIONS):
		X = X.compose_after(lambda x: x / b) # values get divided

		X = X.compose_before(lambda x: x * b) # range gets multiplied

		X = convolution(X, a)
		
		X = X.compose_before(lambda x: tanh(x))
		aux_fac = PiecewiseLinearFunction(X.division, (lambda x: 1 / (1 - x*x)))
		X = X * aux_fac
		X = X.rescale(Division(linspace(X.range_left, X.range_right, POINTS)))


		tq = X.quad_total()
		if True: #50 < i < 57:
			X.plot(label="it=%d, q=%.4f" % (it, tq), alpha=0.2)
	tq = X.quad_total()
	X.plot(label="a=%f, b=%f q=%.4f" % (a,b,tq))

X = PiecewiseLinearFunction([0, 0.5, 1], [0, 2, 0])
X.plot(label="orig")

for i, a in enumerate(linspace(0.3, 0.8, 6)):
	for j, b in enumerate(linspace(0.3, 0.8, 6)):
		pyplot.subplot(6, 6, i * 6 + j + 1)
		doforab(a, b, X)
		print(i,j)

#X.plot(label="it=%d, q=%.4f" % (i, tq))

#pyplot.title("quad=%.5f" % tq)

#pyplot.legend()

pyplot.show()