# 下面是一个更详细的步骤，说明如何使用PyInstaller将Python脚本（和它的依赖项）打包到一个.exe文件中：
# 打开命令提示符(cmd)或终端。
# 安装PyInstaller。在命令行中输入pip install pyinstaller然后回车。
# 使用cd命令切换到你的Python脚本所在的目录。例如，如果你的脚本在"C:\Users\YourName\Documents\MyScript.py"，你应该输入cd C:\Users\YourName\Documents\然后回车。
# 在命令行中输入pyinstaller --noconsole --onefile --icon=ico/Natsume.ico filename.py然后回车。这会告诉PyInstaller将你的脚本和所有的依赖项打包到一个单一的.exe文件中。
# 等待PyInstaller完成打包过程。这可能需要几分钟的时间，取决于你的脚本的大小和复杂性。
# 完成后，你会在当前目录下的"dist"文件夹中找到你的.exe文件。你可以直接运行这个文件，或者将它复制到其他地方。

current_version = "v1.0" # 版本号
# 坚果云账号和密码
username = "imybfu@outlook.com"
password = "axzyqd3a6brx99ei"

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, simpledialog
import pandas as pd
from webdav4.client import Client
import os
from getmac import get_mac_address
import pandas as pd
from datetime import datetime
import openpyxl
import webbrowser

#####################################################################################
# 创建或加载术语表
try:
    df = pd.read_excel('glossary.xlsx', engine='openpyxl')
    glossary = {}
    for index, row in df.iterrows():
        term = str(row['terms']).upper()
        full = str(row['full_form'])
        expl = str(row['explanation'])
        if term:
            glossary[term] = {"full_form": full, "explanation": expl}
except FileNotFoundError:
    # 创建一个空的DataFrame
    df = pd.DataFrame(columns=['terms', 'full_form', 'explanation'])
    # 将DataFrame保存为Excel文件
    df.to_excel('glossary.xlsx', index=False)
    # 创建一个空的词典
    glossary = {}

# 定义全局变量来跟踪当前匹配项的索引
current_match_index = -1
# 在search_term函数中，更新左侧列表并显示匹配到的术语
def search_term(event=None):
    global current_match_index  # 声明全局变量
    
    search_query = entry_search.get().lower()
    matching_terms = []
    # 清空文本框
    text_full_form.delete(1.0, tk.END)
    text_explanation.delete(1.0, tk.END)
    # 在术语表中进行模糊搜索
    for term, data in glossary.items():
        full_form_term = data["full_form"].lower()
        explanation_term = data["explanation"].lower()
        
        if search_query in term.lower() or search_query in full_form_term or search_query in explanation_term:
            matching_terms.append(term)
    if matching_terms:
        current_match_index = (current_match_index + 1) % len(matching_terms)  # 更新当前匹配项的索引
        
        result = glossary[matching_terms[current_match_index]]
        # 插入新内容
        text_full_form.insert(tk.END, result["full_form"])
        text_explanation.insert(tk.END, result["explanation"])
        # 更新左侧列表的选中项，并确保它在可视范围内
        index = glossary_list.get(0, tk.END).index(matching_terms[current_match_index])  #获取当前匹配术语在术语列表中的索引
        glossary_list.selection_clear(0, tk.END)
        glossary_list.selection_set(index)
        glossary_list.see(index)
    else:
        messagebox.showerror("Error", "Term not found")
        
        
# 更新标题栏中的术语数目
def update_title():
    root.title(f"Glossary ({current_version}) - {len(glossary)} terms")

# 更新术语列表
def update_glossary_list():
    glossary_list.delete(0, tk.END)  # 清空术语列表
    for term in sorted(glossary.keys()):  # 按字母顺序排序
        glossary_list.insert(tk.END, term)
    glossary_count.set(len(glossary))

def update_excel():
    # 将字典转换为 DataFrame，并设置合适的列名
    df = pd.DataFrame.from_dict(glossary, orient='index')
    df.index.name = 'terms'
    df.reset_index(inplace=True)
    # 将 DataFrame 写入 Excel 文件
    df.to_excel('glossary.xlsx', index=False)

# 添加术语
def add_term(event=None):  # 修改函数签名以接受事件参数，参数设置为None以确保不会影响直接调用
    term = entry_add_term.get().upper()
    full = entry_add_full.get()
    expl = entry_add_expl.get()
    if term:
        glossary[term] = {"full_form": full, "explanation": expl}
        update_excel()  # 更新Excel文件
        update_glossary_list()  # 更新术语列表
        update_title()  # 更新标题栏中的术语数目
        messagebox.showinfo("Success", "Term added successfully")
        # 在列表中定位到添加的术语
        index = glossary_list.get(0, tk.END).index(term)
        glossary_list.selection_clear(0, tk.END)
        glossary_list.selection_set(index)
        glossary_list.see(index)
    else:
        messagebox.showerror("Error", "Please fill in the term field")

# 删除术语
def delete_term():
    selection = glossary_list.curselection()  # 获取当前选中的索引
    if selection:
        term = glossary_list.get(selection[0])  # 获取当前选中的术语
        if term in glossary:
            del glossary[term]
            update_excel()  # 更新Excel文件
            update_glossary_list()  # 更新术语列表
            update_title()  # 更新标题栏中的术语数目
            messagebox.showinfo("Success", "Term deleted successfully")
        else:
            messagebox.showerror("Error", "Term not found")

# 更新术语
def update_term():
    selection = glossary_list.curselection()  # 获取当前选中的索引
    if selection:
        term = glossary_list.get(selection[0])  # 获取当前选中的术语
        if term in glossary:
            full = simpledialog.askstring("Update Term", "Enter the full form:", initialvalue=glossary[term]['full_form'])
            # Check if user pressed Cancel
            if full is None:
                return
            expl = simpledialog.askstring("Update Term", "Enter the explanation:", initialvalue=glossary[term]['explanation'])
            # Check if user pressed Cancel
            if expl is None:
                return
            if full or expl:
                glossary[term] = {"full_form": full, "explanation": expl}
                update_excel()  # 更新Excel文件
                messagebox.showinfo("Success", "Term updated successfully")
                update_glossary_list()  # 更新术语列表
            else:
                messagebox.showerror("Error", "Please fill in one field at least")
        else:
            messagebox.showerror("Error", "Term not found")

# 显示术语
def show_term(event):
    selection = glossary_list.curselection()
    if selection:
        term = glossary_list.get(selection[0])
        result = glossary[term]
        # 清空文本框
        text_full_form.delete(1.0, tk.END)
        text_explanation.delete(1.0, tk.END)
        # 插入新内容
        text_full_form.insert(tk.END, result["full_form"])
        text_explanation.insert(tk.END, result["explanation"])

# 显示右键菜单        
def show_context_menu(event):
    global context_menu  # 将context_menu声明为全局变量
    selection = glossary_list.curselection()
    if selection:
        context_menu = tk.Menu(glossary_list, tearoff=0)
        context_menu.add_command(label="Update", command=update_term)
        context_menu.add_command(label="Delete", command=delete_term)
        context_menu.post(event.x_root, event.y_root)

def upload_to_jianguoyun():
    # 检查本地是否存在glossary文件
    if not os.path.exists('glossary.xlsx'):
        messagebox.showerror("Error", "Glossary file does not exist")
        return
    # 如果存在，继续执行上传操作
    mac_address = get_mac_address()  # 获取设备的 MAC 地址
    cloud_filename = f'{mac_address.replace(":", "")}.xlsx'
    client = Client(base_url='https://dav.jianguoyun.com/dav/', auth=(username, password))
    cloud_path = f'/nutshare/glossary/{cloud_filename}'  # 替换为您的实际目标路径
    try:
        client.upload_file(from_path='glossary.xlsx', to_path=cloud_path, overwrite=True)
        messagebox.showinfo("Success", "File uploaded successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to upload file: {str(e)}")
        return

def download_from_jianguoyun():
    mac_address = get_mac_address()  # 获取设备的 MAC 地址
    cloud_filename = f'{mac_address.replace(":", "")}.xlsx'
    client = Client(base_url='https://dav.jianguoyun.com/dav/', auth=(username, password))
    cloud_path = f'/nutshare/glossary/{cloud_filename}' # 替换为您的实际文件路径
    # 检查云端文件是否存在，如果存在进行后续操作，否则抛出异常
    try:
        file_info = client.exists(cloud_path)
    except HTTPError as e:
        if e.response.status_code == 404:
            messagebox.showerror("Error", "File not found on cloud")
            return
        else:
            messagebox.showerror("Error", f"Failed to check file existence: {str(e)}")
            return
    current_time = datetime.now().strftime("%Y%m%d%H%M%S") # 生成当前时间的标记，用于重命名本地文件
    # 如果本地有glossary文件，将之改名为备份文件
    backup_filename = f"glossary_{current_time}.xlsx"
    try:
        if os.path.exists("glossary.xlsx"):
            os.rename("glossary.xlsx", backup_filename)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to backup local file: {str(e)}")
        return
    # 下载远程文件到本地，如果下载成功，则更新术语列表和标题栏，并显示成功消息
    try:
        client.download_file(from_path=cloud_path, to_path="glossary.xlsx")
        try:
            df = pd.read_excel('glossary.xlsx', engine='openpyxl')  # 重新读取下载后的 glossary.xlsx 文件
            glossary.clear()  # 清空当前的 glossary 字典
            for index, row in df.iterrows():
                term = str(row['terms']).upper()
                full = str(row['full_form'])
                expl = str(row['explanation'])
                if term:
                    glossary[term] = {"full_form": full, "explanation": expl}  # 更新 glossary 字典
            update_glossary_list()
            update_title()
            messagebox.showinfo("Success", "File downloaded successfully")
        # 如果下载后的文件未找到或者无法读取，则显示错误消息，并将备份文件名改回glossary
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found")
            remove("glossary.xlsx") # 预防产生一个错误的xlsx文件的情况，将其删除
            if os.path.exists(backup_filename):
                os.rename(backup_filename, "glossary.xlsx")
            return
    # 如果下载失败，则显示错误消息，并将备份文件名改回glossary
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download file: {str(e)}")
        if os.path.exists(backup_filename):
            os.rename(backup_filename, "glossary.xlsx")
        return

def read_local_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
            glossary.clear()
            for index, row in df.iterrows():
                term = str(row['terms']).upper()
                full = str(row['full_form'])
                expl = str(row['explanation'])
                if term:
                    glossary[term] = {"full_form": full, "explanation": expl}
            update_excel()
            update_glossary_list()
            update_title()
            messagebox.showinfo("Success", "File loaded successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")

# README_TEXT = """
# PRINT YOUR README HERE
# """
# def open_readme():
#     messagebox.showinfo("Readme", README_TEXT)

# 跳转GITHUB项目地址
def open_readme():
    url = "https://github.com/imybfu/glossary.git"
    webbrowser.open_new(url)

#####################################################################################
# 创建GUI
root = tk.Tk()  # 创建根窗口
update_title()  # 修改标题，添加术语计数

# 框架部件的单位是像素，文本和按钮的单位是字符数
root.geometry("400x400")  # 设置窗口大小。
root.resizable(False, False)

# 左侧区域：列表和滚动条
glossary_frame = tk.Frame(root)
glossary_frame.place(x=10, y=10, width=100, height=380)

scrollbar = tk.Scrollbar(glossary_frame)  # 创建一个滚动条部件
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

glossary_list = tk.Listbox(glossary_frame, yscrollcommand=scrollbar.set)  # 创建一个列表框部件，显示术语列表
glossary_list.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=glossary_list.yview)  # 将滚动条与列表框关联，实现滚动功能

glossary_list.bind("<<ListboxSelect>>", show_term)  # 绑定列表框选中事件
glossary_list.bind("<Button-3>", show_context_menu)  # 绑定鼠标右键点击事件

glossary_count = tk.IntVar() # 创建一个整型变量，用于显示术语数目
update_glossary_list() # 更新术语列表

# 第一层：Search Term模块
search_frame = tk.Frame(root)  # 创建一个框架用于容纳搜索术语相关的部件
search_frame.place(x=120, y=10, width=260, height=30)

entry_search = tk.Entry(search_frame, width=20)  # 创建一个文本输入框部件
entry_search.pack(side=tk.LEFT)

button_search = tk.Button(search_frame, text="Search", command=search_term, width=10)  # 创建一个按钮部件，并关联一个函数作为回调函数
button_search.pack(side=tk.RIGHT)

entry_search.bind("<Return>", search_term)  # 在entry_search上绑定<Return>事件

# 第二层：显示内容
show_frame = tk.Frame(root)  # 创建一个框架用于容纳搜索术语相关的部件
show_frame.place(x=120, y=50, width=260, height=170)

text_full_form = tk.Text(show_frame, wrap=tk.WORD, height=2)
text_full_form.pack()

text_explanation = tk.Text(show_frame, wrap=tk.WORD, height=10)
text_explanation.pack()

# 第三层：Add New Term模块
add_frame = tk.Frame(root)  # 创建一个框架用于容纳搜索术语相关的部件
add_frame.place(x=120, y=230, width=260, height=80)

add1_frame = tk.Frame(add_frame)
add1_frame.pack(fill=tk.X, expand=True) # 这里的fill不可取消

entry_add_term = tk.Entry(add1_frame, width=15)  # 创建一个文本输入框部件
entry_add_term.pack(side=tk.LEFT)

button_add = tk.Button(add1_frame, text="Add New Term", command=add_term, width=15)  # 创建一个按钮部件，并关联一个函数作为回调函数
button_add.pack(side=tk.RIGHT)

entry_add_full = tk.Entry(add_frame)  # 创建一个文本输入框部件
entry_add_full.pack(fill=tk.X, expand=True) # 这里的fill不可取消

entry_add_expl = tk.Entry(add_frame)  # 创建一个文本输入框部件
entry_add_expl.pack(fill=tk.X, expand=True) # 这里的fill不可取消

entry_add_term.bind("<Return>", lambda event: entry_add_full.focus_set())  # 在entry_add_term上绑定<Return>事件
entry_add_full.bind("<Return>", lambda event: entry_add_expl.focus_set())  # 在entry_add_full上绑定<Return>事件
entry_add_expl.bind("<Return>", add_term)  # 在entry_add_expl上绑定<Return>事件

# 第四层：设置区域
set_frame = tk.Frame(root)
set_frame.place(x=120, y=320, width=260, height=30)

button_upload = tk.Button(set_frame, text="Upload File", command=upload_to_jianguoyun, width=15)  # 创建一个按钮部件，并关联一个函数作为回调函数
button_upload.pack(side=tk.LEFT)

button_download = tk.Button(set_frame, text="Download File", command=download_from_jianguoyun, width=15)  # 创建一个按钮部件，并关联一个函数作为回调函数
button_download.pack(side=tk.RIGHT)

# 第五层：README区域
read_frame = tk.Frame(root)
read_frame.place(x=120, y=360, width=260, height=30)

button_readfile = tk.Button(read_frame, text="Read File", command=read_local_file, width=15)
button_readfile.pack(side=tk.LEFT)

button_readme = tk.Button(read_frame, text="Readme", command=open_readme, width=15)
button_readme.pack(side=tk.RIGHT)

# 启动主循环
root.mainloop()
