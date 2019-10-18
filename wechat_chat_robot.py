import re
import time

import requests
import itchat
import random
from pymongo import MongoClient

# # 创建连接对象
client = MongoClient(host='localhost', port=27017)
# # 获得数据库，此处使用 data
db = client.wechat
col = db.chattingcontent
# start mongodb command
# sudo /usr/local/mongodb/bin/mongod --dbpath=/data/db/

# KEY='e4c59585ded1480b87c10b753e7baae7'
#
KEY = '62a98648325a4eea9407945a275ea29c'
# KEY = '9d22f7e2a7a347b18d57743882fe7367'
# KEY = 'e4c59585ded1480b87c10b753e7baae7'

from itchat.content import *
def get_response(msg):
    api_url = 'http://www.tuling123.com/openapi/api'  # 图灵机器人网址
    data = {
        'key': KEY,
        'info': msg,  # 这是我们从好友接收到的消息 然后转发给图灵机器人
        # 'userid': 'wechat-robot',  # 这里你想改什么都可以
        'userid': 'wechat-robot-test',  # 这里你想改什么都可以

    }
    try:
        r = requests.post(api_url, data=data).json()
        # 向服务器发送请求
        return r.get("text")
    except:
        return


# @itchat.msg_register(itchat.content.TEXT)
# def tuling_reply(msg):
#     defaultReplay = 'I received: ' + msg['Text']
#     robots = ['I am Jarvis.May I have a message to Tony?', 'Hello,I am Jarvis.']
#     reply = get_response(msg['Text'])
#     # random.choice会从robots中随机选取一个元素，这个可以根据自己喜好来修改
#     return reply


@itchat.msg_register([itchat.content.TEXT], isGroupChat=True)
# 用于接收群里面的对话消息
def print_content(msg):
    return get_response(msg['Text'])


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=True)
def text_reply(msg):
    if msg.User["NickName"] == 'YY爬虫群':
        present_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("Now is %s, the msg or pic is from %s, %s. " % (present_time, msg.User['NickName'], msg['ActualNickName']))
        receive_msg = str(msg['Text'])
        print(receive_msg)
        # print(receive_msg)
        sender = msg.User['NickName']+","+msg['ActualNickName']
        with open("chatting_content.txt", "a+") as f:
            f.write("time" + ":"+present_time + " "+"sender" + ":"+sender+"  Message: "+receive_msg+'\n')

        # itchat.send("测试中,聊天内容已存入数据库", msg['FromUserName'])

        data_ = [{"time": present_time,
                  "sender": sender,
                  'message': receive_msg,
                  }]

        for item in data_:
            if col.update_one(item, {'$set': item}, upsert=True):
                # print('存储成功')
                pass

"""
        msg_ = []
        print("-------------------------------------------------接受的消息--------------------------------------------------")
        for i in receive_msg:
            print(i)
            try:
                # 匹配文本中的数字
                numbers = re.findall(r"\d+\.?\d*", i)
                # print(numbers)
                # remove date 7.5 7.22
                for index, value in enumerate(numbers):
                    if "." in str(value) and (index == 0 or index == 2 or index == 3):
                        numbers.remove(value)
                # 十万扣息
                max_number = int(numbers[0])
                for number in numbers:
                    if max_number < int(number):
                        max_number = int(number)
                hundred_thousand_interest = str(max_number)
                #
                numbers.remove(hundred_thousand_interest)
                amount = numbers[0]

                n_nums=len(numbers)


                # 匹配文本中的汉字
                words = re.findall(r'[\u4e00-\u9fa5]+', i)
                # print(words)
                for word in words:
                    # print(word, len(word))
                    if len(numbers) != 0 and len(word) < 8:
                        all_price = sorted([eval(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", x)) for x in numbers], reverse=True)
                        max_length, content = max([(len(x), x) for x in words])
                        # print(content)

                        n = len(words)
                        # print(n)
                        no_words = ["张",  "几张", "出", "多张", "少量", '一张', '多张加', "张起", '张代', ]
                        delete_all_ls_by_words = ["重复", "大回", "价高", "询价", "带价", "天价", "回头", '高价', '不限行批量',
                                                  '每天批量收一年', '户里大量现款收批量半年']
                        # 删除无用数据
                        for delete_all_ls_by_word in delete_all_ls_by_words:
                            for word_x in words:
                                if delete_all_ls_by_word == word_x or len(word_x) >= 7 or "批量" in word_x:
                                    del words[-n:]
                        # print(words)

                        #删除特殊字符
                        for no_word in no_words:
                            for word_ in words:
                                if no_word == word_:
                                    words.remove(no_word)


                        m = len(words)
                        # print(m)
                        if m == 2 and ("半年" == str(words[1]) or "一" == str(words[1]) or "一年" == str(words[1]) or "剩半年" == str(words[1])):
                            date_range = words[1]
                            content = words[0]
                            print("-------------situation 1 -------------------------------------------")
                            a = date_range + "    " + content.strip("半年").strip("一年期").strip("一年").strip(
                                "一") + "    " + amount + "    " + hundred_thousand_interest + "\n"

                        elif m == 2 and ("半年" == str(words[0]) or "一" == str(words[0]) or "一年" == str(words[0]) or "剩半年" == str(words[0])):
                            date_range = words[0]
                            content = words[1]
                            print("-------------situation 2 -------------------------------------------")

                            a = date_range + "    " + content.strip("半年").strip("一年期").strip("一年").strip(
                                "一") + "    " + amount + "    " + hundred_thousand_interest + "\n"

                        elif m == 1 and ("半" in str(words[0]) or "一" in str(words[0])):
                            date_range = words[0]
                            content = words[0]
                            print("-------------situation 3 -------------------------------------------")

                            a = date_range + "    " + content.strip("半年").strip("一年期").strip("一年").strip(
                                "一") + "    " + amount + "    " + hundred_thousand_interest + "\n"

                        elif m == 1 and ("半年" not in str(words[0]) and "一年期" not in str(words[0]) and "一" not in str(words[0])):
                            date_range = "无"
                            content = words[0]
                            print("-------------situation 4 -------------------------------------------")

                            a = date_range + "    " + content.strip("半年").strip("一年期").strip("一年").strip(
                                "一") + "    " + amount + "    " + hundred_thousand_interest + "\n"


                        msg_.append(a)
                        # 向集合同城票据中插入一条文档
                        data_ = [{"time_limition": date_range,
                                  " bank": content.strip("半年").strip("一年期").strip("一年").strip(
                                "一"),
                                  'amount': amount,
                                  'hundred_thousand_interest ': hundred_thousand_interest

                                  }]

                    for item in data_:
                        col.insert_one(item)
            except (IndexError, UnboundLocalError, ValueError) as e:
                # print(e)
                pass

        print("--------------------------------------------------处理后的信息-----------------------------------------------")
        y = ""
        for x in msg_:
            # 将消息的类型和文本内容返回给发送者
            y += x
        print(y)
        # time.sleep(3)
        #
        # itchat.send('%s \n' % y, msg['FromUserName'])

"""




@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)    #群图片消息的处理
def download_files(msg):
    if msg.User["NickName"] == 'YY爬虫群':

    # print(msg.User['NickName'] + ":" + msg['Text'])     #打印哪个群给你发了什么消息
    # 传入文件名，将文件下载下来
        msg['Text'](msg['FileName'])    # 把下载好的文件再发回给发送者

    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])
    
    # return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

    #     if msg["Content"]=="图片":
    #         pic = "mao.jpg"
    #         print(111)
    #     # print(get_response(msg['Text'])+"\n")           #打印机器人回复的消息
    #         name = msg.User["NickName"]
    #         print(name)
    #         itchat.send_image(pic, toUserName=name)
    #     else:
    #         return get_response(msg['Text'])
    # else:                                         #其他群聊直接忽略
    #     pass

# @itchat.msg_register([itchat.content.TEXT,itchat.content.PICTURE], isGroupChat=True):


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)  # , 保持在线，下次运行代码可自动登录  hotReload=True
    itchat.run()

