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


    connect(fileListWidget, SIGNAL(itemClicked(QListWidgetItem *)),
                this, SLOT(slotChoose(QListWidgetItem*)));
    connect(fileListWidget, SIGNAL(itemDoubleClicked(QListWidgetItem *)),
                this, SLOT(slotDirShow(QListWidgetItem*)));
    connect(fileListWidget,SIGNAL(currentItemChanged(QListWidgetItem *,QListWidgetItem *)),
            this,SLOT(slotChoose_1(QListWidgetItem*,QListWidgetItem*)));
    connect(fileListWidget, SIGNAL(itemActivated(QListWidgetItem *)),
                this, SLOT(slotDirShow_1(QListWidgetItem*)));

    QString rootStr ="/mnt/volume/download/";// "/mnt/volume/download/";
    QDir rootDir(rootStr);
    QStringList stringlist;
    stringlist << "*";
    list = rootDir.entryInfoList(stringlist);
    showFileInfoList(list);

}

omxplayer::~omxplayer()
{
    delete ui;
}

void omxplayer::keyPressEvent(QKeyEvent * event)
{
    switch (event->key()) {
    case Qt::Key_P:
        on_actionPause_triggered();
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
        break;
    default:
        break;
    }
}

void omxplayer::on_actionOpen_triggered()
{
    QStringList args;
    QString prog = OMXPLAYER;
    if (Videofile == "ff")
    {
        ui->statusBar->showMessage("no right file choose");
    }else{
        on_actionStop_triggered();
        args << Videofile;
        player->start(prog, args);
        ui->statusBar->showMessage(Videofile);
    }

}


void omxplayer::on_actionPause_triggered()
{

    player->write(pause);
    ui->statusBar->showMessage("Paused/Go");
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


void omxplayer::slotShow(QDir dir)
{
     QStringList stringList;
     stringList << "*";
     QFileInfoList InfoList = dir.entryInfoList(stringList, QDir :: AllEntries, QDir :: DirsFirst);
     showFileInfoList(InfoList);
}


void omxplayer::showFileInfoList(QFileInfoList list)
{

    fileListWidget->clear();

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


void omxplayer::slotDirShow(QListWidgetItem *Item)
{

    QString string = Item->text();
    QDir dir;

    dir.setPath(fileLineEdit->text());

    if (dir.cd(string))
    {

        fileLineEdit->setText(dir.absolutePath());

        slotShow(dir);
        Videofile = "ff";
        ui->statusBar->showMessage(dir.absolutePath());
    }
    else
    {
        Videofile = dir.absolutePath().append('/');
        Videofile.append(string);
        ui->statusBar->showMessage(Videofile);
        on_actionOpen_triggered();
    }

}

void omxplayer::slotDirShow_1(QListWidgetItem *Item)
{

    QString string = Item->text();
    QDir dir;

    dir.setPath(fileLineEdit->text());

    if (dir.cd(string))
    {

        fileLineEdit->setText(dir.absolutePath());

        slotShow(dir);
        Videofile = "ff";
        ui->statusBar->showMessage(dir.absolutePath());
    }
    else
    {
        Videofile = dir.absolutePath().append('/');
        Videofile.append(string);
        ui->statusBar->showMessage(Videofile);
        on_actionOpen_triggered();
    }

}

void omxplayer::slotChoose(QListWidgetItem *Item)
{

    QString string = Item->text();
    QDir dir;

    dir.setPath(fileLineEdit->text());

    if (dir.cd(string))
    {
        Videofile = "ff";
         ui->statusBar->showMessage(dir.absolutePath());
    }
    else
    {
        Videofile = dir.absolutePath().append('/');
        Videofile.append(string);
        ui->statusBar->showMessage(Videofile);
    }

}

void omxplayer::slotChoose_1(QListWidgetItem *current,QListWidgetItem *previous)
{

    if (current == NULL)
    {
        return;
    }
    QString string = current->text();
    QDir dir;

    dir.setPath(fileLineEdit->text());

    if (dir.cd(string))
    {
        Videofile = "ff";
         ui->statusBar->showMessage(dir.absolutePath());
    }
    else
    {
        Videofile = dir.absolutePath().append('/');
        Videofile.append(string);
        ui->statusBar->showMessage(Videofile);
    }

}
