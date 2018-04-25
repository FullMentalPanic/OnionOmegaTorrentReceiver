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
//const char*  const left_arrow = (wchar_t) 8594 ;
//const char*  const up_arrow = '\u2191';
//const char*  const right_arrow = '\u2192';
//const char*  const down_arrow = '\u2193';


class omxplayer : public QMainWindow
{
    Q_OBJECT

public:
    explicit omxplayer(QWidget *parent = 0);
    ~omxplayer();


private slots:
    void on_actionOpen_triggered();
    void on_actionPlay_triggered();
    void on_actionPause_triggered();
    void on_actionStop_triggered();
    void on_actionBack_triggered();
    void on_actionForward_triggered();
    //--显示当前目录下的所有文件
    void slotShow(QDir dir);
    //----根据选择显示下一级目录下的文件，
    void slotDirShow(QListWidgetItem *Item);


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
    //---用双击浏览器中显示的目录进入下一级，或者返回上一级目录。
    void showFileInfoList(QFileInfoList list);
};

#endif // OMXPLAYER_H
