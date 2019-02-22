from UI import MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys, re, Comm


class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)


def CS(list):
    sum = 0
    while list:
        sum = sum + ord(list.pop())
    sum = hex(sum & 0xff)[2:]
    if len(sum) == 1:
        sum = "0" + sum
    return sum


def strto0x(context):  # list
    context = [int(x, 16) for x in context]
    new_context = []
    while context:
        current_context = chr(context.pop())
        new_context.append(current_context)
    new_context.reverse()
    return new_context


def plus33(message):
    newstr = ''
    if message is None:
        print('plus33 is none')
    else:
        if re.findall(',', message):
            message = message.split(',')
            lenth = len(message)
            i = 0
            while lenth:
                new_list = []
                lenth -= 1
                returnvalue = Comm.makelist(message[i])
                i += 1
                while returnvalue:
                    new_list.append(hex(int(returnvalue.pop(), 16) + 51)[2:])
                value_str = Comm.list2str(new_list)
                newstr = newstr + value_str
                return newstr
        else:
            message = Comm.makelist(message)
            lenth = len(message)
            new_list = []
            while lenth:
                lenth -= 1
                new_list.append(hex(int(message.pop(), 16) + 51)[2:])
            newstr = Comm.list2str(new_list)
            return newstr


def minus33(list_):
    new_list = []
    while list_:
        middle = hex(int(list_.pop(), 16) - 51)[2:]
        if len(middle) == 1:
            middle = '0' + middle
        if middle == 'x1':
            middle = 'FF'
        new_list.append(middle)
    return new_list


def returnframe(add, reconctrlcode, L, D, N):
    text = '68' + add + '68' + reconctrlcode + L + D + N
    cs = CS(strto0x(Comm.makelist(text)))
    text = text + cs + '16'
    return text


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = Main()
    MainWindow.show()
    sys.exit(app.exec_())
