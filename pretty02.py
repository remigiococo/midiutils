from prettymidiutils import *
import random

def test01():
	c = setup_composition(nbars=4)
	#print(c)
	#print(c.instruments)
	#print(c.instruments[0].notes)

	for i in c.instruments:
		i.program = random.randint(1, 100)
		p = 64
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
	sc = [0,2,5,7,9]
	base_pitch=64
	for i in c.instruments:
		i.program = random.randint(1, 100)
		for n in i.notes:
			p = base_pitch + rm.extract_note_tri(sc, interval=3)
			v = random.randint(100, 127)
			n.pitch = p
			n.velocity = v
	# print(c.instruments[0].notes)
	c.write("testrand02.mid")
	
test02()