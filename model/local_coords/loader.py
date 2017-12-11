from data_structures import *

def load_event(file_path, max_hits_per_chip=65536):
    FEC = None
    board = None
    chip = None
    
    skip_this_chip = False
    
    with open(file_path) as infile:
        ev = Event(75)
        for line in infile:
            if not skip_this_chip and line[0].isdigit():  # hit parameters: x, y, value (charge or time)
                xp, yp, value = [int(s) for s in line.split()]
                ev.add_hit(Hit(FEC, board, chip, xp, yp, value))
                
            elif line[0] == 'C':  # Chip id, e.g.: Chip 3 ,Hits: 11 
                nhits = int(line.split()[-1])
                if nhits <= max_hits_per_chip:
                    chip = int(line.split()[1])
                    skip_this_chip = False
                else:
                    skip_this_chip = True
                    
            elif line[0] == 'B':  # Board id, e.g.: Board 0
                board = int(line.split()[-1])
                
            elif line[0] == 'F':  # FEC id, e.g.: FEC 0
                FEC = int(line.split()[-1])

    return ev

def display_event(event):
    for h in event.hits:
        print(h)


