#include "omxplayer.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    omxplayer w;
    w.show();


    return a.exec();
}
