#include <QNetworkReply>

#include "http_client.h"


HttpClient::HttpClient()
{
}

void HttpClient::connectMethod(QJSValue func)
{
    QObject::connect(&_manager, &QNetworkAccessManager::finished,
        this, [=](QNetworkReply *reply) {
            if(func.isCallable()){      // QJSValue::isCallable() : Returns true if this QJSValue is a function, otherwise returns false.
                QJSValueList args;
                if(reply->error()){
                    args << reply->error();
                    args << reply->errorString();
                    qDebug() << reply->errorString();
                }
                else {
                    QString answer = reply->readAll();
                    args << 0;
                    args << answer;
                    qDebug() << answer;
                }
                func.call(args);
            } //if
        }
    );
}


// V01
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


// V02
// func 오류 : QMAKE_CXXFLAGS += -fpermissive 설정 해줘야함
void HttpClient::get(QString url, QJSValue func)        // qml 에서 function(error, value)
{
    // URL 설정
    QNetworkRequest request;
    request.setUrl(QUrl(url));

    QObject::connect(&_manager, &QNetworkAccessManager::finished,
        this, [=](QNetworkReply *reply) {
            if(func.isCallable()){      // QJSValue::isCallable() : Returns true if this QJSValue is a function, otherwise returns false.
                QJSValueList args;
                if(reply->error()){
                    args << reply->error();
                    args << reply->errorString();
                    qDebug() << reply->errorString();
                }
                else {
                    QString answer = reply->readAll();
                    args << 0;
                    args << answer;
                    qDebug() << answer;
                }
                func.call(args);
            } //if
        }
    );
    //connectMethod(func);
    _manager.get(request);
}



void HttpClient::post(QString url, QJSValue func)
{
    // Build your JSON string as usual
    QByteArray jsonString = "{\"name\": \"eunyoung\", \"description\": \"POST test\", \"price\": 500, \"tax\": 500}";

    // For your "Content-Length" header
    QByteArray postDataSize = QByteArray::number(jsonString.size());

    // URL 설정
    QUrl serviceURL(url);
    QNetworkRequest request(serviceURL);

    // Add the headers specifying their names and their values with the following method :
    // setRawHeader(const QByteArray & headerName, const QByteArray & headerValue);
    // Header 설정
    request.setRawHeader("User-Agent", "My app name v0.1");
    request.setRawHeader("X-Custom-User-Agent", "My app name v0.1");
    request.setRawHeader("Content-Type", "application/json");
    request.setRawHeader("Content-Length", postDataSize);

    QNetworkReply *reply = _manager.post(request, jsonString);

    if(func.isCallable()){
        QJSValueList args;
        if(reply->error()){
            args << reply->error();
            args << reply->errorString();
        }
        else {
            QString answer = reply->readAll();
            args << 0;
            args << answer;
        }
        func.call(args);
    }

    //connectMethod(func);
    //_manager.post(request, jsonString);
}


void HttpClient::put(QString url, QJSValue func)
{
    QByteArray jsonString = "{\"name\": \"eunyoung\", \"description\": \"PUT test\", \"price\": 500, \"tax\": 500}";
    QByteArray postDataSize = QByteArray::number(jsonString.size());

    QUrl serviceURL(url);
    QNetworkRequest request(serviceURL);

    QNetworkReply *reply = _manager.put(request, jsonString);

    if(func.isCallable()){
        QJSValueList args;
        if(reply->error()){
            args << reply->error();
            args << reply->errorString();
        }
        else {
            QString answer = reply->readAll();
            args << 0;
            args << answer;
        }
        func.call(args);
    }

    //connectMethod(func);
    //_manager.put(request, jsonString);
}



void HttpClient::deleteMethod(QString url, QJSValue func)
{
    QUrl serviceURL(url);
    QNetworkRequest request(serviceURL);

    QNetworkReply *reply = _manager.deleteResource(request);

    if(func.isCallable()){
        QJSValueList args;
        if(reply->error()){
            args << reply->error();
            args << reply->errorString();
        }
        else {
            QString answer = reply->readAll();
            args << 0;
            args << answer;
        }
        func.call(args);
    }

    //connectMethod(func);
    //_manager.deleteResource(request);
}

