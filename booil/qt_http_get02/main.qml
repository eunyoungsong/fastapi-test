import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Window 2.12

import smsoft 1.0

Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Hello World")

    HttpClient {
        id: httpClient
    }

    function a(error, value) {
        _text.text = value
    }

    Column {
        Text {
            id: _text
            text: "no text"
            height: 200
        }

        Button {
            text: "get http://www.smsoft.co.kr"
            onClicked: {
                httpClient.get("http://www.smsoft.co.kr", a)
            }
        }
    }
}
