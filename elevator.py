#!/usr/bin/python
import sys

def parse_commandline():
    if len(sys.argv) > 2:
        return sys.argv[1], sys.argv[2].lower()
    print "usage: elevator filename mode"
    print "examples:"
    print ">elevator ~/myinputfile a"
    print ">elevator ~/myinputfile b"
    return None, None

def read_file(filename):
    with open(filename, "r") as f:
        lines = f.read().strip().splitlines()
        return lines      

def move(start, destination):
    count = abs(start - destination)
    return count, destination

def mode_a(line):
    total = 0
    start = line.start
    print start,
    for trip in line.trips:
        if start != trip.entry_floor:
            print trip.entry_floor,
        print trip.exit_floor,
        count, start = move(start, trip.entry_floor)
        total += count
        count, start = move(start, trip.exit_floor)
        total += count
    print '(%s)' % total

def mode_b(line):
    total = 0
    start = line.start
    print start,
    for transit in line.transits:
        floors = transit.floors()
        for floor in floors:
            if floor != start:
                print floor,
            count, start = move(start, floor)
            total += count
    print '(%s)' % total
    
class Line(object):
    # handle a line of test input
    def __init__(self, data):
        parts = data.split(":")
        self.start = int(parts[0])
        self.trips = self._parse_trips(parts[1])
        self.transits = self._parse_transits(self.trips)        

    def _parse_trips(self, data):
        trips = []
        items = data.split(',')
        for item in items:
            trips.append(Trip(item))
        return trips
    
    def _parse_transits(self, trips):
        transits = []
        transit = Transit()
        transits.append(transit)
        for trip in trips:
            if transit.added(trip):
                continue
            transit = Transit()
            transits.append(transit)
            transit.added(trip)
        return transits
      
class Trip(object):
    # represents one elevator trip
    def __init__(self, data):
        items = data.split('-')
        self.entry_floor = int(items[0])
        self.exit_floor = int(items[1])
        if self.entry_floor < self.exit_floor:
            self.direction = 'up'
        else:
            self.direction = 'down'

class Transit(object):
    # represents a series of trips that are all in the same direction
    # combined into a series of unique ordered floor stops.
    def __init__(self):
        self.direction = None
        self._values = set()
    def added(self, trip):
        if self.direction == None or self.direction == trip.direction:
            self.direction = trip.direction
            self._values.add(trip.entry_floor)
            self._values.add(trip.exit_floor)
            return True
        return False
    def floors(self):
        temp = []
        temp.extend(self._values)
        if self.direction == 'up':
            temp.sort()
        else:
            temp.sort(reverse=True)
        return temp
        
def main(mode, filename):
    lines = read_file(filename)
    for data in lines:
        line = Line(data)
        if mode == 'a':
            mode_a(line)
        else:
            mode_b(line)
        
filename, mode = parse_commandline()

if mode != 'a' and mode != 'b':
    print 'The mode command line argument should be either "a" or "b" (without any quotes).'
else:
    main(mode, filename)

