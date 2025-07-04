#!/usr/bin/env python3
import pygame #this needs to be ad the top or else it throws and error...
import tcod
import traceback
import exceptions
import input_handlers
import color
from utils import resource_path
from components.sound_mixer import SoundMixer

import entity_factories
import setup_game

def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")

def main() -> None:
    screen_width = 80
    screen_height = 50

    image_path = resource_path("images/dejavu10x10_gs_tc.png")

    tileset = tcod.tileset.load_tilesheet(
        image_path, 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

    sound_mixer = SoundMixer()
    sound_mixer.play_music()

    # this is how we create the map
    with tcod.context.new_terminal(

            columns=screen_width,
            rows=screen_height,
            tileset=tileset,
            title="Pyton Rougelike Tutorial",
            vsync=True,

    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order='F')

        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except Exception:  # Handle exceptions in game.
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.error
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:  # Save and quit.
            save_game(handler, "savegame.sav")
            raise
        except BaseException:  # Save on any other unexpected exception.
            save_game(handler, "savegame.sav")
            raise


if __name__ == "__main__":
    main()

# done add sound to the game
# todo add more sound effects
# todo improve npc ai, maybe move away from turn based
# todo npc can drop loot on death
# done keybinds menu
# done level up!
# done add dungeon floors
# done gear
# todo improve gear
# todo animate attacks and maybe use mouse click to attack. you get 1 attack per turn
# done inventory should be 1-n and best be clickable and not a-z.
# todo add more monster types and give them ranged attacks
# done add main menu
# done function to save game
# done auto pickup
# todo dropped items can be of higher quantity and can stack