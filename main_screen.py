from __future__ import annotations

from pathlib import Path

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.tabbedpanel import TabbedPanelItem
from utils import FileDescription, get_list_of_files

Builder.load_string(
    """
<MainScreen>
    BoxLayout:
        orientation: 'vertical'
        Widget:
            size_hint_y: 0.1
        RelativeLayout:
            id: content_view
            size_hint_y: 0.9
            TabbedPanel:
                id: tabbed_panel
                do_default_tab: False
                FilesTabbedPanel:
                    id: guide_line_panel
                    text: 'Guidance Line'
                    on_press: root.update_tabs_scroll_views(app.guide_path)
                FilesTabbedPanel:
                    id: path_panel
                    text: 'Path'
                    on_press: root.update_tabs_scroll_views(app.paths_path)
                FilesTabbedPanel:
                    id: field_bound_panel
                    text: 'Field Boundary'
                    on_press: root.update_tabs_scroll_views(app.boundary_path)
            Button:
                id: tab_action_button
                text: '+'
                pos_hint: {'top': 1.0, 'right': 1.0}
                size_hint: 0.1, 0.1
                on_release: root.on_tab_action_button()
<FilesTabbedPanel>:
    ScrollView:
        id: scroll_view
        do_scroll_x: False
        GridLayout:
            id: layout_grid
            cols: 1
            size_hint_y: None
            height: self.minimum_height
<FileDescriptionWidget@BoxLayout>:
    orientation: 'horizontal'
    size_hint_y: None
    Button:
        id: root.id
        text: root.text
        on_release: root.printing(root.text, root.id)
"""

)

# ui classes


class FilesTabbedPanel(TabbedPanelItem):
    pass


class FileDescriptionWidget(BoxLayout):
    id = StringProperty()
    text = StringProperty()
    
    def printing(self, text, id):
        print('Hello, you tapped a button', text)
        print('id is', id)
        print('Loading other file')
        
        # TODO URGENT Find a better way to change screens 
        # self.parent.parent.parent.parent.parent.parent.parent.parent.current = "boundary_screen"
        # print(self.parent)
    

class MainScreen(Screen):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # initialize tabbed panel
        # methods = [method_name for method_name in dir(MainScreen) if callable(getattr(MainScreen, method_name))]
        # print(methods)
        
        self.update_tabs_scroll_views(self.app.guide_path)

    @property
    def app(self) -> App:
        """Get app instance."""
        return App.get_running_app()
    

    # TODO: improve this later, now just to prove concept
    def update_tabs_scroll_views(self, path) -> None:
        """Update tabbed panel scroll views."""
        # get list of files to update
        print(path)
        data_path = Path(path)
        files: list[FileDescription] = get_list_of_files(data_path)

        # update tabbed panel
        for tab in self.ids.tabbed_panel.tab_list:
            # get tab scroll view
            tab_grid_layout: GridLayout = tab.ids.layout_grid

            # clear scroll view grid layout
            tab_grid_layout.clear_widgets()

            # add files to scroll view grid layout
            file: FileDescription
            for file in files:
                tab_grid_layout.add_widget(
                    FileDescriptionWidget(
                        id = file.name,
                        text = f"{tab.text} -- {file.name} -- {file.size_bytes} bytes -- {file.modification_time_str}"
                    )
                )

    def on_tab_action_button(self) -> None:
        """Handle tab action button press.
        This method is called when the tab action button is pressed and redirects to the correct screen.
        """
        # get current tab text
        current_tab_text: str = self.ids.tabbed_panel.current_tab.text.lower().replace(
            " ", "_"
        )

        # change screen
        if current_tab_text == "field_boundary":
            self.manager.current = "boundary_screen"
            self.manager.transition.direction = "left"
        elif current_tab_text == "path":
            self.manager.current = "path_screen"
            self.manager.transition.direction = "left"
        else:
            print("do nothing for now")