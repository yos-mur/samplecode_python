# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 21:27:14 2021

@author: sukek
"""
import random

class Responder: # 基底クラス
    def response(self, point):
        return ''
    
class LuckyResponder(Responder):
    def response(self, point):
        return ['lucky: point', point]
    
class DrawResponder(Responder):
    def response(self, point):
        point = 0
        return ['draw: point = 0', point]
    
class BadResponder(Responder):
    def response(self, point):
        return ['bad: -point', -point]
    
    
class Controller:
    def __init__(self):
        self.lucky = LuckyResponder()
        self.draw = DrawResponder()
        self.bad = BadResponder()
        
    def attack(self, point):
        x = random.randint(0, 100)
        
        if x <= 30:
            self.responder = self.lucky
            
        elif 31 <= x <= 60:
            self.responder = self.draw
            
        else:
            self.responder = self.bad
        
        return self.responder.response(point)
            

if __name__ == '__main__':
    point = 3
    
    # 継承
    # responder = LuckyResponder()
    # res = responder.response(point)
    # print(res)
    
    # responder = DrawResponder()
    # res = responder.response(point)
    # print(res)
    
    # responder = BadResponder()
    # res = responder.response(point)
    # print(res)
    
    responder = []
    responder.append(LuckyResponder())    
    responder.append(DrawResponder())
    responder.append(BadResponder())
    
    for i in range(len(responder)):
        res = responder[i].response(point)
        print(res)

    
    # ctr = Controller()
    # # res = ctr.lucky.response(point)
    # res = ctr.attack(point)
    # print(res)
