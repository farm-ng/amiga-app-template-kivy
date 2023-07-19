from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string(
    """
<PathScreen>
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            id: content_view
            size_hint_y: 0.9
            RelativeLayout:
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
                            Widget:
                                size_hint_y: 0.3
                        BoxLayout:
                            orientation: 'vertical'
                            size_hint_y: 0.5
                            Button:
                                id: action_button
                                size_hint_y: 0.1
                                text: 'O'
                            Widget:
                                size_hint_y: 0.1
                            Button:
                                id: zoom_in_button
                                size_hint_y: 0.1
                                text: '+'
                            Button:
                                id: zoom_out_button
                                size_hint_y: 0.1
                                text: '-'
        BoxLayout:
            id: bottom_menu_view
            size_hint_y: 0.1
            orientation: 'horizontal'
            BoxLayout:
                id: left_menu_view
                size_hint_x: 0.8
                Label:
                    id: status_label
                    text: 'Drive Amiga to ...'
            BoxLayout:
                id: right_menu_view
                size_hint_x: 0.2
                orientation: 'horizontal'
                Widget:
                    size_hint_x: 0.5
                Button:
                    id: cancel_button
                    text: 'Cancel'
                    on_release: root.on_back_to_main_button()
"""
)


class PathScreen(Screen):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def on_back_to_main_button(self) -> None:
        """Go back to main screen."""
        self.manager.current = "main_screen"
        self.manager.transition.direction = "right"
