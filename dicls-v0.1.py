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
        update_glossary_list()
    else:
        messagebox.showerror("Error", "Please fill in all fields")

def delete_term():
    term = simpledialog.askstring("Delete Term", "Enter the term to delete:")
    if term in glossary:
        del glossary[term]
        with open('glossary.json', 'w') as f:
            json.dump(glossary, f)
        messagebox.showinfo("Success", "Term deleted successfully")
        update_glossary_list()
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

# GUI 设置
root = tk.Tk()
root.title("English Terms Glossary (v0.1)")

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

# 术语列表
label_glossary = tk.Label(root, text="Glossary")
label_glossary.pack()

glossary_frame = tk.Frame(root)
glossary_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

scrollbar = tk.Scrollbar(glossary_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

glossary_list = tk.Listbox(glossary_frame, yscrollcommand=scrollbar.set)
glossary_list.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=glossary_list.yview)

glossary_list.bind("<<ListboxSelect>>", show_term)

glossary_count = tk.IntVar()
label_glossary_count = tk.Label(root, textvariable=glossary_count)
label_glossary_count.pack()

update_glossary_list()

root.mainloop()
