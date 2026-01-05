from bluesky.plan_stubs import sleep, mv, null

UNSET_PEAK_POSITION = -10_000_000_000

def prepare_alignment_scan(rkvs=None, dwell_time=None, inttime=0.1):
    '''Prepare for an alignment scan:

    1. Set the redis parameter used to communicate the alignment
       result back from the Kafka client to its unset value.

    2. Set the dwell time to a value suitable for an alignment scan.
       The default is 0.1 seconds, but can be overwritten if need be.

    '''
    if rkvs is None:
        cprint('[orange_red1]You have not provided an instance of the local Redis server.[/orange_red1]')
        cprint('[orange_red1]Unable to prepare for alignment scan.[/orange_red1]')
        yield from null()
        return
    rkvs.set('BMM:peakposition', UNSET_PEAK_POSITION - 0.1)
    if dwell_time is not None:
        yield from mv(dwell_time, inttime)



def fetch_peak_position_via_redis(rkvs=None, maxtries=6, verbose=False):
    '''Retrieve a result found by the Kafka consumer and posted to redis.

    The function prepare_alignment_scan() should have been called
    prior to the alignment scan.

    This function waits increasing times for that parameter in redis
    to be set to value bigger than UNSET_PEAK_POSITION.  This gives
    the kafka consumer some time to do its thing.

    '''
    if rkvs is None:
        return UNSET_PEAK_POSITION
    time.sleep(0.25)
    top = float(rkvs.get('BMM:peakposition').decode('utf8'))
    count = 0
    #if verbose: print(f"{count = }, {top = }")
    while top < UNSET_PEAK_POSITION:
        time.sleep(0.1 * 2**count)
        top = float(rkvs.get('BMM:peakposition').decode('utf8'))
        count += 1
        if verbose: print(f"{count = }, {top = }", flush=True)
        if count > maxtries:
            return(None)
    return top
