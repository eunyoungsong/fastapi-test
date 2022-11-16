#include <QNetworkReply>

#include "http_client.h"


HttpClient::HttpClient()
{
}


void HttpClient::get(QString url, QJSValue func) const
{
    // SSL/TLS
    // QSslConfiguration config = QSslConfiguration::defaultConfiguration();
    // config.setProtocol(QSsl::TlsV1_2);

    QNetworkRequest request;
    // request.setSslConfiguration(config); // SSL TLS
    request.setUrl(QUrl(url));
    QObject::connect(&_manager, &QNetworkAccessManager::finished,
        this, [=](QNetworkReply *reply) {        //  [=] : lamda함수 캡쳐절로 참조 하는 모든 변수가 참조되고 캡처됨을 의미
            if (reply->error()) {
                if (func.isCallable()) {  // QJSValue::isCallable() : Returns true if this QJSValue is a function, otherwise returns false.
                    QJSValueList args;
                    args << reply->error();
                    args << reply->errorString();
                    func.call(args);
                }
            }
            if (func.isCallable()) {
                QJSValueList args;
                QString answer = reply->readAll();
                args << 0   ;
                args << answer;
                func.call(args);
            }
        }
    );
    _manager.get(request);
}
