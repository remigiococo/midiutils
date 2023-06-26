import numpy as np
import sys
import matplotlib.pyplot as plt
from xml.dom import minidom
from xml.dom import Node
import gzip
import os
import wave

NUM_FFT_POINTS=8192
HALF_FFT_POINTS=(NUM_FFT_POINTS//2)

template_preset='''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ZynAddSubFX-data>
<ZynAddSubFX-data version-major="1" version-minor="0">
<BASE_PARAMETERS>
<par name="max_midi_parts" value="16"/>
<par name="max_kit_items_per_instrument" value="16"/>
<par name="max_system_effects" value="4"/>
<par name="max_insertion_effects" value="8"/>
<par name="max_instrument_effects" value="3"/>
<par name="max_addsynth_voices" value="8"/>
</BASE_PARAMETERS>
<Poscilgen>
<par name="harmonic_mag_type" value="0"/>
<par name="base_function" value="0"/>
<par name="base_function_par" value="64"/>
<par name="base_function_modulation" value="0"/>
<par name="base_function_modulation_par1" value="64"/>
<par name="base_function_modulation_par2" value="64"/>
<par name="base_function_modulation_par3" value="32"/>
<par name="modulation" value="0"/>
<par name="modulation_par1" value="64"/>
<par name="modulation_par2" value="64"/>
<par name="modulation_par3" value="32"/>
<par name="wave_shaping" value="64"/>
<par name="wave_shaping_function" value="0"/>
<par name="filter_type" value="0"/>
<par name="filter_par1" value="74"/>
<par name="filter_par2" value="64"/>
<par name="filter_before_wave_shaping" value="0"/>
<par name="spectrum_adjust_type" value="0"/>
<par name="spectrum_adjust_par" value="64"/>
<par name="rand" value="64"/>
<par name="amp_rand_type" value="0"/>
<par name="amp_rand_power" value="64"/>
<par name="harmonic_shift" value="0"/>
<par_bool name="harmonic_shift_first" value="no"/>
<par name="adaptive_harmonics" value="0"/>
<par name="adaptive_harmonics_base_frequency" value="128"/>
<par name="adaptive_harmonics_power" value="100"/>
<HARMONICS>
HARMONICS_VAL
</HARMONICS>
</Poscilgen>
</ZynAddSubFX-data>
'''

template_harmonic='''
<HARMONIC id="ID_VAL">
<par name="mag" value="MAG_VAL"/>
<par name="phase" value="64"/>
</HARMONIC>'''

FILE_ANALISI="spettro.txt"
BASE_FREQUENCY=510.0
xmldoc=None


def leggi_wav(nomewav, fftpoints=NUM_FFT_POINTS):
	f = wave.open(nomewav, 'rb')
	w = f.readframes( f.getnframes() )
	sig = np.frombuffer(w, dtype=np.int16)
	ffR = None
	ffL = None
	#winfunc = np.blackman(NUM_FFT_POINTS)
	winfunc = 1.0
	if f.getnchannels() == 2:
		sigR = sig[0::2]
		sigL = sig[1::2]
		ffR = np.fft.rfft(winfunc*sigR[0:NUM_FFT_POINTS]/32768.0, n=fftpoints, norm='ortho')
		ffL = np.fft.rfft(winfunc*sigL[0:NUM_FFT_POINTS]/32768.0, n=fftpoints, norm='ortho')
	elif f.getnchannels() == 1:
		sigR = sig[0:]
		sigL = []
		ffR = np.fft.rfft(winfunc*sigR[0:NUM_FFT_POINTS]/32768.0, n=fftpoints, norm='ortho')
		ffL = []
	else:
		print("Wrong number of channels!!! - must be 1 or 2")
	samplerate = f.getframerate()	
	f.close()
	return ffR, ffL, samplerate


def find_nearest(array, value):
	array = np.asarray(array)
	idx = (np.abs(array - value)).argmin()
	return idx, array[idx]

######
#if len(sys.argv) > 1:
#	fR,fL = leggi_wav(sys.argv[1])
#	fig, ax = plt.subplots(2)
#	ax[0].plot(np.abs(fR)[1:4095]) # tolgo la componente continua ???
#	ax[1].plot(np.angle(fR)[1:4095])
#	plt.show()
#sys.exit(0)
######
xmldoc=template_preset[0:]
	
filename=FILE_ANALISI
if len(sys.argv) < 2:
	print("python spectrum_zyn.py <input_file> <base_freq> <poscilgen_name> <plot=0|1>")
	sys.exit(0)
if len(sys.argv) >= 2:
	filename = sys.argv[1]
base_freq=BASE_FREQUENCY	
if len(sys.argv) >= 3:
	base_freq = float(sys.argv[2])
enable_plot=False	
if len(sys.argv) >= 5:	
	enable_plot=True
if ".txt" in filename:	
	xx = np.loadtxt(filename, skiprows=1, converters={0:lambda s: float(s.replace(",",".")), 1: lambda s: float(s.replace(",","."))}, encoding='ascii' )
	x = np.ndarray( (len(xx),3) )
	for i in range(0,len(xx)):
		x[i][0] = xx[i][0]
		x[i][1] = xx[i][1]
		x[i][2] = -np.pi + i * 2.0 * np.pi / len(xx)
	#print(type(x), x.shape)
elif ".wav" in filename:
	fR,fL, sr = leggi_wav(filename)
	# DA FARE - gestione 2 canali !
	#
	# modulo FFT
	#
	ampiezze = np.abs(fR)
	y = ampiezze[1:HALF_FFT_POINTS+1]
	maxamp = max(y)
	#
	# fase FFT
	#
	#fasi = np.arctan2( np.imag( fR ) , np.real( fR ) )
	fasi = np.angle(fR)[1:HALF_FFT_POINTS+1]
	fasiu = np.unwrap(fasi[1:])
	ph = np.where(y<(maxamp/100.0), 0, fasi)
	#ph = fasiu[0:HALF_FFT_POINTS]
	#ph = np.unwrap(np.angle(fR))[1:HALF_FFT_POINTS+1]
	#
	# frequenze FFT
	#
	#f = [i*float(sr)/NUM_FFT_POINTS for i in range(1,HALF_FFT_POINTS)]
	f = np.fft.fftfreq(NUM_FFT_POINTS, d=1.0/sr)[1:HALF_FFT_POINTS+1]
	ydb = 20.0 * np.log10(y)
	x = np.ndarray( (HALF_FFT_POINTS,3) )
	for i in range(0,HALF_FFT_POINTS):
		x[i][0] = f[i]
		x[i][1] = ydb[i]
		x[i][2] = ph[i]
	#print(type(x), x.shape)
	print(len(fR))
	print(ph[0:30])
else:
	sys.exit(0)	
#max_db=x.max(axis=1)
max_db = max(x[:,1])
imax_db=np.argmax(x[:,1])
print("[" + str(imax_db) + "]", "max dB:", max_db, "freq:", x[imax_db][0])
max_freq, m_db, m_ph = x.max(axis=0)
print("max freq:", max_freq)
f=base_freq
fr=x[:,0]
harmonics=[]
phases=[]
while f < max_freq:
	j, f2 = find_nearest(fr, f)
	z = x[j][1]
	mag = np.power( 10.0, (z/20.0) ) # inverso del dB
	harmonics.append(mag)
	phases.append(x[j][2])
	f += base_freq
print("n. harmonics:", len(harmonics))	
#print(harmonics)
max_h = max(harmonics)
#normalizzazione
harmonics_n = [int( h * 63.0 / max_h ) + 64 for h in harmonics]
#print(harmonics_n)
#
# ricostruzione forma d'onda - non funziona con le fasi !!!
#
i = 0
npoints = NUM_FFT_POINTS
pl = np.array([0.0 for j in range(npoints)])
for h in harmonics_n:
	true_h = ( h - 64 )
	for j in range(npoints):
		pl[j] += true_h * np.cos( phases[i] + 2 * np.pi * 4 * (i+1) * j / npoints )
		#pl[j] += true_h * np.sin( 2.0 * np.pi * 4 * (i+1) * j / npoints )
		#pl[j] += true_h * np.sin( (phases[i]/base_freq) + 2.0 * 4 * np.pi * (i+1) * j / npoints )
	i += 1
# print(pl)
if enable_plot:
	fig, ax = plt.subplots(3)
	ax[0].plot(pl)
	ax[1].plot(harmonics)
	ax[2].plot(ph)
	plt.show()
# XML
h_xml = []
i = 1
for h in harmonics_n:
	tmpx = template_harmonic[0:]
	tmpx = tmpx.replace("ID_VAL", str(i))
	tmpx = tmpx.replace("MAG_VAL", str(h))
	i = i + 1
	h_xml.append(tmpx)
armonici = "".join(h_xml)	
#print(armonici)
xmldoc = xmldoc.replace("HARMONICS_VAL", armonici)
#print(xmldoc)
if len(sys.argv) >= 4:
	fx = open(sys.argv[3] + ".tmp", 'w')
	fx.write(xmldoc)
	fx.close()
	f = open(sys.argv[3] + ".tmp", 'rb')
	g = gzip.GzipFile(sys.argv[3], 'wb')
	g.write(f.read())
	f.close()
	g.close()
	os.rename(sys.argv[3], sys.argv[3] + ".xpz")
	os.remove(sys.argv[3] + ".tmp")
