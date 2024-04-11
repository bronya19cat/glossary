# 定义全局变量来跟踪当前匹配项的索引
current_match_index = -1

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