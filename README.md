rpk
=======

A tool to generate skeletons of robot application controller.

Relies on ROS 2 and the ROS 2 `Intents` interface.

**Note: this branch only contains ROS 2 support. For ROS 1, check the `main` branch.**

Installation
------------
`rpk` is written in python3.

**Installation with pip**

You require the following libraries:

``pip install jinja2``

You can install rpk as any other python package as follows:

``pip install .``

If the location where it is installed is not yet on your path, you will get a warning which includes the path location where it has been installed. You need to add this location to your path, e.g., in linux ``export PATH="$HOME/.local/bin:$PATH"`` or in [windows use the GUI or command line](https://stackoverflow.com/questions/9546324/adding-a-directory-to-the-path-environment-variable-in-windows)

**Installation with ROS debian**

Install the pal-alum-pal-app debian package and source ``/opt/pal/alum/setup.bash``.


Building your first rpk
---------------------------
Once you have installed rpk, you are ready to create new
applications for your robots. To do so, you just have to run:

``rpk create``

... and follow the instructions!

It will create a ROS2 package ready to be run.

You're then ready to play with the application controller.
Visit the PAL SDK documentation for further information.

