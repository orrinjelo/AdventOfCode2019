#!/Users/user/anaconda3/bin/pythonw
# -*- coding: utf-8 -*-

"""
This example uses the Python Orbital Module to take a state vector and its epoch to generates its
Keplerian orbit. The state vector has units of km and km/sec.
"""

# -----------------------------------------------------------------------------
#  Declare module imports
# -----------------------------------------------------------------------------
import f90nml

import string
import os
import sys

import numpy             as np
import scipy.constants   as sc
import matplotlib.pyplot as plt
import pytz

from orbital             import earth, KeplerianElements, plot, plot3d
from scipy.constants     import kilo
from astropy.coordinates import FK5
from datetime            import datetime
from matplotlib          import animation


# point to 'ffmpeg' to output mp4 file, refer to
# https://stackoverflow.com/questions/23856990/cant-save-matplotlib-animation
# ---------------------------------------------------------------------------
plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'


# the FK5 Catalog and Julian Epoch J2000 are the defaults
# -------------------------------------------------------
f = FK5(equinox='J2000')


# set backend to display plots
# ----------------------------
plt.switch_backend('QT5Agg')


# set the state vector (in meters and meters/sec) and its epoch
# -------------------------------------------------------------
ictime = datetime(2016,12,9,16,38,45,0,tzinfo=pytz.utc)
print(ictime)

X = np.array([-6045, -3490, 2500, -3.457, 6.618, 2.533])
X = X * sc.kilo
print(X)


# generate the orbit with two-body physics
# ----------------------------------------
myorbit = KeplerianElements.from_state_vector( X[0:3], X[3:6],body=earth,ref_epoch=ictime )


# generate plots
# --------------
plot(myorbit)
plt.savefig('MyOrbit-1.png')

plot3d(myorbit)
plt.savefig('MyOrbit-2.png')


# Animation
# ---------
line1_anim = plot(myorbit, title='MyOrbit 1', animate=True )
line1_anim.save('MyOrbit-1.mp4')

line2_anim = plot3d(myorbit, title='MyOrbit 2', animate=True )
line2_anim.save('MyOrbit-2.mp4')


# Display plots
# -------------
plt.show()
