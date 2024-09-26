# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from rclpy.lifecycle import Node
from rclpy.lifecycle import State
from rclpy.lifecycle import TransitionCallbackReturn

from rclpy.action import ActionClient
from tts_msgs.action import TTS
from std_msgs.msg import String

from hri_actions_msgs.msg import Intent
from lifecycle_msgs.msg import State as StateMsg

from {{ id }}.dependent_tasks import get_referenced_tasks
from {{ id }}.ollama_connector import OllamaConnector

class MissionController(Node):

    def __init__(self) -> None:
        """Construct the node."""
        super().__init__('app_{{ id }}')

        self.get_logger().info("Initialising...")
        self._intents_sub = None
        self._timer = None

        self._text_input_sub = None
        self._text_output_pub = None

        self._ollama = None


    def on_intent(self, msg):

        self.get_logger().info("Received an intent: %s" % msg.intent)


        data = json.loads(msg.data) if msg.data else {}  # noqa: F841
        source = msg.source  # noqa: F841
        modality = msg.modality  # noqa: F841
        confidence = msg.confidence  # noqa: F841
        priority_hint = msg.priority  # noqa: F841

        if msg.intent == Intent.START_ACTIVITY:
            pass
        else:
            self.get_logger().warning("I don't know how to process intent "
                                      "<%s>!" % msg.intent)

    def generate_intent_list(self):

        tasks = get_referenced_tasks("{{ id }}", "task")

        intents = []

        for task in tasks:
            intents.append(
                    {"id": task["name"].upper(),
                     "description": task["description"],
                     "example": task["examples"][0]
                     }
                    )


    #########################################################################

    #################################
    #
    # Lifecycle transitions callbacks
    #
    def on_configure(self, state: State) -> TransitionCallbackReturn:
        """
        Configure the node
        """

        #host = 'http://spring-basestation:11434'
        host = 'http://localhost:11434'

        #model = 'llama3.1:8b'
        model = 'llama3.2:1b'
        
        self._ollama = OllamaConnector(host=host, model=model)



        self.get_logger().info('on_configure() is called.')
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state: State) -> TransitionCallbackReturn:
        """
        Activate the node
        """
        self._intents_sub = self.create_subscription(
            Intent,
            '/intents',
            self.on_intent,
            10)
        self.get_logger().info("Listening to %s topic" %
                               self._intents_sub.topic_name)

        self._text_input_sub = self.create_subscription(
            String,
            '/user_input',
            lambda msg : self._ollama.input_queue.put_nowait(msg.data),
            10)
        self.get_logger().info("Listening to %s topic for user input" %
                               self._text_input_sub.topic_name)


        self._text_output_pub = self.create_publisher(String, '/robot_output', 10)
        self.get_logger().info("Robot output will be published on topic %s" %
                               self._text_output_pub.topic_name)


        timer_period = 0.1  # in sec
        self._timer = self.create_timer(timer_period, self.run)

        self.get_logger().info("Running")

        return super().on_activate(state)

    def on_deactivate(self, state: State) -> TransitionCallbackReturn:
        """Stop the timer to stop calling the `run` function (main task of your application)."""
        self.get_logger().info("Stopping application")

        self.destroy_timer(self._timer)
        self.destroy_subscription(self._intents_sub)

        return super().on_deactivate(state)

    def on_shutdown(self, state: State) -> TransitionCallbackReturn:
        """
        Shutdown the node, after a shutting-down transition is requested.

        :return: The state machine either invokes a transition to the
            "finalized" state or stays in the current state depending on the
            return value.
            TransitionCallbackReturn.SUCCESS transitions to "finalized".
            TransitionCallbackReturn.FAILURE remains in current state.
            TransitionCallbackReturn.ERROR or any uncaught exceptions to
            "errorprocessing"
        """
        self.destroy_timer(self._timer)
        self.destroy_subscription(self._intents_sub)

        self.get_logger().info('Shutting down node.')
        return TransitionCallbackReturn.SUCCESS

    def run(self) -> None:

        if self._ollama and not self._ollama.output_queue.empty():
            msg = self._ollama.output_queue.get_nowait()
            self._text_output_pub.publish(String(data=msg))

        self.get_logger().info(str(self.inc))

