# Zadanie: Hetmani i Pionek

import random
from tabulate import tabulate
import unittest
import argparse

# Test =========================
class TestHetmaniPionek(unittest.TestCase):
    def setUp(self):
        # Ustawienie początkowego stanu mapy dla testów
        global map, pown_pos
        map = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, "h", 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, "p", 0, 0, 0, 0],
            [0, 0, "h", 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, "h", 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
        pown_pos = [3, 3]  # Ustawienie pozycji pionka na środku

    def test_can_hetman_get_pawn(self):
        # Test czy funkcja prawidłowo identyfikuje hetmany, które mogą atakować pionka
        self.assertTrue(can_hetman_get_pawn(1, 1), "Hetman na (1, 1) powinien atakować pionka")
        self.assertTrue(can_hetman_get_pawn(4, 2), "Hetman na (4, 2) powinien atakować pionka")
        self.assertFalse(can_hetman_get_pawn(6, 5), "Hetman na (6, 5) nie powinien atakować pionka")

    def test_display_map_with_attacking_hetmans(self):
        # Test wyświetlenia planszy tylko z atakującymi hetmanami
        expected_map = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, "h", 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, "p", 0, 0, 0, 0],
            [0, 0, "h", 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
        # Sprawdzamy, czy tylko hetmani atakujący pionka są wyświetlani
        result_map = display_map_with_attacking_hetmans()
        self.assertEqual(result_map, expected_map)

# Program ======================
size = [7,7]
pown_pos = None

map = [
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
]

def get_position():
    row = random.randint(0, size[0])
    col = random.randint(0, size[1])
    res = [row, col]
    return res

def add_hetman():
    pos = get_position()
    print(pos)
    if map[pos[0]][pos[1]] == 0:
            map[pos[0]][pos[1]] = "h"
    else:
        print("pozycja jest już zajęta")
        add_hetman()

def add_pionek():
    global pown_pos
    pos = get_position()
    if map[pos[0]][pos[1]] == 0:
            map[pos[0]][pos[1]] = "p"
            pown_pos = pos
    else:
        print("pozycja jest już zajęta")
        add_pionek()

# *zakładam że hetmany nie blokują się o siebie nawzajem
def can_hetman_get_pawn(pos_y, pos_x):
    if map[pos_y][pos_x] != "h":
        return False
    
    directions = [
        (0, 1), (0, -1),  # poziomo
        (1, 0), (-1, 0),  # pionowo
        (1, 1), (-1, -1),  # przekątna lewy górny -> prawy dolny
        (1, -1), (-1, 1)   # przekątna prawy górny -> lewy dolny
    ]

    for dy, dx in directions:
        y, x = pos_y, pos_x
        while 0 <= y < len(map) and 0 <= x < len(map[0]):
            y += dy
            x += dx
            if 0 <= y < len(map) and 0 <= x < len(map[0]) and map[y][x] == "p":
                return True
            elif not (0 <= y < len(map) and 0 <= x < len(map[0])) or map[y][x] == "h":
                break
    return False

# Poprawiona funkcja display_map_with_attacking_hetmans
def display_map_with_attacking_hetmans():
    display_map = [[0 for _ in range(8)] for _ in range(8)]
    display_map[pown_pos[0]][pown_pos[1]] = "p"
    
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] == "h" and can_hetman_get_pawn(y, x):
                display_map[y][x] = "h"

    print(tabulate(display_map))
    return display_map  # Dodane, aby test mógł pobrać wynik

def display_map_with_attacking_hetmans_test():
    display_map = [[0 for _ in range(8)] for _ in range(8)]
    display_map[pown_pos[0]][pown_pos[1]] = "p"
    
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] == "h" and can_hetman_get_pawn(y, x):
                display_map[y][x] = "h"

    print(tabulate(display_map))
    return display_map 

def main_program():
    ## Generowanie mapy [3 pkt]
    print("Ilośc hetmanow: ")
    i = input()
    for x in range(int(i)):
        add_hetman()
        
    add_pionek()
    print("Pełna mapa z hetmanami i pionkiem:")
    print(tabulate(map))
    print("\nMapa tylko z pionkiem i hetmanami, które go atakują:")
    display_map_with_attacking_hetmans()

    print("pown pos: ", pown_pos)

if __name__ == "__main__":
    # handle flags
    parser = argparse.ArgumentParser()
    parser.add_argument("-test", action="store_true", help="Uruchom testy jednostkowe")
    args = parser.parse_args()
 
    if args.test:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        main_program()