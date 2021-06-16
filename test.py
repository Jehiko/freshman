
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# <div style='background-image: url("../share/images/header.svg") ; padding: 0px ; background-size: cover ; border-radius: 5px ; height: 250px'>
#     <div style="float: right ; margin: 50px ; padding: 20px ; background: rgba(255 , 255 , 255 , 0.7) ; width: 50% ; height: 150px">
#         <div style="position: relative ; top: 50% ; transform: translatey(-50%)">
#             <div style="font-size: xx-large ; font-weight: 900 ; color: rgba(0 , 0 , 0 , 0.8) ; line-height: 100%">Signal Processing</div>
#             <div style="font-size: large ; padding-top: 20px ; color: rgba(0 , 0 , 0 , 0.5)">Filtering Basics - Solution</div>
#         </div>
#     </div>
# </div>

# Seismo-Live: http://seismo-live.org
#
# ##### Authors:
# * Stefanie Donner ([@stefdonner](https://github.com/stefdonner))
# * Celine Hadziioannou ([@hadzii](https://github.com/hadzii))
# * Ceri Nunn ([@cerinunn](https://github.com/cerinunn))
#
#
# ---

# <h1>Basics in filtering</h1>
# <br>

# + {"code_folding": [0]}
# Cell 0 - Preparation: load packages, set some basic options  
# %matplotlib inline
from obspy import *
from obspy.clients.fdsn import Client
import numpy as np
import matplotlib.pylab as plt
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = 15, 4
plt.rcParams['lines.linewidth'] = 0.5
# -

# ## The filter
#
# A good definition of what a filter is can be found in the book 'Of poles and zeros' by Frank Scherbaum:
#
# > _Filters or systems are, in the most general sense, devices (in the physical world) or algorithms (in the mathematical world) which act on some input signal to produce a - possibly different - output signal_
#
# In seismology, filters are used to correct for the instrument response, avoid aliasing effects, separate 'wanted' from 'unwanted' frequencies, identify harmonic signals, model a specific recording instrument, and much more ...   
#
# There is no clear classification of filters. Roughly speaking, we can distinguish linear vs. non-linear, analog (circuits, resistors, conductors) vs. digital (logical components), and continuous vs. discrete filters. In seismology, we generally avoid non-linear filters, because their output contains frequencies which are not in the input signal. Analog filters can be continuous or discrete, while digital filters are always discrete. Discrete filters can be subdivided into infinite impulse response (IIR) filters, which are recursive and causal, and finite impulse response (FIR) filters, which are non-recursive and causal or acausal. We will explain more about these types of filters below.   
# Some filters have a special name, such as Butterworth, Chebyshev or Bessel filters, but they can also be integrated in the classification described above.
#
# A filter is characterised by its *frequency response function* which is the [Fourier transformation](fourier_transform.ipynb) of the output signal divided by the Fourier transformation of the input signal:
#
# $$ T(j\omega) = \frac{Y(j\omega)}{X(j\omega)}$$
#
# For a simple lowpass filter it is given as:
#
# $$ |T(j\omega)| = \sqrt{ \frac{1}{1+(\frac{\omega}{\omega_c})^{2n}} } $$
#
# with $\omega$ indicating the frequency samples, $\omega_c$ the corner frequency of the filter, and $n$ the order of the filter (also called the number of corners of the filter). For a lowpass filter, all frequencies lower than the corner frequency are allowed to pass the filter. This is the *pass band* of the filter. On the other hand, the range of frequencies above the corner frequency is called *stop band*. In between lies the *transition band*, a small band of frequencies in which the passed amplitudes are gradually decreased to zero. The steepness of the slope of this *transition band* is defined by the order of the filter: the higher the order, the steeper the slope, the more effectively 'unwanted' frequencies get removed. 
#
# In the time domain, filtering means to [convolve](convolution.ipynb) the data with the *impulse response function* of the filter. Doing this operation in the time domain is mathematically complex, computationally expensive and slow. Therefore, the digital application of filters is almost always done in the frequency domain, where it simplifies to a much faster multiplication between data and filter response. The procedure is as follows: transfer the signal into the frequency domain via FFT, multiply it with the filter's *frequency response function* (i.e. the FFT of the *impulse response function*), and transfer the result back to the time-domain. As a consequence, when filtering, we have to be aware of the characteristics and pit-falls of the [Fourier transformation](fourier_transform.ipynb).

# ---
# ### Filter types
#
# There are 4 main types of filters: a lowpass, a highpass, a bandpass, and a bandstop filter. Low- and highpass filters only have one corner frequency, allowing frequencies below and above this corner frequency to pass the filter, respectively. In contrast, bandpass and bandstop filters have two corner frequencies, defining a frequency band to pass and to stop, respectively.   
# Here, we want to see how exactly these filters act on the input signal. In Cell 1, the vertical component of the M$_w\,$9.1 Tohoku earthquake, recorded at Wettzell - Germany, is downloaded and [pre-processed](spectral_analysis+preprocessing.ipynb). In Cell 2, the four basic filters are applied to these data and plotted together with the filter functions and the resulting amplitude spectrum. 
#
# 1) Look at the figure and explain what the different filters do.   
# 2) Change the order of the filter (i.e the number of corners). What happens and why?  

# Cell 1: prepare data from Tohoku earthquake. 
client = Client("BGR")
t1 = UTCDateTime("2011-03-11T05:00:00.000")
st = client.get_waveforms("GR", "WET", "", "BHZ", t1, t1 + 6 * 60 * 60, 
                          attach_response = True)
st.remove_response(output="VEL")
st.detrend('linear')
st.detrend('demean')
st.plot()
