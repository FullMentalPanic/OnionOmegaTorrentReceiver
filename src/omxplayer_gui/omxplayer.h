#ifndef OMXPLAYER_H
#define OMXPLAYER_H

#include <QMainWindow>
#include <QVideoWidget>
#include <QFileDialog>
#include <QProgressBar>
#include <QSlider>
#include <QtCore/QCoreApplication>
#include <QtDBus/QtDBus>
#include <QKeyEvent>
#include <QFileInfo>


#include <QWidget>
#include <QDir>
#include <QListWidgetItem>
#include <QFileInfoList>
#include <QListWidget>
#include <QLineEdit>
#include <QVBoxLayout>
#include <QIcon>
#include <QStringList>
#include <QTextCodec>


#define OMXPLAYER "/usr/bin/omxplayer"
#define OMXPLAYER_DBUS "/home/pi/python_application/src/omxplayer_gui/dbuscontrol.sh"

#define PAUSE "pause"
#define STOP "stop"

namespace Ui {
class omxplayer;
}



const char*  const pause = "p";
const char*  const play = "p";
const char*  const stop = "q";
const char*  const left_arrow = "\033[D";
const char*  const up_arrow = "\033[A";
const char*  const right_arrow = "\033[C";
const char*  const down_arrow = "\033[B";


class omxplayer : public QMainWindow
{
    Q_OBJECT

public:
    explicit omxplayer(QWidget *parent = 0);
    ~omxplayer();


private slots:
    void on_actionOpen_triggered();
    void on_actionPause_triggered();
    void on_actionStop_triggered();
    void on_actionBack_triggered();
    void on_actionForward_triggered();
    void slotShow(QDir dir);
    void slotDirShow(QListWidgetItem *Item);
    void slotChoose(QListWidgetItem *Item);


private:
    Ui::omxplayer *ui;
    QProcess *player;
    QLineEdit *fileLineEdit;
    QListWidget *fileListWidget;
    QVBoxLayout *vLayout;
    QFileInfoList list;
    QWidget *filewidget;
    QString Videofile;
    void keyPressEvent(QKeyEvent * event);
    void showFileInfoList(QFileInfoList list);
};

#endif // OMXPLAYER_H
