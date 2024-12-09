^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package pal_app
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Forthcoming
-----------
* tpl: add app template for a basic chatbot (ie, no llm)
* tpl: intents/llm_bridge_python now compliant with PAL arch + support for setting locale
  While here, fix some error case when handling LLM responses
* tpl: intent/basic_chatbot now compliant with PAL arch + support for setting locale
* add a mapping between robots and features
  This enables us to have eg all PAL robots following the 'pal_arch' feature
  and adapt the templates accordingly.
  While here, added generic-pal, tiago-pro and tiago-head robots
  Also, adapt the tpl/mission/base_intents_python to use the
  new feature
* Contributors: Séverin Lemaignan

4.3.0 (2024-11-27)
------------------
* Fix trailing whitespace
* Moving module-related files to res/ directory
* Adding i18 support
* Updating instructions to create new translations
* Binary files shall be copied as is, and not parsed by jinja.
* tpl: add python3-requests as a dep of llm_bridge
* Contributors: Raquel Ros, Séverin Lemaignan

4.2.0 (2024-11-14)
------------------
* linting
* tpl: {ollama -> llm}_bridge_python
* tpl: apps: remove erroneous dep on db_connector
* tpl: ollama: use OpenAI REST API to get compat with both ollama and chatgpt
  As a nice side effect, no more dependency on python-ollama
* Contributors: Séverin Lemaignan

4.1.0 (2024-11-12)
------------------
* linting
* tpl: improve performance of the ollama intent extractor
* do not generate twice the 'say' skill
* more robust error handling during interactive tpl creation
* tpl: fix action client semantics in llm_supervisor
* tpl: various fixes in the greet_task_python tpl
* tpl: improve READMEs
* Contributors: Séverin Lemaignan

4.0.0 (2024-11-08)
------------------
* [tpl] complete the mission/llm_chatbot
* [tpl] various clean up
* [tpl] add new 'say' skill template
* [tpl] move missions templates around
* [tpl] missions/{super_basic_python -> base_python}
* [tpl] missions/{base_python -> base_intents_python}
* [tpl] more work on READMEs
* [tpl] clean up skill/base_python
* [tpl] replace db skill msgs by generic SkillControl msg
* [tpl] improve several READMEs
* [test] test that all the templates compile
* [tpl] remove unused deps from mission/super_basic_mission
* improve performance of the ollama connector
* mv chatbots tpl to a new 'intent extraction' category
  While here: chatbots now directly publish intents, no need for the
  chatbot_msgs/GetResponse.msg anymore
* polish the complete 'LLM chatbot' app. Still missing a way to take user input
* import chatbot_msgs for skills that require them
* minor clean up in greet_task_python tpl
* add a basic task python template
* gracefully handle ctrl+c during interactive tpl creation
* add a cmd line flag to display version
* initial working version of the ollama connector skill
  It includes independent dialogue histories for each user
* Contributors: Séverin Lemaignan

3.2.0 (2024-11-05)
------------------
* test: also enable auto-tests for ari and tiago variants
* fix linters issues in existing templates
* test: auto generate all possible template, and check with linters
* add 'rpk list' to list available templates
* add -y option to use default values
  while here, fix some paths on console output
* Contributors: Séverin Lemaignan

3.1.0 (2024-10-23)
------------------
* defined template for basic chatbot
* Contributors: lorenzoferrini

3.0.0 (2024-10-20)
------------------
* do not expose yet the LLM supervisor + app
* updated mission descriptions
* defined super basic mission template
* tune the rpk help descriptions
* [tpl] update the app template, adding a launch file
* [tpl] add tasks/greet_task_python}
* [tpl] update mission ctrl template with manifest + split ollama connector to own skill
* [tpl] add skills/llm_msgs
* [tpl] add skills/ollama_connector_python (not functional yet)
* [tpl] add skills/base_python (probably not functional yet)
* [tpl] {tasks/python -> tasks/greet_task_python}
* [tpl] {skills/python -> skills/db_commector_python}
* update README + add it as long_description in setup.py
* {pal_app -> rpk}
* add dependency on jinja2
* small script to fetch the task/skill dependencies of a app/task
* add manifests to the skill and task templates
* [tpl] add initial mission_ctrl/llm_chatbot_python
  currently, simply a copy of mission/base_python, with additional dependency on greet_task
* [tpl] mission_ctrl/{python -> base_python}
* completed the 'greet' task template. Starts by seems to be stuck somewhere
  (most likely waiting for the 'say' action client to become available)
* add basic initial template for the 'LLM' app -- just a metapkg for now
* rpk: handle dependencies between templates
* rpk: small refactor, no functional changes
* move missions and tasks tpl to new folder hierarchy
* [tpl] fully working skill template
  This template create a mock 'mongo db connector' and include the generation of a custom message package
  To test:
  $ pal_app create -r generic -p src skill -t simple_python -i mongo_db_connector
  $ colcon build --packages-select mongo_db_connector
  $ ros2 launch mongo_db_connector mongo_db_connector.launch.py
  You should then be able to call the skill via the /mongo_db_connector/db_request action:
  $ ros2 action send_goal /mongo_db_connector/db_request sample_skill_msgs/action/DbRequest ...
* support multiple template folders per type of code generation
  Use case: create a skill package + a example action msgs package
* prepare for tasks template + various minor bug fixes
* [tpl] basic skill template
* extended cmd line interface for applications and skill
  While here, did a couple of quality of life improvements, like sane defaults
* Contributors: Séverin Lemaignan, lorenzoferrini

2.3.0 (2024-10-16)
------------------
* add missing file after renaming to rpk
* Contributors: Séverin Lemaignan

2.2.0 (2024-10-14)
------------------
* {pal_app->rpk}
* Contributors: Séverin Lemaignan

2.1.0 (2024-08-20)
------------------
* refine a little the main app template, mostly documentation
* [tpl] clean-up README
* fix msg.data to data and readme
* fix indentation and add examples
* fix readme and say, perform motion intent calls
* Formatting fixed. Adding missing code for ARI.
* Formatting fixed
* create pages only for ari, change tts topic name
* extend to tiago and fix naming to mission controller
* Fix module set path
* Fix change state services and linters.
* Add communication hub management.
  Fix and added module management.
* Contributors: Luka Juricic, Raquel Ros, Sara Cooper, Séverin Lemaignan

2.0.2 (2024-07-03)
------------------
* update TTS action topic to /speak
* Contributors: Séverin Lemaignan

2.0.1 (2024-07-03)
------------------
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
