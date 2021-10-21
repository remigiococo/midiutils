import numpy as np
import sys
import matplotlib.pyplot as plt
from xml.dom import minidom
from xml.dom import Node
import gzip
import os

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
<par name="rand" value="113"/>
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

def find_nearest(array, value):
	array = np.asarray(array)
	idx = (np.abs(array - value)).argmin()
	return idx, array[idx]

xmldoc=template_preset[0:]
	
filename=FILE_ANALISI
if len(sys.argv) >= 2:
	filename = sys.argv[1]
base_freq=BASE_FREQUENCY	
if len(sys.argv) >= 3:
	base_freq = float(sys.argv[2])
x = np.loadtxt(filename, skiprows=1, converters={0:lambda s: float(s.replace(",",".")), 1: lambda s: float(s.replace(",","."))}, encoding='ascii' )
#max_db=x.max(axis=1)
max_db = max(x[:,1])
imax_db=np.argmax(x[:,1])
print("[" + str(imax_db) + "]", "max dB:", max_db, "freq:", x[imax_db][0])
max_freq, y = x.max(axis=0)
print("max freq:", max_freq)
f=base_freq
fr=x[:,0]
harmonics=[]
while f < max_freq:
	j, f2 = find_nearest(fr, f)
	z = x[j][1]
	mag = np.power( 10.0, (z/20.0) ) # inverso del dB
	harmonics.append(mag)
	f += base_freq
print("n. harmonics:", len(harmonics))	
#print(harmonics)
max_h = max(harmonics)
#normalizzazione
harmonics_n = [int( h * 63.0 / max_h ) + 64 for h in harmonics]
#print(harmonics_n)
i = 0
npoints = 100
pl = np.array([0.0 for j in range(npoints)])
for h in harmonics_n:
	for j in range(npoints):
		pl[j] += h * np.sin( 2 * np.pi * (i+1) * j / npoints )
	i += 1
# print(pl)
enable_plot=False
if enable_plot:
	plt.plot(pl)
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