"this will handle loading and starting saved games"
from __future__ import annotations

import copy
from idlelib.runscript import indent_message
from typing import Optional

import tcod
from tcod import libtcodpy
from tcod.event import T
from tcod.libtcodpy import map_get_height, console_get_width
from PIL import Image

import color
from engine import Engine
import entity_factories
import input_handlers
from procgen import generate_dungeon


background_image = tcod.image.load("Images/main_menu_image_resized.png")[:, :, :3]

def new_game() -> Engine:
    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 2
    max_items_per_room = 2

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_max_size=room_max_size,
        room_min_size=room_min_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        max_items_per_room=max_items_per_room,
        engine=engine,
    )
    engine.update_fov()

    engine.message_log.add_message(
        "Hello adventurer,suffer well in yet another dungeon!", color.welcome_text
    )
    return engine


class MainMenu(input_handlers.BaseEventHandler):
    # this will render the main menu
    def on_render(self, console: tcod.Console) -> None:
        # this loads the image
        console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "TOMBS OF THE UNDYING QUEEN",
            fg=color.menu_title,
            alignment=libtcodpy.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            "By Kamen, made while following https://rogueliketutorials.com/ tutorial",
            fg=color.menu_title,
            alignment=libtcodpy.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
                ["[N] Play a new game", "[C] Continue", "[Q] Quit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=libtcodpy.CENTER,
                bg_blend=libtcodpy.BKGND_ALPHA(64),
            )

    def ev_keydown(
            self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.KeySym.q, tcod.event.KeySym.ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.KeySym.c:
            pass
        elif event.sym == tcod.event.KeySym.n:
            return input_handlers.MainGameEventHandler(new_game())

        return None
