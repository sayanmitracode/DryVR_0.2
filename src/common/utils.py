"""
This file contains common utils for DryVR
"""

import importlib
import random

from collections import namedtuple


# This is the tuple for input file parsed by DryVR
DryVRInput = namedtuple(
    'DryVRInput',
    'vertex edge guards variables initialSet unsafeSet timeHorizon path resets initialMode deterministic bloatingMethod kvalue'
)

# This is the tuple for rtt input file parsed by DryVR
RrtInput = namedtuple(
    'RttInput',
    'modes initialMode variables initialSet unsafeSet goalSet timeHorizon minTimeThres path goal bloatingMethod kvalue'
)

def importSimFunction(path):
    """
    Load simulation function from given file path
    Note the folder in the examples directory must have __init__.py
    And the simulation function must be named TC_Simulate
    The function should looks like following:
        TC_Simulate(Mode, initialCondition, time_bound)
    
    Args:
        path (str): Similator directory.

    Returns:
        simulation function

    """
    path = path.replace('/', '.')
    try:
        module = importlib.import_module(path)
    except:
        print("Import simulation function failed!")
    
    return module.TC_Simulate

def randomPoint(lower, upper):
    """
    Pick a random point between lower and upper bound
    This function supports both int or list
    
    Args:
        lower (list or int or float): lowerbound.
        upper (list or int or float): upperbound.

    Returns:
        random point (either float or list of float)

    """
    if isinstance(lower, int) or isinstance(lower, float):
        return random.uniform(lower, upper)

    if isinstance(lower, list):
        assert len(lower) == len(upper), "Random Point List Range Error"

        return [random.uniform(lower[i], upper[i]) for i in range(len(lower))]

def calcDelta(lower, upper):
    """
    Calculate the delta value between the lower and upper bound
    The function only supports list since we assue initial set is always list
    
    Args:
        lower (list): lowerbound.
        upper (list): upperbound.

    Returns:
        delta (list of float)

    """
    # Convert list into float in case they are int
    lower = [float(val) for val in lower]
    upper = [float(val) for val in upper]

    assert len(lower) == len(upper), "Delta calc List Range Error"
    return [(upper[i]-lower[i])/2 for i in range(len(upper))]

def calcCenterPoint(lower, upper):
    """
    Calculate the center point between the lower and upper bound
    The function only supports list since we assue initial set is always list
    
    Args:
        lower (list): lowerbound.
        upper (list): upperbound.

    Returns:
        delta (list of float)

    """

    # Convert list into float in case they are int
    lower = [float(val) for val in lower]
    upper = [float(val) for val in upper]
    assert len(lower) == len(upper), "Center Point List Range Error"
    return [(upper[i]+lower[i])/2 for i in range(len(upper))]

def buildModeStr(g, vertex):
    """
    Build a unique string to represent a mode
    This should be something like "modeName,modeNum"
    
    Args:
        g (obj): Graph object.
        vertex (int): vetex number.

    Returns:
        a string to represent a mode

    """
    return g.vs[vertex]['label']+','+str(vertex)

def handleReplace(inputStr, keys):
    """
    Replace variable in inputStr to self.varDic["variable"]
    For example:
        input
            And(y<=0,t>=0.2,v>=-0.1)
        output: 
            And(self.varDic["y"]<=0,self.varDic["t"]>=0.2,self.varDic["v"]>=-0.1)
    
    Args:
        inputStr (str): original string need to be replaced
        keys (list): list of variable strings

    Returns:
        a string that all variables have been replaced into a desire form

    """
    idxes = []
    i = 0
    original = inputStr

    keys.sort(key=lambda s:len(s))
    for key in keys[::-1]:
        for i in range(len(inputStr)):
            if inputStr[i:].startswith(key):
                idxes.append((i, i+len(key)))
                inputStr = inputStr[:i] + "@"*len(key) + inputStr[i+len(key):]

    idxes = sorted(idxes)

    inputStr = original
    for idx in idxes[::-1]:
        key = inputStr[idx[0]:idx[1]]
        target = 'self.varDic["'+key+'"]'
        inputStr = inputStr[:idx[0]] + target + inputStr[idx[1]:]
    return inputStr

def neg(orig):
    """
    Neg the original condition
    For example:
        input
            And(y<=0,t>=0.2,v>=-0.1)
        output: 
            Not(And(y<=0,t>=0.2,v>=-0.1))
    
    Args:
        orig (str): original string need to be neg

    Returns:
        a neg condition string

    """
    return 'Not('+orig+')'

def trimTraces(traces):
    """
    trim all traces to the same length
    
    Args:
        traces (list): list of traces generated by simulator
    Returns:
        traces (list) after trim to the same length

    """

    ret_traces = []
    trace_lengths = []
    for trace in traces:
        trace_lengths.append(len(trace))
    trace_len = min(trace_lengths)


    for trace in traces:
        ret_traces.append(trace[:trace_len])

    return ret_traces

def checkVerificationInput(data):
    """
    Check verification input to make sure it is valid
    
    Args:
        data (obj): json data object
    Returns:
        None

    """
    assert len(data['variables']) == len(data['initialSet'][0]), "Initial set dimension mismatch"

    assert len(data['variables']) == len(data['initialSet'][1]), "Initial set dimension mismatch"

    assert len(data['edge']) == len(data["guards"]), "guard number mismatch"

    assert len(data['edge']) == len(data["resets"]), "reset number mismatch"

    if data["bloatingMethod"] == "PW":
        assert 'kvalue' in data, "kvalue need to be provided when bloating method set to PW"

    for i in range(len(data['variables'])):
        assert data['initialSet'][0][i] <= data['initialSet'][1][i], "initial set lowerbound is larger than upperbound"


def checkSynthesisInput(data):
    """
    Check Synthesis input to make sure it is valid
    
    Args:
        data (obj): json data object
    Returns:
        None

    """
    assert len(data['variables']) == len(data['initialSet'][0]), "Initial set dimension mismatch"

    assert len(data['variables']) == len(data['initialSet'][1]), "Initial set dimension mismatch"

    for i in range(len(data['variables'])):
        assert data['initialSet'][0][i] <= data['initialSet'][1][i], "initial set lowerbound is larger than upperbound"

    assert data["minTimeThres"] < data["timeHorizon"], "min time threshold is too large!"

    if data["bloatingMethod"] == "PW":
        assert 'kvalue' in data, "kvalue need to be provided when bloating method set to PW"

def isIpynb():
    """
    Check if the code is running on Ipython notebook
    """
    try:
        cfg = get_ipython().config 
        if "IPKernelApp" in cfg:
            return True
        else:
            return False
    except NameError:
        return False

def overloadConfig(configObj, userConfig):
    """
    Overload user config to config module
    
    Args:
        configObj (module): config module
        userConfig (dict): user specified config
    """

    if "SIMUTESTNUM" in userConfig:
        configObj.SIMUTESTNUM = userConfig["SIMUTESTNUM"]

    if "SIMTRACENUM" in userConfig:
        configObj.SIMTRACENUM = userConfig["SIMTRACENUM"]

    if "REFINETHRES" in userConfig:
        configObj.REFINETHRES = userConfig["REFINETHRES"]

    if "CHILDREFINETHRES" in userConfig:
        configObj.CHILDREFINETHRES = userConfig["CHILDREFINETHRES"]

    if "RANDMODENUM" in userConfig:
        configObj.RANDMODENUM = userConfig["RANDMODENUM"]

    if "RANDSECTIONNUM" in userConfig:
        configObj.RANDSECTIONNUM = userConfig["RANDSECTIONNUM"]



