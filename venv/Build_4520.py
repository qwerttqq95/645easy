from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, pyqtSignal
import sys
from UI import UI_build4520
import binascii


class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = UI_build4520.Ui_MainWindow()
        self.ui.setupUi(self)
        self.text = '060100452002000106'
        self.ui.pushButton.clicked.connect(self.compose)

    def compose(self):
        self.text = self.text + self.build_mob() + self.build_Telecom() + self.build_unicom() + '00'
        self.ui.textEdit.setText(self.text)
        self.text = '060100452002000106'

    def build_mob(self):
        self.mob_ip_1 = self.ui.lineEdit.displayText().split('.')  # 主用IP
        qq1 = ''
        for q in self.mob_ip_1:
            qq1 = qq1 + hex(int(q, 10))[2:].zfill(2)

        self.mob_serial_1 = hex(int(self.ui.lineEdit_3.displayText()))[2:].zfill(4)  # 主用端口

        self.mob_ip_2 = self.ui.lineEdit_2.displayText().split('.')  # 备用IP
        qq2 = ''
        for q in self.mob_ip_2:
            qq2 = qq2 + hex(int(q, 10))[2:].zfill(2)

        self.mob_serial_2 = hex(int(self.ui.lineEdit_4.displayText()))[2:]  # 备用端口
        self.mob_3G_APN = self.str_to_hex(self.ui.lineEdit_5.displayText())
        self.mob_3G_APN_len = hex(int(str(len(self.mob_3G_APN) // 2)))[2:]
        self.mob_4G_APN = self.str_to_hex(self.ui.lineEdit_6.displayText())
        self.mob_4G_APN_len = hex(int(str(len(self.mob_4G_APN) // 2)))[2:]

        self.mob_name = self.ui.lineEdit_7.displayText()
        if self.mob_name == '':
            self.mob_name_len = '00'
        else:
            self.mob_name_len = hex(int(str(len(self.str_to_hex(self.mob_name)) // 2)))[2:].zfill(2)
            self.mob_name = self.str_to_hex(self.mob_name)

        self.mob_pass = self.ui.lineEdit_8.displayText()
        if self.mob_pass == '':
            self.mob_pass_len = '00'
        else:
            self.mob_pass_len = hex(int(str(len(self.str_to_hex(self.mob_pass)) // 2)))[2:].zfill(2)
            self.mob_pass = self.str_to_hex(self.mob_pass)

        self.mob_proxy_add = self.ui.lineEdit_9.displayText().split('.')
        qq = ''
        for q in self.mob_proxy_add:
            qq = qq + hex(int(q, 10))[2:].zfill(2)

        self.mob_proxy_serial = hex(int(self.ui.lineEdit_10.displayText()))[2:].zfill(4)

        self.mon_text = ['020816001601', '020816001602']
        times = 0
        for x in self.mon_text:
            if times == 0:
                print('x',x,'\nself.mob_3G_APN_len.zfill(2)',self.mob_3G_APN_len.zfill(2),'\nself.mob_3G_APN',self.mob_3G_APN)
                mob1 = x + '0a' + self.mob_3G_APN_len.zfill(
                    2) + self.mob_3G_APN + '0a' + self.mob_name_len + self.mob_name + '0a' + self.mob_pass_len + self.mob_pass + '0904' + qq + '12' + self.mob_proxy_serial+ '0102' + '02020904' + qq1 + '12' + self.mob_serial_1 + '02020904' +  qq2 + '12' + self.mob_serial_2
                times += 1
            if times == 1:
                mob2 = x + '0a' + self.mob_4G_APN_len.zfill(2) + self.mob_4G_APN + '0a' + self.mob_name_len + self.mob_name + '0a' + self.mob_pass_len + self.mob_pass + '0904' + qq + '12' +self.mob_proxy_serial+ '0102' + '02020904' + qq1 + '12' + self.mob_serial_1 + '02020904' +  qq2 + '12' + self.mob_serial_2
        print('mob1', mob1)
        print('mob2', mob2)
        return mob1 + mob2

    def build_unicom(self):
        self.unicom_ip_1 = self.ui.lineEdit_27.displayText().split('.')  # 主用IP
        qq1 = ''
        for q in self.unicom_ip_1:
            qq1 = qq1 + hex(int(q, 10))[2:].zfill(2)

        self.unicom_serial_1 = hex(int(self.ui.lineEdit_29.displayText()))[2:].zfill(4)   # 主用端口

        self.unicom_ip_2 = self.ui.lineEdit_23.displayText().split('.')  # 备用IP
        qq2 = ''
        for q in self.unicom_ip_2:
            qq2 = qq2 + hex(int(q, 10))[2:].zfill(2)

        self.unicom_serial_2 = hex(int(self.ui.lineEdit_24.displayText()))[2:].zfill(4)  # 备用端口

        self.unicom_3G_APN = self.str_to_hex(self.ui.lineEdit_28.displayText())
        self.unicom_4G_APN = self.str_to_hex(self.ui.lineEdit_22.displayText())
        self.unicom_3G_APN_len = hex(int(str(len(self.unicom_3G_APN) // 2)))[2:]
        self.unicom_4G_APN_len = hex(int(str(len(self.unicom_4G_APN) // 2)))[2:]

        self.unicom_name = self.ui.lineEdit_26.displayText()
        if self.unicom_name == '':
            self.unicom_name_len = '00'
        else:
            self.unicom_name_len = hex(int(str(len(self.str_to_hex(self.unicom_name)) // 2)))[2:].zfill(2)
            self.unicom_name = self.str_to_hex(self.unicom_name)

        self.unicom_pass = self.ui.lineEdit_30.displayText()
        if self.unicom_pass == '':
            self.unicom_pass_len = '00'
        else:
            self.unicom_pass_len = hex(int(str(len(self.str_to_hex(self.unicom_pass)) // 2)))[2:].zfill(2)
            self.unicom_pass = self.str_to_hex(self.unicom_pass)

        self.unicom_proxy_add = self.ui.lineEdit_25.displayText().split('.')
        qq = ''
        for q in self.unicom_proxy_add:
            qq = qq + hex(int(q, 10))[2:].zfill(2)

        self.unicom_proxy_serial = hex(int(self.ui.lineEdit_21.displayText()))[2:].zfill(4)

        self.unicom_text = ['020816021601', '020816021602']
        times = 0
        for x in self.unicom_text:
            if times == 0:
                print('x', x, '\nself.unicom_3G_APN_len.zfill(2)', self.unicom_3G_APN_len.zfill(2), '\nself.unicom_3G_APN',
                      self.unicom_3G_APN)
                unicom1 = x + '0a' + self.unicom_3G_APN_len.zfill(
                    2) + self.unicom_3G_APN + '0a' + self.unicom_name_len + self.unicom_name + '0a' + self.unicom_pass_len + self.unicom_pass + '0904' + qq + '12' + self.unicom_proxy_serial+ '0102' + '02020904' + qq1 + '12' + self.unicom_serial_1 + '02020904' + qq2 + '12' + self.unicom_serial_2
                times += 1
            if times == 1:
                unicom2 = x + '0a' + self.unicom_4G_APN_len.zfill(
                    2) + self.unicom_4G_APN + '0a' + self.unicom_name_len + self.unicom_name + '0a' + self.unicom_pass_len + self.unicom_pass + '0904' + qq + '12' + self.unicom_proxy_serial+ '0102' + '02020904' + qq1 + '12' + self.unicom_serial_1 + '02020904' + qq2 + '12' + self.unicom_serial_2
        print('unicom1', unicom1)
        print('unicom2', unicom2)
        return unicom1 + unicom2

    def build_Telecom(self):
        self.Telecom_ip_1 = self.ui.lineEdit_19.displayText().split('.')  # 主用IP
        qq1 = ''
        for q in self.Telecom_ip_1:
            qq1 = qq1 + hex(int(q, 10))[2:].zfill(2)

        self.Telecom_serial_1 = hex(int(self.ui.lineEdit_12.displayText()))[2:].zfill(4)  # 主用端口

        self.Telecom_ip_2 = self.ui.lineEdit_18.displayText().split('.')  # 备用IP
        qq2 = ''
        for q in self.Telecom_ip_2:
            qq2 = qq2 + hex(int(q, 10))[2:].zfill(2)

        self.Telecom_serial_2 = hex(int(self.ui.lineEdit_14.displayText()))[2:].zfill(4)  # 备用端口

        self.Telecom_3G_APN = self.str_to_hex(self.ui.lineEdit_13.displayText())
        self.Telecom_4G_APN = self.str_to_hex(self.ui.lineEdit_17.displayText())
        self.Telecom_3G_APN_len = hex(int(str(len(self.Telecom_3G_APN) // 2)))[2:]
        self.Telecom_4G_APN_len = hex(int(str(len(self.Telecom_4G_APN) // 2)))[2:]

        self.Telecom_name = self.ui.lineEdit_15.displayText()
        if self.Telecom_name == '':
            self.Telecom_name_len = '00'
        else:
            self.Telecom_name_len = hex(int(str(len(self.str_to_hex(self.Telecom_name)) // 2)))[2:]
            self.Telecom_name = self.str_to_hex(self.Telecom_name)


        self.Telecom_pass = self.ui.lineEdit_16.displayText()
        if self.Telecom_pass == '':
            self.Telecom_pass_len = '00'
        else:
            self.Telecom_pass_len = hex(int(str(len(self.str_to_hex(self.Telecom_pass)) // 2)))[2:].zfill(2)
            self.Telecom_pass = self.str_to_hex(self.Telecom_pass)

        self.Telecom_proxy_add = self.ui.lineEdit_11.displayText().split('.')
        qq = ''
        for q in self.Telecom_proxy_add:
            qq = qq + hex(int(q, 10))[2:].zfill(2)

        self.Telecom_proxy_serial = hex(int(self.ui.lineEdit_20.displayText()))[2:].zfill(4)

        self.Telecom_text = ['020816011601', '020816011602']
        times = 0
        for x in self.Telecom_text:
            if times == 0:
                print('x', x, '\nself.Telecom_3G_APN_len.zfill(2)', self.Telecom_3G_APN_len.zfill(2),
                      '\nself.unicom_3G_APN',
                      self.Telecom_3G_APN)
                Telecom1 = x + '0a' + self.Telecom_3G_APN_len.zfill(
                    2) + self.Telecom_3G_APN + '0a' + self.Telecom_name_len + self.Telecom_name + '0a' + self.Telecom_pass_len + self.Telecom_pass + '0904' + qq + '12' +self.Telecom_proxy_serial+ '0102' + '02020904' + qq1 + '12' + self.Telecom_serial_1 + '02020904' + qq2 + '12' + self.Telecom_serial_2
                times += 1
            if times == 1:
                Telecom2 = x + '0a' + self.Telecom_4G_APN_len.zfill(
                    2) + self.Telecom_4G_APN + '0a' + self.Telecom_name_len + self.Telecom_name + '0a' + self.Telecom_pass_len + self.Telecom_pass + '0904' + qq + '12'+self.Telecom_proxy_serial + '0102' + '02020904' + qq1 + '12' + self.Telecom_serial_1 + '02020904' + qq2 + '12' + self.Telecom_serial_2
        print('Telecom1', Telecom1)
        print('Telecom2', Telecom2)
        return Telecom1 + Telecom2

    def show_text(self, text):
        self.ui.textEdit.setPlainText(text)

    def str_to_hex(self, s):
        return ''.join([hex(ord(c)).replace('0x', '') for c in s])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = Main()
    MainWindow.show()
    sys.exit(app.exec_())
