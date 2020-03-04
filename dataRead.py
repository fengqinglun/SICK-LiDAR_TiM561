#coding=utf-8
from socket import *
import time



class dataRead:
    def __init__(self,port=2111):
        self.radar_data = []
        self.BUFSIZE = 40000
        self.ADDR = ('192.168.66.101', port)

    def startclient(self):
        while True:
            if 1:
                return self.client()
            else:
                print("data Reading exception")

    def client(self):
        self.tcpclisocket = socket(AF_INET, SOCK_STREAM)
        self.tcpclisocket.connect(self.ADDR)
        self.tcpclisocket.send(b'\x02sRN LMDscandata\x03\0')
        pcddata = ""
        while True:
            pcddata += self.tcpclisocket.recv(self.BUFSIZE).decode()
            #print("pcddata is ",len(pcddata))
            enddata = pcddata[-1]
            if enddata.encode(encoding="utf-8") == b"\x03":
                break

        
        # print(pcddata)
        self.caldata(pcddata)
        self.tcpclisocket.close()
        return self.radar_data

    def caldata(self, data):
        data = data.split(' ')
        #print(data)
        if len(data) == 0:
            return
        #print("data length: ", len(data))
        if len(data) > 20:
            if data[21] == '3F800000':
                pass
                #print('find 3F800000')
            #'''起始角度'''
            startangle = int(data[23], 16) / 10000
            #print("angle start: ", startangle)
            #'''角度分辨率'''
            anglestep = int(data[24], 16) / 10000
            #print("angle fps:  ", anglestep)
            #'''数据总量'''
            datanum = int(data[25], 16)
            #print("data numbers:  ", datanum)

            tmp_scandatas = []
            scandatas = []
            for i in range(datanum):
                tmp_data = int(data[26 + i], 16)
                tmp_scandatas.append(tmp_data)
            #print(scandatas[135:-135])
            for d in tmp_scandatas:
                if int(d) <= 10:
                    d = int(50000)
                scandatas.append(d)

            #print(scandatas)
            self.radar_data = scandatas


if __name__ == '__main__':
    dr = dataRead()
    #读取一次传感器数据
    while True:
        datas = dr.startclient()
        print(datas)
        time.sleep(0.1)
    #打印传感器数据
    #file1 = open("/home/pi/readdatas.txt")
    #print (dr.radar_data)
    #file1.write(str(dr.radar_data))
    #file1.close()

