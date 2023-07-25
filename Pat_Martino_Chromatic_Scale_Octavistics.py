# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 20:20:28 2022

@author: Frank
"""
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

# Arbitrary assignment of notes to integers
#
# 0:'C', 1:'C#', 2:'D', 3:'D#', 4:'E', 5:'F',
# 6:'F#', 7:'G', 8:'G#', 9:'A', 10:'A#', 11:'B'
#

# String Set
# A regular 6 string guitar,
# The open string notes are E, B, G, D, A, E; respectively to strings 1 to 6
# The keys of stringSet are the string numbers.
# The list of each key stores the integer representation of the note,
# the note, and the frequnecy in Hz of the note
#
stringSet = {1:[4, 'E', 329.63],
             2:[11, 'B', 246.94],
             3:[7, 'G', 196.00],
             4:[2, 'D', 146.83],
             5:[9, 'A', 110.00],
             6:[4, 'E', 82.41]}

# Choose ascending patterns
# Comment out the descending stuff
# Chromatic scale going up
direction = 'ascend'

# Define an area of activity on the fretboard (start fret, end fret)  
fretRange = (2,5)

# Starting note B, the integer representation
start = 11

# Pat's ascending pattern (string, fret) 
martino = [(5, 2), (3, 5), (5, 4),
            (2, 3), (2, 4), (4, 2),
            (4, 3), (1, 2), (1, 3),
            (6, 4), (6, 5), (3, 3),
            (3, 4)]    

# # Choose descending patterns
# # Comment out the ascending stuff
# # Chromatic scale going down
# direction = 'descend'

# # Define an area of activity on the fretboard (start fret, end fret)  
# fretRange = (9,14)

# # Starting note B, the integer representation
# start = 4

# # Pat's descending pattern according to Chuck
# martino = [(1,12), (6,11), (4,12),
#             (1,9), (2,13), (4,9),
#             (2,11), (5,12), (5,11),
#             (3,12), (1,14), (3,10),
#             (3,9)]

def fretboardAreaNotesGen(stringSet, fretRange):
    '''
    Parameters
    ----------
    stringSet : List
        The list of open strings of the instrument.
    fretRange : tuple
        The two integers in the tuple defines the 
        start and stop frets in the 'area of activity'

    Returns
    -------
    fretboardArea : list of lists
        Each list within the list represents a string. 
        Withing each list, are the notes defined within 
        fretRange
    '''
    fretboardAreaNotes = {}
    fretSpan = fretRange[1] - fretRange[0] + 1
    fretStart = fretRange[0]
    for string in stringSet.keys():
        openStringNote = stringSet[string][0]
        fretboardAreaNotes[string]=list((np.arange(fretSpan)+fretStart+openStringNote)%12)
    return fretboardAreaNotes    
        
fretboardAreaNotes = fretboardAreaNotesGen(stringSet, fretRange)

def stringFretComboGen(startNote, fretRange, fretboardAreaNotes, direction='ascend'):
    '''
    Parameters
    ----------
    startNote : int
        The integer representation of the starting note.
    fretboardAreaNotes : list of list of integers
        The lists represent the strings of the defined fretboard.
        The integers within each list are the integer
        representation of the notes on that string for each
        fret in the defined range of frets
    direction: 'ascend' or whatever

    Returns
    -------
    stringFretCombo : list of lists of tuples
        The lists represent the starting note and subsequent 
        chromatic notes. There are 13 lists since the ocatave is 
        included.  Within each list, are tuples of possible 
        (string, fret) combination in their integer representation.

    '''
    if direction == 'ascend':
        patDir = 1
    else:
        patDir = -1
        
    stringFretCombo=[]
    currentNote = startNote
    for _ in range(13) :
        noteLst = []
        for string in fretboardAreaNotes.keys():
            notes = fretboardAreaNotes[string]
            if currentNote in notes:
                fret = notes.index(currentNote) + fretRange[0]
                noteLst.append((string, fret))
        stringFretCombo.append(noteLst)        
        currentNote = (currentNote + patDir) % 12
    return stringFretCombo

startNote = start
stringFretCombo = stringFretComboGen(startNote, fretRange, fretboardAreaNotes, direction)  

def patternsGen(stringFretCombo):
    '''
    All possible patterns of the chromatic scale from the
    defined starting note, starting fret, and fret span are
    collected into lists of tuples

    Parameters
    ----------
    stringFretCombo : list of lists of tuples
        The lists represent the starting note and subsequent 
        chromatic notes. There are 13 lists since the ocatave is 
        included.  Within each list, are tuples of possible 
        (string, fret) combination in their integer representation.

    Returns
    -------
    patterns : list of lists of tuples
        Each list represents a pattern of the chromatic scale
        in the previously defined fretboard area.
        The tuples in each list are the (string, fret) of 
        the chromatic scale.

    '''
    patterns=[]
    chromaLst = []
     
    def recur(noteIndex):
        '''
        Parameters
        ----------
        noteIndex : int
            The integer representing the starting note.
        
        Returns
        -------
        None.
    
        '''
        if noteIndex == 13:
            # Once thenoteIndex is 13, the octave cycle
            # is complete with the octave note included  
            patterns.append(chromaLst.copy())
            return
        else:
            for note in stringFretCombo[noteIndex]:
                chromaLst.append(note)
                recur(noteIndex + 1)
                chromaLst.pop()                
    recur(0)
    return patterns

patterns = patternsGen(stringFretCombo)

def permCalc(stringFretCombo):
    combo=1
    for notes in stringFretCombo:
        combo = combo * len(notes)
    print('There are',combo, 'different patterns')
    
permCalc(stringFretCombo)

def findPatMartinoPattern(patterns):
    '''
    Find the Pat Martino pattern (PMP) in all possible 
    patterns generated based on the starting note, 
    starting fret, and fret span

    Parameters
    ----------
    patterns : patterns
        All possible patterns found by 'patternsGen'

    Returns
    -------
    The index pointing to PMP in patterns

    '''
   
    PMPI = 0
    for patI, testPat in enumerate(patterns):
        test = 1
        for I, stringFretI in enumerate(testPat):
            if martino[I] != stringFretI:
                test = 0
                break
        if test == 1:
            print("Pat Martino's pattern is at index",patI)
            PMPI = patI
            break
    return PMPI    

pat_index = findPatMartinoPattern(patterns)
pattern = patterns[pat_index]

def fretboardPlot(pattern, stringSet, fretRange):
    plt.clf()
  
    # Y-Axis Info
    numStrings = len(stringSet)
    yAxNum = np.arange(-1*numStrings, 0, 1)
    yAxNote = []
    for string in stringSet.keys():
        yAxNote.append(stringSet[string][1])
    yAxNote.reverse() 
    
    # X-Axis Info
    if fretRange[0] - 3 < 0:
        xAxStart = 0
    else:
        xAxStart = fretRange[0] - 2
    xAxStop = fretRange[1] + 3
    xAx = np.arange(xAxStart, xAxStop)
    
    for i, stringFret in enumerate(pattern):
        # string
        y = stringFret[0]
        # fret
        x = stringFret[1]
        # consider the case that start and end are the same note
        if i == len(pattern)-1 and stringFret == pattern[0]:
            plt.text(x + 0.1, -1*y, '1, '+str(i+1))           
        else:
            plt.text(x + 0.1, -1*y, i+1)
        plt.scatter(x, -1*y)
    
    plt.xticks(xAx)    
    plt.yticks(yAxNum, yAxNote)
    plt.grid()
    plt.show()

fretboardPlot(pattern, stringSet, fretRange)

def playChromaticPattern(pattern, stringSet, fs, noteDuration, cycles, direction='ascend'):
    timeArray = np.arange(0, noteDuration, 1/fs)
    noteLength = len(timeArray)
    cycleLength = noteLength*len(pattern)
    buffer = np.zeros(cycleLength*cycles)
    windowArray = np.hanning(len(timeArray))   
    for cycle in range(cycles):
        for I, stringFret in enumerate(pattern): 
            string = stringFret[0]
            if direction == 'ascend':
                fret = stringFret[1] + cycle
            else:
                fret = stringFret[1] - cycle
            
            freq = stringSet[string][2]*((2**(1/12))**fret) 
            note = (2**15-1)*np.sin(2*np.pi*freq*timeArray)
            noteWindowed = note*windowArray
            buffer[I*noteLength + cycleLength*cycle : 
                    (I+1)*noteLength + cycleLength*cycle] = noteWindowed      
    buffer = buffer.astype(np.int16)
    sd.play(buffer, fs)
    #sd.stop()

# Sampling frequency in Hz
fs = 44100

# Duration of each note in seconds
noteDuration = .2

# Number of times to repeat the pattern at half step lower (descending)
# or higher (ascending)
cycles = 5

playChromaticPattern(pattern, stringSet, fs, noteDuration, cycles, direction)    