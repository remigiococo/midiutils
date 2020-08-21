from prettymidiutils import *
import random

def test1():
	rd = randdrum(16, 32, 104)
	rd.set_kit(25)
	#------------------|---|---|---|---
	rd.base_str("bd", "1000100010001000")
	rd.base_str("sn", "0000100000001000")
	rd.base_str("ch", "0010001000100010")
	#
	rd.set_var("ch", [1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,
	 1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4])
	rd.gen("testrd1.mid")

def test2():
	rd = randdrum(16, 32, 152)
	rd.set_kit(25)
	#------------------|---|---|---|---
	rd.base_str("bd", "1000000010000000")
	rd.base_str("sn", "0000001000001000")
	rd.base_str("ch", "1011101010111010")
	#rd.base_str("oh", "0010001000100010")
	#
	rd.set_var("ch", [2 for i in range(32)])
	rd.gen("testrd2.mid")

def test3():
	rd = randdrum(32, 32, 152, 8)
	rd.set_kit(25)
	#------------------|---|---|---|---|---|---|---|---
	rd.base_str("bd", "10000000000000001000000000000000")
	rd.base_str("sn", "00000000000010000000000010000000")
	rd.base_str("ch", "10001000100010001000100010001000")
	#
	#rd.set_var("ch", [2 for i in range(32)])
	rd.gen("testrd3.mid")

def test4():
	rd = randdrum(32, 32, 152, 128)
	rd.set_kit(25)
	#------------------|---|---|---|---|---|---|---|---
	rd.base_str("bd", "10000000000000001000000000000000")
	rd.base_str("sn", "00000000000010000000000010000000")
	rd.base_str("ch", "10001000100010001000100010001000")
	#
	#rd.set_var("ch", [2 for i in range(32)])
	rd.gen("testrd4.mid")

def test5():
	rd = randdrum(32, 32, 70, 256)
	rd.set_kit(25)
	#------------------|---|---|---|---|---|---|---|---
	rd.base_str("bd", "10000000000000001000000000000000")
	rd.base_str("sn", "00000000100000000000000010000000")
	rd.base_str("ch", "10001000300010001000100010001222")
	#
	rd.set_var("ch", [24 for i in range(32)])
	rd.set_var("bd", [2 for i in range(32)])
	rd.gen("testrd5.mid")

def test6():
	rd = randdrum(16, 32, 70)
	rd.set_kit(25)
	#------------------|---|---|---|---
	rd.base_str("bd", "1000000010000000")
	rd.base_str("sn", "0000100000001000")
	rd.base_str("ch", "1010101210101033")
	#rd.base_str("oh", "0010001000100010")
	#
	rd.set_var("ch", [8 for i in range(32)])
	rd.set_var("bd", [2 for i in range(32)])
	rd.gen("testrd6.mid")

def test7():
	rd = randdrum(32, 32, 64, 32)
	rd.set_kit(25)
	#------------------|---|---|---|---|---|---|---|---
	rd.base_str("bd", "10000010000010000010100000000000")
	rd.base_str("sn", "00000000100000000000000010000000")
	rd.base_str("cl", "00000000100000000000000010000000")
	rd.base_str("oh", "00000010000000000000001000000000")
	rd.base_str("ch", "10001000100011121000100010001222")
	#
	rd.vartype = rd._XOR_VAR_
	rd.set_var("ch", [24 for i in range(32)])
	#rd.set_var("ch", [4 for i in range(32)])
	#rd.set_var("sn", [2 for i in range(32)])
	rd.gen("testrd7.mid")

def test8():
	rd = randdrum(32, 32, 64, 32)
	rd2 = randdrum(24, 32, 64, 32)
	rd.set_kit(25)
	rd2.set_kit(25)
	#------------------|---|---|---|---|---|---|---|---
	rd.base_str("bd", "10000010000010000010100000000000")
	rd.base_str("sn", "00000000100000000000000010000000")
	rd.base_str("cl", "00000000100000000000000010000000")
	rd.base_str("oh", "00000010000000000000001000000000")
	rd.base_str("ch", "10001000100010001000100010001000")
	#
	#
	# variazione - 24 steps
	#-------------------|--|--|--|--|--|--|--|--
	rd2.base_str("ch", "100100100111100100100222")
	#
	#rd2.vartype = rd._XOR_VAR_
	rd2.set_var("ch", [12 for i in range(32)])
	#rd.set_var("ch", [4 for i in range(32)])
	#rd.set_var("sn", [2 for i in range(32)])
	rd2.gen()
	rd.gen()
	rd.merge(rd2)
	rd.save("testrd8.mid")

def test9():
	nbars=32
	tempo=68
	rd = randdrum(32, nbars, tempo, 32) # nsteps, nbars, tempo, dur.
	rd2 = randdrum(8, nbars, tempo, 64)
	rd3 = randdrum(16, nbars, tempo, 64)
	rd.set_kit(25)
	rd2.set_kit(25)
	rd3.set_kit(25)
	#------------------|---|---|---|---|---|---|---|---
	rd.base_str("bd", "10000010000010000010100000000000")
	rd.base_str("sn", "00000000100000000000000010000000")
	rd.base_str("cl", "00000000100000000000000010000000")
	rd.base_str("oh", "00000010000000000000001000000000")
	rd.base_str("ch", "10001000100010001000100010001000")
	#
	#
	# variazione closed hats - 8 steps
	rd2.base_str("ch", "00460368")
	# variazione snare - 16 steps
	rd3.base_str("sn", "0006000000030000")
	#
	rd2.vartype = rd._AND_VAR_
	rd2.set_var("ch", [4 for i in range(nbars)])
	#rd.set_var("ch", [4 for i in range(nbars)])
	rd3.vartype = rd._AND_VAR_
	rd3.set_var("sn", [3 for i in range(nbars)])
	rd.gen()
	rd2.gen()
	rd3.gen()
	rd.merge(rd2)
	rd.merge(rd3)
	rd.save("testrd9.mid")
	
#test1()		
#test2()	
test9()	