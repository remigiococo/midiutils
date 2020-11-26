import sys
import array
import struct
import pretty_midi
import mido

# gestione file binario
def gestione_file(nomefile):
	ff = open(nomefile, 'r+b')
	ff.seek(0, 2)
	flen = ff.tell()
	ff.seek(0, 0)
	print("total len:", flen)
	data_raw=array.array('B')
	while True:
		b = ff.read(8192) # blocchi di 8k max
		if not b:
			break
		data_raw.frombytes(b)
	if data_raw[0:4] != array.array('B', [ord(x) for x in "AC07"]):
		print("not AC7 format !!!", data_raw[0:4])
		sys.exit(0)
	dlen = struct.unpack('H', data_raw[4:6])[0]
	print("data len:", dlen)
	parse_mixr(data_raw, 6)
	parse_drum(data_raw, 6)
	parse_othr(data_raw, 6)
	#ff.seek(4, 0)
	#ff.write(struct.pack('l', dlen+36))
	#ff.seek(40, 0)
	#ff.write(struct.pack('l', dlen))
	ff.close()
	
def parse_mixr(raw, offset=0):
	i = offset
	max_i = len(raw[i:]) - 4
	while (i < max_i) and ( raw[i:i+4] != array.array('B', [ord(x) for x in "MIXR"]) ):
		i = i + 1
	start_mixr = i	
	print("found MIXR at offset:", start_mixr, hex(start_mixr))
	i = i + 4
	mlen = struct.unpack('H', raw[i:i+2])[0]
	print("mixr section len:", mlen)
	i = i + 4
	nsect = struct.unpack('H', raw[i:i+2])[0]
	print("n. sections:", nsect)
	mlen_eff = mlen - 10 # tolti 4 byte  "MIXR", 4 byte di lunghezza, 2 byte di num. sezioni
	mlen_eff = mlen_eff - (nsect*4) # tolti gli offset
	sectlen = mlen_eff // nsect
	print("section length:", sectlen)
	i = i + 2
	sect_offs = []
	for j in range(nsect):
		offs = struct.unpack('L', raw[i:i+4])[0]
		sect_offs.append(offs)
		i = i + 4
	# final offset
	sect_offs.append(start_mixr + mlen)	
	print([hex(x) for x in sect_offs]) # debug
	for j in range(nsect):
		print("MIXR Sect. #", j+1)
		i = sect_offs[j]
		while i < sect_offs[j+1]:
			b = [raw[i+k] for k in range(sectlen)]
			print(b) # debug	
			i = i + sectlen	
	
def parse_drum(raw, offset=0):
	global SAVE_MIDI
	if SAVE_MIDI:
		mf = mido.MidiFile()
		mf.ticks_per_beat = 96
		trk = mido.MidiTrack()
		trk.channel = 9
		trk.name = "t1"
	i = offset
	max_i = len(raw[i:]) - 4
	while (i < max_i) and ( raw[i:i+4] != array.array('B', [ord(x) for x in "DRUM"]) ):
		i = i + 1
	start_drum = i	
	print("found DRUM at offset:", start_drum, hex(start_drum))	
	i = i + 4
	dlen = struct.unpack('H', raw[i:i+2])[0]
	print("drum section len:", dlen)
	i = i + 4
	nsect = struct.unpack('H', raw[i:i+2])[0]
	print("n. sections:", nsect)
	i = i + 2
	sect_offs = []
	for j in range(nsect):
		offs = struct.unpack('L', raw[i:i+4])[0]
		sect_offs.append(offs)
		i = i + 4
	# final offset
	sect_offs.append(start_drum + dlen)	
	print([hex(x) for x in sect_offs]) # debug
	for j in range(nsect):
		print("DRUM Sect. #", j+1)
		i = sect_offs[j]
		while i < sect_offs[j+1]:
			b1 = raw[i]
			b2 = raw[i+1]
			b3 = raw[i+2]
			dr = '{0:24s}'.format(pretty_midi.note_number_to_drum_name(b2))
			print("time: ", b1, "\tnote: ", b2, "\t", dr, "\tvel: ", b3)
			if SAVE_MIDI:
				if (b2 <= 127):
					mm = mido.Message('note_on', note=b2, time=b1, velocity=b3) # note off ???
					mm.channel = 9
					trk.append(mm)
				elif (b2 < 250):
					mm = mido.Message('note_on', note=0, time=b1, velocity=0) # note non gestite - pause ???
					mm.channel = 9
					trk.append(mm)
			i = i + 3
	if SAVE_MIDI:
		mf.tracks.append(trk)
		mf.save("test.mid")

def parse_othr(raw, offset=0):
	global SAVE_MIDI
	if SAVE_MIDI:
		mf = mido.MidiFile()
		mf.ticks_per_beat = 96
		trk = mido.MidiTrack()
		trk.channel = 0
		trk.name = "t1"
	i = offset
	max_i = len(raw[i:]) - 4
	while (i < max_i) and ( raw[i:i+4] != array.array('B', [ord(x) for x in "OTHR"]) ):
		i = i + 1
	start_othr = i	
	print("found OTHR at offset:", start_othr, hex(start_othr))	
	i = i + 4
	dlen = struct.unpack('H', raw[i:i+2])[0]
	print("othr section len:", dlen)
	i = i + 4
	nsect = struct.unpack('H', raw[i:i+2])[0]
	print("n. sections:", nsect)
	i = i + 2
	sect_offs = []
	for j in range(nsect):
		offs = struct.unpack('L', raw[i:i+4])[0]
		sect_offs.append(offs)
		i = i + 4
	# final offset
	sect_offs.append(start_othr + dlen)	
	print([hex(x) for x in sect_offs]) # debug
	for j in range(nsect):
		print("OTHR Sect. #", j+1)
		i = sect_offs[j]
		while i < sect_offs[j+1]:
			b1 = raw[i]
			b2 = raw[i+1]
			b3 = raw[i+2]
			if b2 <= 120:
				dr = '{0:6s}'.format(pretty_midi.note_number_to_name(b2))
			else:
				dr = "######"
			print("time: ", b1, "\tnote: ", b2, "\t", dr, "\tvel: ", b3)
			if SAVE_MIDI: 
				if (b2 <= 127):
					mm = mido.Message('note_on', note=b2, time=b1, velocity=b3) # note off ???
					mm.channel = 0
					trk.append(mm)
				elif (b2 < 250):
					mm = mido.Message('note_on', note=0, time=b1, velocity=0) # note non gestite - pause ???
					mm.channel = 0
					trk.append(mm)
			i = i + 3
	if SAVE_MIDI:
		mf.tracks.append(trk)
		mf.save("test2.mid")

SAVE_MIDI = True		
if len(sys.argv) > 1:
	gestione_file(sys.argv[1])
