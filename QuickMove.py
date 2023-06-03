
class ERS52Straight:
    def __init__(self, clearance, roller_pitch, zone_length, length, zone_count):
        # Check that parameters are within acceptable ranges
        acceptable_clearances = [420, 520, 620, 820]
        if clearance not in acceptable_clearances:
            raise ValueError(f"Clearance must be one of {acceptable_clearances}")

        acceptable_roller_pitches = [75, 100]
        if roller_pitch not in acceptable_roller_pitches:
            raise ValueError(f"Roller Pitch must be one of {acceptable_roller_pitches}")

        if not (75 <= zone_length <= 1500):
            raise ValueError("Zone Length must be between 75 and 1500 mm")

        if not (75 <= length <= 3000):
            raise ValueError("Length must be between 75 and 3000 mm")

        acceptable_zone_counts = [1, 2, 3, 4]
        if zone_count not in acceptable_zone_counts:
            raise ValueError(f"Zone Count must be one of {acceptable_zone_counts}")

        self.clearance = clearance
        self.roller_pitch = roller_pitch
        self.zone_length = zone_length
        self.length = length
        self.zone_count = zone_count

    def __str__(self):
        return (
            f"ERS52 Straight:\n"
            f"  Clearance: {self.clearance} mm\n"
            f"  Roller Pitch: {self.roller_pitch} mm\n"
            f"  Zone Length: {self.zone_length} mm\n"
            f"  Length: {self.length} mm\n"
            f"  Zone Count: {self.zone_count}"
        )

def calculate_clearance(length, width, orientation):
    acceptable_clearances = [420, 520, 620, 820]

    if orientation == "short side leading":
        tu_width = min(int(length), int(width))
    else:  # tu.orientation == "long side leading"
        tu_width = max(int(length), int(width))

    # Find the smallest clearance that is greater than tu_width
    clearance = min(c for c in acceptable_clearances if c > tu_width)

    return clearance

def calculate_roller_pitch(length, width, orientation):
    acceptable_roller_pitches = [75, 100]

    if orientation == "short side leading":
        tu_leading_side = max(int(length), int(width))
    else:  # tu.orientation == "long side leading"
        tu_leading_side = min(int(length), int(width))

    required_pitch = tu_leading_side / 3

    # Choose the largest pitch that is greater than or equal to required_pitch
    roller_pitch = max(p for p in acceptable_roller_pitches if p <= required_pitch)

    return roller_pitch

def calculate_zone_length(length, width, roller_pitch, orientation):
    if orientation == "short side leading":
        tu_leading_side = max(int(length), int(width))
    else:  # tu.orientation == "long side leading"
        tu_leading_side = min(int(length), int(width))

    # Find a multiple of the roller pitch that is at least as long as the TU
    zone_length = ((tu_leading_side // int(roller_pitch)) + 2) * roller_pitch

    return zone_length

def calcConveyor(length, width, orientation):
     
    clearance = calculate_clearance(int(length), int(width), orientation)
    roller_pitch = calculate_roller_pitch(int(length), int(width), orientation)
    zone_length = calculate_zone_length(int(length), int(width), roller_pitch, orientation)

    myERS52 = ERS52Straight(clearance, roller_pitch, zone_length, 75, 1)

    return myERS52

def parsing_calcConveyor(string):

    length, width, orientation = string.split(",")
    
    orientation = orientation.replace(' "', '')

    return calcConveyor(int(length), int(width), orientation)



