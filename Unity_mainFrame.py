import Ui_mainFrame
import SerialPort
import threading
from time import sleep
from PyQt5 import QtCore, QtGui, QtWidgets



class MyError(QtWidgets.QWidget):
    def __init__(self, e):
        super(MyError, self).__init__()
        self.move(650,270)
        err =  QtWidgets.QMessageBox.critical(self,
                                 "错误",
                                 str(e),
                                 QtWidgets.QMessageBox.Yes)


class MyNotice(QtWidgets.QWidget):
    def __init__(self, inf):
        super(MyNotice, self).__init__()
        self.move(600, 270)
        notice =  QtWidgets.QMessageBox.information(self,
                                 "提示",
                                 str(inf),
                                 QtWidgets.QMessageBox.Yes)


class UnitySerialTest(Ui_mainFrame.Ui_SerialTest):

    def __init__(self, MainWindow):
        self.setupUi(MainWindow)
        self.serialPort = SerialPort.serialPort()
        self.getSerialPort()
        self.set_event()
        self.startListen()

        self.strdata = ''
        self.bytdata = b''

    # 获取可用串口号
    def getSerialPort(self):            # 获取所有串口号并添加到复选框中
        ItemData = []                   # comboBox已有串口
        Ports = []
        Ports = self.serialPort.detectPort()    # 获取现有可用端口
        if Ports is None:
            return

        for i in range(self.comboBox.count()):
            ItemData.append(self.comboBox.itemText(i))

        for port in Ports:
            if port in ItemData:
                continue
            self.comboBox.addItem(port)

    # 打开串口
    def openPort(self):                                 #　初始化串口serial
        if self.serialPort.ser is not None:             # 已有serial实例，调用Open方法打开
            if self.serialPort.ser.isOpen():
                return
            self.serialPort.ser.open()
            MyNotice("串口已打开")
            return
        try:
            port = self.comboBox.currentText()          # 获取串口号
        except:
            return
        baudrate = self.comboBox_2.currentText()        # 获取波特率
        bytesize = int(self.comboBox_3.currentText())   # 获取数据位
        try:
            self.serialPort.set(port=port, baudrate=baudrate,bytesize=bytesize) # 调用成员的子函数
            self.statuslabel.setText("串口已打开")
            MyNotice("串口已打开")

        except Exception as e:
            MyError(e)                                  # 错误提示框

    # 关闭串口
    def closePort(self):
        if self.serialPort.ser is None or not self.serialPort.ser.isOpen():
            MyError("串口未打开")
            return
        try:
            self.serialPort.ser.close()
            self.statuslabel.setText("串口已关闭")
            MyNotice("串口已关闭")
        except Exception as e:
            MyError(e)

    # 发送消息
    def sendMes(self):

        def makeFrame(data):            # 组帧
            length = bytes(((len(data)),))
            data = b'a' + length + data + b'z'  #帧首+长度+数据+帧尾
            datalist = []
            # print("组帧后的十六进制数据：")
            # for byt in data:
            #     print(hex(byt), end=' ')
            # print()
            return data

        def sendMesByHex(self):         #　十六进制内容发送　格式前缀0x可省略 以，或空格分开

            text = self.lineEdit.text()
            text = text.strip('0x')
            bytestext = b''
            if ',' in text:
                text = text.split(',')
            else:
                text = text.split(' ')
            try:
                for num in text:
                    bytestext += bytes((int(num, 16),))     # str ==> hex ==>bytes
            except:
                MyError("Hex格式不正确-前缀0x可省略，以，或空格分开")
                return
            # print(bytestext)
            self.serialPort.ser.write(bytestext)
            self.statuslabel.setText("消息发送成功")
            pass
        def sedMesbyStr(self):
            text = self.lineEdit.text()
            self.serialPort.ser.write(text.encode('gbk'))
            self.statuslabel.setText("消息发送成功")
            pass

        if self.serialPort.ser is None or not self.serialPort.ser.isOpen():
            MyNotice("请先打开串口！")
            return
        if  not self.checkBox.isChecked():
            sedMesbyStr(self)
        else:
            sendMesByHex(self)


        pass
    # 监听串口信息
    def startListen(self):
        def listen(self):
            while True:
                try:
                    while self.serialPort.ser.inWaiting()>0:
                        sleep(0.1)
                        # 读取缓冲区内容
                        if len(self.strdata) > 500:        # 设置长度阈值
                            self.clean()
                        data = self.serialPort.ser.read(self.serialPort.ser.inWaiting())
                        self.bytdata += data
                        mes = data.decode('gbk')        # 解码
                        self.strdata += mes

                       	self.extraTask()
                       	
                        if  not self.checkBox_2.isChecked():
                            self.textArea.insertPlainText(mes)              # 插入文本显示区域
                        else:
                            hexdata = []
                            for byt in data:
                                hexdata.append(hex(byt))
                            self.textArea.insertPlainText((('  '.join(hexdata)).replace('0x', ''))+'  ')
                        # self.textArea.insertPlainText(mes)       # 追加显示(用append方法会另起一行)
                        self.textArea.moveCursor(QtGui.QTextCursor.End)
                        print(mes, end='')
                        sleep(0.01)
                except:
                    sleep(1)
        thread = threading.Thread(target=listen,args=[self])
        thread.deamon = False
        thread.start()

    # 自定义额外功能
    def extraTask(self):
    	pass
    # 清空信息框
    def clean(self):
        self.bytdata = b''
        self.strdata = ''
        self.textArea.setText('')

    # Hex或字节显示接收信息
    def mesShow(self):
        def hexShow(bytdata):               # 以十六进制显示
            hexdata = []
            for byt in bytdata:
                hexdata.append(hex(byt))
            self.textArea.setText((('  '.join(hexdata)).replace('0x','') + '  '))

        def strShow(strdata):               # Bytes解码后显示
            self.textArea.setText(strdata)

        self.textArea.setText('')           # 切换显示方式前将其置空

        if self.checkBox_2.isChecked():
            hexShow(self.bytdata)
        else:
            strShow(self.strdata)
        self.textArea.moveCursor(QtGui.QTextCursor.End) # 使其自动下滚

    def set_event(self):                # 设置事件关联
        self.scanButton.clicked.connect(self.getSerialPort) # 重新扫描串口
        self.openButton.clicked.connect(self.openPort)      # 打开串口按钮
        self.closeButton.clicked.connect(self.closePort)    # 关闭串口按钮
        self.cleanButton.clicked.connect(self.clean)        # 清除窗口
        self.checkBox_2.stateChanged.connect(self.mesShow)  # Hex str 显示
        self.sendButton.clicked.connect(self.sendMes)

# import sys
# app = QtWidgets.QApplication(sys.argv)
# SerialTest = QtWidgets.QMainWindow()
# ui = UnitySerialTest(SerialTest)
# SerialTest.show()
# sys.exit(app.exec_())
