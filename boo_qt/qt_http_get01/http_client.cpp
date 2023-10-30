#include <QNetworkReply>

#include "http_client.h"


HttpClient::HttpClient()
{
}


void HttpClient::get(QString url)
{
    // SSL TLS
    // QSslConfiguration config = QSslConfiguration::defaultConfiguration();
    // config.setProtocol(QSsl::TlsV1_2);

    QNetworkRequest request;
    // request.setSslConfiguration(config); // SSL TLS
    request.setUrl(QUrl(url));
    QObject::connect(&_manager, &QNetworkAccessManager::finished,
        this, [=](QNetworkReply *reply) {
            if (reply->error()) {
                qDebug() << reply->errorString();
                return;
            }
            QString answer = reply->readAll();
            qDebug() << answer;
        }
    );
    _manager.get(request);
}
