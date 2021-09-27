import os
import numpy as np


class XY_and_Scalars:
    
    def __init__(self):
        
        # initialize all variables to describe wave location
        self.filelocation = None
        self.filefolder = None
        self.filename = None
        self.classname = None

        # initialize all variables loaded in. Assume that 'x,y' for plots are first two.
        self.load = 0

        # initialize all vectors to describe data
        self.vector = 0

        # initialize all scalars to describe data
        self.scalar = 0

        #initialize all lists and dictionaries
        self.Variable = {}
        self.Name = {}
        self.Label = {}
        self.Unit = {}
        self.loadedlist = []
        self.vectorlist = []
        self.scalarlist = []
    


class JVCurve:

    
    # init call
    def __init__(self):

        #create ID (e.g. JV) and initialize load, vector, and scalar to 0
        self.ID = 'JV'
        self.load = 0
        self.vector = 0
        self.scalar = 0
               
    
    # gets neccisary list --> easy to create dummyfile of class and call this for other class organization while saving memory
    def createlists(self):

        # list of all values loaded, all vectors calculated, and all scalars calculated
        self.loadedlist = ['v','j','i','area']
        self.vectorlist = ['p']
        self.scalarlist = ['pce', 'jsc', 'voc', 'ff', 'jmp', 'vmp', 'pmp', 'rs', 'rsh', 'rch']

        # list of variables to caplital variables (good for short hand in UI)
        self.Variable = {'i': 'I',
                      'j': 'J',
                      'v': 'V',
                      'p': 'P',
                      'area': 'A',
                      'jsc': 'Jsc',
                      'voc': 'Voc',
                      'ff': 'FF',
                      'pce': 'PCE',
                      'jmp': 'Jmp',
                      'vmp': 'Vmp',
                      'pmp': 'Pmp',
                      'rs': 'Rs',
                      'rsh': 'Rsh',
                      'rch': 'Rch'}

        # list of variables long hand names (good for long hand)
        self.Name = {'i': 'Current / I (mA)',
                     'j': 'Current Density / J (mA/cm²)',
                     'v': 'Voltage / V (V)',
                     'p': 'Power / P (mW/cm²)',
                     'area': 'Area / A (cm²)',
                     'jsc': 'Short Circuit Current Density / Jsc (mA/cm²)',
                     'voc': 'Open Circuit Voltage / Voc (V)',
                     'ff': 'Fill Factor / FF (%)',
                     'pce': 'Power Conversion Efficiency / PCE (%)',
                     'jmp': 'MPP Current Density / Jmp (mA/cm²)',
                     'vmp': 'MPP Voltage / Vmp (V)',
                     'pmp': 'MPP Power Density / Pmp (mW/cm²)',
                     'rs': 'Series Resistance / Rs (Ω/cm²)',
                     'rsh': 'Shunt Resistance / Rsh (Ω/cm²)',
                     'rch': 'Channel Resistance / Rch (Ω/cm²)'}

        # the opposite on name, i think i could reogranize to remove this
        self.NameRev = {'Current / I (mA)' : 'i',
                        'Current Density / J (mA/cm²)' : 'j',
                        'Voltage / V (V)' : 'v',
                        'Power / P (mW/cm²)' : 'p',
                        'Area / A (cm²)' : 'area',
                        'Short Circuit Current Density / Jsc (mA/cm²)' : 'jsc',
                        'Open Circuit Voltage / Voc (V)' : 'voc',
                        'Fill Factor / FF (%)' : 'ff',
                        'Power Conversion Efficiency / PCE (%)' : 'pce',
                        'MPP Current Density / Jmp (mA/cm²)' : 'jmp',
                        'MPP Voltage / Vmp (V)' : 'vmp',
                        'MPP Power Density / Pmp (mW/cm²)' : 'pmp',
                        'Series Resistance / Rs (Ω/cm²)' : 'rs',
                        'Shunt Resistance / Rsh (Ω/cm²)' : 'rsh',
                        'Channel Resistance / Rch (Ω/cm²)': 'rch'}

        # labels for axis
        self.Label = {'i': 'I (mA)',
                      'j': 'J (mA/cm²)',
                      'v': 'V (V)',
                      'p': 'P (mW/cm²)',
                      'area': 'A (cm²)',
                      'jsc': 'Jsc (mA/cm²)',
                      'voc': 'Voc (V)',
                      'ff': 'FF (%)',
                      'pce': 'PCE (%)',
                      'jmp': 'Jmp (mA/cm²)',
                      'vmp': 'Vmp (V)',
                      'pmp': 'Pmp (mW/cm²)',
                      'rs': 'Rs (Ω/cm²)',
                      'rsh': 'Rsh (Ω/cm²)',
                      'rch': 'Rch (Ω/cm²)'}

        # units -- unused for now but good to keep track of
        self.Unit = {'i': 'mA',
                     'j': 'mA/cm²',
                     'v': 'V',
                     'p': 'mW/cm²',
                     'area': 'cm²',
                     'jsc': 'mA/cm²',
                     'voc': 'V',
                     'ff': '%',
                     'pce': '%',
                     'jmp': 'mA/cm²',
                     'vmp': 'V',
                     'pmp': 'mW/cm²',
                     'rs': 'Ω/cm²',
                     'rsh': 'Ω/cm²',
                     'rch': 'Ω/cm'}


    # loads file from file locaton. This should calc i, j, v, and area for every curve.
    def loadfile(self, filepath):

        #set self.vector to 1 to let program know loadvalues have been calc
        self.load = 1

        # split file path into folder and file name        
        self.filepath = filepath
        self.filefolder, self.filename = os.path.split(self.filepath)
        self.classname = self.filename.split('.', 1)[0]

        # load wave
        file = np.genfromtxt(self.filepath,
                             delimiter=",",
                             unpack=True,
                             skip_header=1)
        
        # break data set into numpy arrays assuming file has v, j, i, and area
        self.v = np.array(file[1])      # Volts
        self.j = np.array(file[2])      # mA/cm^2
        self.i = np.array(file[3])      # A
        self.area = self.i*100/self.j   # cm^2

        # if wave is in quadrant 4 pull to quadrant 1
        if self.j[np.where(np.diff(np.signbit(self.v)))[0]] < 0:
            self.i *= -1
            self.j *= -1

# Note to Rishi: if self.j[np.argmin(np.abs(self.v))] < 0: will flag even if we dont cross 0. in this instance we want to flag only if it does


    # calc vectors: p
    def calcvectors(self):

        # set self.vector to 1 to let program know vectors have been analyzed
        self.vector = 1
        
        # calc p
        self.p = self.v * self.j


    # calc scalars: jsc, voc, ff, pce, jmp, vmp, pmp, rs, rsh, rch
    def calcscalars(self):

        # set self.vector to 1 to let program know vectors have been analyzed
        self.scalar = 1

        # get locations v (j0) and j (v0) cross 0
        wherevis0 = np.where(np.diff(np.signbit(self.v)))[0]
        wherejis0 = np.where(np.diff(np.signbit(self.j)))[0]

        #if we have more than 1 crossing, set all scalars we could calculate to NaN & let user know trace is bad
        if len(wherevis0) != 1 or len(wherejis0) != 1:
            print(self.filename + " is bad")
            self.jsc = None
            self.voc = None
            self.ff = None
            self.pce = None            
            self.jmp = None
            self.vmp = None
            self.pmp = None
            self.rs = None
            self.rsh = None
            self.rch = None 

        #otherwise calculate statistics
        else:

            # calculate Voc & Rs using point before 0 value, point after 0 value, and linear interp
            j1 = self.j[wherevis0]
            j2 = self.j[wherevis0 + 1]
            v1 = self.v[wherevis0]
            v2 = self.v[wherevis0 + 1]
            m = (j2 - j1) / (v2 - v1)
            b = j1 - m * v1
            self.rsh = float(abs(1 / m))
            self.jsc = float(b)

            # calculate Jsc & Rsh using point before 0 value, point after 0 value, and linear interp
            j1 = self.j[wherejis0]
            j2 = self.j[wherejis0 + 1]
            v1 = self.v[wherejis0]
            v2 = self.v[wherejis0 + 1]
            m = (j2 - j1) / (v2 - v1)
            b = j1 - m * v1
            self.rs = float(abs(1 / m))
            self.voc = float(-b / m)

            # calculate Pmp, Vmp, Jmp
            self.pmp = np.max(self.p)
            pmaxloc = np.argmax(self.p)
            self.vmp = self.v[pmaxloc]
            self.jmp = self.j[pmaxloc]

            # calculate Rch using point before max val, point after max val, and linear interp
            j1 = self.j[pmaxloc - 1]
            j2 = self.j[pmaxloc + 1]
            v1 = self.v[pmaxloc - 1]
            v2 = self.v[pmaxloc + 1]
            m = (j2 - j1) / (v2 - v1)
            self.rch = float(abs(1 / m))

            # calculate FF
            self.ff = 100 * self.pmp / (self.voc * self.jsc)

            # calculate PCE
            self.pce = self.ff * self.jsc * self.voc / 100

# Ignore this for now!        
    # takes in list of scalar variables (e.g. ff, rs) returns a list of parameter values
#        def getparamvalsold(self, inputvallist):
#            if inputvallist[0].find('all') != -1:
#                returnstring = [0]*len(self.scalarlist)
#                for ii, item in enumerate(self.scalarlist):
#                    returnstring[ii]=eval('self.' + item)
#            else:
#                returnstring = np.zeros(len(inputvallist))
#                for ii, item in enumerate(inputvallist):
#                    returnstring[ii] = eval('self.' + item)
#            return returnstring


    # takes in list of scalar variables (e.g. ff, rs) returns a list of parameter values
    # the change here is that it outputs data with 1 row and many columns, rather than many rows and 1 column. 
    def getparamvals(self, inputvallist):
        if inputvallist[0].find('all') != -1:
            returnstring = np.zeros(0,len(self.scalarlist))
            for ii, item in enumerate(self.scalarlist):
                returnstring[ii]=eval('self.' + item)
        else:
            returnstring = np.zeros(len(inputvallist))
            for ii, item in enumerate(inputvallist):
                returnstring[ii] = eval('self.' + item)
        return returnstring
