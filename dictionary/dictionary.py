'''
2021/6/24
python英文学习词典
功能：
1. 添加英文单词
2. 删除英文单词
3. 查询英文单词
4. 单词测试
5. 绘制测试用户雷达图
'''
from __future__ import division
import os
import time
import random
import numpy as np
import matplotlib.pyplot as plt

Dictionary = {}     # 字典，用来存储单词
status = {'1':'极佳','2':'很好', '3':'一般','4': '不好', '5':'很差'}  # 状态字典



def import_txt():
    '''
    作者：龚攀祈
    '''
    print("字典初始化中...")
    if os.path.isfile("Dictionary.txt"):
        # 判断文件是否存在，若存在，则读文件对字典初始化，若不存在，
        # 则调用dict_add()新建文件并添加单词
        with open('Dictionary.txt', 'r', encoding='utf-8') as file:
            # 使用with可以不用close()关闭文件，发生错误可以安全的退出
            for line in file:
                #eval()用字符串初始化字典，对文件每一行进行读取创建新的字典
                Dictionary1 = eval(line)
                #用update函数添加到原字典
                Dictionary.update(Dictionary1)
            # print(Dictionary)
        init()      #初始化成功后开始运行程序
    else:
        print("词典尚未初始化，请先添加单词！")
        option = input("是否进入添加单词界面？(yes/no)")
        if (option == "yes"):
            dict_add()
            init()
        else:
            print("欢迎下次使用！")

def dict_add():
    '''
    添加单词
    最后调用自定义的词典-字符串转换函数，将字典存储在txt文件中
    作者：关慧臻
    '''
    print("字典添加功能...")
    while(1):
       word = input("请输入单词(q to quit)")
       if(word != 'q' and word != 'Q'):
           mean = input("请输入释义")
           Dictionary[word] = mean
           print("单词添加成功!\n")
           continue
       else:
           print("退出添加单词功能")
           break
    dict2string()

def dict_search():
    '''
    作者 郭之源
    查询单词
    '''
    print("单词查询功能...")
    while(1):
        word = input("请输入查询的英文(q to quit)")
        if (word == 'q' or word == 'Q'):
            break
        else:
            if(word in Dictionary):
                print("释义 ： %s" % Dictionary.get(word))
            else:
                print("词典未收录此单词")
                result = input("是否需要添加这个单词(yes/no)？")
                if(result == "yes"):
                    dict_add()
                    continue
                else:
                    continue
def dict_delete():
    '''
    作者：关慧臻
    字典删除功能，若删除整个字典需要管理员权限（默认密码123456）
    调用os.remove删除txt文件
    若单个删除，调用字典的pop函数
    最后将更新的字典重新存储
    '''
    option = input("字典删除功能...\n1.删除所有\n2.删除特定单词")
    #file = open("Dictionary.txt", "r+")
    if (option == '1'):
        print("删除所有...")
        option2 = input("确定删除所有？请输入管理员密码：")
        if(option2 == "123456"):
            Dictionary.clear()
            os.remove("Dictionary.txt")
        else:
            print("密码错误，您的权限不足")
    if (option == '2'):
        word = input("请输入单词(q to quit)")
        if (word != 'q' and word != 'Q'):
            while(1):
                Dictionary.pop(word)
                option3 = input("删除成功，是否继续删除？(yes/no)")
                if(option3 == "yes"):
                    continue
                else:
                    break
        dict2string()

def dict2string():
    '''
    作者：龚攀祈
    由于在import_txt函数中用txt对字典进行了初始化，
    在这写入时需要对整个txt文件进行覆盖
    将字典中的key:value抽取转换成字符串，再写到文件中
    '''
    with open("Dictionary.txt", "w+") as file:
        for key, value in Dictionary.items():
            string1 = "{\"%s\" : \"%s\"}\n" % (key, value)
            file.write(string1)

def radiomap():
    #作者 郭之源
    # 中文和负号的正常显示
    plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
    plt.rcParams['axes.unicode_minus'] = False

    # 使用ggplot的风格绘图
    plt.style.use('ggplot')

    # 构造数据  将对应变量直接填入下列数组，下列为测试所用数据.若增加数据项只需修改下面两项数据即可
    values = [int(numA), test_time/300*5, precision*5]
    feature = ['状态', '答题速度', "答题准确率"]

    # 数据项数目，由数组数据项而定
    N = len(values)

    # 设置雷达图的角度，用于平分切开一个平面
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False)

    # 使雷达图封闭起来
    values = np.concatenate((values, [values[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    # 绘图 面向对象编程，创建一个对象ax以调用plt相关函数
    fig = plt.figure()
    # 设置为极坐标格式
    ax = fig.add_subplot(111, polar=True)
    # 绘制折线图
    ax.plot(angles, values, 'pink', linewidth=2, label='Result')
    ax.fill(angles, values, 'b', alpha=0.5)

    # 添加每个数据的标签
    ax.set_thetagrids(angles * 180 / np.pi, feature)
    # 设置极轴范围  此处预设分为5个等级
    ax.set_ylim(0, 5)
    # 添加标题
    plt.title('测试评价图')
    # 增加网格纸
    ax.grid(True)
    plt.show()

# KMP算法
# 调用此算法在test中进行字符串匹配
def get_next(T):
    i = 0
    j = -1
    next_val = [-1] * len(T)
    while i < len(T) - 1:
        if j == -1 or T[i] == T[j]:
            i += 1
            j += 1
            # next_val[i] = j
            if i < len(T) and T[i] != T[j]:
                next_val[i] = j
            else:
                next_val[i] = next_val[j]
        else:
            j = next_val[j]
    return next_val

def kmp(S, T):
    i = 0
    j = 0
    next = get_next(T)
    while i < len(S) and j < len(T):
        if j == -1 or S[i] == T[j]:
            i += 1
            j += 1
        else:
            j = next[j]
    if j == len(T):
        return i - j
    else:
        return -1

def dict_test():
    '''作者：焦圣杰'''
    print("开始测试...请根据屏幕显示的英文输入对应中文含义\n"
          "若完全正确，得2分，不完整得1分，错误得0分，总分：20")
    global numA
    numA = input("请输入您本次测试状态(1(很差)-5(极好))")
    test_status = status[numA]

    score = 0
    starttime = time.time() # 时间函数，开始
    for i in range(10):
        sum = 0
        # 随机抽取一个测试单词
        test_word = random.sample(Dictionary.keys(), 1)
        print("第%d个： %s" % (i+1, test_word))
        test_mean = input("请输入单词的中文含义：")
        if(test_mean == ''):
            print("请不要输入空")
            continue
        #my_list将输入的释义test_mean得每个单词提取，建立一个列表
        #my_list2将正确释义提取为列表
        my_list = [x.strip() for x in test_mean.split('，')]         #将输入得test_mean进行抽取形成列表
        my_list2 = [x.strip() for x in Dictionary[''.join(test_word)].split('，')]
        # 对my_list中每个单词遍历对比正确释义字符串
        # sum保存匹配正确的次数
        # 若sum = len(my_list2),即正确答案的单词数，则说明完全正确
        # 若sum != 0,则说明至少有一个匹配成功，答案不完整
        # 若sum == 0,则说明一个都不对，错误
        for i in range(len(my_list)):
            if(kmp( Dictionary[''.join(test_word)], my_list[i]) != -1):    #对每个单词进行匹配
                sum = sum + 1
        if(sum == len(my_list2)):
            score += 2
            print("恭喜，完全正确！")

        elif(sum !=0):
            score += 1
            print("正确，但不完整。正确答案为")
            print(Dictionary[''.join(test_word)])

        else:
            score += 0
            print("抱歉，您答错了。正确答案为")
            print(Dictionary[''.join(test_word)])

    endtime =  time.time()         # 时间函数，结束
    global test_time
    global precision
    precision = round((float(score) / 20), 2)   # 计算准确性，调用round计算小数
    print(precision)
    test_time = (endtime - starttime)
    print(test_time)

def init():
    #作者:区锐明
    menu = """
            ##############################
            1. 添加单词
            2. 查询单词
            3. 删除单词
            4. 单词测试
            5. 测试结果
            quit. 退出程序
            ##############################
        """
    while (1):
        print(menu)
        choice = input('Please input your choice(q to quit):')
        if (choice == 'q' or choice == 'Q'):
            break
        else:
            dict_menu = {"1": dict_add,
                         "2": dict_search,
                         "3": dict_delete,
                         "4": dict_test,
                         "5": radiomap,
                         }
            dict_menu[choice]()

if __name__ == '__main__':
    import_txt()



