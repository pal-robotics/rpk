^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package pal_app
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
