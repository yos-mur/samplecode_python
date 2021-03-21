# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 19:37:30 2020

指定のシリアルポートから1が来た時にマウスクリックする
"""

import serial
import pyautogui
import os
import sys

def main():
    dold = 0
    tcount = 0

# 外部ファイルの存在確認
    if not (os.path.exists('ttlconfig.txt')):
        print('ttlconfig.txtを用意してください。終了します。')
        sys.exit()
        
# comポートとマウスボタンの選択 を外部ファイルから読み込む        
    with open('ttlconfig.txt',encoding ='utf-8') as f:
        l = f.readlines()
        serial_port = l[0].strip()
        serial_brate = l[1].strip()
        serial_tout = l[2].strip()
        mfunc = l[3].strip()
        mfunc_x = l[4].strip()
        mfunc_y = l[5].strip()
        mfunc_xinc = l[6].strip()
        mfunc_yinc = l[7].strip()
        
    print('シリアルポート',serial_port,'からの入力に応じてマウスクリックします。終了はCtrl+c')
    
# COMポートオープン、トリガ検出開始
    with serial.Serial(str(serial_port),int(serial_brate),timeout=float(serial_tout))as ser:
        while True:
            c = ser.readline()
            d = c.strip().decode('utf-8')
            
            if(d != dold) and (d == '1'):
                print('トリガ入力検出',d,tcount+1)

                if(mfunc == '1'):
                    pyautogui.click()
                elif(mfunc == '2'):
                    pyautogui.rightClick()
                
                elif(mfunc == 'X'):
                # XD用
                    if(tcount == 0):
                        pyautogui.click(int(mfunc_x),int(mfunc_y))
                        # pyautogui.moveTo(int(mfunc_x),int(mfunc_y))
                        # print(int(mfunc_x),int(mfunc_y))
                    else:
                        pyautogui.click(int(mfunc_x) + int(mfunc_xinc),int(mfunc_y) + int(mfunc_yinc))
                        # pyautogui.moveTo(int(mfunc_x) + int(mfunc_xinc),int(mfunc_y) + int(mfunc_yinc))
                        # print(int(mfunc_x) + int(mfunc_xinc),int(mfunc_y) + int(mfunc_yinc))
                tcount += 1
                
            dold = d
           
    ser.close() 

try:
    main()
        
except KeyboardInterrupt:
        # 終了用コマンド
        print('終了します')

            



