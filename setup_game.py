"this will handle loading and starting saved games"
from __future__ import annotations

import copy
import lzma
import pickle
import traceback
from idlelib.runscript import indent_message
from typing import Optional

import tcod
from tcod import libtcodpy
from tcod.event import T
from tcod.libtcodpy import map_get_height, console_get_width
from PIL import Image

import color
from SpriteManager import Sprite
from engine import Engine
import entity_factories
import input_handlers
from game_map import GameWorld

from utils import resource_path

image_path = resource_path("images/main_menu_image_resized.png")
background_image = tcod.image.load(image_path)[:, :, :3]


def new_game() -> Engine:
    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_max_size=room_max_size,
        room_min_size=room_min_size,
        map_width=map_width,
        map_height=map_height,
    )
    engine.game_world.generate_floor()
    engine.update_fov()

    engine.message_log.add_message(
        "Hello adventurer,suffer well in yet another dungeon!", color.welcome_text
    )
    return engine


def load_game(filename: str) -> Engine:
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
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
            try:
                return input_handlers.MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.KeySym.n:
            engine = new_game()
            game_handler = input_handlers.MainGameEventHandler(engine)
            return input_handlers.KeybindingsHandler(engine, game_handler)

        return None
