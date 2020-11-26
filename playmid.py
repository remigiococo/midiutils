import sys
import mido

def play_file(nomefile, scelta=False, porta=None):
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
				if porta != None:
					print( "port number: ", porta )
					pnum = porta
				else:
					pnum = -1
					for nn in range(len(nomi)):
						if "VirtualMIDI" in nomi[nn]:
							pnum = nn
							break
					if pnum == -1:		
						pnum = 0
			print("opening Midi port: ", nomi[pnum])
			port=mido.open_output(nomi[pnum])
			if port:
				try:
					[port.send(x) for x in m.play()]
				except KeyboardInterrupt:
					print("stopped")

lsys = len(sys.argv)					
if lsys == 2:
	play_file(sys.argv[1], True)
elif lsys == 3:
	if sys.argv[2] in list("0123456789"):
		play_file(sys.argv[1], scelta=False, porta=int(sys.argv[2]))
	else:
		play_file(sys.argv[1], scelta=False)
		