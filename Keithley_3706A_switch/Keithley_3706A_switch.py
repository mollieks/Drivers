# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:58:36 2019

@author: DA21921
"""


from VISA_Driver import VISA_Driver
import InstrumentDriver
import numpy as np

__version__  = '0.5'

class Driver(VISA_Driver):

    def performOpen(self,options={}):
#        VISA_Driver.performOpen(self,options)
#        #Set the format for the output
        #VISA_Driver.writeAndLog(self,'reset()')
#        #Put source modes to fixed (rather than sweep)
#        VISA_Driver.writeAndLog(self,'SOUR:CURR:MODE FIX; :SOUR:VOLT:MODE FIX')
        pass

    def performSetValue(self, quant, value, sweepRate=0.0, options={}):
        pass
        #self.log('performSetValue called: '+quant.name+' value: '+str(value))
        #return VISA_Driver.performSetValue(self,quant,value,options=options,sweepRate=sweepRate)

    def performGetValue(self, quant, options={}):
        pass
#        self.log('performGetValue called: '+quant.name)
#        if quant.name.startswith('Measure '):
#            #Determine which variables are being measured
#            quantDict = {'Measure Current':'CURR', \
#                         'Measure Voltage':'VOLT', \
#                         'Measure Resistance':'RES'}
#            reply = VISA_Driver.askAndLog(self,'FUNC?')
#            if quantDict[quant.name] in reply:
#                return True
#            else:
#                return False
#
#            return VISA_Driver.performGetValue(self,quant,options)


if __name__ == '__main__':
    pass
