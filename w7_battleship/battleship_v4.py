def guess(record):
    import random

    board_size = 10

    class Ship:
        # length = ?
        # pos = [(x1,y1), (x2,y2), (x3, y3)]
        # direction = 'vertical' or 'horizontal'
        # id = 1, 2, 3, 4, or 5
        # active = True

        def __init__(self, id, x, y, direction, active):
            self.id = id
            self.active = active
            if id < 3:
                self.length = id + 1
            else:
                self.length = id

            self.direction = direction
            self.pos = [(x, y)]
            if direction == 'vertical':
                for i in range(1, self.length):
                    self.pos.append((x, y + i))
            elif direction == 'horizontal':
                for i in range(1, self.length):
                    self.pos.append((x + i, y))
            else:
                print "Error occurred in initialize Ship class object"
            # print self.pos

    def genShips(ship_id, active):
        # print "remaining ships: ", ship_id
        # print "active: ", active
        ship = Ship(1, 0, 0, 'horizontal', active)
        ships = [ship]
        ships_all = [ships]
        ships_all.pop()

        for id in ship_id:
            ship = Ship(id, 0, 0, 'horizontal', active)
            ships = [ship]
            ships.pop()

            if id < 3:
                length = id + 1
            else:
                length = id

            direction = 'horizontal'
            for x in range(0, board_size - length + 1):
                for y in range(0, board_size):
                    ships.append(Ship(id, x, y, direction, active))

            direction = 'vertical'
            for x in range(0, board_size):
                for y in range(0, board_size - length + 1):
                    ships.append(Ship(id, x, y, direction, active))

            ships_all.append(ships)

        return ships_all

    log = record.get_latest()

    if len(log) == 0:  # if log equals to {} (empty dictionary)
        mode = "hunt"
        iter = 1
        # the supplement matrix indicating each position has been missed or
        # sank
        visited = [0 for x in xrange(board_size * board_size)]

        # the supplement chess board like matrix
        # checker_board = [0 for x in xrange(board_size * board_size)]
        # for y in range(0, board_size):
        #     for x in range(y % 2, board_size, 2):
        #         checker_board[y * board_size + x] = 1
        # for x in range(0, 10):
        #     for y in range(0, 10):
        #         print "%3d " % checker_board[y * board_size + x],
        #     print " "
        # record.data["checker_board"] = checker_board
        record.data["visited"] = visited
        record.data["mode"] = mode
        record.data["iter"] = iter
    else:
        iter = record.data["iter"]
        iter += 1
        # checker_board = record.data["checker_board"]
        visited = record.data["visited"]
        mode = record.data["mode"]
        print "iteration: ", iter

        if log["result"] == Record.Status.MISSED:
            visited[log["guess"]["y"] * board_size + log["guess"]["x"]] = 1
        elif log["result"] == Record.Status.HIT:
            print "It was HIT!"
            mode = "target"
            print "mode: ", mode
        elif log["result"] == Record.Status.SINK:
            mode = "hunt"
            for x in range(0, board_size):
                for y in range(0, board_size):
                    if record.get_status_at(x, y) == Board.Status.HIT:
                        visited[y * board_size + x] = 1
        elif log["result"] == Record.Status.WIN:
            mode = "win"
            print "I won!"
        else:
            print ":)"

        record.data["visited"] = visited
        record.data["mode"] = mode
        record.data["iter"] = iter
        # for x in range(0, 10):
        #     for y in range(0, 10):
        #         print "%3d " % visited[y * board_size + x],
        #     print " "

    # if log["result"] == Record.Status.MISSED or Record.Status.SINK:
    #     mode = "hunt"
    # elif log["result"] == Record.Status.HIT:
    #     mode = "target"
    # elif log["result"] == Record.Status.WIN:
    #     mode = "win"
    #     print "I won!"

    if mode == "hunt":
        # print "Hunting!!!!!!!!!!!!!!!!!!!!!!!"
        # Step0: generate ships
        # ship_id = record.get_remaining_ships()
        # if len(log) == 0:  # if log equals to {} (empty dictionary)
        #     print "Start the program!"
        #     ships_all = genShips(ship_id)
        # else:  # if there exist log before
        #     ships_all = record.data["ship_id"]
        # ship_id = [1, 2, 3, 4, 5]
        ship_id = record.get_remaining_ships()
        ships_all = genShips(ship_id, True)

        # Step1: eliminate ships overlapped with missed positions
        # Step2: eliminate ships overlapped with positions of other ships
        # for id in ship_id:
        #     if id < 3:
        #         length = id + 1
        #     else:
        #         length = id

        #     ships = ships_all[id]
        for ships in ships_all:
            for ship in ships:
                for (x, y) in ship.pos:
                    if record.get_status_at(x, y) == Board.Status.HIT or record.get_status_at(x, y) == Board.Status.MISSED:
                        ship.active = False

        # get_status_at(x, y)
        # get_remaining_ships()
        # get_sink_info([ship_id])
        # Step3: vote the positions of all remaining ships
        board = [0 for x in xrange(board_size * board_size)]
        for ships in ships_all:
            for ship in ships:
                # print ship.active
                if ship.active is True:
                    for i in range(0, ship.length):
                        (x, y) = ship.pos[i]
                        # print (x,y)
                        board[y * board_size + x] += 1

        # for x in range(0, 10):
        #     for y in range(0, 10):
        #         print "%3d " % board[y * board_size + x],
        #     print " "

        # Step4: narrowing candidates with checkerboard
        # for x in range(0, 10):
        #     for y in range(0, 10):
        #         if checker_board[y * board_size + x] == 0:
        #             board[y * board_size + x] = 0
        # for y in range(0, board_size):
        #     for x in range(y % 2, board_size, 2):
        #         board[y * board_size + x] = 0

        # Step5: find the maximum probable position
        index = sorted(range(len(board)), key=lambda k: board[k], reverse=True)
        
        # Step6: give randomness in selecting the next guess
        len_random = 5
        i = 0
        while i < board_size * board_size and board[index[i]] != 0:
            # print i
            i += 1

        if i > 12 * len_random:
            # print "index : ", index
            index = index[0:len_random]
            print "index shorten :", index
            random.shuffle(index)
            print "index shuffled :", index

        x = index[0] % board_size
        y = index[0] / board_size
        # return x, y

    elif mode == "target":
        # print "Targetting!!!!!!!!!!!!!!!!!!!!!!!"
        ship_id = record.get_remaining_ships()
        ships_all = genShips(ship_id, False)

        # Step1: leave the ships overlapped with the only hits that are not
        # related to sanked ships.
        n_hits = 0
        for y in range(0, board_size):
            for x in range(0, board_size):
                if record.get_status_at(x, y) == Board.Status.HIT and visited[y * board_size + x] == 0:
                    n_hits += 1

        print "n_hits: ", n_hits

        if n_hits > 1:
            for ships in ships_all:
                for ship in ships:
                    n_hits_tmp = 0
                    for (x, y) in ship.pos:
                        if record.get_status_at(x, y) == Board.Status.HIT and visited[y * board_size + x] == 0:
                            n_hits_tmp += 1
                    if n_hits_tmp == n_hits:
                        ship.active = True
        else:
            for ships in ships_all:
                for ship in ships:
                    for (x, y) in ship.pos:
                        if record.get_status_at(x, y) == Board.Status.HIT and visited[y * board_size + x] == 0:
                            ship.active = True

        # Step2: eliminate ships overlapped with missed positions
        for ships in ships_all:
            for ship in ships:
                if ship.active is True:
                    for (x, y) in ship.pos:
                        if record.get_status_at(x, y) == Board.Status.MISSED:
                            ship.active = False

        # get_status_at(x, y)
        # get_remaining_ships()
        # get_sink_info([ship_id])
        # Step3: vote the positions of all remaining ships
        board = [0 for x in xrange(board_size * board_size)]
        for ships in ships_all:
            for ship in ships:
                # print ship.active
                if ship.active is True:
                    for i in range(0, ship.length):
                        (x, y) = ship.pos[i]
                        # print (x,y)
                        board[y * board_size + x] += 1

        # for x in range(0, 10):
        #     for y in range(0, 10):
        #         print "%3d " % board[y * board_size + x],
        #     print " "

        index = sorted(range(len(board)), key=lambda k: board[k], reverse=True)
        i = 0
        x = index[i] % board_size
        y = index[i] / board_size
        while record.get_status_at(x, y) != Board.Status.EMPTY:
            i += 1
            x = index[i] % board_size
            y = index[i] / board_size
        # return x, y

    elif mode == "win":
        print "I won!"
        # return 0, 0
        x = 0
        y = 0
    else:
        print "Error occurred in overall logic"
        # return 0, 0
        x = 0
        y = 0

    # record.data["visited"] = visited
    print "Guess : ", (x,y)
    return x, y
