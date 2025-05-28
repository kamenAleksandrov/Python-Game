#!/usr/bin/env python3
import tcod
import traceback
import exceptions
import input_handlers
import color

import entity_factories
import setup_game


def main() -> None:
    screen_width = 80
    screen_height = 50

    tileset = tcod.tileset.load_tilesheet(
        "Images/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

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
