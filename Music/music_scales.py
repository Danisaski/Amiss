#===================================# 
#      Music scales generator       #
#         Date: 29/10/2021          #
#       Author: Daniel Perez        #
#           Version: 1.0            #
#===================================#===============================#
#                                                                   #
# Explaination: Given the main chord with its respective mode and   #
# alteration (if any), it returns on screen the armonized scale.    #
#                                                                   #
# This program is the first one of the upcoming project, where      #
# different chord progressions and solos will be generated randomly #
# by the code, taking into account all the music theory behind it   #
# in order to make it sound "correctly".                            #
#                                                                   #
# If you ever use this code make sure you at least give credit ;)   #
# Which I doubt because this is one of my first "decent" program    #
# and surely can be done better.                                    #
#===================================================================#

# TODO List:
#   
#   Implement the code with Tkinter for a better interface
#   Random geretation of chord progressions    
#   Random generation of string and fret combinations for a given scale
#

class Chord:
    def __init__(self,note,alt="",mode=""):
        try:
            self.note = note.capitalize()
            self.mode = mode
            if mode == "m":
                self.mode = "m"
            elif mode == "M":
                self.mode = ""
            elif mode == "dim":
                self.mode = "dim"
            elif mode == "":
                self.mode = ""
            else:
                print("Wrong mode")    

            if alt == "s":
                self.alt = "#"
            elif alt == "ss":
                self.alt = "##"
            elif alt == "b":
                self.alt = u"\u266D"
            elif alt == "bb":
                self.alt = u"\u266D" + u"\u266D"
            elif alt == "":
                self.alt = ""
            else:
                self.alt = ""
                print("Wrong alteration")
        except:
            print("Inputs must be; note, mode, alteration (optional)")

    def name(self):
        return self.note.capitalize() +  self.alt + self.mode

    def third(self):
        pass

class Scale:
    def __init__(self,main_note):                       #Initialization of any scale, based on its first (main) chord
        self.main_note = main_note.note
        self.mode = main_note.mode
        self.alt = main_note.alt
        self.chords = [""]*7

        self.chords[0] = main_note

        for i in range(1,7):                            #Operations needed to determine the mode and alterations of each chord            
            if self.chords[0].mode == "":               
                intervals = [1,1,0.5,1,1,1]
                if self.chords[i-1].note == "G":
                    if (i == 3 or i == 4):
                        self.chords[i] = Chord("A",interval(self.chords[i-1].note,"A",intervals[i-1],self.chords[i-1].alt),"")
                    elif i == 6:
                        self.chords[i] = Chord("A",interval(self.chords[i-1].note,"A",intervals[i-1],self.chords[i-1].alt),"dim")
                    else:
                        self.chords[i] = Chord("A",interval(self.chords[i-1].note,"A",intervals[i-1],self.chords[i-1].alt),"m")

                else:
                    if (i == 3 or i == 4):
                        self.chords[i] = Chord(chr(ord(self.chords[i-1].note) + 1),interval(self.chords[i-1].note,chr(ord(self.chords[i-1].note) + 1),intervals[i-1],self.chords[i-1].alt),"")
                    elif i == 6:
                        self.chords[i] = Chord(chr(ord(self.chords[i-1].note) + 1),interval(self.chords[i-1].note,chr(ord(self.chords[i-1].note) + 1),intervals[i-1],self.chords[i-1].alt),"dim")
                    else:
                        self.chords[i] = Chord(chr(ord(self.chords[i-1].note) + 1),interval(self.chords[i-1].note,chr(ord(self.chords[i-1].note) + 1),intervals[i-1],self.chords[i-1].alt),"m")
            
            elif self.chords[0].mode == "m":
                intervals = [1,0.5,1,1,0.5,1]
                if self.chords[i-1].note == "G":
                    if (i == 5 or i == 6 or i == 2):
                        self.chords[i] = Chord("A",interval(self.chords[i-1].note,"A",intervals[i-1],self.chords[i-1].alt),"")
                    elif i == 1:
                        self.chords[i] = Chord("A",interval(self.chords[i-1].note,"A",intervals[i-1],self.chords[i-1].alt),"dim")
                    else:
                        self.chords[i] = Chord("A",interval(self.chords[i-1].note,"A",intervals[i-1],self.chords[i-1].alt),"m")

                else:
                    if (i == 5 or i == 6 or i == 2):
                        self.chords[i] = Chord(chr(ord(self.chords[i-1].note) + 1),interval(self.chords[i-1].note,chr(ord(self.chords[i-1].note) + 1),intervals[i-1],self.chords[i-1].alt),"")
                    elif i == 1:
                        self.chords[i] = Chord(chr(ord(self.chords[i-1].note) + 1),interval(self.chords[i-1].note,chr(ord(self.chords[i-1].note) + 1),intervals[i-1],self.chords[i-1].alt),"dim")
                    else:
                        self.chords[i] = Chord(chr(ord(self.chords[i-1].note) + 1),interval(self.chords[i-1].note,chr(ord(self.chords[i-1].note) + 1),intervals[i-1],self.chords[i-1].alt),"m")                 




    def scale(self):

        #Just prepares a list with the name of the chords to print them

        self.dispchords = []
        for i in range(0,7):
            self.dispchords.append(self.chords[i].name())
        return self.dispchords    

def interval(note1,note2,desired_interval,alt): 

    #   Takes two notes and determines if the second one needs
    #   any alteration in order to fulfill the interval's desired
    #   size, taking into account the alteration (if any) from the first note.


    if (note1 == "B" and note2 == "C") or (note1 == "E" and note2 == "F"):
        interval = 0.5
    else:
        interval = 1
    if alt == "":
        if interval == desired_interval:
            return ""
        elif interval < desired_interval:
            return "s"
        else:
            return "b"
    elif alt == "#":
        interval = interval - 0.5
        if interval == desired_interval:
            return ""
        elif desired_interval - interval == 0.5:
            return "s"
        elif interval - desired_interval == 0.5:
            return "b"
        elif desired_interval - interval == 1:
            return "ss"

    else:
        interval = interval + 0.5
        if interval == desired_interval:
            return ""
        elif desired_interval - interval == 0.5:
            return "s"
        elif interval - desired_interval == 0.5:
            return "b"
        elif interval - desired_interval == 1:
            return "bb"


#========================================================================
#            Introduce the user input to get the scales                 #
#========================================================================

note = "c"                #Note = A, B, C, D, E, F, G
alteration = "s"                 #Alteration = s (sharp), b (flat), "" (no alteration)
mode = "m"                      #Mode = M (major), m (minor), "" (major)

c = Chord(note,alteration,mode)
sc = Scale(c)
print(sc.scale())
