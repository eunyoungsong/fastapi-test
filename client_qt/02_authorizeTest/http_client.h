#ifndef HTTPCLIENT_H
#define HTTPCLIENT_H

#include <QObject>
#include <QNetworkAccessManager>

#include <QJSValue>
#include <QJsonDocument>
#include <QJsonObject>
#include <QSettings>

//#include <QOAuth2AuthorizationCodeFlow>


class HttpClient : public QObject
{
    Q_OBJECT

public:
    HttpClient();

private:
    QNetworkAccessManager  _manager;
    //QOAuth2AuthorizationCodeFlow _auth;
    QString  _accessToken;
    QString _tokenType;

public:
    Q_INVOKABLE void get(QString url, QJSValue func);
    Q_INVOKABLE void post(QString url, QJSValue func);
    Q_INVOKABLE void put(QString url, QJSValue func);
    Q_INVOKABLE void deleteMethod(QString url, QJSValue func);

    Q_INVOKABLE void authorize(QString url, QJSValue func);
    Q_INVOKABLE void authorized_get(QString url, QJSValue func);
    Q_INVOKABLE void authorized_post(QString url, QJSValue func);
    Q_INVOKABLE void authorized_put(QString url, QJSValue func);
};

#endif // HTTPCLIENT_H
