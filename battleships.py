import numpy as np


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

Dreadnaught:
  1
  1
111
1
1
'''

class ship:
    def __init__(self, type, location):
        self.row,self.col = location
        self.all_points = []
        self.hits = 0

        if type == 'docking':
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
        elif type == 'bident':
            self.all_points = [
                (self.row, self.col),
                (self.row, self.col + 1),
                (self.row + 1, self.col),
                (self.row + 2, self.col),
                (self.row + 2, self.col + 1)
            ]
        elif type == 'spear':
            self.all_points = [
                (self.row, self.col),
                (self.row + 1, self.col),
                (self.row + 2, self.col)
            ]
        elif type == 'row-defender':
            self.all_points = [
                (self.row, self.col),
                (self.row, self.col + 2),
                (self.row + 1, self.col + 1),
                (self.row + 2, self.col),
                (self.row + 2, self.col + 2)
            ]
        elif type == 'dreadnaught':
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
        return self.hits

    def is_sunk(self):
        if self.hits == len(self.all_points):
            return True
        else:
            return False


def create_empty_grids(size=10):
    # Create empty grids to get started
    #opfor_grid = np.zeros((size, size), dtype=int)
    radar = np.full((size, size), None)
    ocean = np.full((size, size), None)

    return radar, ocean

def place_ships(ship, location, grid):
    # Add ship to the location (top left corner)
    for row,col in ship.all_points():
        grid[row,col] = ship
    return None

def check_placement(ship, location, grid):
    for row,col in ship.all_points():
        if(row >= len(grid) or col >= len(grid[0])):
            return False
        if grid[row, col] is not None:
            return False
    return True

