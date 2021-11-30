import numpy as np
def calc_l(a1, a2):
    a1 = np.array(a1)
    a2 = np.array(a2)
    return np.sqrt(((a1-a2)**2).sum())

def calc_angles(l):
    return np.arccos((l[0]**2 + l[1]**2 - l[2]**2)/(2 * l[0] * l[1]))/np.pi*180.

def slope(a, b):
    sub = np.array(a)-np.array(b)
    return np.abs(sub[1]/sub[0])

def calc_l3(kp):
    l = {}
    l['Leftarmpitangle'] = [calc_l(kp['LEFT_SHOULDER'], kp['LEFT_ELBOW']),
                            calc_l(kp['LEFT_SHOULDER'], kp['LEFT_HIP']),
                            calc_l(kp['LEFT_ELBOW'], kp['LEFT_HIP'])]

    l['Rightarmpitangle'] = [calc_l(kp['RIGHT_SHOULDER'], kp['RIGHT_ELBOW']),
                            calc_l(kp['RIGHT_SHOULDER'], kp['RIGHT_HIP']),
                            calc_l(kp['RIGHT_ELBOW'], kp['RIGHT_HIP'])]

    l['Leftshoulderangle'] = [calc_l(kp['LEFT_SHOULDER'], kp['RIGHT_SHOULDER']),
                            calc_l(kp['LEFT_SHOULDER'], kp['LEFT_HIP']),
                            calc_l(kp['RIGHT_SHOULDER'], kp['LEFT_HIP'])]

    l['Rightshoulderangle'] = [calc_l(kp['RIGHT_SHOULDER'], kp['LEFT_SHOULDER']),
                            calc_l(kp['RIGHT_SHOULDER'], kp['RIGHT_HIP']),
                            calc_l(kp['LEFT_SHOULDER'], kp['RIGHT_HIP'])]

    l['Leftelbowangle'] = [calc_l(kp['LEFT_ELBOW'], kp['LEFT_SHOULDER']),
                        calc_l(kp['LEFT_ELBOW'], kp['LEFT_WRIST']),
                        calc_l(kp['LEFT_SHOULDER'], kp['LEFT_WRIST'])]

    l['Rightelbowangle'] = [calc_l(kp['RIGHT_ELBOW'], kp['RIGHT_SHOULDER']),
                            calc_l(kp['RIGHT_ELBOW'], kp['RIGHT_WRIST']),
                            calc_l(kp['RIGHT_SHOULDER'], kp['RIGHT_WRIST'])]

    l['Lefthipangle'] = [calc_l(kp['LEFT_HIP'], kp['RIGHT_HIP']),
                        calc_l(kp['LEFT_HIP'], kp['LEFT_SHOULDER']),
                        calc_l(kp['RIGHT_HIP'], kp['LEFT_SHOULDER'])]

    l['Righthipangle'] = [calc_l(kp['RIGHT_HIP'], kp['LEFT_HIP']),
                        calc_l(kp['RIGHT_HIP'], kp['RIGHT_SHOULDER']),
                        calc_l(kp['LEFT_HIP'], kp['RIGHT_SHOULDER'])]

    l['Leftgroinangle'] = [calc_l(kp['LEFT_HIP'], kp['LEFT_KNEE']),
                        calc_l(kp['LEFT_HIP'], kp['LEFT_ANKLE']),
                        calc_l(kp['LEFT_KNEE'], kp['LEFT_ANKLE'])]

    l['Rightgroinangle'] = [calc_l(kp['RIGHT_HIP'], kp['RIGHT_KNEE']),
                            calc_l(kp['RIGHT_HIP'], kp['RIGHT_ANKLE']),
                            calc_l(kp['RIGHT_KNEE'], kp['RIGHT_ANKLE'])]
                            
    l['Leftkneeangle'] = [calc_l(kp['LEFT_KNEE'], kp['LEFT_ANKLE']),
                        calc_l(kp['LEFT_KNEE'], kp['LEFT_HIP']),
                        calc_l(kp['LEFT_ANKLE'], kp['LEFT_HIP'])]

    l['Rightkneeangle'] = [calc_l(kp['RIGHT_KNEE'], kp['RIGHT_ANKLE']),
                        calc_l(kp['RIGHT_KNEE'], kp['RIGHT_HIP']),
                        calc_l(kp['RIGHT_ANKLE'], kp['RIGHT_HIP'])]
    return l