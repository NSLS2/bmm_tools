from rich import print as cprint


######################################################################################
# here is an example of what a message tuple looks like when moving a motor          #
# (each item in the tuple is on it's own line):                                      #
#     set:                                                                           #
#     (XAFSEpicsMotor(prefix='XF:06BMA-BI{XAFS-Ax:LinX}Mtr', name='xafs_linx', ... ) #
#     (-91.5999475,),                                                                #
#     {'group': '8c8df020-23aa-451e-b411-c427bc80b375'}                              #
######################################################################################

def BMM_msg_hook(msg):
    '''
    BMM-specific function for RE.msg_hook
    '''
    #print(msg)
    if msg[0] == 'set' and msg[2][0] is not None:
        if 'EpicsMotor' in str(type(msg[1])):
            print('Moving %s to %.3f'  % (msg[1].name, msg[2][0]))
        elif 'EpicsSignal' in str(type(msg[1])):
            cprint('[grey42]Setting %s to %.3f[/grey42]' % (msg[1].name, msg[2][0]))
        elif 'LockedDwell' in str(type(msg[1])):
            cprint('[grey42]Setting %s to %.3f[/grey42]' % (msg[1].name, msg[2][0]))
        elif 'PseudoSingle' in str(type(msg[1])):
            print('Moving %s to %.3f'  % (msg[1].name, msg[2][0]))
    # else:
    #     report('something went wrong with the last data point')
    #     print(msg)


