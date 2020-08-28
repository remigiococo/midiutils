from prettymidiutils import *
import random
import mido

def play_file(nomefile, scelta=False):
	m=mido.MidiFile(nomefile)
	if m:
		nomi=mido.get_output_names()
		if nomi:
			if scelta:
				print("Midi Ports:")
				i = 0
				for p in nomi:
					print(i, " -- ", p)
					i = i+1
				pnum = int(input("select:"))
			else:
				pnum = 0
			print("opening Midi port: ", nomi[pnum])
			port=mido.open_output(nomi[pnum])
			if port:
				try:
					[port.send(x) for x in m.play()]
				except KeyboardInterrupt:
					print("stopped")

def test01():
	c = setup_composition(nbars=4)
	#print(c)
	#print(c.instruments)
	#print(c.instruments[0].notes)

	for i in c.instruments:
		i.program = random.randint(1, 100)
		p = 48
		for n in i.notes:
			p = p + random.randint(-2, 2)
			v = random.randint(100, 127)
			n.pitch = p
			n.velocity = v
	print(c.instruments)
	#print(len(c.instruments[0].notes))		
	print(c.instruments[0].notes)
	print(c.instruments[1].notes)
	c.write("testrand01.mid")

def test02():
	c = setup_composition(nbars=8)
	rm = randmel()
	sc = [0,2,5,7,9] # esatonica 1
	sc = [0,2,4,5,7,9,11] # maggiore
	sc = [0,2,3,5,7,8,10] # minore nat.
	sc = [0,2,3,5,7,8,11] # minore arm.
	sc = [0,2,3,7,10] # esatonica 2
	base_pitch=48
	for i in c.instruments:
		i.program = random.randint(1, 100)
		for n in i.notes:
			p = base_pitch + rm.extract_note_tri(sc, interval=2)
			v = random.randint(0, 127)
			n.pitch = p
			n.velocity = v
	# print(c.instruments[0].notes)
	c.write("testrand02.mid")
	play_file("testrand02.mid", True)
	
test02()