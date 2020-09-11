#
# Some code to help with creating Minkowski Plots.
#
#
import math as m
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from matplotlib import colors as ccc

pio.templates.default="plotly_white"


def t_prime(t, x, u) -> float:
    """Compute the relativistic t' from t_p """
    gamma = 1 / (m.sqrt(1 - u * u))
    return gamma * (t - x * u)


def x_prime(t, x, u) -> float:
    """Compute the relativistic x' from t_p and x_p """
    gamma = 1 / (m.sqrt(1 - u * u))
    return gamma * (x - u * t)

def rel_add_velocity(v1 , v2) -> float:
    """Add velocity v1 and v2 relativistically. Assumed is that the velocities are in units of c"""
    return (v1 + v2)/(1 + v1*v2)


class Actor(object):

    def __init__(self, name, velocity, position=0, color='rgba(0,255,0,1.)', size=5):
        self.name = name
        self.velocity = velocity
        self.position = position
        self.color = self.convert_color(color)
        self.size = size

        self.NDots = 20
        self.DotSpacing = 1
        self.PositiveOnly = False

        self.gamma = 1/(m.sqrt(1-velocity*velocity))

    def convert_color(self, color):
        """Take in a color name and convert it to a plotly color tuple."""
        color_tuple = None
        if type(color) is str:
            ct = ccc.to_rgb(color)
            return (int(ct[0]*255), int(ct[1]*255), int(ct[2]*255))
        elif type(color) is tuple or type(color) is list:
            return color

    def color_rgba(self, alpha=1.):
        return "rgba({:d},{:d},{:d},{:4.3f})".format(self.color[0], self.color[1], self.color[2], alpha)

class MinkowsiPlot(object):

    def __init__(self):
        self.__version__ = 1.
        self._actors = []
        self._fig = None
        self.SliderSteps = 21
        self.ShowAltAxes = False
        self._xmin = -10
        self._xmax = 10
        self._ymin = -10
        self._ymax = 10

    def get_version(self):
        return self.__version__

    def test_func(self, test):
        print(test)

    def add_actor(self, actor):
        self._actors.append(actor)

    def make_figure(self, width=800, height=800, xmin=-10, xmax=10, ymin=-10, ymax=10):
        """Create a Plotly figure for the actors.
        The figure will have the light rays and the dots for each of the actors."""

        self._xmin = xmin
        self._xmax = xmax
        self._ymin = ymin
        self._ymax = ymax

        self._fig = go.Figure(
            layout=go.Layout(
                xaxis=dict(range=[self._xmin, self._xmax], autorange=False),
                yaxis=dict(range=[self._ymin, self._ymax], autorange=False),
                width=width,
                height=height,
                title="Minkowski Diagram",
                xaxis_title="x [light-seconds]",
                yaxis_title="t [seconds]"
            ))

        for actor in self._actors:
            self.add_actor_trace(self._fig, actor)

        self._fig.add_trace(go.Scatter(
            line=dict(color='rgba(255,200,0,1.)', width=1),
            mode='lines',
            x=[2*self._xmin, 2*self._xmax, None, 2*self._xmax, 2*self._xmin],
            y=[2*self._ymin, 2*self._ymax, None, 2*self._ymin, 2*self._ymax],
            name="Light Ray"
        ))

        self.add_slider()

        return self._fig

    def compute_u_from_step(self, i) -> float:
        """Compute the u velocity from step i"""
        u = (i / (self.SliderSteps // 2) - 1.)
        if (1 - u * u) == 0 and u < 0:
            u = u + 0.001
        if (1 - u * u) == 0 and u > 0:
            u = u - 0.001
        return u

    def add_actor_trace(self, fig, actor):
        """Add the dots for the actor to the figure"""

        for i in range(self.SliderSteps):
            u = self.compute_u_from_step(i)
            xx = []
            yy = []

            for itt in range(actor.NDots):
                tt = (itt - actor.NDots//2)*actor.DotSpacing
                t = actor.gamma * tt
                if t >= 0 or actor.PositiveOnly is False:
                    xx.append(x_prime(t, actor.position + actor.velocity*t, u))
                    yy.append(t_prime(t, actor.position + actor.velocity*t, u))

            fig.add_trace(go.Scatter(
                marker=dict(color=actor.color_rgba(1.), size=actor.size),
                line=dict(color=actor.color_rgba(0.8), width=1.0),
                mode='lines+markers',
                x=xx,  # [ x_prime(t,0.*t,u) for t in range(10)],
                y=yy,  # [ t_prime(t,0.*t,u) for t in range(10)],
                visible=False,
                name="{}".format(actor.name),
                # name="{} at u={:3.1f}".format(actor.name,u),
            ))

            (x_grid, y_grid) = self.make_grid(rel_add_velocity(u, -actor.velocity))
            fig.add_trace(go.Scatter(
                # marker=dict(color=actor.color, size=actor.size),
                line=dict(color=actor.color_rgba(0.3), width=0.5),
                mode='lines',
                x=x_grid,
                y=y_grid,
                visible=False,
                showlegend=False,
                # name="A: for {} at u={:3.1f}".format(actor.name, u),

            ))

    def make_grid(self, beta):

        NGridSteps = 21 * 2
        Zmin = -10 * 2
        Zmax = 10 * 2

        # Draw the vertical lines.
        xx1=[]
        yy1=[]
        for i in range(NGridSteps):
            x = Zmin + i
            t_up = Zmax
            t_down = Zmin
            xx1.append(x_prime(t_down, x, beta))
            yy1.append(t_prime(t_down, x, beta))
            xx1.append(x_prime(t_up, x, beta))
            yy1.append(t_prime(t_up, x, beta))
            xx1.append(None)
            yy1.append(None)
        #
        # yy1 = [Zmin, Zmax, None] * NGridSteps
        # xx1 = list(np.array([(x - (3 * NGridSteps // 2 - 1)) // 3 for x in range(3 * NGridSteps)]) +
        #            np.array([x0_min, x0_max, 0] * NGridSteps))

        xx2 = []
        yy2 = []
        for i in range(NGridSteps):
            t = Zmin + i
            x_left = Zmax
            x_right = Zmin
            xx2.append(x_prime(t, x_left, beta))
            yy2.append(t_prime(t, x_left, beta))
            xx2.append(x_prime(t, x_right, beta))
            yy2.append(t_prime(t, x_right, beta))
            xx2.append(None)
            yy2.append(None)

        # xx2 = [Zmin, Zmax, None] * NGridSteps
        # yy2 = list(np.array([(x - (3 * NGridSteps // 2 - 1)) // 3 for x in range(3 * NGridSteps)]) +
        #            np.array([y0_min, y0_max, 0] * NGridSteps))

        x_grid = xx1 + xx2
        y_grid = yy1 + yy2
        return (x_grid, y_grid)

    def add_slider(self):
        """Add the slider to the figure."""

        NSets = len(self._actors)
        steps = []
        for i in range(self.SliderSteps):
            u = self.compute_u_from_step(i)
            step = dict(
                method="update",
                # Here we set which graphs will be visible.
                args=[{"visible": [False] * (2*NSets * self.SliderSteps + 1)},
                      {"title": "Minkowski Space Time with boost u = {:4.2f} c".format(u)},
                      ],  # layout attribute
                label="{:3.1f}".format(u),
            )

            for j in range(NSets):
                step["args"][0]["visible"][2*self.SliderSteps * j + 2*i] = True  # Toggle i'th trace to "visible"
                step["args"][0]["visible"][2*self.SliderSteps * j + 2*i+1] = self.ShowAltAxes  # Toggle i'th trace to "visible"

            step["args"][0]["visible"][2*NSets * self.SliderSteps] = True  # Toggle last trace to "visible"
            steps.append(step)

        # Create and add slider
        sliders = [dict(
            active=(self.SliderSteps // 2),
            currentvalue={"visible": False, "prefix": "i = "},
            pad={"t": 50},
            steps=steps
        )]

        for j in range(NSets):
            self._fig.data[2*self.SliderSteps * j + 2 * (self.SliderSteps // 2)].visible = True
            self._fig.data[2*self.SliderSteps * j + 2 * (self.SliderSteps // 2) + 1].visible = self.ShowAltAxes

        # if len(self._fig.data) > NSets*NSets:
        #     for j in range(NSets*NSets, len(self._fig.data)):
        #         self._fig.data[j].visible = True

        self._fig.update_layout(
            sliders=sliders
        )

