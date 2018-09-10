#!/usr/bin/env python
#
# Test ODE integration
#
"""
Author: Maurik Holtrop @ UNH
==============================================================
   The Double Pendumum
==============================================================
This code will integrate the equations for the double pendulum.
The output is an animated pendumum and graphs of the phase diagrams.
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
from IPython.display import HTML
#
# This function defines a time step t, for a double pendulum.
#
# Setup the constants for the problem.
#
#
# This function defines a time step t, for a double pendulum.
#
def double_pendulum_step(invars,t,params):
    theta1,omega1,theta2,omega2 = invars  # Unpack (rename) the input for ease of use.
    l1,m1,l2,m2,g = params                # Upack the parameters for ease of use.

    out = np.zeros_like(invars)
    out[0] = omega1
    out[2] = omega2

    cdt = np.cos(theta1-theta2) # Cosine diff theta
    sdt = np.sin(theta1-theta2) # Sine diff theta
    if l1 > 0. and m1>0.:       # If this is not true, then frac1 can be zero!
        frac1 = l1*(m1 + m2 - m2*cdt**2)
        d_omega1 = ( -g*(m1+m2)*np.sin(theta1) +
                    g*m2*cdt*np.sin(theta2)-
                    l1*m2*omega1*omega1*cdt*sdt -    # np.sin(theta1) -
                    l2*m2*omega2*omega2*sdt )/frac1
    else:
        d_omega1 = 0*omega1

    if l2 > 0. and m1>0.:      # If this is not true, then frac1 can be zero!
        frac2 = l2*(m1+m2- m2*cdt*cdt)
        d_omega2 =((m1+m2)*(g*cdt*np.sin(theta1)-g*np.sin(theta2)+l1*omega1*omega1*sdt) +
                    l2*m2*omega2*omega2*cdt*sdt )/frac2
    else:
        d_omega2 = 0*omega2

    out[1] = d_omega1
    out[3] = d_omega2
    return(out)


G = 9.8  # acceleration due to gravity, in m/s^2
L1 = 1.0  # length of pendulum 1 in m
M1 = 1.1  # mass of pendulum 1 in kg
L2 = 0.47  # length of pendulum 2 in m
M2 = 0.5  # mass of pendulum 2 in kg
parameters = (L1,M1,L2,M2,G)
# th1 and th2 are the initial angles (degrees)
# w10 and w20 are the initial angular velocities (degrees per second)
theta1_0 = 80.0
omega1_0 = 0.0
theta2_0 = -25.0
omega2_0 = 0.0

# Define the Initial State of the problem.
state = np.radians([theta1_0,omega1_0,theta2_0,omega2_0])

# create a time array from 0..60 seconds, sampled at dt second steps
# Making the step size too small increases computational time, but makes the solution more accurate.
Max_time = 60
dt = 0.05
t = np.arange(0.0, Max_time, dt)

#
# For clarity of coding, define the indexes.
#
i_theta1 = 0
i_omega1 = 1
i_theta2 = 2
i_omega2 = 3

# We integrate the ODE using scipy.integrate. This does the computational heavy lifting for us.
result_t = integrate.odeint(double_pendulum_step, state, t,args=(parameters,))
#
#
# The result_t is now an array of arrays.
# The first index are the time steps, the second are the variable index.
# Convert the polar coordinates back to cartesian (x,y)
x1 = L1*np.sin(result_t[:, i_theta1])
y1 = -L1*np.cos(result_t[:,i_theta1])

x2 = L2*np.sin(result_t[:, i_theta2]) + x1
y2 = -L2*np.cos(result_t[:,i_theta2]) + y1

fig1,(ax1,ax2,ax3) = plt.subplots(3,sharex=False,figsize=(8,12))
plt.tight_layout()
#ax1.set_title('Double Pendulum')
ax1.set_xlabel('time (sec)')
ax1.set_ylabel("$\\theta$(deg)")
ax1.plot(t,result_t[:,i_theta1]*180./np.pi,label="$\\theta_1$")
ax1.plot(t,result_t[:,i_theta2]*180./np.pi,label="$\\theta_2$")
ax1.legend(loc="lower right")

ax2.set_xlabel('time (sec)')
ax2.set_ylabel("$\omega$(deg/s)")
ax2.plot(t,result_t[:,i_omega1]*180./np.pi,label="$\\omega_1$")
ax2.plot(t,result_t[:,i_omega2]*180./np.pi,label="$\\omega_2$")
ax2.legend(loc="lower right")

ax3.plot(result_t[:,i_theta1]*180./np.pi,result_t[:,i_omega1]*180./np.pi,label="$rod_1$")
ax3.plot(result_t[:,i_theta2]*180./np.pi,result_t[:,i_omega2]*180./np.pi,label="$rod_2$")
ax3.set_xlabel("$\\theta$(deg)")
ax3.set_ylabel("$\omega$(deg/s)")
ax3.legend(loc="lower right")
plt.show()

fig2 = plt.figure(figsize=(9,7))
plt.tight_layout()
ax = fig2.add_subplot(111, autoscale_on=False, xlim=(-(L1+L2), (L1+L2)), ylim=(-(L1+L2)*1.05, (L2)))
ax.grid()

line, = ax.plot([], [], 'o-', lw=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)


def init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text


def animate(i):
    thisx = [0, x1[i], x2[i]]
    thisy = [0, y1[i], y2[i]]

    line.set_data(thisx, thisy)
    time_text.set_text(time_template % (i*dt))
    return line, time_text

ani = animation.FuncAnimation(fig2, animate, np.arange(1, len(result_t)),
                              interval=100, blit=True, init_func=init)
plt.show()
