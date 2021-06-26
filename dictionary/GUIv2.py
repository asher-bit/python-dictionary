import wx
import os
import numpy as np
import matplotlib.pyplot as plt

dictionary = {}
class dict(wx.Frame):
    def __init__(self):
        with open('Dictionary.txt', 'r', encoding='utf-8') as file:
            for line in file:
                '''
                用文件初始化字典，对文件每一行进行读取创建新的字典
                用update函数添加到原字典
                '''
                Dictionary1 = eval(line)
                dictionary.update(Dictionary1)

        wx.Frame.__init__(self, None, -1, 'English Dictionary',
                size=(1000, 500))
        gbk = wx.Panel(self)

        self.loadbutton = wx.Button(gbk, label='查询')
        self.loadbutton.Bind(wx.EVT_BUTTON, self.dict_search)
        self.savebutton = wx.Button(gbk, label='clear')
        self.savebutton.Bind(wx.EVT_BUTTON, self.dict_clear)
        self.insertbutton = wx.Button(gbk, label='插入')
        self.insertbutton.Bind(wx.EVT_BUTTON, self.dict_insert)
        self.deletebutton = wx.Button(gbk, label='删除')
        self.deletebutton.Bind(wx.EVT_BUTTON, self.Onmsgbox)
        self.mapbutton = wx.Button(gbk, label='雷达图')
        self.mapbutton.Bind(wx.EVT_BUTTON, self.map)

        self.textframe1 = wx.TextCtrl(gbk)
        self.textframe2 = wx.TextCtrl(gbk)
        self.contents = wx.TextCtrl(gbk, style=wx.TE_MULTILINE | wx.HSCROLL)

        hbox = wx.BoxSizer()
        hbox.Add(self.textframe1, proportion=1, flag=wx.ALL, border=5)
        hbox.Add(self.loadbutton, proportion=0, flag=wx.ALL, border=5)
        hbox.Add(self.savebutton, proportion=0, flag=wx.ALL, border=5)

        hbox2 = wx.BoxSizer()
        hbox2.Add(self.textframe2, proportion=1, flag=wx.ALL, border=5)
        hbox2.Add(self.insertbutton, proportion=0, flag=wx.ALL, border=5)
        hbox2.Add(self.deletebutton, proportion=0, flag=wx.ALL, border=5)
        hbox2.Add(self.mapbutton, proportion=0, flag=wx.ALL, border=5)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox, proportion=0, flag=wx.EXPAND)
        vbox.Add(hbox2, proportion=0, flag=wx.EXPAND)
        vbox.Add(self.contents, proportion=1, flag=wx.EXPAND, border=5)

        gbk.SetSizer(vbox)






    def dict_search(self, event):
        # GetValue返回空间中的字符串，在字典中进行查找
        if self.textframe1.GetValue() in dictionary:
            # SetValue将词典中释义输出到文字框
            self.contents.SetValue(dictionary[self.textframe1.GetValue()] + "\n")
        else:
            # 设置字符串
            self.contents.SetValue("该词汇尚未录入，敬请期待！")

    def dict_clear(self, event):
        # 清空文字框内容
        self.contents.Clear()

    def dict_insert(self, event):
        word = self.textframe1.GetValue()
        mean = self.textframe2.GetValue()
        if(dictionary[word] == ""):
            self.contents.SetValue("无法添加空条目")
        else:
            dictionary[word] = mean
            self.dict2string()
            self.contents.SetValue("添加成功")

    def dict_delete(self, event):
        option = event.GetEventObject()
        if (option.GetLabel() == '删除所有单词'):
            self.textframe1.Clear()
            self.contents.SetValue("确定删除所有？请输入管理员密码：")
            if (self.textframe1.GetValue() == "123456"):
                dictionary.clear()
                os.remove("Dictionary.txt")
            else:
                self.contents.SetValue("密码错误，您的权限不足")
        if (option.GetLabel() == '删除特定单词'):
            #textframe1.Clear()
            word = self.textframe1.GetValue()
            dictionary.pop(word)
            self.dict2string()
            self.contents.SetValue("删除成功")

    def map(self, event):
        plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
        plt.rcParams['axes.unicode_minus'] = False

        # 使用ggplot的风格绘图
        plt.style.use('ggplot')

        # 构造数据  将对应变量直接填入下列数组，下列为测试所用数据.若增加数据项只需修改下面两项数据即可
        values = [3.2, 2.1, 3.5]
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

    def Onmsgbox(self, event):
        f2 = wx.Frame(None, title='Choice')
        pnl = wx.Panel(f2)
        wx.StaticText(pnl, -1, '请注意，在选择方式前，请现在English Dictionary中\n填写您想要删除的单词（密码）', (10,10))

        f2.cb1 = wx.CheckBox(pnl, label='删除所有单词(需输入管理员密码)', pos=(10, 70))
        f2.cb2 = wx.CheckBox(pnl, label='删除特定单词', pos=(10, 100))

        f2.Bind(wx.EVT_CHECKBOX, self.dict_delete)
        f2.Centre()
        f2.Show(True)


    def dict2string(self):
        #由于在程序开始对字典进行了初始化，在这写入时需要对整个txt文件进行覆盖
        file = open("Dictionary.txt", "w+")
        for key, value in dictionary.items():
            string1 = "{\"%s\" : \"%s\"}\n" % (key, value)
            file.write(string1)
        file.close()




def main():
    app = wx.App()
    frame = dict()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()