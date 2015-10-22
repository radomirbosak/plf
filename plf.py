#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Piecewise Linear Functions
"""
# inpackage dependencies
from division import Division

# other dependencies
from matplotlib import pyplot
import operator
from numbers import Number

#testing deps
from numpy import linspace



class PiecewiseLinearFunction:

	def __init__(self, division, values):
		# takes Division or a list
		self.division = division if isinstance(division, Division) else Division(division)
		self.range_left = self.division[0]
		self.range_right = self.division[-1]
		# takes R -> R function or a list
		self.values = [values(x) for x in self.division] if callable(values) else values

	def __call__(self, x):
		if x < self.division[0]:
			return self.values[0]

		for left, right, lval, rval in zip(self.division[:-1], self.division[1:], self.values[:-1], self.values[1:]):
			if left <= x < right:
				return lval + (x - left) * (rval - lval) / (right - left)
		else:
			return self.values[-1]

	def __add__(self, f2):
		return self._apply_pointwise_binop(f2, operator.add)
	

	def __sub__(self, f2):
		return self._apply_pointwise_binop(f2, operator.sub)

	def __mul__(self, f2):
		return self._apply_pointwise_binop(f2, operator.mul)

	def __truediv__(self, f2):
		return self._apply_pointwise_binop(f2, operator.truediv)

	def __radd__(self, f2):
		return self.__add__(f2)
	def __rmul__(self, f2):
		return self.__mul__(f2)


	def _apply_pointwise_binop(self, f2, binop):
		if isinstance(f2, Number):
			f2 = PiecewiseLinearFunction([0],[f2])
		if self.division == f2.division:
			newvalues = [binop(x, y) for x, y in zip(self.values, f2.values)]
			return PiecewiseLinearFunction(self.division, newvalues)
		else:
			newdiv = self.division + f2.division
			newvalues = [binop(self(x), f2(x)) for x in newdiv]
			return PiecewiseLinearFunction(newdiv, newvalues)

	def compose_after(self, f2):
		return PiecewiseLinearFunction(self.division, [f2(y) for y in self.values])

	def compose_before(self, finv):
		return PiecewiseLinearFunction([finv(x) for x in self.division], self.values)

	def quad(self, a, b):
		return self.rescale(self.division.restrict(a, b)).quad_total()

	def quad_total(self):
		tsum = 0
		for left, right, lval, rval in zip(self.division[:-1], self.division[1:], self.values[:-1], self.values[1:]):
			tsum += (lval + rval) / 2 * (right - left)
		return tsum

	def rescale(self, newdiv):
		newvalues = [self(x) for x in newdiv]
		return PiecewiseLinearFunction(newdiv, newvalues)

	def plot(self, show=False, *args, **kwargs):
		pyplot.plot(self.division.points, self.values, *args, **kwargs)
		if show:
			pyplot.show()