import numpy as np
from random import choice
from collections import deque

'''
Docking Ship:
1111
1  1
1  1
1111

Bident Fighter:
11
1
11

Spear Fighter:
1
1
1

X-Defender:
1 1
 1
1 1

Dreadnought: named because the tetris pieces shaped like this always gave me a feeling of dread...
  1
  1
111
1
1
'''


class ship:
    def __init__(self, ship_type, location):
        self.row,self.col = location
        self.all_points = []
        self.hits = 0
        self.ship_type = ship_type

        if ship_type == 'docking':
            self.type = 'Docking Ship'
            self.abbr = 'D'
            self.all_points = [
                (self.row,self.col),
                (self.row,self.col + 1),
                (self.row,self.col + 2),
                (self.row,self.col + 3),
                (self.row + 1,self.col),
                (self.row + 1,self.col + 3),
                (self.row + 2,self.col),
                (self.row + 2,self.col + 3),
                (self.row + 3,self.col),
                (self.row + 3, self.col + 1),
                (self.row + 3, self.col + 2),
                (self.row + 3, self.col + 3)
            ]
        elif ship_type == 'bident':
            self.type = 'Bident Fighter'
            self.abbr = 'B'
            self.all_points = [
                (self.row, self.col),
                (self.row, self.col + 1),
                (self.row + 1, self.col),
                (self.row + 2, self.col),
                (self.row + 2, self.col + 1)
            ]
        elif ship_type == 'spear':
            self.type = 'Spear Figher'
            self.abbr = 'S'
            self.all_points = [
                (self.row, self.col),
                (self.row + 1, self.col),
                (self.row + 2, self.col)
            ]
        elif ship_type == 'x-defender':
            self.type = 'X-Defender'
            self.abbr = 'X'
            self.all_points = [
                (self.row, self.col),
                (self.row, self.col + 2),
                (self.row + 1, self.col + 1),
                (self.row + 2, self.col),
                (self.row + 2, self.col + 2)
            ]
        elif ship_type == 'dreadnought':
            self.type = 'Dreadnought'
            self.abbr = 'R'
            self.all_points = [
                (self.row, self.col + 2),
                (self.row + 1, self.col + 2),
                (self.row + 2, self.col),
                (self.row + 2, self.col + 1),
                (self.row + 2, self.col + 2),
                (self.row + 3, self.col),
                (self.row + 4, self.col),
            ]

    def hit(self):
        self.hits += 1
        return self.is_sunk()

    def is_sunk(self):
        if self.hits == len(self.all_points):
            return True
        else:
            return False


def create_empty_grids(size):
    # Create empty grids to get started
    #opfor_grid = np.zeros((size, size), dtype=int)
    radar = np.full((size, size), None)
    ocean = np.full((size, size), None)

    return radar, ocean


def place_ships(ship_obj, grid):
    # Add ship to the location (top left corner)
    for row,col in ship_obj.all_points:
        grid[row,col] = ship_obj
    return None


def check_placement(ship_obj, grid):
    for row,col in ship_obj.all_points:
        if row >= len(grid) or col >= len(grid[0]):
            return False
        if grid[row, col] is not None:
            return False
    return True


def choose_ship_location(grid,ship_type):
    empty_cells = np.where(grid == None)
    empty_cells = [(empty_cells[0][i], empty_cells[1][i]) for i in range(0, len(empty_cells[0]))]
    valid_ship = False
    while not valid_ship:
        if len(empty_cells) == 0:
            print("something went wrong and the system could not find a place to place a ship")
            quit()
        location = choice(empty_cells)
        curr_ship = ship(ship_type, location)
        if check_placement(curr_ship, grid):
            #place_ships(curr_ship, grid)
            valid_ship = True
        else:
            empty_cells.remove(location)
            del curr_ship
    return curr_ship


def setup_ai_game(size, list_of_ships):
    # list_of_ships = ['docking', 'bident', 'spear', 'x-defender', 'dreadnought']
#    p1_radar, p1_ocean = create_empty_grids()
    p2_radar, p2_ocean = create_empty_grids(size)
    for ship_type in list_of_ships:
        valid_ship = choose_ship_location(p2_ocean, ship_type)
        place_ships(valid_ship, p2_ocean)
    return p2_radar, p2_ocean


def visualize(grid,ocean=False):
    header_top = [str(x).rjust(2,' ') for x in range(len(grid[0]))]
    header_left = [y for y in range(len(grid))]
    grid = np.vstack((header_top,grid))
    print(' ', end=' ')
    for r_idx,row in enumerate(grid):
        if r_idx != 0:
            print(str(header_left[r_idx-1]).rjust(2,' '), end=' ')
        for col in row:
            if col is None:
                print('  ', end=' ')
            elif r_idx == 0 or col == 'O' or col == '*' or not ocean:
                print(col+' ', end=' ')
            else:
                print(col.abbr+' ', end=' ')
        print()


def setup_human_game(size, list_of_ships):
    p1_radar, p1_ocean = create_empty_grids(size)
    print("Welcome aboard Commander!")
    for ship_type in list_of_ships:
        valid_ship = False
        while not valid_ship:
            visualize(p1_ocean, True)
            location = input(
                "Enter the location (top left corner) "
                "where you would like us to deploy our {} ship. eg. (2,3) for row 2 col 3: ".format(ship_type)
            )
            curr_ship = ship(ship_type, eval(location))
            if check_placement(curr_ship, p1_ocean):
                place_ships(curr_ship, p1_ocean)
                valid_ship = True
            else:
                del curr_ship
                print('Not a valid ship placement. Try Again')
    visualize(p1_ocean, True)
    return p1_radar, p1_ocean

def fire_cannons(location, grid):
    row,col = location
    if row >= len(grid):
        return False
    elif col >= len(grid[0]):
        return False
    elif row < 0:
        return False
    elif col < 0:
        return False
    else:
        if(grid[row,col] is None):
            # valid shot, but missed any ships
            return True
        else:
            return grid[row,col]

def sector_cleared(grid, point):
    r,c = point
    bottom = top = right = left = False
    if r+1 >= len(grid) or grid[r+1,c] is not None:
        bottom = True
    if r-1 < 0 or grid[r-1,c] is not None:
        top = True
    if c+1 >= len(grid[0]) or grid[r,c+1] is not None:
        right = True
    if c-1 < 0 or grid[r,c-1] is not None:
        left = True

    if bottom and top and left and right:
        return True
    else:
        return False

def choose_sector(grid, hit_queue):
    '''
    :param grid: a friendly radar grid
    :param hit_queue: a deque queue
    :return:
    '''

    if len(hit_queue) > 0 and sector_cleared(grid, hit_queue[0]):
        hit_queue.popleft()

    if len(hit_queue) == 0:
    # If we don't have a previous hit marker, start firing randomly until we get a hit
        empty_cells = np.where(grid == None)
        empty_cells = [(empty_cells[0][i], empty_cells[1][i]) for i in range(0, len(empty_cells[0]))]
        mgrs_coordinate = choice(empty_cells)
    else:
        start_point = hit_queue[0]
        start_row, start_col = start_point
        if start_row-1 >= 0 and grid[start_row-1,start_col] is None:
            mgrs_coordinate = (start_row-1,start_col)
        elif start_row+1 < len(grid) and grid[start_row+1,start_col] is None:
            mgrs_coordinate = (start_row+1,start_col)
        elif start_col-1 >= 0 and grid[start_row,start_col-1] is None:
            mgrs_coordinate = (start_row,start_col-1)
        elif start_col+1 < len(grid[0]) and grid[start_row,start_col+1] is None:
            mgrs_coordinate = (start_row,start_col+1)


    return mgrs_coordinate


def play_game(p1_r, p1_o, p2_r, p2_o, list_of_ships):
    p1_sunk_ships = []
    p2_sunk_ships = []
    game_done = False
    player = 1
    hit_queue = deque()
    while not game_done:
        if player == 1:
            print("OCEAN")
            visualize(p1_o, True)
            print("RADAR")
            visualize(p1_r)
            p1_move = eval(input("Enter the position you would like to fire at (eg. 2,3 for row 2 col 3): "))
            result = fire_cannons(p1_move, p2_o)
            if result == False:
                print("Our cannons can't fire that far Commander, pick a closer sector")
                continue
            elif result == True:
                print("Commander, our shell hit nothing but water!")
                p1_r[p1_move] = 'O'
                p2_o[p1_move] = 'O'
            else:
                print("Commander! We hit an enemy ship!")
                p1_r[p1_move] = '*'
                p2_o[p1_move] = '*'
                if result.hit():
                    print("Huzzah Commander! We sunk the enemy's {} ship!".format(result.type))
                    p1_sunk_ships.append(result.ship_type)
                    if(len(p1_sunk_ships) == len(list_of_ships)):
                        print("Commander, the enemy armada as been vanquished! The day is ours! HUZZAH!")
                        game_done = True
            player = 2
        elif player == 2:
            mgrs = choose_sector(p2_r, hit_queue)
            result = fire_cannons(mgrs,p1_o)
            if result == True:
                p2_r[mgrs] = 'O'
                p1_o[mgrs] = 'O'
            else:
                print("Commander, our {} ship has been hit!".format(result.type))
                p2_r[mgrs] = '*'
                p1_o[mgrs] = '*'
                hit_queue.append(mgrs)
                if result.hit():
                    print("Commander, our {} ship has been sunk!".format(result.type))
                    p2_sunk_ships.append(result.ship_type)
                    if (len(p2_sunk_ships) == len(list_of_ships)):
                        print("Commander, the enemy has destroyed our armada! We must surrender.")
                        game_done = True
            player = 1







if __name__ == '__main__':
    size = 10
    list_of_ships = ['docking', 'bident', 'spear', 'x-defender', 'dreadnought']
    p1_radar, p1_ocean = setup_human_game(size, list_of_ships)
    p2_radar, p2_ocean = setup_ai_game(size, list_of_ships)
    play_game(p1_radar, p1_ocean, p2_radar, p2_ocean, list_of_ships)
    visualize(p2_ocean)

