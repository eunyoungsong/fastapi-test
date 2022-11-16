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

//        RowLayout {
//            Layout.topMargin: 50
//            Label {
//                text: "URL : "
//            }
//            TextField {
//                id: _url
//                Layout.fillWidth: true
//                text: "http://127.0.0.1:8000/"
//            }
//        }

        Label {
            text: "Regestration Test"
            topPadding: 50
        }

        RowLayout {
            Button {
                text: qsTr("Creat User")
                Layout.fillWidth: true
                onClicked: {
                    _regesterDir.open()
                }
            }
            Button {
                text: qsTr("Current User")
                Layout.fillWidth: true
                onClicked: {
                    httpClient.authorized_get("http://127.0.0.1:8000/users/me", request_answer)
                }
            }
            Button {
                text: qsTr("Update DB")
                Layout.fillWidth: true
                onClicked: {
                    _updateDir.open()
                    httpClient.authorized_patch("http://127.0.0.1:8000/users/update_db", request_answer)
                }
            }
            Button {
                text: qsTr("Update password")
                Layout.fillWidth: true
                onClicked: {
                    httpClient.authorized_patch("http://127.0.0.1:8000/users/update_password", request_answer)
                }
            }
            Button {
                text: qsTr("File upload")
                Layout.fillWidth: true
                onClicked: {
                    _fileDial.open()
                }
            }
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
        standardButtons: "NoButton"

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
                    httpClient.login("http://127.0.0.1:8000/token", request_answer, _id.text, _pw.text)
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
                onClicked: {
                    _regesterDir.open()
                }
            }

        }
    }

    Dialog {
        id: _regesterDir
        width: 500
        height: 380
        title: qsTr("FastAPI regestration")
        standardButtons: "NoButton"

        ColumnLayout {
            anchors.centerIn: parent
            anchors.left: parent.left
            anchors.right: parent.right
            Label {
                topPadding: 10
                text: "Do you want register?"
            }

            TextField {
                id: _newid
                placeholderText: "아이디"
                Layout.fillWidth: true
            }
            TextField {
                id: _newpw
                placeholderText: "비밀번호"
                Layout.fillWidth: true
                echoMode: TextInput.Password
            }
            Button {
                text: qsTr("등록하기")
                Layout.fillWidth: true
                onClicked: {
                    httpClient.regester("http://127.0.0.1:8000/creat/user", request_answer, _newid.text, _newpw.text)
                    _regesterDir.close()
                }
            }
        }
    }


    Dialog {
        id: _updateDir
        width: 500
        height: 380
        title: qsTr("FastAPI DB")
        standardButtons: "NoButton"

        ColumnLayout {
            anchors.centerIn: parent
            anchors.left: parent.left
            anchors.right: parent.right
            Label {
                topPadding: 10
                text: "User DB"
            }

            TextField {
                id: _email
                placeholderText: "e-mail"
                Layout.fillWidth: true
            }
            TextField {
                id: _fullname
                placeholderText: "full_name"
                Layout.fillWidth: true
            }
            Button {
                text: qsTr("변경하기")
                Layout.fillWidth: true
                onClicked: {
                    httpClient.update_db("http://127.0.0.1:8000/users/update_db", request_answer, _email.text, _fullname.text)
                    _updateDir.close()
                }
            }
        }
    }


    FileDialog {
        id: _fileDial
        title: "Please choose a file"
        folder: shortcuts.home
        onAccepted: {
            httpClient.files_upload("http://127.0.0.1:8000/users/files", request_answer, _fileDial.fileUrl)
        }
    }


}
