#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from psychopy import visual, core, event, clock, monitors, gui
from psychopy.sound import Sound
import helpers as hp
import numpy as np
import pandas as pd


# GUI
myDlg = gui.Dlg(title=u"实验")
myDlg.addText(u'被试信息')
myDlg.addField('姓名:')
myDlg.addField('性别:', choices=['male', 'female'])
myDlg.addField('年龄:', 21)

myDlg.addField('屏幕分辨率:', choices=['1920*1080', '3200*1800', '1280*720', '2048*1152', '2560*1440'])
ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
if not myDlg.OK:
    core.quit()
name = ok_data[0]
sex = ok_data[1]
age = ok_data[2]
resolution = ok_data[3]

w, h = resolution.split('*')
w = int(w)
h = int(h)
a = h/720

results = {
    'choice':[],'p_choose':[], 'result':[], 'rt': []
    }
n_repeat = 35
df = hp.generate(n_repeat=n_repeat)
df_train = hp.generate_train(n=6)
win = visual.Window(size=(w, h), fullscr=True, units='pix')
# Text
text = visual.TextStim(win, height=64 * h / 720, pos=(0, 0), wrapWidth=10000)
feedback = visual.TextStim(win, height=64 * h / 720, pos=(0, -100*a), wrapWidth=10000)
# image
box_left = visual.ImageStim(win, size=720*a/3, pos=(-200*a, 0))
box_right = visual.ImageStim(win, size=720*a/3, pos=(200*a, 0))
fix = visual.ImageStim(win, image='img/fix.png', size=720*a/20)
hand = visual.ImageStim(win, image='img/hand.png', size=720*a/10)
gain = visual.ImageStim(win, image='img/win.png', size=720*a/3, pos=(0, 100*a))
loss = visual.ImageStim(win, image='img/fail.png', size=720*a/3, pos=(0, 100*a))
intro = visual.ImageStim(win, size=(w, h))
# 实验
myMouse = event.Mouse()
myMouse.setVisible(0)
clk = core.Clock()
# 介绍
for i in range(2):
    intro.image = 'img/introduction_%s.png' % i
    intro.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    event.clearEvents()
# 练习
intro.image = 'img/train.png'
intro.draw()
win.flip()
event.waitKeys(keyList=['space'])
rt_last = 3
clk.reset()
for i in range(len(df_train)):
    box_left.image = 'img/%s'%(df_train['pic_left'][i])
    box_right.image = 'img/%s' % (df_train['pic_right'][i])
    pic = gain
    fix.draw()
    win.flip()
    clk.reset()
    while clk.getTime() <= 3.2 - rt_last:
        pass
    box_left.draw()
    box_right.draw()
    win.flip()
    clk.reset()
    while True:
        key = event.waitKeys(keyList=['f', 'j', 'escape'], maxWait=3)
        rt = clk.getTime()
        rt_last = min([rt, 3])
        if key is not None:
            if 'f' in key:
                hand.pos = (-200*a, -150*a)
                p = df_train['p_left'][i]
            elif 'j' in key:
                hand.pos = (200 * a, -150 * a)
                p = 1-df_train['p_left'][i]
            elif 'escape' in key:
                win.close()
                core.quit()
            hand.draw()
            box_left.draw()
            box_right.draw()
            win.flip()
            core.wait(0.5)
            if np.random.uniform() < p:
                pic.draw()
                feedback.text = '+10分'
                feedback.pos = (0, -100 * a)
            else:
                feedback.text = '0分'
                feedback.pos = (0, 0)
            feedback.draw()
            win.flip()
            core.wait(2)
            win.flip()
            break
        else:
            text.text = '请再快一点'
            text.draw()
            win.flip()
            core.wait(1)
            box_left.draw()
            box_right.draw()
            win.flip()

# 正式实验
# 练习
intro.image = 'img/exp.png'
intro.draw()
win.flip()
event.waitKeys(keyList=['space'])
money_total = 0
rt_last = 3
clk.reset()
for i in range(len(df)):
    if i in [n_repeat, n_repeat*3]:
        text.text = "本房间探索结束，你累积%s分" % money_total
        text.draw()
        win.flip()
        core.wait(2)
        clk.reset()
        while clk.getTime()<10:
            text.text = '请休息，%s秒后进入下一组'%10-int(clk.getTime())
            text.draw()
            win.flip()
    elif i in [0, n_repeat*2]:
        if i != 0:
            text.text = "本房间探索结束，你累积%s分" % money_total
            text.draw()
            win.flip()
            core.wait(2)
        if df['condition'][i] == 'Gain':
            intro.image = 'img/Condition_Gain.png'
        else:
            intro.image = 'img/Condition_Loss.png'
        intro.draw()
        win.flip()
        event.waitKeys(keyList=['space'])
        event.clearEvents()
    box_left.image = 'img/%s'%(df['pic_left'][i])
    box_right.image = 'img/%s' % (df['pic_right'][i])
    if df['condition'][i] == 'Gain':
        pic = gain
    else:
        pic = loss
    fix.draw()
    win.flip()
    clk.reset()
    while clk.getTime() <= 3.2 - rt_last:
        pass
    box_left.draw()
    box_right.draw()
    win.flip()
    clk.reset()
    while True:
        key = event.waitKeys(keyList=['f', 'j', 'escape'], maxWait=3)
        rt = clk.getTime()
        rt_last = min([rt, 3])
        if key is not None:
            results['rt'].append(rt)
            if 'f' in key:
                hand.pos = (-200*a, -150*a)
                p = df['p_left'][i]
                results['choice'].append('left')
                results['p_choose'].append(p)
            elif 'j' in key:
                hand.pos = (200 * a, -150 * a)
                p = 1-df['p_left'][i]
                results['choice'].append('right')
                results['p_choose'].append(p)
            elif 'escape' in key:
                win.close()
                core.quit()
            hand.draw()
            box_left.draw()
            box_right.draw()
            win.flip()
            core.wait(0.5)
            if np.random.uniform() < p:
                feedback.pos = (0, -100 * a)
                pic.draw()
                if df['condition'][i] == 'Gain':
                    feedback.text = '+10分'
                    results['result'].append(10)
                    money_total += 10
                else:
                    feedback.text = '-10分'
                    results['result'].append(-10)
                    money_total -= 10
            else:
                feedback.text = '0分'
                feedback.pos = (0, 0)
                results['result'].append(0)
            feedback.draw()
            win.flip()
            core.wait(2)
            win.flip()
            break
        else:
            text.text = '请再快一点'
            text.draw()
            win.flip()
            core.wait(1)
            box_left.draw()
            box_right.draw()
            win.flip()

df['choice'] = results['choice']
df['p_choose'] = results['p_choose']
df['result'] = results['result']
df['rt'] = results['rt']
df.to_csv('data/exp_%s_%s.csv' % (name, time.strftime("%y-%m-%d-%H-%M")))
text.text = "本实验结束，你获得%s分" % money_total
text.draw()
win.flip()
core.wait(3)
print('总分：%s' % money_total)
win.close()
core.quit()









