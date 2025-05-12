#!/usr/bin/env python3
import copy
import tcod
import traceback
import exceptions
import input_handlers
import color

from engine import Engine
import entity_factories
from procgen import generate_dungeon

def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 2
    max_items_per_room = 2

    tileset = tcod.tileset.load_tilesheet(
        "Images/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size = room_min_size,
        room_max_size = room_max_size,
        map_width = map_width,
        map_height = map_height,
        max_monsters_per_room = max_monsters_per_room,
        max_items_per_room=max_items_per_room,
        engine=engine,
    )
    engine.update_fov()

    engine.message_log.add_message(
        "Hello adventurer,suffer well in yet another dungeon!", color.welcome_text
    )

    handler: input_handlers.BaseEventHandler = input_handlers.MainGameEventHandler(engine)

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
            # TODO: Add the save function here
            raise
        except BaseException:  # Save on any other unexpected exception.
            # TODO: Add the save function here
            raise


if __name__ == "__main__":
    main()

# todo add sound to the game
# todo improve npc ai, maybe move away from turn based
# todo npc can drop loot on death
# todo keybinds menu
# todo level up!
# todo add dungeon floors
# todo gear?
# todo animate attacks and maybe use mouse click to attack. you get 1 attack per turn
# todo inventory should be 1-X and best be clickable and not a-z.
# todo add more monster types and give them ranged attacks
# todo add main menu
# todo function to save game