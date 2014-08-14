def guess(record):
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


    print "ahha!"
    ship_id = record.get_remaining_ships()
    # print "remaining ships: ", ship_id
    ships_all = genShips(ship_id, True)

    print "length of ships_all :", len(ships_all)

    board = [0 for x in xrange(board_size * board_size)]
    for ships in ships_all:
        for ship in ships:
            # print ship.active
            if ship.active is True:
                for i in range(0, ship.length):
                    (x, y) = ship.pos[i]
                    # print (x,y)
                    board[y * board_size + x] += 1

    for x in range(0,10):
        for y in range(0, 10):
                print "%3d " % board[y * board_size + x],
        print " "

    history = record.get_history()
    length = len(history)
    record.data['test'] = 1
    return length % 10, length / 10