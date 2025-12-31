import time

def wait_for_connection(thing):
    '''Wait a sensible amount of time for a connection to a device to be made.

    Make a sensible number of connection attempts with exponentially increasing 
    wait times between attempts.
    '''
    count = 0
    while thing.connected is False:
        count += 1
        time.sleep(0.2*2**count)  # 0.2 0.4 0.8 1.6 3.2 6.4
        if count > 5:
            break
        
