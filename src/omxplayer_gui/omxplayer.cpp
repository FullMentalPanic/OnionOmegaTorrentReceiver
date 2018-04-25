#include "omxplayer.h"
#include "ui_omxplayer.h"

/*
1           decrease speed
2           increase speed
<           rewind
>           fast forward
z           show info
j           previous audio stream
k           next audio stream
i           previous chapter
o           next chapter
n           previous subtitle stream
m           next subtitle stream
s           toggle subtitles
w           show subtitles
x           hide subtitles
d           decrease subtitle delay (- 250 ms)
f           increase subtitle delay (+ 250 ms)
q           exit omxplayer
p / space   pause/resume
-           decrease volume
+ / =       increase volume
left arrow  seek -30 seconds
right arrow seek +30 seconds
down arrow  seek -600 seconds
up arrow    seek +600 seconds
 */

omxplayer::omxplayer(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::omxplayer)
{
    ui->setupUi(this);
    player = new QProcess();

    fileLineEdit = new QLineEdit("/mnt/volume/download/", this);
    fileListWidget = new QListWidget(this);

    filewidget = new QWidget();
    vLayout = new QVBoxLayout(this);
    vLayout->addWidget(fileLineEdit);
    vLayout->addWidget(fileListWidget);
    filewidget->setLayout(vLayout);
    this->setCentralWidget(filewidget);


    //--设置对应信号与槽
    connect(fileListWidget, SIGNAL(itemDoubleClicked(QListWidgetItem *)),
                this, SLOT(slotDirShow(QListWidgetItem*)));

    QString rootStr = "/mnt/volume/download/";
    QDir rootDir(rootStr);
    QStringList stringlist;
    stringlist << "*";
    list = rootDir.entryInfoList(stringlist);
    showFileInfoList(list);

    //---显示布局
 //   setLayout(vLayout);
    //----设置窗口属性
    //setWindowTitle("File View");
}

omxplayer::~omxplayer()
{
    delete ui;
}

void omxplayer::keyPressEvent(QKeyEvent * event)
{
    switch (event->key()) {
    case Qt::Key_P:
        on_actionPlay_triggered();
        break;
    case Qt::Key_Q:
        on_actionStop_triggered();
        break;
    case Qt::Key_O:
        on_actionOpen_triggered();
        break;
    case Qt::Key_Left:
        on_actionBack_triggered();
        break;
    case Qt::Key_Right:
        on_actionForward_triggered();
    default:
        //this->raise();
        //this->activateWindow();
        break;
    }
}

void omxplayer::on_actionOpen_triggered()
{
    //this->raise();
    //this->activateWindow();
    //on_actionPause_triggered();
    //QString filename = QFileDialog::getOpenFileName(this,"Open a file", "/nmt/volumn/download/", "Video File (*.avi, *.mpg, *.mp4)");
    QStringList args;
    QString prog = OMXPLAYER;
    on_actionStop_triggered();
    args << Videofile;
    player->start(prog, args);
    ui->statusBar->showMessage(Videofile);

}

void omxplayer::on_actionPlay_triggered()
{
    player->write(play);
    ui->statusBar->showMessage("Playing");
}

void omxplayer::on_actionPause_triggered()
{

    player->write(pause);
    ui->statusBar->showMessage("Paused");
}

void omxplayer::on_actionStop_triggered()
{

    player->write(stop);
    ui->statusBar->showMessage("Stoped");
}

void omxplayer::on_actionBack_triggered()
{
    player->write(left_arrow);
    ui->statusBar->showMessage("-30");
}


void omxplayer::on_actionForward_triggered()
{
    player->write(right_arrow);
    ui->statusBar->showMessage("+30");

}

//--显示当前目录下的所有文件
void omxplayer::slotShow(QDir dir)
{
     QStringList stringList;
     stringList << "*";
     QFileInfoList InfoList = dir.entryInfoList(stringList, QDir :: AllEntries, QDir :: DirsFirst);
     showFileInfoList(InfoList);
}

//---用双击浏览器中显示的目录进入下一级，或者返回上一级目录。
void omxplayer::showFileInfoList(QFileInfoList list)
{
    //--清空列表控件
    fileListWidget->clear();

    //----取出所有项，按照目录，文件方式添加到控件内
    for (unsigned int i = 0; i < list.count(); i++)
    {
        QFileInfo tmpFileInfo = list.at(i);
        if (tmpFileInfo.isDir())
        {
            QString fileName = tmpFileInfo.fileName();
            QListWidgetItem*tmpListWidgetItem = new QListWidgetItem( QIcon(":/images/icon/dir.png"), fileName);
            fileListWidget->addItem(tmpListWidgetItem);
        }
        else
        {
            QString ext = tmpFileInfo.completeSuffix();

            if ( (ext == "mp4") || (ext == "avi") || (ext == "mkv") )
            {
                QString fileName = tmpFileInfo.fileName();
                QListWidgetItem*tmpListWidgetItem = new QListWidgetItem( QIcon(":/images/icon/file.png"), fileName);
                fileListWidget->addItem(tmpListWidgetItem);
            }
        }
    }
}

//----根据用户的选择显示下一级目录下的文件，
void omxplayer::slotDirShow(QListWidgetItem *Item)
{
    //----保存下一级目录名
    QString string = Item->text();
    QDir dir;
    //----设置路径为当前目录路径
    dir.setPath(fileLineEdit->text());
    //-----重新设置路径
    if (dir.cd(string))
    {
        //----更新当前显示路径， 这里获取的是绝对路径
        fileLineEdit->setText(dir.absolutePath());
        //---显示当前文件目录下的所有文件
        slotShow(dir);
    }
    else
    {
        Videofile = dir.absolutePath().append('/');
        Videofile.append(string);
        ui->statusBar->showMessage(Videofile);
    }

}
