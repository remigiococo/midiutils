import random
from pretty_midi import PrettyMIDI, Note, Instrument
import pretty_midi as pm

'''
-----------------------------------------------------------------------------
   Key / Perc. sound            Key / Perc. sound            Key / Perc. sound
  -----------------------------------------------------------------------------
   35. Acoustic Bass Drum       51. Ride Cymbal 1            67. High Agogo
   36. Bass Drum 1              52. Chinese Cymbal           68. Low Agogo
   37. Side Stick               53. Ride Bell                69. Cabasa
   38. Acoustic Snare           54. Tambourine               70. Maracas
   39. Hand Clap                55. Splash Cymbal            71. Short Whistle
   40. Electric Snare           56. Cowbell                  72. Long Whistle
   41. Low Floor Tom            57. Crash Cymbal 2           73. Short Guiro
   42. Closed Hi-Hat            58. Vibraslap                74. Long Guiro
   43. High Floor Tom           59. Ride Cymbal 2            75. Claves
   44. Pedal Hi-Hat             60. High Bongo               76. Hi Woodblock
   45. Low Tom                  61. Low Bongo                77. Low Woodblock
   46. Open Hi-Hat              62. Mute Hi Conga            78. Mute Cuica
   47. Low-Mid Tom              63. Open Hi Conga            79. Open Cuica
   48. High-Mid Tom             64. Low Conga                80. Mute Triangle
   49. Crash Cymbal 1           65. High Timbale             81. Open Triangle
   50. High Tom                 66. Low Timbale
'''	 
	 
def gen_bin_str(len, n_ones):
	no = 0
	s = set()
	for i in range(n_ones):
		f = 0
		while f == 0:
			x = random.randint(0, len-1)
			# print x # debug
			if x not in s:
				s.add(x)
				f = 1
	rs = ''			
	# print s # debug
	for i in range(len):
		if i in s:
			rs += '1'
		else:
			rs += '0'
	return rs			

def and_str0(a, b):
	x1 = int(a,2)
	x2 = int(b,2)
	x = x1 & x2
	if len(a) == 16:
		return "{0:016b}".format(x) # N.B.: solo per stringhe lunghe 16
	elif len(a) == 32:	
		return "{0:032b}".format(x)
	else:
		return "{0:064b}".format(x)

def and_str(a, b):
	s = ""
	for i in range(len(a)):
		x1 = int(a[i], 10)
		x2 = int(b[i], 10)
		# x2 contiene 0 e 1, x1 puo' essere > 1
		if x2 == 0:
			x = 0
		else:
			x = x1
		s = s + str(x)
	return s

def or_str0(a, b):
	x1 = int(a,2)
	x2 = int(b,2)
	x = x1 | x2
	if len(a) == 16:
		return "{0:016b}".format(x) # N.B.: solo per stringhe lunghe 16
	elif len(a) == 32:	
		return "{0:032b}".format(x)
	else:
		return "{0:064b}".format(x)

def or_str1(a, b): # or tra numeri in base 10
	s = ""
	for i in range(len(a)):
		x1 = int(a[i], 10)
		x2 = int(b[i], 10)
		x = x1 | x2
		s = s + str(x)
	return s

def or_str(a, b):
	s = ""
	for i in range(len(a)):
		x1 = int(a[i], 10)
		x2 = int(b[i], 10)
		# x2 contiene 0 e 1, x1 puo' essere > 1
		if x2 == 0:
			y = x2
		else:
			if x1 != 0:
				y = x1
			else:
				y = x2
		x = x1 | y
		s = s + str(x)
	return s

def xor_str0(a, b):
	x1 = int(a,2)
	x2 = int(b,2)
	x = x1 ^ x2
	if len(a) == 16:
		return "{0:016b}".format(x) # N.B.: solo per stringhe lunghe 16
	elif len(a) == 32:	
		return "{0:032b}".format(x)
	else:
		return "{0:064b}".format(x)

def xor_str(a, b):
	s = ""
	for i in range(len(a)):
		x1 = int(a[i], 10)
		x2 = int(b[i], 10)
		# x2 contiene 0 e 1, x1 puo' essere > 1 -> si modifica l'operazione di xor
		if x2 == 0:
			y = x2
		else:
			y = x1
		x = x1 ^ y
		s = s + str(x)
	return s
	
# bar e' una semplice lista di note	
# pos e' relativo alla durata della battuta (tra 0 e 1)
# dur e' espresso in notazione musicale (4, 8, 16 ...)
def place_at(bar, note, pos, dur=16):
	global BarDur
	# print( "place at", pos ) # debug
	single_dur = BarDur / float(dur)
	tmpnote = Note(note.velocity, note.pitch, 0.0, 0.0)
	tmpnote.start = pos * BarDur
	tmpnote.end = tmpnote.start + single_dur
	# print( note ) # debug
	bar.append(tmpnote)

def bin_to_bar(bar, note, str, dur=16):
	ls = len(str)
	dt = 1.0 / float(ls)
	for i in range(ls):
		if str[i] == '1':
			place_at(bar, note, i*dt, dur)
		elif int(str[i],10) > 1: # n-uplicate ("stutter" effect)
			n = int(str[i],10)
			for j in range(n):
				dt2 = dt / n
				place_at(bar, note, i*dt + j*dt2, dur)

def init_bar(b, quantiz=16, time_offset=0.0):
	global BarDur
	# Note ha i seguenti campi: pitch, velocity, start, end
	singledur = BarDur/float(quantiz)
	for j in range(quantiz):
		dummy = Note( 0, 0, 0, 0 )
		dummy.start = j * singledur + time_offset
		dummy.end = dummy.start + singledur
		b.append(dummy)
		
def clean_bar(b):
	for x in b:
		b.remove(x)
		
def setup_composition(nbars=64, ntracks=2, quant=16, tempo=120):
	global BarDur
	BarDur = 4 * 60.0 / tempo # 4/4 @ 120 bpm
	comp = pm.PrettyMIDI()
	tks =[Instrument(1) for i in range(ntracks)]
	for i in range(ntracks):
		bars = [[] for j in range(nbars)]
		for j in range(nbars):
			init_bar(bars[j], quant, BarDur*j)
			for k in bars[j]:
				tks[i].notes.append( k )
		comp.instruments.append( tks[i] )
	return comp
	
def set_track_instrument(track, instr, channel=0):
	track.program = instr
		
def gen_dur_div(x=[1.0], n=3):
	if n == 0:
		return x
	l = len(x)
	r = random.randint(0, l-1)
	x[r] = x[r] / 2
	x.insert(r+1, x[r])
	return gen_dur_div(x, n-1)

def gen_bar_1(b, time_offset=0.0, chord="C maj", octave=3):
	global BarDur
	durate = [ BarDur/2.0, BarDur/4.0, BarDur/8.0, BarDur/16.0 ]
	majc = [0, 4, 7]
	minc = [0, 3, 7]
	sevc = [0, 4, 7, 10]
	ch = chord.split(" ")
	#print(ch) # debug
	if ch[1] == "maj":
		cur_ch = majc
	elif	ch[1] == "min":
		cur_ch = minc
	elif	ch[1] == "7":
		cur_ch = sevc
	else:
		cur_ch = majc
	d = 0
	while d < BarDur:
		basepitch = pm.note_name_to_number(ch[0]+ str(octave))
		roct = random.randint(-1,1)
		rpitch = cur_ch[ random.randint(0, len(cur_ch)-1) ] + basepitch + roct*12
		#print(basepitch, roct, rpitch, pm.note_number_to_name(rpitch)) # debug
		rvel = random.randint(80,127)
		rdur = 2.0*BarDur
		while (d + rdur) > BarDur:
			rdur = durate[ random.randint(0,3) ]
		#print(rdur, BarDur)	
		n = Note(rvel, rpitch, time_offset + d, time_offset + d + rdur)
		b.append(n)
		d = d + rdur
	#print("---")
	
def gen_bar_2(b, time_offset=0.0, chord="C maj", octave=3, add_root=False):
	global BarDur
	durate = [ BarDur/2.0, BarDur/4.0, BarDur/8.0, BarDur/16.0 ]
	ch = chord.split(" ")
	basepitch = pm.note_name_to_number(ch[0]+ str(octave))
	if add_root:	
		root = Note(100, pm.note_name_to_number(ch[0]+"1"), time_offset, time_offset + BarDur)
		b.append(root)
	mk = markov(basepitch)	
	d = 0
	while d < BarDur:
		rpitch = mk.next()
		#print(basepitch, rpitch, pm.note_number_to_name(rpitch)) # debug
		rvel = random.randint(80,127)
		rdur = 2.0*BarDur
		while (d + rdur) > BarDur:
			rdur = durate[ random.randint(0,3) ]
		n = Note(rvel, rpitch, time_offset + d, time_offset + d + rdur)
		b.append(n)
		d = d + rdur

def gen_bar_3(b, time_offset=0.0, chord="C maj", octave=3, add_root=False):
	global BarDur
	durate = [ BarDur/2.0, BarDur/4.0, BarDur/8.0, BarDur/16.0 ]
	ch = chord.split(" ")
	basepitch = pm.note_name_to_number(ch[0]+ str(octave))
	if add_root:	
		root = Note(100, pm.note_name_to_number(ch[0]+"1"), time_offset, time_offset + BarDur)
		b.append(root)
	mk = markov(basepitch)
	quarter = BarDur/4.0
	durs = gen_dur_div([quarter, quarter, quarter, quarter], 2)
	d = 0
	for rdur in durs:
		rpitch = mk.next()
		#print(basepitch, rpitch, pm.note_number_to_name(rpitch)) # debug
		rvel = random.randint(80,127)
		n = Note(rvel, rpitch, time_offset + d, time_offset + d + rdur)
		b.append(n)
		d = d + rdur

def gen_bar_4(b, time_offset=0.0, chord="C maj", octave=3, add_root=False):
	global BarDur
	durate = [ BarDur/2.0, BarDur/4.0, BarDur/8.0, BarDur/16.0 ]
	ch = chord.split(" ")
	basepitch = pm.note_name_to_number(ch[0]+ str(octave))
	if add_root:	
		root = Note(100, pm.note_name_to_number(ch[0]+"1"), time_offset, time_offset + BarDur)
		b.append(root)
	mk = scala(sc="101010010000", dist="gauss", ini=basepitch, octaves=1)
	quarter = BarDur/4.0
	durs = gen_dur_div([quarter, quarter, quarter, quarter], 2)
	d = 0
	for rdur in durs:
		rpitch = mk.next()
		#print(basepitch, rpitch, pm.note_number_to_name(rpitch)) # debug
		rvel = random.randint(80,127)
		n = Note(rvel, rpitch, time_offset + d, time_offset + d + rdur)
		b.append(n)
		d = d + rdur
		
def gen_composition_1(nbars=64, ntracks=2, quant=16, tempo=120, chords=["C maj", "D min", "A min", "F maj"]):
	global BarDur
	BarDur = 4 * 60.0 / float(tempo) # 4/4 @ 120 bpm
	BarDurDiv = int(65536 * BarDur)
	BarDur = BarDurDiv / 65536
	#print("BarDur", BarDur)
	comp = pm.PrettyMIDI()
	chord_div = nbars//len(chords)
	tks =[Instrument(1) for i in range(ntracks)]
	addr = False
	for i in range(ntracks):
		if i == ntracks - 1:
			addr = True
		bars = [[] for j in range(nbars)]
		for j in range(nbars):
			# gen bar
			#gen_bar_1(bars[j], BarDur*j, chords[j//chord_div])
			#gen_bar_2(bars[j], BarDur*j, chords[j//chord_div], add_root=addr)
			#gen_bar_3(bars[j], BarDur*j, chords[j//chord_div], add_root=addr)
			gen_bar_4(bars[j], BarDur*j, chords[j//chord_div], add_root=addr)
			for k in bars[j]:
				tks[i].notes.append( k )
		comp.instruments.append( tks[i] )
	return comp
	
class randmel:	
	def __init__(self):
		self.stato = 0
		self.clip = 0 # 0 - clip, 1 - mirror
		
	def extract_note(self, scala, ottave=3):
		ls = len(scala)
		x = random.randint(-1, 1)
		y = self.stato + x
		if self.clip == 0:
			if y < 0:
				y = 0
			if y > ls*ottave-1:
				y = ls*ottave-1
		else:		
			if y < 0:
				y = -y
			if y > ls*ottave-1:
				y = ls*ottave-y
		self.stato = y	
		return scala[ y % ls ] + 12 * (y//ls)

	# extract_note2 filtra le ripetizioni del numero casuale
	def extract_note2(self, scala, ottave=3):
		ls = len(scala)
		x = 0
		while x == 0:
			x = random.randint(-1, 1)
		y = self.stato + x
		if self.clip == 0:
			if y < 0:
				y = 0
			if y > ls*ottave-1:
				y = ls*ottave-1
		else:		
			if y < 0:
				y = -y
			if y > ls*ottave-1:
				y = ls*ottave-y
		self.stato = y	
		return scala[ y % ls ] + 12 * (y//ls)
	
	# extract_note_tri genera con distribuzione triangolare
	def extract_note_tri(self, scala, ottave=3, interval=2):
		ls = len(scala)
		x = 0
		while x == 0:
			x1 = random.randint(-interval, interval)
			x2 = random.randint(-interval, interval)
			x = (x1+x2)//2
		y = self.stato + x
		if self.clip == 0:
			if y < 0:
				y = 0
			if y > ls*ottave-1:
				y = ls*ottave-1
		else:		
			if y < 0:
				y = -y
			if y > ls*ottave-1:
				y = ls*ottave-y
		self.stato = y
		# print( self.stato )# debug	
		return scala[ y % ls ] + 12 * (y//ls)
	
class randdrum:
	_OR_VAR_=0
	_XOR_VAR_=1
	_AND_VAR_=2
	_DUMMY_NOTE_=Note(pitch=pm.note_name_to_number('B1'),velocity=0,start=0.0,end=0.05)
	def __init__(self, nsteps=16, nbars=16, tempo=120, duration=16):
		global BarDur
		# self.bd = Note('C', 2) # bass drum
		self.bd = Note(0,pm.note_name_to_number('B1'),0.0,0.05) # bass drum
		self.lt = Note(0,pm.note_name_to_number('F2'),0.0,0.05) # lo tom
		self.ht = Note(0,pm.note_name_to_number('B2'),0.0,0.05) # hi tom
		self.lb = Note(0,pm.note_name_to_number('C#4'),0.0,0.05) # lo bongo
		self.hb = Note(0,pm.note_name_to_number('C4'),0.0,0.05) # hi bongo
		self.ch = Note(0,pm.note_name_to_number('F#2'),0.0,0.05) # closed hat
		self.oh = Note(0,pm.note_name_to_number('A#2'),0.0,0.05) # open hat
		self.sn = Note(0,pm.note_name_to_number('D2'),0.0,0.05) # snare
		self.cl = Note(0,pm.note_name_to_number('D#2'),0.0,0.05) # clap
		self.DRMAP={"bd":self.bd, "sn":self.sn, "ch":self.ch, "oh":self.oh, 
			"lt":self.lt, "ht":self.ht, "hb":self.hb, "lb":self.lb, "cl":self.cl}
		for x in self.DRMAP.keys():
			self.DRMAP[x].velocity = 100
			self.DRMAP[x].start = 0.0
			self.DRMAP[x].end = 0.05
		# TR-808 kit = 25 (26 but zero-based!)	
		self.tk = Instrument(25, is_drum=1)
		self.bds=""	
		self.sns=""	
		self.hts=""	
		self.lts=""	
		self.chs=""	
		self.ohs=""	
		self.lbs=""	
		self.hbs=""
		self.cls=""		
		self.bdv=[]	
		self.snv=[]	
		self.htv=[]	
		self.ltv=[]	
		self.chv=[]	
		self.ohv=[]	
		self.lbv=[]	
		self.hbv=[]	
		self.clv=[]
		self.nsteps = nsteps
		self.dur = duration
		self.n_bars = nbars
		self.tempo = tempo
		self.STRMAP={"bd":self.bds, "sn":self.sns, "ch":self.chs, "oh":self.ohs, 
			"lt":self.lts, "ht":self.hts, "hb":self.hbs, "lb":self.lbs, "cl":self.cls}
		self.VARMAP={"bd":self.bdv, "sn":self.snv, "ch":self.chv, "oh":self.ohv, 
			"lt":self.ltv, "ht":self.htv, "hb":self.hbv, "lb":self.lbv, "cl":self.clv}
		self.vartype = self._OR_VAR_
		BarDur = 4 * (60.0 / self.tempo)
		
	def base_str(self, instr, s):
		if len(s) != self.nsteps:
			print ("error: pattern length not corresponding to num. of steps !!!")
			return
		self.STRMAP[instr] = s
		
	def set_var(self, instr, v):
		if len(v) != self.n_bars:
			print ("error: variation length not corresponding to num. of bars !!!")
			return
		self.VARMAP[instr] = v
		
	def set_kit(self, prog):
		set_track_instrument(self.tk, prog)
		
	def gen(self, midifilename=None):
		global BarDur
		single_dur = BarDur / float(self.dur)
		dummy = self._DUMMY_NOTE_ # Note(pm.note_name_to_number('C0'))
		dummy.velocity = 0
		dummy.start = 0.0
		dummy.end = dummy.start + single_dur
		bar_offset = 0.0
		# print( "BarDur", BarDur, "single_dur", single_dur ) # debug
		for nb in range( self.n_bars ):
			b = []
			# ------
			# note "dummy" posizionate su una "griglia di quantizzazione"	- NON SERVONO in pretty_midi
			#for i in range(self.nsteps):
			#	dummy.start += single_dur
			#	dummy.end += single_dur
			#	b.append(dummy)
			# print repr(b) # debug
			# ------
			# note "vere"	
			for x in self.STRMAP.keys():
				ys = self.STRMAP[x]
				y = self.DRMAP[x]
				if len(ys) > 0:
					if len(self.VARMAP[x]) > 0:
						var = self.VARMAP[x][nb]
					else:
						var = 0
					if self.vartype == self._OR_VAR_: # or/and = variazione aggiunge/toglie !? xor = toggle
						tmps = or_str( ys, gen_bin_str(self.nsteps, var) ) 
					elif self.vartype == self._XOR_VAR_:
						tmps = xor_str( ys, gen_bin_str(self.nsteps, var) )
					elif self.vartype == self._AND_VAR_:
						tmps = and_str( ys, gen_bin_str(self.nsteps, var) )
					else:
						tmps = ys # no var.
					# print( "tmps", tmps )	# debug
					bin_to_bar(b, y, tmps, self.dur)
			# print ( "relative bar n.", nb, "offset" , bar_offset, repr(b)) # debug			
			# ------		
			# cleanup - tolgo le note "dummy"
			#for x in b.bar :
			#	x[2].remove_note('C', 0)
			# ------
			# posizionamento assoluto e aggiunta alla track
			for y in b:
				y.start += bar_offset
				y.end += bar_offset
				self.tk.notes.append( y )
			# print ( "bar n.", nb, "offset" , bar_offset, repr(b)) # debug	
			bar_offset += BarDur
		# ------		
		# "dummy bar"
		#db = Bar('C', (4,4))
		#db.place_notes(dummy,1)
		#self.tk + db
		self.comp = pm.PrettyMIDI()
		timesig = pm.TimeSignature(numerator=4, denominator=4, time=0.0)
		self.comp.time_signature_changes.append( timesig )
		self.comp.instruments.append( self.tk )
		if midifilename != None:
			self.comp.write(midifilename)
	
	def save(self, midifilename):
		if midifilename != None:
			self.comp.write(midifilename)
	
	def merge(self, randdrum2):
		ninst2 = len(randdrum2.comp.instruments)
		ninst = len(self.comp.instruments)
		if ninst != ninst2:
			print( "Error - different num. of tracks !!!" )
			return
		for i in range(ninst2):
			for n in randdrum2.comp.instruments[i].notes:
				self.comp.instruments[i].notes.append(n)
			# print("TRACK ", i, self.comp.instruments[i].notes) # debug

class markov:
	def __init__(self, st=40):
		# weighs (interval transition)
		self.prob_w = [ 
			# row = 0..11   col = 0..12
			[ 1,0,90,0,90,1,0,2,0,1,0,0,1 ],
			[ 1,0,0,0,0,0,0,0,0,0,0,0,0 ],
			[ 1,0,90,1,0,2,0,1,0,0,0,0,0 ],
			[ 1,0,0,0,0,0,0,0,0,0,0,0,0 ],
			[ 1,1,0,2,0,1,0,0,1,0,0,0,0 ],
			[ 1,0,2,0,1,0,0,1,0,0,0,0,0 ],
			[ 1,0,0,0,0,0,0,0,0,0,0,0,0 ],
			[ 1,0,1,0,0,1,0,0,0,0,0,0,0 ],
			[ 1,0,0,0,0,0,0,0,0,0,0,0,0 ],
			[ 1,0,0,1,0,0,0,0,0,0,0,0,0 ],
			[ 1,0,0,0,0,0,0,0,0,0,0,0,0 ],
			[ 1,1,0,0,0,0,0,0,0,0,0,0,0 ] ]
		# normalization
		self.prob = [ [ [0.0, 0.0] for c in range(13) ] for r in range(12) ]
		for r in range(12):
			sum_w = 0
			for c in range(13):
				sum_w += self.prob_w[r][c]
			start = 0.0
			for c in range(13):
				p = self.prob_w[r][c] / sum_w
				self.prob[r][c][0] = start
				self.prob[r][c][1] = start + p
				start = start + p
		self.start = st
		self.stato = 0
		
	def next(self):
		ok = False
		row = self.stato % 12
		#print("row", row)
		while ok == False:
			rx = random.uniform(0,1)
			col = random.randint(0, 12)
			if rx >= self.prob[row][col][0] and rx < self.prob[row][col][1]:
				val = self.start + self.stato + col
				if val >= 0 and val <= 127:
					self.stato = self.stato + col
					return val
					
class scala:
	def __init__(self, sc="101011010101", dist="uniform", ini=40, octaves=2):
		if len(sc) != 12:
			raise RuntimeError("Not valid Scale string")
		self.scale1 = [ int(x) for x in sc ]
		self.scale = [ i for i in range(len(sc)) if self.scale1[i] == 1 ]
		self.length = self.scale1.count(1)
		self.min = -octaves * self.length
		self.max = octaves * self.length
		self.dist = dist
		self.stato = 0
		self.start = ini
		#print("length", self.length)
		#print("scale", self.scale)
		
	def next(self):
		if self.dist == "uniform":
			rn = random.uniform(-1,1)
		elif self.dist == "tri":
			rn = random.triangular(-1,1)
		elif self.dist == "gauss":
			rn = random.gauss(0, 0.5)
			if rn < -0.99:
				rn = -0.99
			if rn > 0.99:
				rn = 0.99
		ndx = int(rn * self.length)
		self.stato = self.stato + ndx
		if( self.stato < self.min ):
			self.stato = self.min
		if( self.stato > self.max ):
			self.stato = self.max
		octave = self.stato // self.length
		note = self.stato % self.length
		#print(self.stato, octave, note)	
		return self.start + self.scale[note] + octave * 12
			