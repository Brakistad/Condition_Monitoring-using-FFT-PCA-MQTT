# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 12:28:35 2017

@author: oyvin
"""

def SaveLoad(opt,filename,variables=None):
    '''
    save or load a file with variables(list)
    '''

    import pickle
    if opt=='save':
        f = open(filename, 'wb')
        pickle.dump(variables,f)
        f.close()
    elif opt=='load':
        f = open(filename, 'rb')
        obj = pickle.load(f)
        f.close()
        return obj
    else:
        print('Invalid saveload option. Must be either \'save\' or \'load\'')

def script_timer(mode, start_time_script=None):
    import datetime
    if mode =='start':
        return datetime.datetime.now()
    elif mode =='stop':
        delta_time = datetime.datetime.now() - start_time_script
        seconds = delta_time.seconds
        minutes = seconds // 60
        seconds = seconds % 60
        print('Script finished in', str(minutes), 'minutes and', str(seconds), 'seconds.')
        return delta_time