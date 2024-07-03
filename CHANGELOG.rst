^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package pal_app
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Forthcoming
-----------
* update to new TTS.action msg
* rename tts package
* Contributors: Luka Juricic, Séverin Lemaignan

2.0.0 (2024-05-07)
------------------
* added registering to pal modules
* Apache licensing
* Update README.md
* added launch file
* Use setuptools instead of distutils
* Changed file structure so the source files are in directory with the same name as the package
* Copyright fixing. Added License file
* Removed pip install option. Added note to refer to ROS 1 development
* Converted application_controller to lifecycle node. Cleaned run_app script to only call application_controller node accordingly. Transitions between cycles are done through CLI lifecycle calls
* Migration to ROS 2.
* Contributors: Luka Juricic, Raquel Ros, ferrangebelli

0.3.0 (2023-07-14)
------------------
* Updated pages which close the cycle between the supervisor and the touch pages.
  Examples of use for both /intent and /user_input topics
* Contributors: raquelros

0.2.2 (2023-05-15)
------------------
* [tpl] fix links in generated READMEs
* Contributors: Séverin Lemaignan

0.2.1 (2023-05-15)
------------------
* [tpl] en_US->en_GB
* remove chatbot from tpl
  Will be brought back when the chatbot training/installation story is better
* allow killing all threads on sigint
* Contributors: Luka Juricic, Séverin Lemaignan

0.2.0 (2023-02-27)
------------------
* more checks to ensure the app ID is valid
* [python tpl] fix typo in run_app
* [python tpl] by default, auto-start the application
  use _autostart:=False to prevent auto-starting.
* warn user if no tpl found instead of silently failing
* doc
* added more interesting HTML pages, that also trigger intents
* install template for chatbot and webpages
* more explanation in README
* Contributors: Séverin Lemaignan

0.1.13 (2023-01-25)
-------------------
* set the version in setup.py from package.xml
* Contributors: Séverin Lemaignan

0.1.12 (2023-01-23)
-------------------
* compat with jinja2 v2
* Contributors: Séverin Lemaignan

0.1.11 (2023-01-23)
-------------------
* compat with older jinja2
  Older jinja2 does not seem to like the pathlib.Path interface
* fix typo
* Contributors: Séverin Lemaignan

0.1.10 (2023-01-23)
-------------------
* add missing sub-directory to pkg root
* Contributors: Séverin Lemaignan

0.1.9 (2023-01-23)
------------------
* gracefully fail if Intent.msg is not available
* Contributors: Séverin Lemaignan

0.1.8 (2023-01-23)
------------------
* remove dependency on ROS libraries
* Contributors: Séverin Lemaignan

0.1.7 (2023-01-05)
------------------
* fix default example to work on robot.
* Contributors: Aina Irisarri

0.1.5 (2022-12-05)
------------------
* fix pkg deps
* ensure the user select a command
* Contributors: Séverin Lemaignan

0.1.4 (2022-12-05)
------------------
* [python tpl] re-architecture to have a single blocking action call, with an action cancel to stop the app
* correctly return the robot name
* {pal_create_app -> pal_app create}
* Contributors: Séverin Lemaignan

0.1.3 (2022-11-29)
------------------
* on ARI, generate a simple behaviour when the intent 'ENGAGE_WITH' is detected
* add GPLv3 license + please pypi
* take the target robot as parameter
* [tpl] add 'application' role to package.xml + doc
* generate template for intents handling
* ensure we depend on actionlib and hri_actions_msgs
* retrieve the list of intents from Intent.msg
* add cmake target to package the behaviour as a zip archive
* generate a complete ROS package
* Contributors: Séverin Lemaignan
