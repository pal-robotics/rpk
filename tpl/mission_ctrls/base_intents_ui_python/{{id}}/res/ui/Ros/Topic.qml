/* Copyright (c) 2025 PAL Robotics SLU. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

import QtQuick 2.15

QtObject  {
    id: mockup_ros_topic

    property string topic: ""
    property string value: ""

    property string modality: ""
    property string source: ""
    property string expression: ""
    property string data: ""

    property bool isPublisher: true
    property bool isSubscriber: true

    function publish() {
        console.log("TOPIC: " + topic + ": msg published: \"" + value + "\"")
    }

    /* this function is only available in the RosSignal object */
    function signal() {
        console.log("ROSSIGNAL: " + topic + ": signal emitted")
    }

    Component.onCompleted: {
        console.log("NEW ROS TOPIC CREATED" + (topic ? ": " + topic : ""));

    }
}
