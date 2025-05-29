from typing import Tuple

import numpy as np
# np.dtype translates to NumPy Data Type and dt is Data Type
# this is a custom datatype
graphic_dt = np.dtype(
    [("ch", np.int32),
     ("fg ", "3B"),
     ("bg ", "3B"),
     ]
)

tile_dt = np.dtype(
    [
        ("walkable", bool),
        ("transparent", bool),
        ("dark", graphic_dt),
        ("light", graphic_dt)
    ]
)

def new_tile(
        *,
        walkable: int,
        transparent: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)
# this represents unexplored, unseen tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (26, 19, 8)),
    light=(ord(" "), (64, 47, 25), (46, 33, 10)),
)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (33, 33, 32)),
    light=(ord(" "), (79, 78, 77), (59, 58, 58)),
)
stairs_down = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(">"), (0, 0, 100), (50, 50, 150)),
    light=(ord(">"), (255, 255, 255), (200, 180, 50)),
)