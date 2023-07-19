from __future__ import annotations

from pathlib import Path

from farm_ng.gps import gps_pb2
from farm_ng.gps_utils.coordinates import GpsCoordinates
from farm_ng.internal_widgets.mapview import AmigaMapView, map_marker_to_gps_proto
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.image import AsyncImage
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatter import Scatter

CURRENT_DIR = Path(__file__).parent


Builder.load_string(
    """
<FullMapView>:
    BoxLayout:
        orientation: 'horizontal'
        Widget:
            size_hint_x: 0.9
        BoxLayout:
            id: map_controls_layout
            orientation: 'vertical'
            size_hint_x: 0.1
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: 0.5
                Widget:
                    size_hint_y: 0.1
                Button:
                    id: compass_button
                    size_hint_y: 0.1
                    text: 'N'
                    on_release: root.set_compass()
                Widget:
                    size_hint_y: 0.3
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: 0.5
                Button:
                    id: action_button
                    size_hint_y: 0.1
                    text: 'O'
                    on_release: root.on_action_button()
                Widget:
                    size_hint_y: 0.1
                Button:
                    id: zoom_in_button
                    size_hint_y: 0.1
                    text: '+'
                    on_release: root.map_view.zoom_in()
                Button:
                    id: zoom_out_button
                    size_hint_y: 0.1
                    text: '-'
                    on_release: root.map_view.zoom_out()

<FakeMapViewScatter>:
    do_rotation: False
    do_scale: True
    do_translation: True
"""
)


class FullMapView(RelativeLayout):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.map_view = AmigaMapView()
        self.add_widget(self.map_view)

        # configure the map view
        self.map_view.set_map_source("satellite")

        # center on the default settings
        self.set_compass()

    @property
    def app(self) -> App:
        return App.get_running_app()

    # TODO: later possibly will do another thing
    def set_compass(self) -> None:
        """Center the map view on the current location."""
        if self.app.current_location is None:
            print("current location is None")
            return
        self.map_view.center_on(
            self.app.current_location.lat,
            self.app.current_location.lon,
        )
        self.map_view.zoom = self.map_view.default_zoom

    def on_action_button(self) -> None:
        self.add_waypoint()

    def add_waypoint(self) -> None:
        """Add a waypoint to the map view from the current location."""
        if self.app.current_location is None:
            print("current location is None")
            return

        # draw the waypoint on the map view
        self.map_view.add_map_marker(
            self.app.current_location.lat,
            self.app.current_location.lon,
        )

        # draw the lines between the waypoints
        if len(self.map_view.current_markers) > 1:
            # get the coordinates of the markers
            coordinates: list[tuple[float, float]] = [
                [marker.lon, marker.lat] for marker in self.map_view.current_markers
            ]

            # create a new geojson layer
            geojson = {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {
                            "color": "blue",
                            "stroke-width": 2,
                        },
                        "geometry": {"type": "LineString", "coordinates": coordinates},
                    }
                ],
            }

            # update the geojson layer
            self.map_view.geojson_layer.geojson = geojson

            # allow to finish the drawing
            # TODO: this is not the best place to do this
            self.parent.parent.parent.ids.finish_save_done_button.disabled = False

    def get_polygon_geojson(self) -> dict:
        """Get the geojson of the polygon."""
        # get the coordinates of the markers
        coordinates: list[tuple[float, float]] = [
            [marker.lon, marker.lat] for marker in self.map_view.current_markers
        ]
        # add the first point to close the polygon
        coordinates.append(coordinates[0])

        # create a new geojson layer
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "color": "blue",
                        "stroke-width": 2,
                    },
                    "geometry": {"type": "LineString", "coordinates": coordinates},
                }
            ],
        }
        return geojson

    def get_waypoints(self) -> list[gps_pb2.GpsFrame]:
        """Get the waypoints from the map view."""
        return [
            map_marker_to_gps_proto(marker) for marker in self.map_view.current_markers
        ]


# TODO: finish me ... easy to go with AmigaMapView
class FakeMapViewScatter(Scatter):
    """A fake map view for testing purposes."""

    default_source = str(CURRENT_DIR / "dummy_map.jpeg")
    default_zoom: float = 1.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # set the background image
        # with self.canvas:
        #    Color(1, 1, 1, 1)  # white
        #    self.rect = Rectangle(size=self.size, pos=self.pos)

        # NOTE: just to showcase how to add an image to the map view
        # TODO: this is not geo-referenced and should be replaced with a real map
        # from a map provider.
        self.add_widget(AsyncImage(source=self.default_source))

    @property
    def app(self) -> App:
        return App.get_running_app()

    def draw_waypoint(self, waypoint: GpsCoordinates) -> None:
        """Draw a waypoint on the map view"""
        pass
