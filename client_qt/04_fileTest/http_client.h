#ifndef HTTPCLIENT_H
#define HTTPCLIENT_H

#include <QObject>
#include <QNetworkAccessManager>

#include <QJSValue>
#include <QJsonDocument>
#include <QJsonObject>
#include <QSettings>


class HttpClient : public QObject
{
    Q_OBJECT

public:
    HttpClient();

private:
    QNetworkAccessManager  _manager;
    QString  _accessToken;
    QString _tokenType;

public:
    Q_INVOKABLE void login(QString url, QJSValue func, QString id, QString pw);

    Q_INVOKABLE void authorized_get(QString url, QJSValue func);
    Q_INVOKABLE void authorized_post(QString url, QJSValue func);
    Q_INVOKABLE void authorized_put(QString url, QJSValue func);

    Q_INVOKABLE void regester(QString url, QJSValue func, QString id, QString pw);
    Q_INVOKABLE void update_pw(QString url, QJSValue func, QString user_name, QString old_password, QString new_password);
    Q_INVOKABLE void update_db(QString url, QJSValue func, QString email, QString fullname);
    Q_INVOKABLE  void files_upload(QString url, QJSValue func, QString fileUrl);
};

#endif // HTTPCLIENT_H
