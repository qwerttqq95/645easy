from UI import MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog,QMessageBox
from PyQt5.QtCore import Qt
import sys, re, Comm, serial, serial.tools.list_ports, threading,time,binascii
from binascii import b2a_hex, a2b_hex
from traceback import print_exc


class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.addItem = self.GetSerialNumber()
        self.addItem.sort()
        for addItem in self.addItem:
            self.ui.comboBox_3.addItem(addItem)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.Connect = Connect()
        self.ui.pushButton.clicked.connect(self.serial_prepare)
        self.ui.pushButton_2.clicked.connect(self.Connect.GetAddress)

    def serial_prepare(self):
        try:
            self.Connect.setDaemon(True)
            self.Connect.start()
            self.ui.pushButton.disconnect()
            self.ui.pushButton.clicked.connect(self.Connect.switch)

        except:
            print_exc(file=open('bug.txt', 'a+'))

    def GetSerialNumber(self):
        SerialNumber = []
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) <= 0:
            print("The Serial port can't find!")
        else:
            for i in list(port_list):
                SerialNumber.append(i[0])
            return SerialNumber

    def Show_Hidden(self, num):
        if num == '0':
            self.ui.comboBox.setDisabled(0)
            self.ui.comboBox_5.setDisabled(0)
            self.ui.comboBox_3.setDisabled(0)
            self.ui.comboBox_4.setDisabled(0)
        else:
            self.ui.comboBox.setDisabled(1)
            self.ui.comboBox_5.setDisabled(1)
            self.ui.comboBox_3.setDisabled(1)
            self.ui.comboBox_4.setDisabled(1)

    def show_list(self):
        posit = self.ui.tableWidget.currentRow()
        print(posit)
        self.ui.tableWidget.insertRow(posit)

    def Warming_message(self):
        QMessageBox.warning(self, 'ERROR', '串口未打开或被占用')

class Connect(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.serial = serial.Serial()
        self.__runflag = threading.Event()

    def run(self):
        self.switch()
        self.serial.port = MainWindow.ui.comboBox_3.currentText()
        self.serial.baudrate = int(MainWindow.ui.comboBox_4.currentText())
        self.serial.parity = MainWindow.ui.comboBox_5.currentText()
        self.serial.stopbits = int(MainWindow.ui.comboBox.currentText())
        self.serial.timeout = 1
        while 1:
            if self.__runflag.isSet():
                self.serial_open()
            else:
                self.serial.close()

    def switch(self):
        if self.__runflag.isSet():
            MainWindow.ui.pushButton.setText('打开')
            print('已关闭')
            MainWindow.Show_Hidden('0')
            self.__runflag.clear()
        else:
            MainWindow.ui.pushButton.setText('关闭')
            print('已启动')
            MainWindow.Show_Hidden('1')
            self.__runflag.set()

    def serial_open(self):
        if self.serial.isOpen():
            pass
        else:
            try:
                self.serial.open()
            except:
                MainWindow.ui.pushButton.setText('打开')
                MainWindow.Show_Hidden('0')
                self.__runflag.clear()
                MainWindow.Warming_message()

    def GetAddress(self):
        if self.serial.isOpen():
            message = 'FE 68 AA AA AA AA AA AA 68 13 00 DF 16'
            message = message.replace(' ', '')
            print('Sending:', message)
            self.serial.write(bytes.fromhex(message))
            time.sleep(2)
            num = self.serial.inWaiting()
            data = str(b2a_hex(self.serial.read(num)))[2:-1]
            print('Receive:', data)
            data = Comm.makelist(data)
            while 1:
                if data[0] == 'fe':
                    data = data[1:]
                else:
                    break
            print(data[8])
            if data[8] == '93':
                add = data[10:16]
                add = Comm.list2str(minus33(add))
                print(add)
                MainWindow.ui.lineEdit.setText(add)
            else:
                print('error')

        else:
            MainWindow.Warming_message()



def CS(list_):
    sum = 0
    while list_:
        sum = sum + ord(list_.pop())
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
