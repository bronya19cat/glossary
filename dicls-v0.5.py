# CMD依赖项：pyinstaller、tkinter(pip install tk)、pandas、openpyxl。

# 下面是一个更详细的步骤，说明如何使用PyInstaller将Python脚本（和它的依赖项）打包到一个.exe文件中：
# 打开命令提示符(cmd)或终端。
# 安装PyInstaller。在命令行中输入pip install pyinstaller然后回车。
# 使用cd命令切换到你的Python脚本所在的目录。例如，如果你的脚本在"C:\Users\YourName\Documents\MyScript.py"，你应该输入cd C:\Users\YourName\Documents\然后回车。
# 在命令行中输入pyinstaller --noconsole -F .\dicls-v5.py然后回车。这会告诉PyInstaller将你的脚本和所有的依赖项打包到一个单一的.exe文件中。
# 等待PyInstaller完成打包过程。这可能需要几分钟的时间，取决于你的脚本的大小和复杂性。
# 完成后，你会在当前目录下的"dist"文件夹中找到你的.exe文件。你可以直接运行这个文件，或者将它复制到其他地方。

README_TEXT = """
Welcome to the Glossary App!    ——240304

This app allows you to manage a glossary of terms. You can search, add, update, delete, import, and export terms easily.

How to use:
- Use the search bar to find a specific term.
- Add new terms using the 'Add' section.
- Update or delete terms by right-clicking on them.
- Import terms from an Excel file using the 'Import' button.
- Export terms to an Excel file using the 'Export' button.
"""

#####################################################################################
import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pandas as pd

try:
    import openpyxl
except ImportError:
    messagebox.showerror("Error", "The 'openpyxl' module is not installed. Please install it using 'pip install openpyxl'")

# 创建或加载术语表
try:
    with open('glossary.json', 'r') as f:
        glossary = json.load(f)
except FileNotFoundError:
    glossary = {
        "AI": {
            "full_form": "Artificial Intelligence",
            "explanation": "The simulation of human intelligence processes by machines, especially computer systems."
        }
        # 添加更多术语...
    }

# 对术语按字母顺序排序
glossary = dict(sorted(glossary.items(), key=lambda x: x[0]))

def search_term(event=None):  # 修改函数签名以接受事件参数，参数设置为None以确保不会影响直接调用
    search_query = entry_search.get().lower()
    matching_terms = []

    # 在这里创建 full_form 和 explanation 的 StringVar 实例
    full_form.set("")  # 清空之前的值
    explanation.set("")  # 清空之前的值
    
    # 在术语表中进行模糊搜索
    for term, data in glossary.items():
        full_form_term = data["full_form"].lower()
        explanation_term = data["explanation"].lower()
        
        if search_query in term.lower() or search_query in full_form_term or search_query in explanation_term:
            matching_terms.append(term)
    
    if matching_terms:
        result = glossary[matching_terms[0]]
        full_form.set(result["full_form"])
        explanation.set(result["explanation"])
    else:
        messagebox.showerror("Error", "Term not found")

def add_term(event=None):  # 修改函数签名以接受事件参数，参数设置为None以确保不会影响直接调用
    term = entry_add_term.get().upper()
    full = entry_add_full.get()
    expl = entry_add_expl.get()
    if term:
        glossary[term] = {"full_form": full, "explanation": expl}
        with open('glossary.json', 'w') as f:
            json.dump(glossary, f)
        messagebox.showinfo("Success", "Term added successfully")
        update_glossary_list()
    else:
        messagebox.showerror("Error", "Please fill in the term field")

def delete_term():
    selection = glossary_list.curselection()  # 获取当前选中的索引
    if selection:
        term = glossary_list.get(selection[0])  # 获取当前选中的术语
        if term in glossary:
            del glossary[term]
            with open('glossary.json', 'w') as f:
                json.dump(glossary, f)
            messagebox.showinfo("Success", "Term deleted successfully")
            update_glossary_list()
        else:
            messagebox.showerror("Error", "Term not found")

def update_term():
    selection = glossary_list.curselection()  # 获取当前选中的索引
    if selection:
        term = glossary_list.get(selection[0])  # 获取当前选中的术语
        if term in glossary:
            full = simpledialog.askstring("Update Term", "Enter the full form:", initialvalue=glossary[term]['full_form'])
            expl = simpledialog.askstring("Update Term", "Enter the explanation:", initialvalue=glossary[term]['explanation'])
            if full and expl:
                glossary[term] = {"full_form": full, "explanation": expl}
                with open('glossary.json', 'w') as f:
                    json.dump(glossary, f)
                messagebox.showinfo("Success", "Term updated successfully")
                update_glossary_list()
            else:
                messagebox.showerror("Error", "Please fill in all fields")
        else:
            messagebox.showerror("Error", "Term not found")

def update_glossary_list():
    glossary_list.delete(0, tk.END)
    for term, data in glossary.items():
        glossary_list.insert(tk.END, term)
    glossary_count.set(len(glossary))

def show_term(event):
    selection = glossary_list.curselection()
    if selection:
        term = glossary_list.get(selection[0])
        result = glossary[term]
        full_form.set(result["full_form"])
        explanation.set(result["explanation"])

def show_context_menu(event):
    global context_menu  # 将context_menu声明为全局变量
    selection = glossary_list.curselection()
    if selection:
        context_menu = tk.Menu(glossary_list, tearoff=0)
        context_menu.add_command(label="Update", command=update_term)
        context_menu.add_command(label="Delete", command=delete_term)
        context_menu.post(event.x_root, event.y_root)

def import_terms():
    file_path = filedialog.askopenfilename(filetypes=[('Excel Files', '*.xlsx')])

    if file_path:
        try:
            df = pd.read_excel(file_path)
            for index, row in df.iterrows():
                term = str(row['terms']).upper()
                full = str(row['full_form'])
                expl = str(row['explanation'])
                if term:
                    glossary[term] = {"full_form": full, "explanation": expl}
            with open('glossary.json', 'w') as f:
                json.dump(glossary, f)
            messagebox.showinfo("Success", "Terms imported successfully")
            update_glossary_list()
        except Exception as e:
            messagebox.showerror("Error", f"Error importing terms: {e}")

def export_terms():
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[('Excel Files', '*.xlsx')])

    if file_path:
        try:
            terms_data = {"terms": [], "full_form": [], "explanation": []}
            for term, data in glossary.items():
                terms_data["terms"].append(term)
                terms_data["full_form"].append(data["full_form"])
                terms_data["explanation"].append(data["explanation"])

            df = pd.DataFrame(terms_data)
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", "Terms exported successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting terms: {e}")

# 在函数中调用这个 README 文本的显示
def open_readme():
    messagebox.showinfo("Readme", README_TEXT)

#####################################################################################
# 创建根窗口
root = tk.Tk()
root.title("Glossary (v0.5) : " + str(len(glossary)) + " terms in glossary.json")  # 修改标题，添加术语计数

# 设置窗口大小
root.geometry("400x400")
root.resizable(False, False)

# 创建一个框架用于容纳术语列表和滚动条
glossary_frame = tk.Frame(root)
glossary_frame.place(x=5, y=10, width=100, height=380)

# Glossary模块
scrollbar = tk.Scrollbar(glossary_frame)  # 创建一个滚动条部件
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

glossary_list = tk.Listbox(glossary_frame, yscrollcommand=scrollbar.set)  # 创建一个列表框部件，显示术语列表
glossary_list.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=glossary_list.yview)  # 将滚动条与列表框关联，实现滚动功能

glossary_list.bind("<<ListboxSelect>>", show_term)  # 绑定列表框选中事件
glossary_list.bind("<Button-3>", show_context_menu)  # 绑定鼠标右键点击事件

# Search Term模块
search_frame = tk.Frame(root)  # 创建一个框架用于容纳搜索术语相关的部件
search_frame.place(x=115, y=10, width=280, height=60)

label_search = tk.Label(search_frame, text="Search Term")  # 创建一个标签用于显示文本
label_search.pack(side=tk.TOP)

entry_search = tk.Entry(search_frame)  # 创建一个文本输入框部件
entry_search.pack(side=tk.LEFT)

button_search = tk.Button(search_frame, text="Search", command=search_term)  # 创建一个按钮部件，并关联一个函数作为回调函数
button_search.pack()

entry_search.bind("<Return>", search_term)  # 在entry_search上绑定<Return>事件

# 显示内容
show_frame = tk.Frame(root)  # 创建一个框架用于容纳搜索术语相关的部件
show_frame.place(x=115, y=80, width=280, height=170)

full_form = tk.StringVar()
label_full_form = tk.Label(show_frame, textvariable=full_form, wraplength=280)  # 创建一个标签用于显示术语的全称，并设置换行宽度为200
label_full_form.pack()

explanation = tk.StringVar()
label_explanation = tk.Label(show_frame, textvariable=explanation, wraplength=280)  # 创建一个标签用于显示术语的解释
label_explanation.pack()

# Add New Term模块
add_frame = tk.Frame(root)  # 创建一个框架用于容纳搜索术语相关的部件
add_frame.place(x=115, y=260, width=200, height=130)

label_add = tk.Label(add_frame, text="Add New Term")  # 创建一个标签用于显示文本
label_add.pack(side=tk.TOP)

entry_add_term = tk.Entry(add_frame)  # 创建一个文本输入框部件
entry_add_term.pack()

entry_add_full = tk.Entry(add_frame)  # 创建一个文本输入框部件
entry_add_full.pack()

entry_add_expl = tk.Entry(add_frame)  # 创建一个文本输入框部件
entry_add_expl.pack()

button_add = tk.Button(add_frame, text="Add", command=add_term)  # 创建一个按钮部件，并关联一个函数作为回调函数
button_add.pack(side=tk.BOTTOM)

# 在entry_add_term上绑定<Return>事件
entry_add_term.bind("<Return>", lambda event: entry_add_full.focus_set())

# 在entry_add_full上绑定<Return>事件
entry_add_full.bind("<Return>", lambda event: entry_add_expl.focus_set())

# 在entry_add_expl上绑定<Return>事件
entry_add_expl.bind("<Return>", add_term)

# Import & Export Terms模块
data_frame = tk.Frame(root)
data_frame.place(x=325, y=280, width=60, height=110)

button_import = tk.Button(data_frame, text="Import", command=import_terms, width=10)
button_import.pack()

button_export = tk.Button(data_frame, text="Export", command=export_terms, width=10)
button_export.pack()

# README按钮
button_readme = tk.Button(data_frame, text="Readme", command=open_readme, width=10)
button_readme.pack()

glossary_count = tk.IntVar()
update_glossary_list()

root.mainloop()
