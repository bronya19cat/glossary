# 首先安装tkinter库。

# 下面是一个更详细的步骤，说明如何使用PyInstaller将Python脚本（和它的依赖项）打包到一个.exe文件中：

# 打开命令提示符(cmd)或终端。

# 安装PyInstaller。在命令行中输入pip install pyinstaller然后回车。

# 使用cd命令切换到你的Python脚本所在的目录。例如，如果你的脚本在"C:\Users\YourName\Documents\MyScript.py"，你应该输入cd C:\Users\YourName\Documents\然后回车。

# 在命令行中输入pyinstaller --onefile MyScript.py然后回车。这会告诉PyInstaller将你的脚本和所有的依赖项打包到一个单一的.exe文件中。
# pyinstaller --noconsole -F .\dicls.py
# 等待PyInstaller完成打包过程。这可能需要几分钟的时间，取决于你的脚本的大小和复杂性。

# 完成后，你会在当前目录下的"dist"文件夹中找到你的.exe文件。你可以直接运行这个文件，或者将它复制到其他地方。

import json
import tkinter as tk
from tkinter import messagebox, simpledialog

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

def search_term():
    term = entry_search.get().upper()
    if term in glossary:
        result = glossary[term]
        full_form.set(result["full_form"])
        explanation.set(result["explanation"])
    else:
        messagebox.showerror("Error", "Term not found")

def add_term():
    term = entry_add_term.get().upper()
    full = entry_add_full.get()
    expl = entry_add_expl.get()
    if term and full and expl:
        glossary[term] = {"full_form": full, "explanation": expl}
        with open('glossary.json', 'w') as f:
            json.dump(glossary, f)
        messagebox.showinfo("Success", "Term added successfully")
    else:
        messagebox.showerror("Error", "Please fill in all fields")

def delete_term():
    term = simpledialog.askstring("Delete Term", "Enter the term to delete:")
    if term in glossary:
        del glossary[term]
        with open('glossary.json', 'w') as f:
            json.dump(glossary, f)
        messagebox.showinfo("Success", "Term deleted successfully")
    else:
        messagebox.showerror("Error", "Term not found")

def update_term():
    term = simpledialog.askstring("Update Term", "Enter the term to update:")
    if term in glossary:
        full = simpledialog.askstring("Update Term", "Enter the full form:")
        expl = simpledialog.askstring("Update Term", "Enter the explanation:")
        if full and expl:
            glossary[term] = {"full_form": full, "explanation": expl}
            with open('glossary.json', 'w') as f:
                json.dump(glossary, f)
            messagebox.showinfo("Success", "Term updated successfully")
        else:
            messagebox.showerror("Error", "Please fill in all fields")
    else:
        messagebox.showerror("Error", "Term not found")

# GUI 设置
root = tk.Tk()
root.title("English Terms Glossary (v0.0)")

# 搜索区域
label_search = tk.Label(root, text="Search Term")
label_search.pack()

entry_search = tk.Entry(root)
entry_search.pack()

button_search = tk.Button(root, text="Search", command=search_term)
button_search.pack()

full_form = tk.StringVar()
label_full_form = tk.Label(root, textvariable=full_form)
label_full_form.pack()

explanation = tk.StringVar()
label_explanation = tk.Label(root, textvariable=explanation)
label_explanation.pack()

# 添加新术语区域
label_add = tk.Label(root, text="Add New Term")
label_add.pack()

entry_add_term = tk.Entry(root)
entry_add_term.pack()

entry_add_full = tk.Entry(root)
entry_add_full.pack()

entry_add_expl = tk.Entry(root)
entry_add_expl.pack()

button_add = tk.Button(root, text="Add", command=add_term)
button_add.pack()

# 删除和更新按钮
button_delete = tk.Button(root, text="Delete Term", command=delete_term)
button_delete.pack()

button_update = tk.Button(root, text="Update Term", command=update_term)
button_update.pack()

root.mainloop()
