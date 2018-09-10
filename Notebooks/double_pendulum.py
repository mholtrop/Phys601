#!/usr/bin/env python
#
# Double Pendulum problem solved with numeric integration.
#
# This is the pure Python version, which runs the animation much faster,
# since it start showing frames while computing the next one.
#
# To run this, just type "python double_pendulum.py"
#
# To get the Notebook version, with complete documentation, go here:
# https://github.com/mholtrop/Phys601/blob/master/Notebooks/Double_Pendulum.ipynb
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

#
# Setup the constants for the problem.
#
save_output = False  # Set to True to save the output to file.
G = 9.8  # acceleration due to gravity, in m/s^2
L1 = 1.0  # length of pendulum 1 in m
M1 = 1.1  # mass of pendulum 1 in kg
L2 = 0.47  # length of pendulum 2 in m
M2 = 0.5  # mass of pendulum 2 in kg
parameters = (L1,M1,L2,M2,G)
# theta1_0 and theta2_0 are the initial angles (degrees)
# omega1_0 and omega2_0 are the initial angular velocities (degrees per second)
theta1_0 = 80.0
omega1_0 = 0.0
theta2_0 = -25.0
omega2_0 = 0.0

# Define the Initial State of the problem.
state = np.radians([theta1_0,omega1_0,theta2_0,omega2_0])

# create a time array from 0..60 seconds, sampled at dt second steps
# Making the step size too small increases computational time, but makes the solution more accurate.
Max_time = 60
dt = 0.01
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
#
x1 = L1*np.sin(result_t[:, i_theta1])
y1 = -L1*np.cos(result_t[:,i_theta1])

x2 = L2*np.sin(result_t[:, i_theta2]) + x1
y2 = -L2*np.cos(result_t[:,i_theta2]) + y1
#
#  Now make a graph.
#  The first two show the behavior of theta 1 and 2 vs time, and the same for omega.
#  The third plot (on the same page) shows the omega vs theta phase diagram.
#
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
if save_output:
    plt.savefig("double_pendulum.pdf")
else:
    plt.show()

#
# Here we setup the animation.
#
fig2 = plt.figure(figsize=(9,7))
plt.tight_layout()
ax = fig2.add_subplot(111, autoscale_on=False, xlim=(-(L1+L2), (L1+L2)), ylim=(-(L1+L2)*1.05, (L2)))
ax.grid()

max_trace_depth=250
line1, = ax.plot([], [], 'o-', lw=2,color="blue") # A line without the parameters set.
trace1, = ax.plot([],[], lw=1,color="blue")
line2, = ax.plot([], [], 'o-', lw=2,color="red") # A line without the parameters set.
trace2, = ax.plot([],[], lw=1,color="red")
time_template = 'time = %.1fs'      # To print the time on the plot
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)


def init():                   # initialize everything
    line1.set_data([], [])
    line2.set_data([], [])
    trace1.set_data([],[])
    trace2.set_data([],[])
    time_text.set_text('')
    return line1,line2,trace1,trace2, time_text


def animate(i):               # Do animation step i.
    thisx1 = [0, x1[i]]
    thisy1 = [0, y1[i]]
    thisx2 = [x1[i], x2[i]]
    thisy2 = [y1[i], y2[i]]
    line1.set_data(thisx1, thisy1)
    line2.set_data(thisx2, thisy2)
    if i < max_trace_depth:
        trace1.set_data(x1[0:i],y1[0:i])
        trace2.set_data(x2[0:i],y2[0:i])
    else:
        trace1.set_data(x1[i-max_trace_depth:i],y1[i-max_trace_depth:i])
        trace2.set_data(x2[i-max_trace_depth:i],y2[i-max_trace_depth:i])

    time_text.set_text(time_template % (i*dt))
    return line1,line2,trace1,trace2, time_text


#
#  Now run the animation.
#
#
# For more on how to animate your results, see:
# https://matplotlib.org/api/animation_api.html
# and
# https://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial
#
ani = animation.FuncAnimation(fig2, animate, np.arange(1, len(result_t)),
                              interval=2, blit=True, init_func=init)
# Note: interval is the delay between frames in ms, IF your computer can keep up.
# So a larger number slows down the animation, a smaller number speeds it up.
# To get "real time" you would want this to be dt*1000.
#
# Don't make the movie.
# video = HTML(ani.to_html5_video())
#
# Just show the result.
if save_output:
    ani.save(filename="double_pendulum.mp4",fps=60)
else:
    plt.show()
