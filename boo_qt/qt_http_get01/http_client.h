#ifndef HTTPCLIENT_H
#define HTTPCLIENT_H

#include <QNetworkAccessManager>
#include <QObject>

class HttpClient : public QObject
{
    Q_OBJECT

public:
    HttpClient();

private:
    QNetworkAccessManager _manager;

public:
    Q_INVOKABLE void get(QString url);
};

#endif // HTTPCLIENT_H
