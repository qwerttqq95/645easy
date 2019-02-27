'''
将645表转场内模式，并设地址和校时
'''

import Comm, sys, serial, serial.tools.list_ports, time,re
from UI import UI_change_mode
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, pyqtSignal
from binascii import b2a_hex, a2b_hex


class Main(QMainWindow):
    _signal_text = pyqtSignal(str)

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = UI_change_mode.Ui_MainWindow()
        self.ui.setupUi(self)
        self.addItem = self.GetSerialNumber()
        self.addItem.sort()
        for addItem in self.addItem:
            self.ui.comboBox.addItem(addItem)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.ui.pushButton.clicked.connect(self.plus)
        self.ui.pushButton_2.clicked.connect(self.dec)
        self.ui.pushButton_3.clicked.connect(self.start)
        self._signal_text.connect(self.show_message)
        self.serial = serial.Serial()

    def start(self):
        self.serial.port = self.ui.comboBox.currentText()
        self.serial.baudrate = 2400
        self.serial.parity = 'E'
        self.serial.stopbits = 1
        self.serial.timeout = 1
        if self.serial.isOpen():
            pass
        else:
            self.serial.open()

        getadd = 'FE FE FE FE 68 AA AA AA AA AA AA 68 13 00 DF 16'
        print('sending: ', getadd)
        self._signal_text.emit('发送：')
        self._signal_text.emit(getadd)
        self.serial.write(a2b_hex(getadd.replace(' ', '')))
        time.sleep(2.5)
        num = self.serial.inWaiting()
        receive = str(b2a_hex(self.serial.read(num)))[2:-1]
        print('receive:', Comm.makestr(receive))
        self._signal_text.emit('收到：')
        self._signal_text.emit(Comm.makestr(receive))
        receive = Comm.makelist(receive)
        while 1:
            if receive[0] == 'fe':
                receive = receive[1:]
            else:
                break
        add = receive[1:7]
        self._signal_text.emit('地址为：')
        self._signal_text.emit(Comm.list2str(add[-1::-1]))
        chang_mode = '68 1F 03 42 88 32'
        mesaage = '68' + Comm.list2str(add) + chang_mode.replace(' ', '')
        cs = self.CS(self.strto0x(Comm.makelist(mesaage.replace(' ', ''))))
        mesaage = mesaage +cs+ '16'

        print('sending: ', mesaage)
        self._signal_text.emit('发送：')
        self._signal_text.emit(Comm.makestr(mesaage))
        self.serial.write(a2b_hex(mesaage.replace(' ', '')))
        time.sleep(2.5)
        num = self.serial.inWaiting()
        receive = str(b2a_hex(self.serial.read(num)))[2:-1]
        print('receive:', Comm.makestr(receive))
        self._signal_text.emit('收到：')
        self._signal_text.emit(Comm.makestr(receive))
        receive = Comm.makelist(receive)
        if receive[-3] == '00' and receive[-4] == '9f':
            self._signal_text.emit('成功转厂内模式')
            print('成功转厂内模式')
        else:
            self._signal_text.emit('转厂内模式结果未知')
            print('转厂内模式结果未知')

        new_add = self.plus33(self.ui.lineEdit.displayText())
        chang_add = '68' + Comm.list2str(add) + '681412343733373533333363636363' + new_add
        cs = self.CS(self.strto0x(Comm.makelist(chang_add.replace(' ', ''))))
        chang_add = chang_add + cs + '16'
        print('sending: ', chang_add)
        self._signal_text.emit('发送：')
        self._signal_text.emit(Comm.makestr(chang_add))
        self.serial.write(a2b_hex(chang_add.replace(' ', '')))
        time.sleep(2.5)
        num = self.serial.inWaiting()
        receive = str(b2a_hex(self.serial.read(num)))[2:-1]
        print('receive:', Comm.makestr(receive))
        self._signal_text.emit('收到：')
        self._signal_text.emit(Comm.makestr(receive))
        receive = Comm.makelist(receive)
        if receive[-3] == '00' and receive[-4] == '94':
            self._signal_text.emit('成功转地址')
            print('成功转地址')
        else:
            self._signal_text.emit('转地址结果未知')
            print('转地址结果未知')

        date_ = Comm.list2str(Comm.makelist(time.strftime('%y%m%d0%w')))
        DI3_0_date = '34343337'
        DI3_0_time = '35343337'
        data = '3533333333333333'
        message_date = '68' + Comm.list2str(Comm.makelist(self.ui.lineEdit.displayText())[::-1]) + '68' + '14' + '10' + DI3_0_date + data + self.plus33(date_)
        CS_ = self.CS(self.strto0x(Comm.makelist(message_date.replace(' ', ''))))

        message_date_full = message_date + CS_ + '16'
        time_ = Comm.list2str(Comm.makelist(time.strftime('%H%M%S')))
        message_time = '68' + Comm.list2str(Comm.makelist(self.ui.lineEdit.displayText())[::-1]) + '68' + '14' + '0f' + DI3_0_time + data + self.plus33(time_)
        CS_ = self.CS(self.strto0x(Comm.makelist(message_time.replace(' ', ''))))

        message_time_full = message_time + CS_ + '16'

        print('sending: message_date', Comm.makestr(message_date_full))
        self.serial.write(a2b_hex(message_date_full))
        time.sleep(2.5)
        num = self.serial.inWaiting()
        receive = str(b2a_hex(self.serial.read(num)))[2:-1]
        print('receive:', Comm.makestr(receive))

        receive = Comm.makelist(receive)
        if receive[-3] == '00' and receive[-4] == '94':
            self._signal_text.emit('成功改日期')
            print('成功改日期')
        else:
            self._signal_text.emit('改日期结果未知')
            print('改日期结果未知')
        print('sending: message_time', Comm.makestr(message_time_full))
        self.serial.write(a2b_hex(message_time_full))
        time.sleep(2.5)
        num = self.serial.inWaiting()
        receive = str(b2a_hex(self.serial.read(num)))[2:-1]
        print('receive:', Comm.makestr(receive))
        receive = Comm.makelist(receive)
        if receive[-3] == '00' and receive[-4] == '94':
            self._signal_text.emit('成功改时间')
            print('成功改时间')
        else:
            self._signal_text.emit('改时间结果未知')
            print('改时间结果未知')


    def plus(self):
        self.number = str(int(self.ui.lineEdit.displayText()) + 1).zfill(12)
        self.ui.lineEdit.setText(self.number)

    def dec(self):
        self.number = str(int(self.ui.lineEdit.displayText()) - 1).zfill(12)
        self.ui.lineEdit.setText(self.number)

    def GetSerialNumber(self):
        SerialNumber = []
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) <= 0:
            print("The Serial port can'serial find!")
        else:
            for i in list(port_list):
                SerialNumber.append(i[0])
            return SerialNumber

    def CS(self, list_):
        sum = 0
        while list_:
            sum = sum + ord(list_.pop())
        sum = hex(sum & 0xff)[2:]
        if len(sum) == 1:
            sum = "0" + sum
        return sum

    def strto0x(self, context):  # list
        context = [int(x, 16) for x in context]
        new_context = []
        while context:
            current_context = chr(context.pop())
            new_context.append(current_context)
        new_context.reverse()
        return new_context

    def plus33(self, message):
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

    def show_message(self, message):
        self.ui.textEdit.append(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = Main()
    MainWindow.show()
    sys.exit(app.exec_())
