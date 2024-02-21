pal_app
=======

A tool to generate skeletons of robot application controller.

Relies on ROS 2 and the ROS 2 `Intents` interface.

**Note: this branch only contains ROS 2 support. For ROS 1, check the `main` branch.**

Installation
------------
`pal_app` is written in python3.

You require the following libraries:

``pip install jinja2``

You can install pal_app as any other python package as follows:

``pip install .``

and then add to the path the installed location:

``export PATH="$HOME/.local/bin:$PATH"``

Installing directly with sudo should make the package already available.


Building your first pal_app
---------------------------
Once you have installed pal_app, you are ready to create new
applications for your robots. To do so, you just have to run:

``pal_app create``

... and follow the instructions!

You're then ready to play with your robot application controller.
Visit the PAL SDK documentation for further information.

