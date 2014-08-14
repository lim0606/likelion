

def guess(record):
    
    history = record.get_history()
    length = len(history)
    record.data['test'] = 1
    # print record.data['test']
    # print record.get_status_at((length - 1) % 10, (length - 1) % 10)
    # if record.get_status_at((length - 1) % 10, (length - 1) % 10) == Record.Status.MISSED:
    #     print "damn!"
    
    board = [[0 for x in xrange(10)] for x in xrange(10)]
    
    # print "Missed: ",
    # print Record.Status.MISSED
    # print "SINK: ",
    # print Record.Status.SINK
    # print "HIT: ",
    # print Record.Status.HIT

    log = record.get_latest()
    if len(log) != 0:
        if log["result"] == Record.Status.SINK:
            print "ahha!"   
            print "miss map!"
            for x in range(0,10):
                for y in range(0, 10):
                    if record.get_status_at(x, y) == Board.Status.MISSED:
                        print "%2d " % (Board.Status.MISSED),
                    else:
                        print (0),
                print " "
            print "sink map!"
            for x in range(0,10):
                for y in range(0, 10):
                    if record.get_status_at(x, y) == Board.Status.HIT:
                        print "%2d " % (Board.Status.HIT),
                    else: 
                        print (0),
                print " "

            print "sanked_ship"
            for id in range(1,6):
                location = record.get_sink_info(id)
                print location

            # if record.get_status_at(x, y) == Record.Status.SINK:
    return length % 10, length / 10