"""Module containing the data for various IGM metal lines.
Species covered are:
H, He,C, N, O, Ne, Mg, Si, Fe
Reads the data from VPFIT's atom.dat file
Ions are:

"""

import re

class LineData:
    """Class to aggregate a number of lines from VPFIT tables"""
    def __init__(self, vpdat = "atom.dat"):
        self.species = ('H', 'He', 'C', 'N', 'O', 'Ne', 'Mg', 'Si', 'Fe')
        #Put in the masses by hand for simplicity
        self.masses = ( 1.00794,4.002602,12.011,14.00674,15.9994,20.18,24.3050,28.0855,55.847 )
        #9 empty lists, one list per species
        self.lines = [[]]*9
        self.read_vpfit(vpdat)

    def read_vpfit(self,vpdat):
        """Read VPFIT's atom.dat file for the 9 species"""
        vp = open(vpdat)
        inline = vp.readline()
        while inline != "":
            (specie, ion) = find_species(inline)
            #is this a line we care about?
            if self.species.count(specie) == 0 or ion < 0:
                continue
            (sigma_X, gamma_X, lambda_X) = parse_line_contents(inline)
            line = Line(ion, sigma_X, gamma_X, lambda_X)
            self.lines[specie].append(line)

    def get_line(self,specie, ion):
        """Get data for a particular line.
        specie: number of species, ion: ionisation number (from 0)"""
        lines = self.lines[specie]
        for ll in lines:
            if ll.ion == ion:
                return ll
        raise ValueError("Ion not found")

class Line:
    """Class to store the parameters of a single line"""
    def __init__(self, ion, sigma_X, gamma_X, lambda_X):
        self.ion = ion
        self.sigma_X = sigma_X
        self.gamma_X = gamma_X
        self.lambda_X = lambda_X

def find_species(line):
    """Parse a line to find which species it is: species is given by first two characters, unless the second character is a capital.
    There may be whitespace.
    Ionisation number is then a capital letter followed by three characters."""
    #Match a capital and possibly a lower case, followed by a capital followed by any three characters.
    mat = re.match(r"([A-Z]\s*[a-z]?)([A-Z].{3})",line)
    species = re.sub(r"\s","",mat.groups()[0])
    ion = mat.groups()[1]
    ion = re.sub(r"\s","",mat.groups()[1])
    try:
        ion_r = roman_to_int(ion)
    except ValueError:
        #This is some special ion species, probably with a *.
        ion_r = -1
    return (species, ion_r)

def parse_line_contents(line):
    """Extract the sigma, gamma, lambda and m from the line:
       just read until we get something looking like a float and then store the first three of them"""
    #Split by spaces
    spl = line.split()
    res = []
    for ss in spl:
        try:
            float(ss)
            res.append(float(ss))
        except ValueError:
            pass
        if len(res) == 3:
            break
    return res



def roman_to_int(roman):
    """
    Convert a roman numeral to an integer.

    >>> r = range(1, 4000)
    >>> nums = [int_to_roman(i) for i in r]
    >>> ints = [roman_to_int(n) for n in nums]
    >>> print r == ints
    1

    >>> roman_to_int('VVVIV')
    Traceback (most recent call last):
     ...
    ValueError: roman is not a valid roman numeral: VVVIV
    >>> roman_to_int(1)
    Traceback (most recent call last):
     ...
    TypeError: expected string, got <type 'int'>
    >>> roman_to_int('a')
    Traceback (most recent call last):
     ...
    ValueError: roman is not a valid roman numeral: A
    >>> roman_to_int('IL')
    Traceback (most recent call last):
     ...
    ValueError: roman is not a valid roman numeral: IL

    Thanks Paul Winkler, on the internet.
    """
    if type(roman) != type(""):
        raise TypeError, "expected string, got %s" % type(roman)
    roman = roman.upper()
    nums = ['M', 'D', 'C', 'L', 'X', 'V', 'I']
    ints = [1000, 500, 100, 50,  10,  5,   1]
    places = []
    for c in roman:
        if not c in nums:
            raise ValueError, "roman is not a valid roman numeral: %s" % roman
    for i in range(len(roman)):
        c = roman[i]
        value = ints[nums.index(c)]
        # If the next place holds a larger number, this value is negative.
        try:
            nextvalue = ints[nums.index(roman[i +1])]
            if nextvalue > value:
                value *= -1
        except IndexError:
            # there is no next place.
            pass
        places.append(value)
    tot = 0
    for n in places:
        tot += n
    return tot