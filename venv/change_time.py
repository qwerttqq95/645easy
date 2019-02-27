import serial, time, Comm, re
from binascii import b2a_hex, a2b_hex


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

qw = input('COM ')
port = 'COM'+qw
t = serial.Serial(port=port, baudrate=2400, parity='E', stopbits=1)
add_09 = '076450090001'
add_13 = '076450130001'
x = 0
list_ = []
date_ = Comm.list2str(Comm.makelist(time.strftime('%y%m%d0%w')))
# time_ = Comm.list2str(Comm.makelist(time.strftime('%H%M%S')))
while x < 50:
    add_ = str(int(add_09) + x).zfill(12)
    x += 1
    A0_A5 = Comm.list2str(Comm.makelist(add_)[-1::-1])
    list_.append(A0_A5)
x = 0
while x < 7:
    add_ = str(int(add_13) + x).zfill(12)
    x += 1
    A0_A5 = Comm.list2str(Comm.makelist(add_)[-1::-1])
    list_.append(A0_A5)
for a in list_:
    DI3_0_date = '34343337'
    DI3_0_time = '35343337'
    data = '3533333333333333'
    message_date = '68' + a + '68' + '14' + '10' + DI3_0_date + data + plus33(date_)
    CS_ = CS(strto0x(Comm.makelist(message_date.replace(' ', ''))))

    message_date_full = message_date + CS_ + '16'
    time_ = Comm.list2str(Comm.makelist(time.strftime('%H%M%S')))
    message_time = '68' + a + '68' + '14' + '0f' + DI3_0_time + data + plus33(time_)
    CS_ = CS(strto0x(Comm.makelist(message_time.replace(' ', ''))))

    message_time_full = message_time + CS_ + '16'

    print('sending: message_date', Comm.makestr(message_date_full))
    t.write(a2b_hex(message_date_full))
    time.sleep(2.5)
    num = t.inWaiting()
    receive = str(b2a_hex(t.read(num)))[2:-1]
    print('receive:', Comm.makestr(receive))
    print('sending: message_time', Comm.makestr(message_time_full))
    t.write(a2b_hex(message_time_full))
    time.sleep(2.5)
    num = t.inWaiting()
    receive = str(b2a_hex(t.read(num)))[2:-1]
    print('receive:', Comm.makestr(receive))

input('Press anything to exit')



