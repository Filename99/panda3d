"""
EntryScale Class: Scale with a label, and a linked and validated entry
"""

from Tkinter import *
import Pmw
import string
from tkSimpleDialog import askfloat

class EntryScale(Pmw.MegaWidget):
    "Scale with linked and validated entry"
 
    def __init__(self, parent = None, **kw):

        # Define the megawidget options.
        optiondefs = (
            ('initialValue',        0.0,           Pmw.INITOPT),
            ('resolution',          0.001,         None),
            ('command',             None,          None),
            ('min',                 0.0,           self._updateValidate),
            ('max',                 100.0,         self._updateValidate),
            ('text',                'EntryScale',  self._updateLabelText),
            ('significantDigits',   2,             self._setSigDigits),
            )
        self.defineoptions(kw, optiondefs)
 
        # Initialise superclass
        Pmw.MegaWidget.__init__(self, parent)

        # Initialize some class variables
        self.value = self['initialValue']
        self.entryFormat = '%.2f'

        # Create the components.

        # Setup up container
        interior = self.interior()
        interior.configure(relief = GROOVE, borderwidth = 2)

        # Create a label and an entry
        self.labelFrame = self.createcomponent('frame', (), None,
                                               Frame, interior)
        # Create an entry field to display and validate the entryScale's value
        self.entryValue = StringVar()
        self.entryValue.set(self['initialValue'])
        self.entry = self.createcomponent('entryField',
                                          # Access widget's entry using "entry"
                                          (('entry', 'entryField_entry'),),
                                          None,
                                          Pmw.EntryField, self.labelFrame,
                                          entry_width = 10,
                                          validate = { 'validator' : 'real',
                                                       'min' : self['min'],
                                                       'max' : self['max'],
                                                       'minstrict' : 0,
                                                       'maxstrict' : 0},
                                          entry_justify = 'right',
                                          entry_textvar = self.entryValue,
                                          command = self._entryCommand)
        self.entry.pack(side='left',padx = 4)
                                          
        # Create the EntryScale's label
        self.label = self.createcomponent('label', (), None,
                                          Label, self.labelFrame,
                                          text = self['text'],
                                          width = 12,
                                          anchor = 'center',
                                          font = "Arial 12 bold")
        self.label.pack(side='left', expand = 1, fill = 'x')

        # Now pack the frame
        self.labelFrame.pack(expand = 1, fill = 'both')

        # Create a label and an entry
        self.minMaxFrame = self.createcomponent('frame', (), None,
                                                Frame, interior)
        # Create the EntryScale's min max labels
        self.minLabel = self.createcomponent('minLabel', (), None,
                                             Button, self.minMaxFrame,
                                             #command = self.askForMin,
                                             text = `self['min']`,
                                             relief = FLAT,
                                             width = 5,
                                             anchor = W,
                                             font = "Arial 8")
        self.minLabel.pack(side='left', expand = 1, fill = 'x')

        # Create the scale component.
        self.scale = self.createcomponent('scale', (), None,
                                          Scale, self.minMaxFrame,
                                          command = self._scaleCommand,
                                          orient = 'horizontal',
                                          length = 150,
                                          from_ = self['min'],
                                          to = self['max'],
                                          resolution = self['resolution'],
                                          showvalue = 0)
        self.scale.pack(side = 'left', expand = 1, fill = 'x')
        # Set scale to the middle of its range
        self.scale.set(self['initialValue'])

        self.maxLabel = self.createcomponent('maxLabel', (), None,
                                             Button, self.minMaxFrame,
                                             #command = self.askForMax,
                                             text = `self['max']`,
                                             relief = FLAT,
                                             width = 5,
                                             anchor = E,
                                             font = "Arial 8")
        self.maxLabel.pack(side='left', expand = 1, fill = 'x')
        self.minMaxFrame.pack(expand = 1, fill = 'both')
         
        # Check keywords and initialise options based on input values.
        self.initialiseoptions(EntryScale)

    def label(self):
        return self.label
    def scale(self):
        return self.scale
    def entry(self):
        return self.entry

    def askForMin(self):
        newMin = askfloat(title = self['text'],
                          prompt = 'New min val:',
                          parent = self.interior())
        if newMin:
            self.setMin(newMin)
            
    def setMin(self, newMin):
        self['min'] = newMin
        self.scale['from_'] = newMin
        self.minLabel['text'] = newMin
        self.entry.checkentry()
    
    def askForMax(self):
        newMax = askfloat(title = self['text'],
                          parent = self.interior(),
                          prompt = 'New max val:')
        if newMax:
            self.setMax(newMax)

    def setMax(self, newMax):
        self['max'] = newMax
        self.scale['to'] = newMax
        self.maxLabel['text'] = newMax
        self.entry.checkentry()
    
    def _updateLabelText(self):
        self.label['text'] = self['text']

    def _updateValidate(self):
        self.configure(entryField_validate = {
            'validator' : 'real',
            'min' : self['min'],
            'max' : self['max'],
            'minstrict' : 0,
            'maxstrict' : 0})
        self.minLabel['text'] = self['min']
        self.scale['from_'] = self['min']
        self.scale['to'] = self['max']
        self.maxLabel['text'] = self['max']

    def _scaleCommand(self, strVal):
        # convert scale val to float
        self.set(string.atof(strVal))
        """
        # Update entry to reflect formatted value
        self.entryValue.set( self.entryFormat % self.value )
        self.entry.checkentry()
        if self['command']:
            self['command'](self.value)
        """

    def _entryCommand(self, event = None):
        try:
            val = string.atof( self.entryValue.get() )
            self.set( val )
        except ValueError:
            pass

    def _setSigDigits(self):
        sd = self['significantDigits']
        self.entryFormat = '%.' + '%d' % sd + 'f'
        # And reset value to reflect change
        self.entryValue.set( self.entryFormat % self.value )

    def get(self):
        return self.value
    
    def set(self, newVal, fCommand = 1):
        # Clamp value
        if self['min'] is not None:
            if newVal < self['min']:
                newVal = self['min']
        if self['max'] is not None:
            if newVal > self['max']:
                newVal = self['max']
        # Round by resolution
        if self['resolution'] is not None:
            newVal = round(newVal / self['resolution']) * self['resolution']
        
        # Record updated value
        self.value = newVal
        # Update scale's position
        self.scale.set(newVal)
        # Update entry to reflect formatted value
        self.entryValue.set( self.entryFormat % self.value )
        self.entry.checkentry()
        
        # execute command
        if fCommand & (self['command'] is not None):
            self['command']( newVal )


class EntryScaleGroup(Pmw.MegaToplevel):
    def __init__(self, parent = None, **kw):

        # Default group size
        DEFAULT_DIM = 1
        # Default value depends on *actual* group size, test for user input
        DEFAULT_VALUE = [0.0] * kw.get('dim', DEFAULT_DIM)
        DEFAULT_LABELS = map(lambda x: 'v[%d]' % x,
                             range(kw.get('dim', DEFAULT_DIM)))

        #define the megawidget options
        INITOPT = Pmw.INITOPT
        optiondefs = (
            ('dim',             DEFAULT_DIM,            INITOPT),
            ('side',            TOP,                    INITOPT),
            ('title',           'EntryScale Group',        None),
            # A tuple of initial values, one for each entryScale
            ('initialValue',    DEFAULT_VALUE,          INITOPT),
            # The command to be executed any time one of the entryScales is updated
            ('command',         None,                   None),
            # A tuple of labels, one for each entryScale
            ('labels',          DEFAULT_LABELS,         self._updateLabels),
            )
        self.defineoptions(kw, optiondefs)

        # Initialize the toplevel widget
        Pmw.MegaToplevel.__init__(self, parent)
        
        # Create the components
        interior = self.interior()
        # Get a copy of the initial value (making sure its a list)
        self._value = list(self['initialValue'])

        # The Menu Bar
        self.balloon = Pmw.Balloon()
        menubar = self.createcomponent('menubar',(), None,
                                       Pmw.MenuBar, (interior,),
                                       balloon = self.balloon)
        menubar.pack(fill=X)
        
        # EntryScaleGroup Menu
        menubar.addmenu('EntryScale Group', 'EntryScale Group Operations')
        menubar.addmenuitem(
            'EntryScale Group', 'command', 'Reset the EntryScale Group panel',
            label = 'Reset',
            command = lambda s = self: s.reset())
        menubar.addmenuitem(
            'EntryScale Group', 'command', 'Dismiss EntryScale Group panel',
            label = 'Dismiss', command = self.withdraw)
        
        menubar.addmenu('Help', 'EntryScale Group Help Operations')
        self.toggleBalloonVar = IntVar()
        self.toggleBalloonVar.set(0)
        menubar.addmenuitem('Help', 'checkbutton',
                            'Toggle balloon help',
                            label = 'Balloon Help',
                            variable = self.toggleBalloonVar,
                            command = self.toggleBalloon)

        self.entryScaleList = []
        for index in range(self['dim']):
            # Add a group alias so you can configure the entryScales via:
            #   fg.configure(Valuator_XXX = YYY)
            f = self.createcomponent(
                'entryScale%d' % index, (), 'Valuator', EntryScale,
                (interior,), initialValue = self._value[index],
                text = self['labels'][index])
            # Do this separately so command doesn't get executed during construction
            f['command'] = lambda val, s=self, i=index: s._entryScaleSetAt(i, val)
            f.pack(side = self['side'], expand = 1, fill = X)
            self.entryScaleList.append(f)

        # Make sure entryScales are initialized
        self.set(self['initialValue'])
        
        # Make sure input variables processed 
        self.initialiseoptions(EntryScaleGroup)

    def _updateLabels(self):
        if self['labels']:
            for index in range(self['dim']):
                self.entryScaleList[index]['text'] = self['labels'][index]

    def toggleBalloon(self):
        if self.toggleBalloonVar.get():
            self.balloon.configure(state = 'balloon')
        else:
            self.balloon.configure(state = 'none')

    def get(self):
        return self._value

    def getAt(self,index):
        return self._value[index]

    # This is the command is used to set the groups value
    def set(self, value, fCommand = 1):
        for i in range(self['dim']):
            self._value[i] = value[i]
            # Update entryScale, but don't execute its command
            self.entryScaleList[i].set(value[i], 0)
        if fCommand & (self['command'] is not None):
            self['command'](self._value)

    def setAt(self, index, value):
        # Update entryScale and execute its command
        self.entryScaleList[index].set(value)

    # This is the command used by the entryScale
    def _entryScaleSetAt(self, index, value):
        self._value[index] = value
        if self['command']:
            self['command'](self._value)

    def reset(self):
        self.set(self['initialValue'])



## SAMPLE CODE
if __name__ == '__main__':
    # Initialise Tkinter and Pmw.
    root = Toplevel()
    root.title('Pmw EntryScale demonstration')

    # Dummy command
    def printVal(val):
        print val
    
    # Create and pack a EntryScale megawidget.
    mega1 = EntryScale(root, command = printVal)
    mega1.pack(side = 'left', expand = 1, fill = 'x')

    """
    # These are things you can set/configure
    # Starting value for entryScale    
    mega1['initialValue'] = 123.456
    mega1['text'] = 'Drive delta X'
    mega1['min'] = 0.0
    mega1['max'] = 1000.0
    mega1['resolution'] = 1.0
    # To change the color of the label:
    mega1.label['foreground'] = 'Red'
    # Max change/update, default is 100
    # To have really fine control, for example
    # mega1['maxVelocity'] = 0.1
    # Number of digits to the right of the decimal point, default = 2
    # mega1['significantDigits'] = 5
    """

    # To create a entryScale group to set an RGBA value:
    group1 = EntryScaleGroup(root, dim = 4,
                          title = 'Simple RGBA Panel',
                          labels = ('R', 'G', 'B', 'A'),
                          EntryScale_min = 0.0,
                          EntryScale_max = 255.0,
                          EntryScale_resolution = 1.0,
                          command = printVal)
    
    # Uncomment this if you aren't running in IDLE
    #root.mainloop()
