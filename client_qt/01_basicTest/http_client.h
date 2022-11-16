#ifndef HTTPCLIENT_H
#define HTTPCLIENT_H

#include <QObject>
#include <QNetworkAccessManager>
#include <QJSValue>

class HttpClient : public QObject
{
    Q_OBJECT

public:
    HttpClient();

private:
    QNetworkAccessManager   _manager;
    //QString _answer;
    //QNetworkReply *_reply;

public:
    Q_INVOKABLE void get(QString url, QJSValue value);
    Q_INVOKABLE void post(QString url, QJSValue value);
    Q_INVOKABLE void put(QString url, QJSValue value);
    Q_INVOKABLE void deleteMethod(QString url, QJSValue value);

    void connectMethod(QJSValue func);

    //void finished();
};

#endif // HTTPCLIENT_H
