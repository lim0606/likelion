record = 1
Record = 1
Board = 1
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


def genShips(ship_id, active):
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

    return ships_all


log = record.get_latest()

if len(log) == 0:  # if log equals to {} (empty dictionary)
    mode = "hunt"

    # the supplement matrix indicating each position has been missed or sank
    visited = [0 for x in xrange(board_size * board_size)]

else:
    visited = record.data["visited"]

    if log["result"] == Record.Status.MISSED:
        visited[log["guess"]["x"] * board_size + log["guess"]["y"]] = 1
    elif log["result"] == Record.Status.HIT:
        mode = "target"
    elif log["result"] == Record.Status.SINK:
        mode = "hunt"
        for x in range(0, board_size):
            for y in range(0, board_size):
                if record.get_status_at(x, y) == Board.Status.HIT:
                    visited[x * board_size + y] = 1
    elif log["result"] == Record.Status.WIN:
        mode = "win"
        print "I won!"

# if log["result"] == Record.Status.MISSED or Record.Status.SINK:
#     mode = "hunt"
# elif log["result"] == Record.Status.HIT:
#     mode = "target"
# elif log["result"] == Record.Status.WIN:
#     mode = "win"
#     print "I won!"

if mode is "hunt":
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
            if ship.active is True:
                for i in ship.length:
                    (x, y) = ship.pos[i]
                    board[x * board_size + y] += 1

    index = sorted(range(len(board)), key=lambda k: board[k])
    x = index % board_size
    y = index / board_size
    return x, y

elif mode == "target":
    ship_id = record.get_remaining_ships()
    ships_all = genShips(ship_id, False)

    # Step1: leave the ships overlapped with the only hits that are not
    # related to sanked ships.
    for ships in ships_all:
        for ship in ships:
            for (x, y) in ship.pos:
                if record.get_status_at(x, y) == Board.Status.HIT and visited[x * board_size + y] == 0:
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
            if ship.active is True:
                for i in ship.length:
                    (x, y) = ship.pos[i]
                    board[x * board_size + y] += 1

elif mode == "win":
    print "I won!"
else:
    print "Error occurred in overall logic"

record.data["visited"] = visited
