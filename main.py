# Copyright (c) farm-ng, inc. Amiga Development Kit License, Version 0.1
from __future__ import annotations

import argparse
import asyncio
import os
from pathlib import Path

# global constants (in pixels)
FARM_NG_SCREEN_WIDTH_PX = 1280
FARM_NG_SCREEN_HEIGHT_PX = 800

# global constants for data paths
# TODO: make this configurable or get from launch file
FARM_NG_DEFAULT_DATA_PATH = Path("/data/farm_ng")

# Must come before kivy imports
os.environ["KIVY_NO_ARGS"] = "1"

# gui configs must go before any other kivy import
from kivy.config import Config  # noreorder # noqa: E402

Config.set("graphics", "resizable", False)
Config.set("graphics", "width", str(FARM_NG_SCREEN_WIDTH_PX))
Config.set("graphics", "height", str(FARM_NG_SCREEN_HEIGHT_PX))
Config.set("graphics", "fullscreen", "false")
Config.set("input", "mouse", "mouse,disable_on_activity")
Config.set("kivy", "keyboard_mode", "systemanddock")

# kivy imports
from boundary_screen import BoundaryScreen
from farm_ng.gps_utils.coordinates import GpsCoordinates
from kivy.app import App  # noqa: E402
from kivy.uix.screenmanager import ScreenManager
from main_screen import MainScreen
from path_screen import PathScreen
from map_view import FullMapView

class AutoPlot(App):
    """The main application class."""

    def __init__(self, data_path: Path) -> None:
        super().__init__()
        self._data_path = data_path

        self.async_tasks: list[asyncio.Task] = []

        self.base_gps_coordinates = GpsCoordinates(
            lat=36.910233, lon=-121.756897, alt=0.0
        )
        self.current_location: GpsCoordinates | None = None

    @property
    def data_path(self) -> Path:
        """The path to the data directory."""
        return self._data_path

    @property
    def paths_path(self) -> Path:
        """The path to the saved paths directory."""
        return "/data/farm_ng/autoplot_files/paths"
    
    @property
    def guide_path(self) -> Path:
        """The path to the saved paths directory."""
        return "/data/farm_ng/autoplot_files/guide"  
    
    @property
    def boundary_path(self) -> Path:
        """The path to the saved paths directory."""
        return "/data/farm_ng/autoplot_files/boundary"

    def build(self) -> ScreenManager:
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name="main_screen"))
        self.sm.add_widget(BoundaryScreen(name="boundary_screen"))
        self.sm.add_widget(PathScreen(name="path_screen"))
        # set the current screen to the MainScreen
        self.sm.current = "main_screen"
        return self.sm

    async def app_func(self) -> None:
        async def run_wrapper() -> None:
            # we don't actually need to set asyncio as the lib because it is
            # the default, but it doesn't hurt to be explicit
            await self.async_run(async_lib="asyncio")
            for task in self.async_tasks:
                task.cancel()

        # task to read from the gps
        self.async_tasks.append(asyncio.create_task(self.stream_gps()))

        return await asyncio.gather(run_wrapper(), *self.async_tasks)

    async def stream_gps(self) -> None:
        # TODO: implement this for real using the client
        import torch

        while True:
            # add some noise to the gps coordinates
            lat, lon, alt = torch.randn(3).mul(0.0001).tolist()
            self.current_location = GpsCoordinates(
                lat=self.base_gps_coordinates.lat + lat,
                lon=self.base_gps_coordinates.lon + lon,
                alt=self.base_gps_coordinates.alt + alt,
            )
            await asyncio.sleep(0.1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="autoplot-app")
    args = parser.parse_args()

    loop = asyncio.get_event_loop()

    app = AutoPlot(data_path=FARM_NG_DEFAULT_DATA_PATH)

    try:
        loop.run_until_complete(app.app_func())
    except asyncio.CancelledError:
        pass
    finally:
        loop.close()
