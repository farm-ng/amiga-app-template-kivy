# Copyright (c) farm-ng, inc. Amiga Development Kit License, Version 0.1
import argparse
import asyncio
import os
import datetime
from typing import List

from amiga_package import ops

# import internal libs

# Must come before kivy imports
os.environ["KIVY_NO_ARGS"] = "1"

# gui configs must go before any other kivy import
from kivy.config import Config  # noreorder # noqa: E402

Config.set("graphics", "resizable", False)
Config.set("graphics", "width", "1280")
Config.set("graphics", "height", "800")
Config.set("graphics", "fullscreen", "false")
Config.set("input", "mouse", "mouse,disable_on_activity")
Config.set("kivy", "keyboard_mode", "systemanddock")

# kivy imports
from kivy.app import App  # noqa: E402
from kivy.lang.builder import Builder  # noqa: E402
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button


class AutoPlot(App):
    """Base class for the main Kivy app."""

    def __init__(self) -> None:
        super().__init__()

        self.counter: int = 0

        self.async_tasks: List[asyncio.Task] = []

    def build(self):
        return Builder.load_file("res/main.kv")

    def on_exit_btn(self) -> None:
        """Kills the running kivy application."""
        App.get_running_app().stop()

    def show_button(self,button):
        print(button.id)

    def on_toggle_button_press(self, instance, directory):
        print('Button pressed:', instance.text, directory)
        try:
            # Get the list of all files in the directory
            file_list = os.listdir(directory)

            # Loop through each file
            for filename in file_list:
                # Create the full file path by joining the directory and the filename
                filepath = os.path.join(directory, filename)

                # Check if it's a file, not a directory
                if os.path.isfile(filepath):
                    # Get file info
                    file_info = os.stat(filepath)

                    # Get file size
                    file_size = file_info.st_size

                    # Get file modification time
                    modification_time = datetime.datetime.fromtimestamp(file_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

                    # Print the information
                    print(f"File Name: {filename}, File Size: {file_size} bytes, Last Modified: {modification_time}")
        except FileNotFoundError:
            print(f"The directory '{directory}' does not exist.")
        except PermissionError:
            print(f"Permission denied for directory '{directory}'.")
    


    async def app_func(self):
        async def run_wrapper() -> None:
            # we don't actually need to set asyncio as the lib because it is
            # the default, but it doesn't hurt to be explicit
            await self.async_run(async_lib="asyncio")
            for task in self.async_tasks:
                task.cancel()

        # Placeholder task
        self.async_tasks.append(asyncio.ensure_future(self.template_function()))

        return await asyncio.gather(run_wrapper(), *self.async_tasks)

    async def template_function(self) -> None:
        """Placeholder forever loop."""
        while self.root is None:
            await asyncio.sleep(0.01)

        # while True:
        #     await asyncio.sleep(1.0)

        #     # increment the counter using internal libs and update the gui
        #     self.counter = ops.add(self.counter, 1)
        #     self.root.ids.counter_label.text = (
        #         f"{'Tic' if self.counter % 2 == 0 else 'Tac'}: {self.counter}"
        #     )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="template-app")

    # Add additional command line arguments here

    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(AutoPlot().app_func())
    except asyncio.CancelledError:
        pass
    loop.close()
