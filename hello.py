## https://hub.gke2.mybinder.org/user/krischer-seismo_live_build-pmiaz5oh/notebooks/Signal%20Processing/filter_basics.ipynb

#Cell 1: prepare data from Tohoku earthquake. 
client = Client("BGR")
t1 = UTCDateTime("2011-03-11T05:00:00.000")
st = client.get_waveforms("GR", "WET", "", "BHZ", t1, t1 + 6 * 60 * 60, 
                          attach_response = True)
st.remove_response(output="VEL")
st.detrend('linear')
st.detrend('demean')
st.plot()
