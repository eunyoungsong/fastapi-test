#include <memory>
#include <QNetworkReply>
#include <QUrl>
#include <QFileInfo>
#include <QHttpPart>
#include <QRandomGenerator>

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


void HttpClient::login(QString url, QJSValue func, QString id, QString pw)
{
    //QByteArray requestData = "grant_type=&username=&password=&scope=&client_id=&client_secret=";
    //QByteArray postDataSize = QByteArray::number(requestData.size());

    QByteArray requestData = "grant_type=&username=";
    requestData.append(id.toUtf8() + "&password=" + pw.toUtf8() +"&scope=&client_id=&client_secret=");

//    // test
//    QString test(requestData);
//    qDebug() << test;

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
    request.setRawHeader("Authorization", _tokenType.toUtf8()+ " " + _accessToken.toUtf8());

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


void HttpClient::regester(QString url, QJSValue func, QString id, QString pw)
{
    // id pw 설정
    QJsonObject jsonData;
    jsonData.insert("username", id);
    jsonData.insert("password", pw);

    // josn타입 QbyteArray 로 바꿔주기
    QJsonDocument jsdoc;
    jsdoc.setObject(jsonData);

    QString jsonString = jsdoc.toJson();
    QByteArray requestData = jsonString.toUtf8();

    // url 설정
    QNetworkRequest request;
    request.setUrl(QUrl(url));

    // 헤더 설정
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
    _manager.post(request, requestData);
}


void HttpClient::update_pw(QString url, QJSValue func, QString user_name, QString old_password, QString new_password)
{
    QJsonObject jsonData;
    jsonData.insert("user_name", user_name);
    jsonData.insert("old_password", old_password);
    jsonData.insert("new_password", new_password);

    // josn타입 QbyteArray 로 바꿔주기
    QJsonDocument jsdoc;
    jsdoc.setObject(jsonData);

    QString jsonString = jsdoc.toJson();
    QByteArray requestData = jsonString.toUtf8();

    // url 설정
    QNetworkRequest request;
    request.setUrl(QUrl(url));

    // 헤더 설정
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
    _manager.put(request, requestData);
}




void HttpClient::update_db(QString url, QJSValue func, QString email, QString fullname)
{
    QJsonObject jsonData;
    jsonData.insert("email", email);
    jsonData.insert("full_name", fullname);

    // josn타입 QbyteArray 로 바꿔주기
    QJsonDocument jsdoc;
    jsdoc.setObject(jsonData);

    QString jsonString = jsdoc.toJson();
    QByteArray requestData = jsonString.toUtf8();

    // url 설정
    QNetworkRequest request;
    request.setUrl(QUrl(url));

    // 헤더 설정
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
    _manager.put(request, requestData);
}


//void HttpClient::files_upload(QString url, QJSValue func, QString fileUrl)
//{
////    // D(data) 로 설정되는거라 F(form) 로 설정되게끔 다시 구현해줘야한다
////    // fileName 설정
////    QString fileName = QUrl(fileUrl).fileName();
////    qDebug() << fileName;

////    // fileType 설정
////    QFileInfo fi(fileUrl);
////    QString fileType = fi.suffix();
////    qDebug() << fileType;

////    QString filedb = "file=@" +fileName + ";type=image/" + fileType;
////    qDebug() << filedb;

////    QByteArray requestData = filedb.toUtf8();

//    // Form 설정
//    QHttpMultiPart *multiPart = new QHttpMultiPart(QHttpMultiPart::FormDataType);

//    QHttpPart photo;
//    photo.setHeader(QNetworkRequest::ContentTypeHeader, QVariant("image/jpeg"));
//    photo.setHeader(QNetworkRequest::ContentDispositionHeader, QVariant("form-data; name=\"users/files\""));

//    QFile *file = new QFile("/home/eunyoung/Pictures/dog.jpg");
//    file->open(QIODevice::ReadWrite);
//    photo.setBodyDevice(file);
//    file->setParent(multiPart);

//    multiPart->append(photo);

//    // url 설정
//    QNetworkRequest request;
//    request.setUrl(QUrl(url));

//    // 헤더 설정
//    request.setRawHeader("accept", "application/json");
//    request.setRawHeader("Content-Type", "multipart/form-data");
//    //request.setRawHeader("Authorization", _tokenType.toUtf8()+ " " + _accessToken.toUtf8());

//    std::unique_ptr<QMetaObject::Connection> connection = std::make_unique<QMetaObject::Connection>();
//    auto connectionPtr = connection.get();

//    *connectionPtr = QObject::connect(&_manager, &QNetworkAccessManager::finished,
//    this, [connection = std::move(connection), func](QNetworkReply *reply) {
//            if (func.isCallable()) {
//                if (reply->error()) {
//                    QJSValueList args;
//                    args << reply->error();
//                    args << reply->errorString();
//                    qDebug() << reply->errorString();
//                    func.call(args);
//                }
//                else {
//                    QJSValueList args;
//                    QString answer = reply->readAll();
//                    args << 0;
//                    args << answer;
//                    qDebug() << answer;
//                    func.call(args);
//                }
//            }
//            QObject::disconnect(*connection);
//        }
//    );
//    _manager.post(request, multiPart);
//}


void HttpClient::files_upload(QString url, QJSValue func, QString fileUrl)
{
    QHttpMultiPart *multiPart = new QHttpMultiPart(QHttpMultiPart::FormDataType);

    QString fileName = QUrl(fileUrl).fileName();
    qDebug() << fileName;

    QString filePath = fileUrl.remove(0, 7);
    qDebug() << filePath;

    QHttpPart imagePart;
    imagePart.setHeader(QNetworkRequest::ContentTypeHeader, QVariant("image/jpeg"));
    imagePart.setHeader(QNetworkRequest::ContentDispositionHeader, QVariant("form-data; name=\"files\"; filename=\"" + fileName + "\""));

    QFile *file = new QFile(filePath);
    file->setParent(multiPart);
    file->open(QIODevice::ReadWrite);

    imagePart.setBodyDevice(file);
    multiPart->append(imagePart);


    QUrl serviceUrl = QUrl(url);
    QNetworkRequest request(serviceUrl);

    quint32 random[6];
    QRandomGenerator::global()->fillRange(random);
    QByteArray boundary = "--boundary_zyl_" + QByteArray::fromRawData(reinterpret_cast<char *>(random), sizeof(random)).toBase64();

    QByteArray contentType;
    contentType += "multipart/";
    contentType += "form-data";
    contentType += "; boundary=";
    contentType += boundary;
    multiPart->setBoundary(boundary);
    request.setHeader(QNetworkRequest::ContentTypeHeader, contentType);
    request.setRawHeader("accept", "application/json");
    //request.setRawHeader("Content-Type", "multipart/form-data;");


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
    _manager.post(request, multiPart);
}
