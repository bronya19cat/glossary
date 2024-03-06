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
    search_query = entry_search.get().lower()
    matching_terms = []
    
    # 在术语表中进行模糊搜索
    for term, data in glossary.items():
        full_form = data["full_form"].lower()
        explanation = data["explanation"].lower()
        
        if search_query in term.lower() or search_query in full_form or search_query in explanation:
            matching_terms.append(term)
    
    if matching_terms:
        result = glossary[matching_terms[0]]
        full_form.set(result["full_form"])
        explanation.set(result["explanation"])
    else:
        messagebox.showerror("Error", "Term not found")

def add_term():
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

def delete_term(event):
    term = glossary_list.get(glossary_list.curselection())
    if term in glossary:
        del glossary[term]
        with open('glossary.json', 'w') as f:
            json.dump(glossary, f)
        messagebox.showinfo("Success", "Term deleted successfully")
        update_glossary_list()

def update_term(event):
    term = glossary_list.get(glossary_list.curselection())
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
    selection = glossary_list.curselection()
    if selection:
        menu = tk.Menu(glossary_list, tearoff=0)
        menu.add_command(label="Update Term", command=update_term)
        menu.add_command(label="Delete Term", command=delete_term)
        menu.post(event.x_root, event.y_root)

# 创建根窗口
root = tk.Tk()
root.title("English Terms Glossary (v0.2) : " + str(len(glossary)))  # 修改标题，添加术语计数

# 设置窗口大小
root.geometry("600x400")
root.resizable(False, False)

# Glossary模块
glossary_frame = tk.Frame(root)  # 创建一个框架用于容纳术语列表和滚动条
glossary_frame.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar = tk.Scrollbar(glossary_frame)  # 创建一个滚动条部件
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

glossary_list = tk.Listbox(glossary_frame, yscrollcommand=scrollbar.set)  # 创建一个列表框部件，显示术语列表
glossary_list.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=glossary_list.yview)  # 将滚动条与列表框关联，实现滚动功能

glossary_list.bind("<<ListboxSelect>>", show_term)  # 绑定列表框选中事件
glossary_list.bind("<Button-3>", show_context_menu)  # 绑定鼠标右键点击事件

# Search Term模块
search_frame = tk.Frame(root)  # 创建一个框架用于容纳搜索术语相关的部件
search_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

label_search = tk.Label(search_frame, text="Search Term")  # 创建一个标签用于显示文本
label_search.pack()

entry_search = tk.Entry(search_frame)  # 创建一个文本输入框部件
entry_search.pack()

button_search = tk.Button(search_frame, text="Search", command=search_term)  # 创建一个按钮部件，并关联一个函数作为回调函数
button_search.pack()

# 显示内容
full_form = tk.StringVar()
label_full_form = tk.Label(search_frame, textvariable=full_form)  # 创建一个标签用于显示术语的全称
label_full_form.pack()

explanation = tk.StringVar()
label_explanation = tk.Label(search_frame, textvariable=explanation)  # 创建一个标签用于显示术语的解释
label_explanation.pack()

# Add New Term模块
add_frame = tk.Frame(root)  # 创建一个框架用于容纳添加新术语相关的部件
add_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

label_add = tk.Label(add_frame, text="Add New Term")  # 创建一个标签用于显示文本
label_add.pack()

entry_add_term = tk.Entry(add_frame)  # 创建一个文本输入框部件
entry_add_term.pack()

entry_add_full = tk.Entry(add_frame)  # 创建一个文本输入框部件
entry_add_full.pack()

entry_add_expl = tk.Entry(add_frame)  # 创建一个文本输入框部件
entry_add_expl.pack()

button_add = tk.Button(add_frame, text="Add", command=add_term)  # 创建一个按钮部件，并关联一个函数作为回调函数
button_add.pack()

glossary_list.bind("<<ListboxSelect>>", show_term)  # 绑定列表框选中事件

glossary_count = tk.IntVar()
label_glossary_count = tk.Label(root, textvariable=glossary_count)
label_glossary_count.pack(side=tk.LEFT)

update_glossary_list()
glossary_count.set(len(glossary))

root.mainloop()
