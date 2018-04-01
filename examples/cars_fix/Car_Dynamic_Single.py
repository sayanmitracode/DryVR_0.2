# The differential equations of a single car dynamics

from scipy.integrate import odeint
from scipy.interpolate import interp1d
import numpy as np 

def Car_dynamic(y,t,v_initial,acc,turn_indicator,turn_time,turn_back_time):
    L = 5.0 # the length of the car, make it fix here
    # make everything double
    v_initial = float(v_initial)
    acc = float(acc)
    y = [float(tmp) for tmp in y]
    turn_time = float(turn_time)
    turn_back_time = float(turn_back_time)
    # end of making float

    # set the velocity

    # Speed upper bound = 108km/hr = 30m/s
    # speed lower bound = 0km/hr = 0m/s
    v = v_initial + acc*t
    if v>=30.0:
        v = 30.0
    if v<=0.0:
        v = 0.0
    # set the steering angle
    delta_initial = 0.0
    vel = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7000000000000002, 1.8, 1.9, 2, 2.1, 2.2, 2.3, 2.4000000000000004, 2.5, 2.6, 2.7, 2.8, 2.9000000000000004, 3.0, 3.1, 3.2, 3.3000000000000003, 3.4000000000000004, 3.5, 3.6, 3.7, 3.8000000000000003, 3.9000000000000004, 4.0, 4.1, 4.17, 4.2, 4.300000000000001, 4.4, 4.5, 4.6, 4.7, 4.800000000000001, 4.9, 5.0, 5.1000000000000005, 5.2, 5.3, 5.4, 5.5, 5.6000000000000005, 5.7, 5.800000000000001, 5.9, 6.0, 6.1000000000000005, 6.2, 6.300000000000001, 6.4, 6.5, 6.6000000000000005, 6.7, 6.800000000000001, 6.9, 7.0, 7.1000000000000005, 7.2, 7.300000000000001, 7.4, 8.0, 8.100000000000001, 8.2, 8.3, 8.4, 8.5, 8.600000000000001, 8.7, 8.8, 8.9, 9.0, 9.1, 9.200000000000001, 9.3, 9.4, 9.5, 9.6, 9.700000000000001, 9.8, 9.9, 10.0, 10.1, 10.200000000000001, 10.3, 10.4, 10.5, 10.600000000000001, 10.700000000000001, 10.8, 10.9, 11.0, 11.100000000000001, 11.200000000000001, 11.3, 11.4, 11.5, 11.600000000000001, 11.700000000000001, 11.8, 11.9, 12.0, 12.100000000000001, 12.200000000000001, 12.3, 12.5, 12.600000000000001, 12.700000000000001, 12.8, 12.9, 13.0, 13.100000000000001, 13.200000000000001, 13.3, 13.4, 13.5, 13.600000000000001, 13.700000000000001, 13.8, 13.9, 14.0, 14.100000000000001, 14.200000000000001, 14.3, 14.4, 14.5, 14.600000000000001, 14.700000000000001, 14.8, 14.9, 15.0, 15.100000000000001, 15.200000000000001, 15.3, 15.4, 15.5, 15.600000000000001, 15.700000000000001, 15.8, 15.9, 16.0, 16.1, 16.200000000000003, 16.3, 16.4, 16.5, 16.67, 16.700000000000003, 16.8, 16.9, 17.0, 17.1, 17.2, 17.3, 17.400000000000002, 17.5, 17.6, 17.7, 17.8, 17.900000000000002, 18.0, 18.1, 18.2, 18.3, 18.400000000000002, 18.5, 18.6, 18.7, 18.8, 18.900000000000002, 19.0, 19.1, 19.2, 19.3, 19.400000000000002, 19.5, 19.6, 19.7, 19.8, 20.0, 20.1, 20.200000000000003, 20.3, 20.400000000000002, 20.5, 20.6, 20.700000000000003, 20.8, 20.900000000000002, 21.0, 21.1, 21.200000000000003, 21.3, 21.400000000000002, 21.5, 21.6, 21.700000000000003, 21.8, 21.900000000000002, 22.0, 22.1, 22.200000000000003, 22.3, 22.400000000000002, 22.6, 22.700000000000003, 22.8, 22.900000000000002, 23.1, 23.200000000000003, 23.3, 23.400000000000002, 23.5, 23.6, 23.8, 23.900000000000002, 24.1, 24.200000000000003, 24.3, 24.400000000000002, 24.6, 24.700000000000003, 24.8, 25.0, 25.1, 25.200000000000003, 25.400000000000002, 25.6, 25.8, 25.900000000000002, 26.1, 26.200000000000003, 26.400000000000002, 26.6, 26.8, 27.5, 27.6, 27.8, 28.0, 28.200000000000003, 28.400000000000002, 28.5, 28.8, 29.1, 29.200000000000003, 29.5, 30.0]
    trn = [4.03, 3.3128124999999997, 2.7637158203124996, 2.3152868652343748, 1.9999852561950682, 1.7424889421463012, 1.5252264271676539, 1.351718168677762, 1.196645162652421, 1.0691572586604343, 0.97, 0.8771874999999999, 0.79333984375, 0.725213623046875, 0.6698610687255859, 0.617391459941864, 0.570543594956398, 0.5266237215325236, 0.4903898259578272, 0.45642054885654937, 0.43, 0.3971875, 0.3750390625, 0.35081420898437504, 0.3303744888305664, 0.31312847495079044, 0.2956668858975172, 0.28147934479173276, 0.26610950859379956, 0.2517002871582372, 0.23981267947389825, 0.22742975480271185, 0.22, 0.2159375, 0.2083203125, 0.19832275390624998, 0.19019973754882813, 0.1813998031616211, 0.17314986467361448, 0.16634366542100906, 0.1592538745328784, 0.155, 0.1469375, 0.14206640625, 0.13635809326171877, 0.131095742225647, 0.12721475833654405, 0.12175712474249306, 0.11845980444608725, 0.11382294777926658, 0.10962079642496034, 0.10581259676012031, 0.10236141581385903, 0.09923378308130976, 0.09639936591743697, 0.09297444517775735, 0.08997763953053768, 0.08735543458922046, 0.0850610052655679, 0.08305337960737191, 0.08041837093098969, 0.07756377819824227, 0.07542283364868171, 0.0738171252365113, 0.07140856261825565, 0.07020428130912783, 0.069, 0.058218750000000014, 0.05701757812500001, 0.055328430175781255, 0.05430790328979493, 0.052872787356376655, 0.052005738146603114, 0.050380020878277726, 0.04966876957338537, 0.0483351733767122, 0.047168276704623174, 0.04614724211654528, 0.04525383685197712, 0.04447210724547998, 0.04310408043410999, 0.04207806032558249, 0.04130854524418687, 0.04073140893314015, 0.039865704466570076, 0.039216426116642514, 0.039, 0.037250000000000005, 0.03686718750000001, 0.03612548828125001, 0.03543014526367188, 0.03477826118469239, 0.03416711986064912, 0.03359417486935855, 0.032788470975356185, 0.032301691539396424, 0.03138898009697187, 0.03098966884091113, 0.030615314538354185, 0.029913400221059913, 0.029299225193427425, 0.028761822044248996, 0.028291594288717872, 0.02788014500262814, 0.02752012687729962, 0.026890095157974716, 0.026417571368481038, 0.02606317852636078, 0.02553158926318039, 0.025265794631590198, 0.025, 0.02396875, 0.0236572265625, 0.023355438232421876, 0.023063080787658695, 0.022496638238430025, 0.022231118293479086, 0.021973895846807867, 0.021475527356382376, 0.021241917126495428, 0.021015607216292448, 0.02057713176527417, 0.02037159639760935, 0.019973371622758765, 0.019786703759547553, 0.01942503477457583, 0.019255502437870338, 0.018927033535503443, 0.018619093939534478, 0.018330400568313573, 0.018059750532793975, 0.017806016124494353, 0.017568140116713454, 0.017345131359418862, 0.017136060649455186, 0.01694005685886424, 0.016756303305185224, 0.016584034348611148, 0.016261030055034757, 0.016119715676595085, 0.0158547512170207, 0.015622907314893113, 0.015420043900531474, 0.01524253841296504, 0.01508722111134441, 0.01495131847242636, 0.01471348885431977, 0.014535116640739826, 0.01440133748055487, 0.014200668740277436, 0.014100334370138717, 0.014, 0.013625000000000002, 0.013484375000000002, 0.013361328125000002, 0.013145996093750001, 0.0129844970703125, 0.012863372802734375, 0.012681686401367187, 0.012590843200683594, 0.0125, 0.012325000000000001, 0.0121609375, 0.012007128906250001, 0.011862933349609375, 0.01172775001525879, 0.011601015639305115, 0.011482202161848545, 0.011370814526733011, 0.011266388618812198, 0.011168489330136436, 0.010984928163869381, 0.010904620153627545, 0.010754042634424102, 0.010688164969772596, 0.010564644348551021, 0.010456563804982142, 0.010361993329359375, 0.01019649499701953, 0.010134433122392088, 0.010025824841794066, 0.00994436863134555, 0.009822184315672776, 0.009761092157836389, 0.0097, 0.009475, 0.00936953125, 0.0092673583984375, 0.00916837844848633, 0.009072491621971131, 0.008979601258784532, 0.008889613719447517, 0.008802438290714781, 0.008717987094129943, 0.008636174997438382, 0.008556919528768431, 0.008480140793494418, 0.008405761393697718, 0.008333706350144665, 0.008263903026702643, 0.008196281057118185, 0.008065263491048299, 0.00800384900695304, 0.007944353725485756, 0.007886717671564326, 0.007775047817091556, 0.007722702572807445, 0.007671993117407213, 0.007573743547569262, 0.007481634575846182, 0.007395282414855796, 0.0073143272639273095, 0.0072384318099318525, 0.007167279821811112, 0.007100574832947917, 0.007038038905888673, 0.006979411474270631, 0.0069244482571287165, 0.0068213922249876265, 0.006731218196864173, 0.0066523159222561514, 0.0065832764319741326, 0.006522866877977367, 0.006470008518230196, 0.006377506388672647, 0.006308129791504485, 0.006256097343628364, 0.006178048671814183, 0.0061, 0.0060437500000000005, 0.005991015625, 0.005892138671875, 0.005805621337890625, 0.0057299186706542965, 0.005663678836822509, 0.005605718982219695, 0.005555004109442234, 0.005466253082081676, 0.005399689811561257, 0.005299844905780628, 0.0052, 0.00503125, 0.004939843750000001, 0.004859863281250001, 0.004789880371093751, 0.004728645324707032, 0.004675064659118653, 0.00458129849433899, 0.004510973870754243, 0.004458230403065682, 0.004379115201532841, 0.0043]
    # interp the turn_factor based on vel and trn
    for i in range(len(vel)-1):
        if abs(v_initial) >= vel[i] and abs(v_initial) <= vel[i+1]:
            ub = trn[i]
            lb = trn[i+1]
            break
    turn_factor = lb + (ub-lb) * (abs(v_initial)if abs(v_initial)>=30 or abs(v_initial)<1.0:
            print("Speed limit error")
            exit() - vel[i])
    if turn_indicator == 'Left':
        # print(t)
        if t <= turn_time:
            delta_steer = delta_initial;
        elif (t > turn_time) and (t <= turn_time + 2.0):
            delta_steer = delta_initial + turn_factor
        elif (t > turn_time + 2.0) and (t <= turn_back_time):
            delta_steer = delta_initial 
        elif (t > turn_back_time) and (t <= turn_back_time + 2.0):
            delta_steer = delta_initial - turn_factor
        elif t > turn_back_time + 2.0:
            delta_steer = delta_initial
        else:
            print('Something is wrong with time here when calculting steering angle!')
    elif turn_indicator =='Right':
        if t <= turn_time:
            delta_steer = delta_initial;
        elif (t > turn_time) and (t <= turn_time + 2.0):
            delta_steer = delta_initial + (-turn_factor) 
        elif (t > turn_time + 2.0) and (t <= turn_back_time):
            delta_steer = delta_initial 
        elif (t > turn_back_time) and (t < turn_back_time + 2.0):
            delta_steer = delta_initial + (turn_factor)
        elif t > turn_back_time + 2.0:
            delta_steer = delta_initial
        else:
            print('Something is wrong with time here when calculting steering angle!')
    elif turn_indicator == 'Straight':
        delta_steer = delta_initial
    else:
        print('Wrong turn indicator!')
    psi, sx, py = y
    psi_dot = (v)/L*(np.pi/8.0)*delta_steer
    w_z = psi_dot
    sx_dot = v * np.cos(psi) - L/2.0 * w_z * np.sin(psi) 
    if abs(sx_dot) < 0.0000001:
        sx_dot = 0.0
    sy_dot = v * np.sin(psi) + L/2.0 * w_z * np.cos(psi)
    if abs(sy_dot) < 0.0000001:
        sy_dot = 0.0
    #sx_dot = v * np.cos(psi) 
    #sy_dot = v * np.sin(psi)
    dydt = [psi_dot, sx_dot, sy_dot]
    return dydt


def Car_simulate(Mode,initial,time_bound):
    time_step = 0.05;
    time_bound = float(time_bound)
    initial = [float(tmp)  for tmp in initial]
    number_points = int(np.ceil(time_bound/time_step))
    t = [i*time_step for i in range(0,number_points)]
    if t[-1] != time_step:
        t.append(time_bound)
    newt = []
    for step in t:
        newt.append(float(format(step, '.2f')))
    t = newt
    # initial = [sx,sy,vx,vy]
    # set the parameters according to different modes
    # v_initial,acc,acc_time,turn_indicator,turn_time,turn_back_time

    sx_initial = initial[0]
    sy_initial = initial[1]
    vx_initial = initial[2]
    vy_initial = initial[3]

    v_initial = (vx_initial**2 + vy_initial**2)**0.5
    if abs(v_initial)>=30:
        print("Speed limit error")
        exit()

    # calculate the initial angle
    val = np.arccos(vx_initial/v_initial)
    if vy_initial < 0:
        val = 2*np.pi-val
    psi_initial = val
    acc = 0.0
    turn_time = 0.0
    turn_back_time = 0.0

    # Initialize according to different mode
    if Mode == 'Const':
        turn_indicator = 'Straight'
    elif ((Mode == 'Acc1') or (Mode == 'Acc2')):
        turn_indicator = 'Straight'
        acc = 1.0
    elif (Mode == 'Dec'): 
        turn_indicator = 'Straight'
        acc = -1.0
    elif (Mode == 'Brk'):
        turn_indicator = 'Straight'
        acc = -5.0

    elif Mode =='TurnLeft':
        if abs(v_initial)>=30 or abs(v_initial)<1.0:
            print("Speed limit error")
            exit()
        turn_indicator = 'Left'
        turn_time = 0.0
        turn_back_time = 5.0

    elif Mode == 'TurnRight':
        if abs(v_initial)>=30 or abs(v_initial)<1.0:
            print("Speed limit error")
            exit()
        turn_indicator = 'Right'
        turn_time = 0.0
        turn_back_time = 5.0

    else:
        print('Wrong Mode name!')

    Initial_ode = [psi_initial, sx_initial, sy_initial]
    sol = odeint(Car_dynamic,Initial_ode,t,args=(v_initial,acc,turn_indicator,turn_time,turn_back_time),hmax = time_step)

    # Construct v
    v = np.zeros(len(t))
    # Speed upper bound = 108km/hr = 30m/s
    # speed lower bound = 0km/hr = 0m/s
    for i in range(len(t)):
        fv = v_initial + acc*t[i]
        if fv>=30.0:
            fv = 30.0
        if fv<=0.0:
            fv = 0.0
        v[i] = fv

    # Construct the final output
    trace = []
    for j in range(len(t)):
        current_psi = sol[j,0]
        #print t[j], current_psi
        tmp = []
        tmp.append(t[j])
        tmp.append(sol[j,1])
        tmp.append(sol[j,2])
        

        vx = v[j]*np.cos(current_psi)
        if abs(vx) < 0.0000001:
            vx = 0.0
        tmp.append(vx)
        vy = v[j]*np.sin(current_psi)
        if abs(vy) < 0.0000001:
            vy = 0.0
        tmp.append(vy)
        trace.append(tmp)
    return trace

if __name__ == "__main__":
    print "start test"
    # 16.67*3.6 = 60km/hr
    traj = Car_simulate("TurnLeft", [0.0,0.0,0.0,21.16], "10")
    for line in traj:
        print line
    # # x = [16.67, 4.17, 30.0, 20.0, 25.0, 10.0,8.0,5.0,3.0,27.5,17.5,2,12.5,1]
    # # y = [0.014,0.22,0.0043,0.0097,0.0061,0.039,0.069,0.155,0.43,0.0052,0.0125,0.97,0.025,4.03]
    # speed = 30
    # print 0.143486*np.exp(-0.134119*speed)
    # print np.exp(-45.17)
    


