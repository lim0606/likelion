board_size = 10


class Ship:
    # length = ?
    # pos = [(x1,y1), (x2,y2), (x3, y3)]
    # direction = 'vertical' or 'horizontal'
    # id = 1, 2, 3, 4, or 5
    # active = True

    def __init__(self, id, x, y, direction):
        self.id = id
        self.active = True
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


def genShips(ship_id):
    ship = Ship(1, 0, 0, 'horizontal')
    ships = [ship]
    ships_all = [ships]
    ships_all.pop()

    for id in ship_id:
        ship = Ship(id, 0, 0, 'horizontal')
        ships = [ship]
        ships.pop()

        if id < 3:
            length = id + 1
        else:
            length = id

        direction = 'horizontal'
        for x in range(0, board_size - length + 1):
            for y in range(0, board_size):
                ships.append(Ship(id, x, y, direction))

        direction = 'vertical'
        for x in range(0, board_size):
            for y in range(0, board_size - length + 1):
                ships.append(Ship(id, x, y, direction))

    return ships_all


# Step0: generate ships
log = result.get_latest()
# ship_id = record.get_remaining_ships()
# if len(log) == 0:  # if log equals to {} (empty dictionary)
#     print "Start the program!"
#     ships_all = genShips(ship_id)
# else:  # if there exist log before
#     ships_all = result.data["ship_id"]
ship_id = [1, 2, 3, 4, 5]
ships_all = genShips(ship_id)


# Step1: eliminate ships overlapped with missed positions
for id in ship_id:
    if id < 3:
        length = id + 1
    else:
        length = id

    ships = ships_all[id]

    for ship in ships:
        for (x, y) in ship.pos:
            if result.get_status_at(x, y) == Record.Status.MISSED:
                ship.active = False


# Step2: eliminate ships overlapped with positions of other ships

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

pos = sorted(range(len(board)), key=lambda k: board[k])
x = pos % board_size
y = pos / board_size
