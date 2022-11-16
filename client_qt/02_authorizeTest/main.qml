import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
import QtQuick.Dialogs 1.2

import smsoft.http 1.0

Window {
    width: 700
    height: 600
    visible: true
    title: qsTr("FastAPI TEST")

    HttpClient {
        id: httpClient
    }


    function request_answer(error, value) {
       _request.text = value
    }


    ColumnLayout {
        width: 650
        anchors.centerIn: parent
        anchors.left: parent.left
        anchors.right: parent.right

        Button {
            text: qsTr("Authorize")
            anchors.right: parent.right
            onClicked: {
                _loginDial.open()
            }
        }

        RowLayout {
            Layout.topMargin: 50
            Label {
                text: "URL : "
            }
            TextField {
                id: _url
                Layout.fillWidth: true
                text: "http://127.0.0.1:8000/"
            }
        }

        RowLayout {

            Button {
                text: qsTr("get")
                Layout.fillWidth: true
                onClicked: {
                    //console.debug(_url.text)
                    httpClient.get("http://127.0.0.1:8000/users/me", request_answer)
                    //httpClient.get(_url.text, request_answer)
                }
            }
            Button {
                text: qsTr("post")
                Layout.fillWidth: true
                onClicked: {
                    httpClient.post("http://127.0.0.1:8000/items/", request_answer)
                }
            }
            Button {
                text: qsTr("put")
                Layout.fillWidth: true
                onClicked: {
                    httpClient.put("http://127.0.0.1:8000/items/5?q=test", request_answer)
                }
            }
            Button {
                text: qsTr("delete")
                Layout.fillWidth: true
                onClicked: {
                    httpClient.deleteMethod("http://127.0.0.1:8000/delete", request_answer)
                }
            }
        }

        Label {
            text: "Authorize TEST "
            topPadding: 50
        }

        RowLayout {
            Button {
                text: qsTr("LOGIN")
                Layout.fillWidth: true
                onClicked: {
                    httpClient.authorize("http://127.0.0.1:8000/token", request_answer)
                    _loginDial.close()
                }
            }
            Button {
                text: qsTr("get : crrent user")
                Layout.fillWidth: true
                onClicked: {
                    //console.debug(_url.text)
                    //httpClient.get(_url.text, request_answer)
                    httpClient.authorized_get("http://127.0.0.1:8000/users/me/", request_answer)
                }
            }
            Button {
                text: qsTr("get : items")
                Layout.fillWidth: true
                onClicked: {
                    //console.debug(_url.text)
                    //httpClient.get(_url.text, request_answer)
                    httpClient.authorized_get("http://127.0.0.1:8000/users/me/items/", request_answer)
                }
            }
            Button {
                text: qsTr("post : items")
                Layout.fillWidth: true
                onClicked: {
                    httpClient.authorized_post("http://127.0.0.1:8000/items/", request_answer)
                }
            }
            Button {
                text: qsTr("put : q")
                Layout.fillWidth: true
                onClicked: {
                    httpClient.authorized_put("http://127.0.0.1:8000/items/5?q=test", request_answer)
                }
            }
//            Button {
//                text: qsTr("authorized_delete")
//                Layout.fillWidth: true
//                onClicked: {
//                    httpClient.authorized_deleteMethod("http://127.0.0.1:8000/delete", request_answer)
//                }
//            }
        }

        Label {
            text: "Response : "
            topPadding: 50
        }

        ScrollView{
            Layout.fillWidth: parent
            implicitHeight: 200

            TextArea{
                id: _request
                readOnly: true
                Layout.fillWidth: true
                color: "white"
                background: Rectangle {
                    //implicitHeight: 200
                    color: "black"
                }
            }
        }
    }


    Dialog {
        id: _loginDial
        width: 500
        height: 380
        title: qsTr("FastAPI LOGIN")

        ColumnLayout {
            anchors.centerIn: parent
            anchors.left: parent.left
            anchors.right: parent.right

            TextField {
                id: _id
                placeholderText: "아이디"
                Layout.fillWidth: true
            }
            TextField {
                id: _pw
                placeholderText: "비밀번호"
                Layout.fillWidth: true
                echoMode: TextInput.Password
            }

            Button {
                text: qsTr("LOGIN")
                Layout.fillWidth: true
                onClicked: {
                    httpClient.authorize("http://127.0.0.1:8000/token", request_answer)
                    _loginDial.close()
                }
            }

            Label {
                topPadding: 10
                text: "Do you want register?"
            }

            Button {
                text: qsTr("등록하기")
                Layout.fillWidth: true
            }

        }
    }


}
