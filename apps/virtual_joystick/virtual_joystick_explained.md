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

NOTE: This assumes you have some experience with Python programming.

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
