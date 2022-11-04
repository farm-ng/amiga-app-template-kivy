# Amiga Brain 'virtual joystick' example

The purpose of this example application and tutorial is to enable you to develop your own custom apps and deploy them to the Amiga brain.

Here we provide an example application that:
- Receives an oak camera stream
- Receives the canbus stream
- Sends canbus commands to control the robot
- Creates kivy application

We hope that this tutorial is sufficient to get you started on developing your own custom Amiga brain applications.
If you feel we missed any key details, please let us know so we can help you through it and add it to the tutorial for the next hacker!


## Necessary Background

The Amiga brain app development meets at the intersection of three key libraries, and some farm-ng base libraries:

1. [gRPC](https://grpc.io/)
2. [asyncio](https://docs.python.org/3/library/asyncio.html)
3. [kivy](https://kivy.org/)
4. [farm-ng-base libraries](#farm-ng-base-libraries)

* Currently we are supporting Python app development, but our infrastructure allows for C++ app development in the near future.

### gRPC

The best place to start to gain an understanding of gRPC is the [gRPC introduction](https://grpc.io/docs/what-is-grpc/introduction/).

gRPC is used as our communication protocol between services (running in the background) and clients (what you link in your app).
The communication is through Protocol Buffers, defined in `*proto` files in our [farm-ng-base libraries](#farm-ng-base-libraries).

### asyncio

The best place to start to gain an understanding of asyncio is the [asyncio docs](https://docs.python.org/3/library/asyncio.html).

We use asyncio in order to run multiple concurrent tasks in our applications.
This allows us to walk and chew bubble gum, rather than take a step, take a chew, take a step, take a chew, and on...

In the virtual joystick example, this means we can have multiple, concurrent `while` loops running that:
- Receives the camera stream (from the camera service)
- Receives the canbus stream (from the canbus service)
- Draws the joystick (in [kivy](#kivy))
- Sends canbus commands (to the canbus service)

### kivy

The best place to start to gain an understanding of kivy is the [kivy Getting Started >> Introduction](https://kivy.org/doc/stable/gettingstarted/intro.html).

We use kivy to draw our apps and handle touch screen interactions for our interactive apps.
kivy has its own language -- [the Kv language](https://kivy.org/doc/stable/guide/lang.html), can be coded in Python, or some combination of both!

We tend to define our apps in the kv language at the top of the app files using `"""` strings, and may add some interaction in Python code.
In this example, however, we also demonstrate creating a custom kivy `Widget` in Python!

### farm-ng base libraries

We have some base libraries that are imported by the brain infrastructure and our apps.
They are:
- defined as python packages (installed with `pip` by pointing to the repo)
- contain the `.proto` definitions used in our gRPC communications
- contain the gRPC clients you can use to interact with the Amiga brain services

- [farm_ng_core](https://github.com/farm-ng/farm-ng-core)
- [farm_ng_amiga](https://github.com/farm-ng/amiga-brain-api)


## Code Breakdown

We recommend opening the [`virtual_joystick/main.py`](https://github.com/farm-ng/amiga-brain-example/blob/main/apps/virtual_joystick/main.py) example on the side as you read through this breakdown.

| NOTE: This assumes you have some experience with Python programming.

### imports

We start with generic Python imports that are used in the app,
followed by imports from our [farm-ng-base libraries](#farm-ng-base-libraries) such as `farm_ng.canbus` and `farm_ng.oak`.
These are both defined in the [farm_ng_amiga](https://github.com/farm-ng/amiga-brain-api) package.

With the kivy imports, things are slightly more complicated.
Before any kivy imports, we must define:
```Python
# Must come before kivy imports
os.environ["KIVY_NO_ARGS"] = "1"
```
so that the command line args for the app is used, rather than the default kivy command line args.

Next we import kivy `Config` and define the config parameters we recommend for running kivy applications on the brain.

```Python
from kivy.config import Config  # noreorder # noqa: E402

Config.set("graphics", "resizable", False)
Config.set("graphics", "width", "1280")
Config.set("graphics", "height", "800")
Config.set("graphics", "fullscreen", "false")
Config.set("input", "mouse", "mouse,disable_on_activity")
Config.set("kivy", "keyboard_mode", "systemanddock")
```

This should come before importing any other Kivy modules, as stated in [kivy - Configuration object](https://kivy.org/doc/stable/api-kivy.config.html).

Finally we import the remaining kivy modules we use in our app, with the
```Python
# noqa: E402
```
flag, so any `pre-commit` formatters don't move these imports above the configuration setting.

### kivy app definition

Next we define our application in the Kv language.
This definition can be a string at the top of a `.py` file or can be defined
in a separate `.kv` file.

| NOTE: We explain the kivy app that we create in this example, but this is by no means a thorough introduction to the kivy language. Try the [kivy tutorials](https://kivy.org/doc/stable/tutorials-index.html) and use the [kivy API](https://kivy.org/doc/stable/api-index.html) for more information on creating applications with kivy.

Two key components of kivy are [`Layouts`](https://kivy.org/doc/stable/gettingstarted/layouts.html#) and [`Widgets`](https://kivy.org/doc/stable/api-kivy.uix.html).
Kivy also has the concept of nesting, so you may notice in our app we have
3 `Label` widgets in a `BoxLayout`, which is in another `BoxLayout`, which itself is in the base `RelativeLayout`.

#### Base layout

The base of our app is a `RelativeLayout`, which contains a `Button` widget and a `BoxLayout`, with multiple nested Widgets and Layouts.

Reference: [Relative Layout](https://kivy.org/doc/stable/api-kivy.uix.relativelayout.html)

#### Back button

The `Button` is used to exit the app when it is pressed, by calling the `VirtualPendantApp.on_exit_btn()` method.

| NOTE: To be precise it's actually when the button is released due to using the `on_release:` keyword).

Since the `VirtualPendantApp` inherits from the kivy `App` class, methods and variables of the `VirtualPendantApp` can be linked with the `app.foo_variable` or `app.bar_method()`
We define the `Button` with two images, one that shows most of the time, and another that shows while the button is pressed down.
You can also just define a button with a string, if you just want test instead of an image.

| TIP: [Material Icons](https://github.com/google/material-design-icons) is a nice place to find symbols to use for app buttons / UI features.

Reference: Button](https://kivy.org/doc/stable/api-kivy.uix.button.html)

#### BoxLayout

We then have a box layout that stacks 3 sub-widgets horizontally (by default):
1. Another BoxLayout with 3 vertically stacked labels
2. A custom `Widget` called `VirtualJoystickWidget`, defined in Python below
3. A [`TabbedPanel`](https://kivy.org/doc/stable/api-kivy.uix.tabbedpanel.html).

Reference: [Box Layout](https://kivy.org/doc/stable/api-kivy.uix.boxlayout.html)

#### Labels

We define 3 labels that are live updated with class variables from the `VirtualPendantApp`.
In order to update the value, e.g.
```Python
Label:
    text: "state:\\n" + str(app.amiga_state)
```
the values must be declared as a `StringProperty` of the class
before the class is initialized and should be defined as type `str`, as in:
```Python
class VirtualPendantApp(App):
    # For kivy labels
    amiga_speed = StringProperty()
    amiga_rate = StringProperty()
    amiga_state = StringProperty()

    def __init__(
        ...
        self.amiga_state: str = "foo"
        self.amiga_speed: str = "bar"
        self.amiga_rate: str = "baz"
        ...
```

Reference: [Label](https://kivy.org/doc/stable/api-kivy.uix.label.html)

Reference: [StringProperty](https://kivy.org/doc/stable/api-kivy.properties.html#kivy.properties.StringProperty)

#### VirtualJoystickWidget

Since the `VirtualJoystickWidget` is fully defined in Python below, the only details we need to add is the `id:`, so the Widget can be easily referenced by the `App`.
This is done with:

```Python
FOO_WIDGET = self.root.ids['FOO_WIDGET_ID']
```
We could add more details here to define various `Widget` parameters, for instance a `size_hint`, but we just leave the default size to be used.

#### TabbedPanel

The `TabbedPanel` is used to select between different pages, which in our case is 4 `Image` Widgets.

Reference: [TabbedPanel](https://kivy.org/doc/stable/api-kivy.uix.tabbedpanel.html)

Reference: [Image](https://kivy.org/doc/stable/api-kivy.uix.image.html)

#### Take it further

Define two kivy [`Slider`](https://kivy.org/doc/stable/api-kivy.uix.slider.html) widgets that allow changing `max_speed` & `max_angular_rate`!
Play around with where you can put these and how you can link them directly to the value in the `VirtualPendantApp`.

Just remember, the actual rates the amiga drives at are limited by the vehicle control unit (VCU), so don't be surprised if the true max speed doesn't reflect the slider.