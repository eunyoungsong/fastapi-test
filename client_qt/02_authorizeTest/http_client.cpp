#include <memory>

#include <QNetworkReply>

#include "http_client.h"


HttpClient::HttpClient()
{
}

// V01 : consol version
//void HttpClient::get(QString url)
//{
//    // URL 설정
//    QNetworkRequest request;
//    request.setUrl(QUrl(url));

//    // connect
//    QObject::connect(&_manager, &QNetworkAccessManager::finished,
//        this, [=](QNetworkReply *reply) {
//            if (reply->error()) {
//                qDebug() << reply->errorString();
//                return;
//            }
//            QString answer = reply->readAll();
//            qDebug() << answer;
//        }
//    );
//    _manager.get(request);
//}


//// V02 : connect 쌓이는 오류  잡기 (임시방편)
//void HttpClient::get(QString url, QJSValue func)        // function(error, value)
//{
//    QNetworkAccessManager manager;

//    QUrl serviceURL(url);
//    QNetworkRequest request(serviceURL);

//    QNetworkReply *reply = manager.get(request);

//    QEventLoop eventLoop;
//    QObject::connect(reply, SIGNAL(finished()), &eventLoop, SLOT(quit()));
//    eventLoop.exec();

//    if(func.isCallable()){     // isCallable() : 함수이면  true
//        QJSValueList args;
//        if(reply->error()){
//            args << reply->error();
//            args << reply->errorString();
//            qDebug() << reply->errorString();
//        }
//        else {
//            QString answer = reply->readAll();
//            args << 0;
//            args << answer;
//            qDebug() << answer;
//        }
//        func.call(args);
//    }
//}

// V03 : connect 쌓이는 문제 해결 (너무어려움)
void HttpClient::get(QString url, QJSValue func)
{
    QNetworkRequest request;
    request.setUrl(QUrl(url));

    std::unique_ptr<QMetaObject::Connection> connection = std::make_unique<QMetaObject::Connection>();
    // unique_ptr : 특정 객체에 유일한 소유권을 부여 (이 포인터 말고는 객체를 소멸시킬 수 없다!)
    // make_unique : 스마트 포인터의 객체를 생성

    auto connectionPtr = connection.get();

    *connectionPtr = QObject::connect(&_manager, &QNetworkAccessManager::finished,
        this, [connection = std::move(connection), func](QNetworkReply *reply) {  // movd : unique_ptr 의 소유권 이전
            if (func.isCallable()) {
                if (reply->error()) {
                    QJSValueList args;
                    args << reply->error();
                    args << reply->errorString();
                    qDebug() << reply->errorString();
                    func.call(args);
                }
                else {
                    QJSValueList args;
                    QString answer = reply->readAll();
                    args << 0;
                    args << answer;
                    qDebug() << answer;
                    func.call(args);
                }
            }
            QObject::disconnect(*connection);
        }
    );
    _manager.get(request);
}


void HttpClient::post(QString url, QJSValue func)
{
    QByteArray jsonString = "{\"name\": \"eunyoung\", \"description\": \"POST test\", \"price\": 500, \"tax\": 500}";
    QByteArray postDataSize = QByteArray::number(jsonString.size());

    // URL 설정
    QNetworkRequest request;
    request.setUrl(QUrl(url));

    // Header 설정
    request.setRawHeader("User-Agent", "My app name v0.1");
    request.setRawHeader("X-Custom-User-Agent", "My app name v0.1");
    request.setRawHeader("Content-Type", "application/json");
    request.setRawHeader("Content-Length", postDataSize);

    std::unique_ptr<QMetaObject::Connection> connection = std::make_unique<QMetaObject::Connection>();
    auto connectionPtr = connection.get();

    *connectionPtr = QObject::connect(&_manager, &QNetworkAccessManager::finished,
        this, [connection = std::move(connection), func](QNetworkReply *reply) {
            if (func.isCallable()) {
                if (reply->error()) {
                    QJSValueList args;
                    args << reply->error();
                    args << reply->errorString();
                    qDebug() << reply->errorString();
                    func.call(args);
                }
                else {
                    QJSValueList args;
                    QString answer = reply->readAll();
                    args << 0;
                    args << answer;
                    qDebug() << answer;
                    func.call(args);
                }
            }
            QObject::disconnect(*connection);
        }
    );
    _manager.post(request, jsonString);

}


void HttpClient::put(QString url, QJSValue func)
{
    QByteArray jsonString = "{\"name\": \"eunyoung\", \"description\": \"PUT test\", \"price\": 500, \"tax\": 500}";
    QByteArray postDataSize = QByteArray::number(jsonString.size());

    QNetworkRequest request;
    request.setUrl(QUrl(url));

    std::unique_ptr<QMetaObject::Connection> connection = std::make_unique<QMetaObject::Connection>();
    auto connectionPtr = connection.get();

    *connectionPtr = QObject::connect(&_manager, &QNetworkAccessManager::finished,
        this, [connection = std::move(connection), func](QNetworkReply *reply) {
            if (func.isCallable()) {
                if (reply->error()) {
                    QJSValueList args;
                    args << reply->error();
                    args << reply->errorString();
                    qDebug() << reply->errorString();
                    func.call(args);
                }
                else {
                    QJSValueList args;
                    QString answer = reply->readAll();
                    args << 0;
                    args << answer;
                    qDebug() << answer;
                    func.call(args);
                }
            }
            QObject::disconnect(*connection);
        }
    );
    _manager.put(request, jsonString);
}



void HttpClient::deleteMethod(QString url, QJSValue func)
{
    QNetworkRequest request;
    request.setUrl(QUrl(url));

    std::unique_ptr<QMetaObject::Connection> connection = std::make_unique<QMetaObject::Connection>();
    auto connectionPtr = connection.get();

    *connectionPtr = QObject::connect(&_manager, &QNetworkAccessManager::finished,
        this, [connection = std::move(connection), func](QNetworkReply *reply) {
            if (func.isCallable()) {
                if (reply->error()) {
                    QJSValueList args;
                    args << reply->error();
                    args << reply->errorString();
                    qDebug() << reply->errorString();
                    func.call(args);
                }
                else {
                    QJSValueList args;
                    QString answer = reply->readAll();
                    args << 0;
                    args << answer;
                    qDebug() << answer;
                    func.call(args);
                }
            }
            QObject::disconnect(*connection);
        }
    );
    _manager.deleteResource(request);
}


void HttpClient::authorize(QString url, QJSValue func)
{
    QByteArray requestData = "grant_type=&username=johndoe&password=secret&scope=&client_id=&client_secret=";
    //QByteArray postDataSize = QByteArray::number(requestData.size());

    // URL 설정
    QNetworkRequest request;
    request.setUrl(QUrl(url));

    // Header 설정
    request.setRawHeader("accept", "application/json");
    request.setRawHeader("Content-Type", "application/x-www-form-urlencoded");

    std::unique_ptr<QMetaObject::Connection> connection = std::make_unique<QMetaObject::Connection>();
    auto connectionPtr = connection.get();

    *connectionPtr = QObject::connect(&_manager, &QNetworkAccessManager::finished,
        this, [connection = std::move(connection), func, this](QNetworkReply *reply) {
            if (func.isCallable()) {
                if (reply->error()) {
                    QJSValueList args;
                    args << reply->error();
                    args << reply->errorString();
                    qDebug() << reply->errorString();
                    func.call(args);
                }
                else {
                    QJSValueList args;
                    QString answer = reply->readAll();
                    args << 0;
                    args << answer;
                    qDebug() << answer;
                    func.call(args);

                    // token 저장하기 V1
                    QJsonDocument loadDoc(QJsonDocument::fromJson(answer.toUtf8()));
                    QJsonObject json = loadDoc.object();
                     _accessToken = json["access_token"].toString();
                     _tokenType = json["token_type"].toString();

//                    // token 저장하기 V2 : QSettings 사용
//                    QJsonDocument loadDoc(QJsonDocument::fromJson(answer.toUtf8()));
//                    QJsonObject json = loadDoc.object();
//                    QString accessToken = json["access_token"].toString();
//                    QString tokenType = json["token_type"].toString();

//                    QSettings settings("smsoft", "fastapi");
//                    settings.setValue("access_token", accessToken);
//                    settings.setValue("toke_type", tokenType);


                }
            }
            QObject::disconnect(*connection);
        }
    );
    _manager.post(request, requestData);
}


void HttpClient::authorized_get(QString url, QJSValue func)
{
    // URL 설정
    QNetworkRequest request;
    request.setUrl(QUrl(url));

    // JSON token 설정 ( 람다안에서 해줌 )

    request.setRawHeader("accept", "application/json");
    request.setRawHeader("Authorization", _tokenType.toUtf8()+ " " + _accessToken.toUtf8());    //V1
    //request.setRawHeader("Authorization", );

    std::unique_ptr<QMetaObject::Connection> connection = std::make_unique<QMetaObject::Connection>();
    auto connectionPtr = connection.get();

    *connectionPtr = QObject::connect(&_manager, &QNetworkAccessManager::finished,
        this, [connection = std::move(connection), func](QNetworkReply *reply) {
            if (func.isCallable()) {
                if (reply->error()) {
                    QJSValueList args;
                    args << reply->error();
                    args << reply->errorString();
                    qDebug() << reply->errorString();
                    func.call(args);
                }
                else {
                    QJSValueList args;
                    QString answer = reply->readAll();
                    args << 0;
                    args << answer;
                    qDebug() << answer;
                    func.call(args);
                }
            }
            QObject::disconnect(*connection);
        }
    );

   _manager.get(request);
}


void HttpClient::authorized_post(QString url, QJSValue func)
{
    QByteArray jsonString = "{\"name\": \"string\", \"description\": \"string\", \"price\": 5, \"tax\": 10}";
    QByteArray postDataSize = QByteArray::number(jsonString.size());

    QNetworkRequest request;
    request.setUrl(QUrl(url));

    request.setRawHeader("accept", "application/json");
    request.setRawHeader("Authorization", _tokenType.toUtf8()+ " " + _accessToken.toUtf8());
    request.setRawHeader("Content-Type", "application/json");

    std::unique_ptr<QMetaObject::Connection> connection = std::make_unique<QMetaObject::Connection>();
    auto connectionPtr = connection.get();

    *connectionPtr = QObject::connect(&_manager, &QNetworkAccessManager::finished,
        this, [connection = std::move(connection), func](QNetworkReply *reply) {
            if (func.isCallable()) {
                if (reply->error()) {
                    QJSValueList args;
                    args << reply->error();
                    args << reply->errorString();
                    qDebug() << reply->errorString();
                    func.call(args);
                }
                else {
                    QJSValueList args;
                    QString answer = reply->readAll();
                    args << 0;
                    args << answer;
                    qDebug() << answer;
                    func.call(args);
                }
            }
            QObject::disconnect(*connection);
        }
    );
    _manager.post(request, jsonString);
}


void HttpClient::authorized_put(QString url, QJSValue func)
{
    QByteArray jsonString = "{\"name\": \"eunyoung\", \"description\": \"PUT test\", \"price\": 500, \"tax\": 500}";
    QByteArray postDataSize = QByteArray::number(jsonString.size());

    QNetworkRequest request;
    request.setUrl(QUrl(url));

    request.setRawHeader("accept", "application/json");
    request.setRawHeader("Authorization", _tokenType.toUtf8()+ " " + _accessToken.toUtf8());
    request.setRawHeader("Content-Type", "application/json");

    std::unique_ptr<QMetaObject::Connection> connection = std::make_unique<QMetaObject::Connection>();
    auto connectionPtr = connection.get();

    *connectionPtr = QObject::connect(&_manager, &QNetworkAccessManager::finished,
        this, [connection = std::move(connection), func](QNetworkReply *reply) {
            if (func.isCallable()) {
                if (reply->error()) {
                    QJSValueList args;
                    args << reply->error();
                    args << reply->errorString();
                    qDebug() << reply->errorString();
                    func.call(args);
                }
                else {
                    QJSValueList args;
                    QString answer = reply->readAll();
                    args << 0;
                    args << answer;
                    qDebug() << answer;
                    func.call(args);
                }
            }
            QObject::disconnect(*connection);
        }
    );
    _manager.put(request, jsonString);
}
