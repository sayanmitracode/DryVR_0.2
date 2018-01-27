"""
This file contains guard class for DryVR
"""

import random
import sympy

from src.common.utils import handleReplace
from z3 import *

class Guard():
	def __init__(self, variables):
		self.varDic = {'t':Real('t')}
		self.variables = variables
		for var in variables:
			self.varDic[var] = Real(var)

	def _buildGuard(self, guardStr):
		# Build solver for current guard based on guard string
		curSolver = Solver()
		# This magic line here is because sympy will evaluate == to be False
		# Therefore we are not be able to get free symbols from it
		# Thus we need to replace "==" to something else
		sympyGuardStr = guardStr.replace("==",">=")

		symbols = list(sympy.sympify(sympyGuardStr, evaluate=False).free_symbols)
		symbols = [str(s) for s in symbols]
		symbolsIdx = {s:self.variables.index(s)+1 for s in symbols if s in self.variables}
		if 't' in symbols:
			symbolsIdx['t'] = 0


		guardStr = handleReplace(guardStr,self.varDic.keys())
		curSolver.add(eval(guardStr))
		return curSolver, symbolsIdx

	def guardSimuTube(self, tube, guardStr):
		if not guardStr:
			return None, tube
		curSolver, symbols = self._buildGuard(guardStr)
		guardSet = {}
		# Implement new guard Algorithm for the simulation tube
		for idx in range(len(tube)-1):
			lower = tube[idx]
			upper = tube[idx+1]
			curSolver.push()
			for symbol in symbols:
				curSolver.add(self.varDic[symbol] >= min(lower[symbols[symbol]], upper[symbols[symbol]]))
				curSolver.add(self.varDic[symbol] <= max(upper[symbols[symbol]], upper[symbols[symbol]]))
			# curSolver.add(self.varDic['t'] >= lower[0])
			# curSolver.add(self.varDic['t'] <= upper[0])
			# for i in range(1, len(lower)):
			# 	if self.variables[i-1] in symbols:
			# 		curSolver.add(self.varDic[self.variables[i-1]]>=min(lower[i],upper[i]))
			# 		curSolver.add(self.varDic[self.variables[i-1]]<=max(upper[i],lower[i]))
			if curSolver.check() == sat:
				curSolver.pop()
				guardSet[idx] = upper
			else:
				curSolver.pop()
				if guardSet:
					# Guard set is not empty, randomly pick one and return
					idx, point = random.choice(list(guardSet.items()))
					# Return the initial point for next mode, and truncked tube
					return point[1:], tube[:idx+1]

		# for idx,t in enumerate(tube):
		# 	curSolver.push()
		# 	curSolver.add(self.varDic['t'] == t[0])
		# 	for i in range(1, len(t)):
		# 		curSolver.add(self.varDic[self.variables[i-1]]==t[i])
		# 	if curSolver.check() == sat:
		# 		# The simulation trace hits the guard
		# 		curSolver.pop()
		# 		guardSet[idx] = t
		# 	else:
		# 		curSolver.pop()
		# 		if guardSet:
		# 			# Guard set is not empty, randomly pick one and return
		# 			idx, point = random.choice(list(guardSet.items()))
		# 			# Return the initial point for next mode, and truncked tube
		# 			return point[1:], tube[:idx+1]

		# No guard hits for current tube
		return None, tube

	def guardSimuTraceTime(self, tube, guardStr):
		if not guardStr:
			return None, tube
		curSolver, symbols = self._buildGuard(guardStr)
		guardSet = {}
		# Implement new guard Algorithm for the simulation tube
		for idx in range(len(tube)-1):
			lower = tube[idx]
			upper = tube[idx+1]
			curSolver.push()
			for symbol in symbols:
				curSolver.add(self.varDic[symbol] >= min(lower[symbols[symbol]], upper[symbols[symbol]]))
				curSolver.add(self.varDic[symbol] <= max(upper[symbols[symbol]], upper[symbols[symbol]]))
			# curSolver.add(self.varDic['t'] >= lower[0])
			# curSolver.add(self.varDic['t'] <= upper[0])
			# for i in range(1, len(lower)):
			# 	if self.variables[i-1] in symbols:
			# 		curSolver.add(self.varDic[self.variables[i-1]]>=min(lower[i],upper[i]))
			# 		curSolver.add(self.varDic[self.variables[i-1]]<=max(upper[i],lower[i]))
			if curSolver.check() == sat:
				curSolver.pop()
				guardSet[idx] = upper
			else:
				curSolver.pop()
				if guardSet:
					# Find max idx
					idx = max(guardSet.keys())
					# Return idx
					return idx+1
		return len(tube)



	def guardReachTube(self, tube, guardStr):
		if not guardStr:
			return None, tube

		curSolver, symbols = self._buildGuard(guardStr)
		guardSetLower = []
		guardSetUpper = []
		for i in range(0,len(tube),2):
			curSolver.push()
			lowerBound = tube[i]
			upperBound = tube[i+1]
			for symbol in symbols:
				curSolver.add(self.varDic[symbol] >= lowerBound[symbols[symbol]])
				curSolver.add(self.varDic[symbol] <= upperBound[symbols[symbol]])
			# curSolver.add(self.varDic['t'] >= lowerBound[0])
			# curSolver.add(self.varDic['t'] <= upperBound[0])
			# for j in range(1,len(lowerBound)):
			# 	if self.variables[j-1] in symbols:
			# 		curSolver.add(self.varDic[self.variables[j-1]]>=lowerBound[j])
			# 		curSolver.add(self.varDic[self.variables[j-1]]<=upperBound[j])

			if curSolver.check() == sat:
				# The reachtube hits the guard
				curSolver.pop()
				guardSetLower.append(lowerBound)
				guardSetUpper.append(upperBound)
			else:
				curSolver.pop()
				if guardSetLower:
					# Guard set is not empty, build the next initial set and return
					# At some point we might futher reduce the initial set for next mode
					initLower = guardSetLower[0][1:]
					initUpper = guardSetUpper[0][1:]
					for j in range(1,len(guardSetLower)):
						for k in range(1,len(guardSetLower[0])):
							initLower[k-1] = min(initLower[k-1], guardSetLower[j][k])
							initUpper[k-1] = max(initUpper[k-1], guardSetUpper[j][k])
					# Return next initial Set, the result tube, and the true transit time
					return [initLower,initUpper], tube[:i], guardSetLower[0][0]

		# Construct the guard if all later trace sat the guard condition
		if guardSetLower:
			# Guard set is not empty, build the next initial set and return
			# At some point we might futher reduce the initial set for next mode
			initLower = guardSetLower[0][1:]
			initUpper = guardSetUpper[0][1:]
			for j in range(1,len(guardSetLower)):
				for k in range(1,len(guardSetLower[0])):
					initLower[k-1] = min(initLower[k-1], guardSetLower[j][k])
					initUpper[k-1] = max(initUpper[k-1], guardSetUpper[j][k])
			# Return next initial Set, the result tube, and the true transit time
			return [initLower,initUpper], tube[:i], guardSetLower[0][0]

		return None, tube, tube[-1][0]
