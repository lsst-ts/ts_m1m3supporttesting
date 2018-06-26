from CalculateDistributionForces import *

def CalculateBalanceForces(Kp, Ki, Kd, N, Ts, f, e1, e2, u1, u2):
    hpForces = [
        [-0.537951127,0.537978215,0.741535212,0.20357124,-0.203584528,-0.741551772    ],
        [-0.545664289,-0.545670097,-0.193046605,0.738738926,0.738711639,-0.193071931  ],
        [-0.642541103,-0.64251349,-0.642540689,-0.642513462,-0.642540625,-0.642513968 ],
        [1.470682833,1.470578579,-1.849344073,0.37915142,0.3790854,-1.849313855       ],
        [1.287305428,-1.285880066,0.630953013,1.917461965,-1.916093256,-0.629419761   ],
        [-2.32450824,2.323383964,-2.323832733,2.324757698,-2.322991346,2.323506302    ]
    ]
    fx = f[0] * hpForces[0][0] + f[1] * hpForces[0][1] + f[2] * hpForces[0][2] + f[3] * hpForces[0][3] + f[4] * hpForces[0][4] + f[5] * hpForces[0][5]
    fy = f[0] * hpForces[1][0] + f[1] * hpForces[1][1] + f[2] * hpForces[1][2] + f[3] * hpForces[1][3] + f[4] * hpForces[1][4] + f[5] * hpForces[1][5]
    fz = f[0] * hpForces[2][0] + f[1] * hpForces[2][1] + f[2] * hpForces[2][2] + f[3] * hpForces[2][3] + f[4] * hpForces[2][4] + f[5] * hpForces[2][5]
    mx = f[0] * hpForces[3][0] + f[1] * hpForces[3][1] + f[2] * hpForces[3][2] + f[3] * hpForces[3][3] + f[4] * hpForces[3][4] + f[5] * hpForces[3][5]
    my = f[0] * hpForces[4][0] + f[1] * hpForces[4][1] + f[2] * hpForces[4][2] + f[3] * hpForces[4][3] + f[4] * hpForces[4][4] + f[5] * hpForces[4][5]
    mz = f[0] * hpForces[5][0] + f[1] * hpForces[5][1] + f[2] * hpForces[5][2] + f[3] * hpForces[5][3] + f[4] * hpForces[5][4] + f[5] * hpForces[5][5]
    e = [-fx, -fy, -fz, -mx, -my, -mz]
    us = []
    for i in range(6):
        A = Kp[i] + Kd[i] * N[i]
        B = -2.0 * Kp[i] + Kp[i] * N[i] * Ts[i] + Ki[i] * Ts[i] - 2.0 * Kd[i] * N[i]
        C = Kp[i] - Kp[i] * N[i] * Ts[i] - Ki[i] * Ts[i] + Ki[i] * N[i] * Ts[i] * Ts[i] + Kd[i] * N[i]
        D = 2.0 - N[i] * Ts[i]
        E = N[i] * Ts[i] - 1.0
        u = D[i] * u1[i] + E[i] * u2[i] + A[i] * e[i] + B[i] * e1[i] + C[i] * e2[i]
        us.append(u)
    
    return CalculateDistributionForces(us[0], us[1], us[2], us[3], us[4], us[5])