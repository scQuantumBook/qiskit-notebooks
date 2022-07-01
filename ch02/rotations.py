from qiskit.quantum_info import Statevector, DensityMatrix
from qiskit.circuit.library import RYGate, RZGate
from matplotlib.colors import LinearSegmentedColormap, rgb2hex
from kaleidoscope import bloch_sphere
import numpy as np

def svPoint(sv):
    #return [sv.expectation_value(Pauli('X')), sv.expectation_value(Pauli('Y')), sv.expectation_value(Pauli('Z'))]
    m = DensityMatrix(sv).data
    z = np.real(m[0][0])*2.0 - 1
    x = np.real(m[1][0])*2.0
    y = np.imag(m[1][0])*2.0
    return [x,y,z]
    

def show_zyz(start, lbda, theta, phi):        
    #adapted from https://nonhermitian.org/kaleido/tutorials/interactive/bloch_sphere.html
    sv = Statevector.from_label(start)
    dstep = 0.04
    z1steps = max(int(np.abs(lbda) / dstep), 1)
    ysteps = max(int(np.abs(theta) / dstep), 1)
    z2steps = max(int(np.abs(phi) / dstep), 1)
    lbda *= np.pi
    theta *= np.pi
    phi *= np.pi
    cm = LinearSegmentedColormap.from_list('graypurple', ["#999999", "#AA00FF"])
    start_positions = {'0': [0,0,1], '1': [0,0,-1], '+': [1,0,0], '-': [-1,0,0], 'r': [0,1,0], 'l': [0,-1,0]}
    sp = start_positions[start]

    if lbda != 0 or theta != 0 or phi != 0:
        # rotate around z axis 
        pointsz1 = []
        if lbda != 0:
            pointsz1 = [svPoint(sv.evolve(RZGate(lb))) for lb in np.linspace(0, lbda, z1steps+1)]
            sv = sv.evolve(RZGate(lbda))
        # rotate around y axis       
        pointsy = []
        if theta != 0:
            pointsy = [svPoint(sv.evolve(RYGate(th))) for th in np.linspace(0, theta, ysteps+1)]
            sv = sv.evolve(RYGate(theta))
        # rotate around z axis
        pointsz2 = []
        if phi != 0:
            pointsz2 = [svPoint(sv.evolve(RZGate(ph))) for ph in np.linspace(0, phi, z2steps+1)]
            sv = sv.evolve(RZGate(phi))
        points = pointsz1 + pointsy + pointsz2
    else:
        points = [sp]
       
    #print(points)
    points_alpha = [np.linspace(0.8,1, len(points))]
    points_color = [[rgb2hex(cm(kk)) for kk in np.linspace(-1,1,len(points))]]
    vectors_color = ["#777777", "#AA00FF"]
    display(bloch_sphere(points=points, 
                         vectors=[sp, sv],
                         vectors_color=vectors_color, points_alpha=points_alpha, points_color=points_color, 
                         as_widget=True, figsize=(300,300), label_fontsize=12))
    return

def show_yz(theta, phi):
    show_zyz('0', 0, theta, phi)
    return
