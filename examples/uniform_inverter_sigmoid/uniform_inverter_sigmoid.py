from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import math

def uniform_inverter_sigmoid(y,t,mode):
    v, stim = y
    v = float(v)
    stim = float(stim)
    if mode == "Inverter_Rampup":
        v_dot = 0.018688194*(-(0.172331258975586*math.pow(0.226308333333333*math.log(134617599.12781*math.exp(-25.6410256410256*stim) + 1) + 1, 0.5) - 0.172331258975586)*(-math.log(math.exp(-10*(-v + 1.2)/(0.344662517951173*math.pow(0.226308333333333*math.log(134617599.12781*math.exp(-25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1) + 0.039*math.log(134617599.12781*math.exp(-25.6410256410256*stim) + 1))*(0.344662517951173*math.pow(0.226308333333333*math.log(134617599.12781*math.exp(-25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(-v + 1.2)/(0.344662517951173*math.pow(0.226308333333333*math.log(134617599.12781*math.exp(-25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/((1.74083333333333e-5*(0.344662517951173*math.pow(0.226308333333333*math.log(134617599.12781*math.exp(-25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(-v + 1.2)/(0.344662517951173*math.pow(0.226308333333333*math.log(134617599.12781*math.exp(-25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(-v - 0.344662517951173*math.pow(0.226308333333333*math.log(134617599.12781*math.exp(-25.6410256410256*stim) + 1) + 1, 0.5) + 2.54466251795117) + 6.0e-6) + 1)*(-6.0e-6*math.log(-v - 0.344662517951173*math.pow(0.226308333333333*math.log(134617599.12781*math.exp(-25.6410256410256*stim) + 1) + 1, 0.5) + 2.54466251795117) + 6.0e-6)) - 0.04722975*(-(0.0686008289266829*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.0686008289266829)*(-math.log(math.exp(-10*v/(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1) + 0.039*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1))*(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366)*(-math.log(math.exp(-10*v/(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1)/((4.373125e-5*(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366)*(-math.log(math.exp(-10*v/(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(v - 0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) + 1.13720165785337) + 6.0e-6) + 1)*(-6.0e-6*math.log(v - 0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) + 1.13720165785337) + 6.0e-6))
        stim_dot = stim*(-5*stim + 6) + 0.005
    elif mode == "Inverter_Rampdown":
        v_dot = 0.018688194*(-(0.172331258975586*math.pow(0.226308333333333*math.log(134617599.12781*math.exp(-25.6410256410256*stim) + 1) + 1, 0.5) - 0.172331258975586)*(-math.log(math.exp(-10*(-v + 1.2)/(0.344662517951173*math.pow(0.226308333333333*math.log(134617599.12781*math.exp(-25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1) + 0.039*math.log(134617599.12781*math.exp(-25.6410256410256*stim) + 1))*(0.344662517951173*math.pow(0.226308333333333*math.log(134617599.12781*math.exp(-25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(-v + 1.2)/(0.344662517951173*math.pow(0.226308333333333*math.log(134617599.12781*math.exp(-25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/((1.74083333333333e-5*(0.344662517951173*math.pow(0.226308333333333*math.log(134617599.12781*math.exp(-25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173)*(-math.log(math.exp(-10*(-v + 1.2)/(0.344662517951173*math.pow(0.226308333333333*math.log(134617599.12781*math.exp(-25.6410256410256*stim) + 1) + 1, 0.5) - 0.344662517951173) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(-v - 0.344662517951173*math.pow(0.226308333333333*math.log(134617599.12781*math.exp(-25.6410256410256*stim) + 1) + 1, 0.5) + 2.54466251795117) + 6.0e-6) + 1)*(-6.0e-6*math.log(-v - 0.344662517951173*math.pow(0.226308333333333*math.log(134617599.12781*math.exp(-25.6410256410256*stim) + 1) + 1, 0.5) + 2.54466251795117) + 6.0e-6)) - 0.04722975*(-(0.0686008289266829*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.0686008289266829)*(-math.log(math.exp(-10*v/(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1) + 0.039*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1))*(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366)*(-math.log(math.exp(-10*v/(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1)/((4.373125e-5*(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366)*(-math.log(math.exp(-10*v/(0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) - 0.137201657853366) + 10) + 1)/10 + 1)/(-6.0e-6*math.log(v - 0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) + 1.13720165785337) + 6.0e-6) + 1)*(-6.0e-6*math.log(v - 0.137201657853366*math.pow(0.56850625*math.log(3.51315750985655e-5*math.exp(25.6410256410256*stim) + 1) + 1, 0.5) + 1.13720165785337) + 6.0e-6))
        stim_dot = -stim*(-5*stim + 6.01) - 0.005
    
    dydt = [v_dot,stim_dot]
    return dydt

def TC_Simulate(Mode,initialCondition,time_bound):
    time_step = 0.05;
    time_bound = float(time_bound)

    number_points = int(np.ceil(time_bound/time_step))
    t = [i*time_step for i in range(0,number_points)]
    if t[-1] != time_step:
        t.append(time_bound)
    newt = []
    for step in t:
        newt.append(float(format(step, '.2f')))
    t = newt

    sol = odeint(uniform_inverter_sigmoid, initialCondition, t, args=(Mode,),hmax=time_step)

    # Construct the final output
    trace = []
    for j in range(len(t)):
        #print t[j], current_psi
        tmp = []
        tmp.append(t[j])
        tmp.append(float(sol[j,0]))
        tmp.append(float(sol[j,1]))
        trace.append(tmp)
    return trace

if __name__ == "__main__":

    sol = TC_Simulate("Inverter_Rampup", [1.2,0.0], 6.4)
    #for s in sol:
	#	print(s)
    time = [row[0] for row in sol]

    v = [row[1] for row in sol]

    stim_local = [row[2] for row in sol]

    plt.plot(v,stim_local,"-r")
    plt.show()