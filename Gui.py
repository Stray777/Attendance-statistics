import tkinter as tk
from tkinter import messagebox
import pyperclip
import datetime
import os


class Gui:
    def __init__(self, master):
        self.master = master

        # 屏幕宽度和高度
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()

        # 窗口居中
        self.master.geometry(f"600x450+{(self.screen_width - 600) // 2}+{(self.screen_height - 450) // 2}")
        # 主窗口title
        self.master.title("考勤文本转换2.0")

        # 组件
        self.transform_button = tk.Button(self.master, text="开始转换", command=self.txt_transform_button)
        self.label = tk.Label(self.master, text="请输入或粘贴原文：")
        self.text = tk.Text(self.master)

        # 布局
        self.transform_button.pack(pady=10)
        self.label.pack(anchor='w', padx=15)
        self.text.pack(padx=15, pady=5)

    def txt_transform_button(self):
        try:
            self.txt_transform()  # 调用文本转换功能
            self.success_popup()
            # 删除pre.txt和result.txt
            self.del_file('pre.txt')
            self.del_file('result.txt')
        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {str(e)}")

    def txt_transform(self):
        flag = 0
        l1 = []
        l2 = []
        l3 = []
        li = [l1, l2, l3]

        with open("pre.txt", 'w', encoding='utf-8') as file:
            text1 = self.text.get("1.0", "end")
            file.write(text1)

        with open("pre.txt", 'r', encoding='utf-8') as file:
            # 星期映射字典
            week_dic = {
                0: '星期一',
                1: '星期二',
                2: '星期三',
                3: '星期四',
                4: '星期五',
                5: '星期六',
                6: '星期日'
            }

            while True:
                if flag == 0:
                    line = file.readline()

                if line == '':
                    break
                elif '考勤' in line:
                    line = line.strip(' ')
                    line = line.replace('考勤', '')
                    num_list = line.split('.')
                    # 构造日期对象
                    date = datetime.datetime(datetime.datetime.now().year, int(num_list[0]), int(num_list[1]))
                    # 星期几
                    day_of_week = date.weekday()
                    day_of_week_ch = week_dic[day_of_week]
                    line = f"{date.year}年{str(date.month).zfill(2)}月{date.day}日{day_of_week_ch}：\n"

                    l1.append(line)
                    l2.append(line)
                    l3.append(line)
                    flag = 0
                elif '舞蹈班' in line:
                    while True:
                        line = file.readline()
                        if line == '\n':
                            continue
                        elif (line == '') or ("考勤" in line) or ("音表1班" in line) or ("音表2班" in line):
                            flag = 1
                            break
                        else:
                            l1.append(line)
                elif '音表1班' in line:
                    while True:
                        line = file.readline()
                        if line == '\n':
                            continue
                        elif (line == '') or ("考勤" in line) or ("舞蹈班" in line) or ("音表2班" in line):
                            flag = 1
                            break
                        else:
                            l2.append(line)
                elif '音表2班' in line:
                    while True:
                        line = file.readline()
                        if line == '\n':
                            continue
                        elif (line == '') or ("考勤" in line) or ("音表1班" in line) or ("舞蹈班" in line):
                            flag = 1
                            break
                        else:
                            l3.append(line)
                else:
                    continue

        for index1, i in enumerate(li):
            for index2, j in enumerate(i):
                if ("年" and '月' and '日' in j) and i[index2] == i[-1]:
                    i[index2] = '00000'
                elif ("年" and '月' and '日' in j) and ("年" and '月' and '日' in i[index2 + 1]):
                    i[index2] = '00000'
            li[index1] = [x for x in li[index1] if x != '00000']

        for i in li:
            if not i:
                i.append("无\n")

        li[0].insert(0, "舞蹈班\n")
        li[1].insert(0, "\n\n音表1班\n")
        li[2].insert(0, "\n\n音表2班\n")

        with open("result.txt", 'w', encoding='utf-8') as file:
            for i in li:
                for j in i:
                    file.write(j)

    def success_popup(self):
        popup = tk.Toplevel(self.master)
        popup.title("转换成功！")
        # 窗口居中
        popup.geometry(f"500x400+{(self.screen_width - 500) // 2}+{(self.screen_height - 400) // 2}")

        button = tk.Button(popup, text="复制", command=lambda: self.copy_to_clipboard(text))
        text = tk.Text(popup)

        button.pack(pady=10)
        text.pack()

        with open("result.txt", 'r', encoding='utf-8') as file:
            content = file.readlines()

        for s in content:
            text.insert(tk.END, s)

    @staticmethod
    def copy_to_clipboard(text):
        selected_text = text.get("1.0", "end")
        if selected_text:
            pyperclip.copy(selected_text)

    @staticmethod
    def del_file(path):
        try:
            os.remove(path)
        except FileExistsError:
            messagebox.showerror('错误', f'{path}不存在，无法删除。')
