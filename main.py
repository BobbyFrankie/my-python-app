import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import hashlib
import os
import time
import threading
from datetime import datetime

class MD5Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("文件哈希计算器")
        self.root.geometry("600x800")
        self.root.minsize(500, 400)
  
        # 设置主题样式
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", background="#ccc")
        self.style.configure("Title.TLabel", font=("Arial", 12, "bold"))
        self.style.configure("Result.TLabel", font=("Consolas", 10))
  
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
  
        # 标题
        title_label = ttk.Label(self.main_frame, text="文件哈希计算器", style="Title.TLabel")
        title_label.pack(pady=(0, 15))
  
        # 创建选项卡
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)
  
        # 文件哈希计算选项卡
        self.file_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.file_tab, text="文件哈希")
  
        # 文本哈希计算选项卡
        self.text_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.text_tab, text="文本哈希")
  
        # 批量计算选项卡
        self.batch_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.batch_tab, text="批量计算")
  
        self.setup_file_tab()
        self.setup_text_tab()
        self.setup_batch_tab()
  
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
  
        # 绑定拖放事件
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)
  
        # 当前计算的文件
        self.current_file = None
  
    def setup_file_tab(self):
        # 算法选择
        algo_frame = ttk.Frame(self.file_tab)
        algo_frame.pack(fill=tk.X, pady=5)
  
        ttk.Label(algo_frame, text="哈希算法:").pack(side=tk.LEFT, padx=(0, 10))
        self.algo_var = tk.StringVar(value="MD5")
        algo_combo = ttk.Combobox(algo_frame, textvariable=self.algo_var,
                                  values=["MD5", "SHA-1", "SHA-256", "SHA-512"], state="readonly")
        algo_combo.pack(side=tk.LEFT)
  
        # 拖放区域
        drop_frame = ttk.LabelFrame(self.file_tab, text="拖放文件到这里", padding="20")
        drop_frame.pack(fill=tk.BOTH, expand=True, pady=10)
  
        self.drop_label = ttk.Label(drop_frame, text="将文件拖拽到此处\n或点击下方按钮选择文件",
                                    justify=tk.CENTER)
        self.drop_label.pack(expand=True)
  
        # 按钮框架
        button_frame = ttk.Frame(self.file_tab)
        button_frame.pack(fill=tk.X, pady=10)
  
        ttk.Button(button_frame, text="选择文件", command=self.open_file_dialog).pack(side=tk.LEFT, padx=5)
        self.copy_button = ttk.Button(button_frame, text="复制哈希值", command=self.copy_hash, state=tk.DISABLED)
        self.copy_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清空结果", command=self.clear_result).pack(side=tk.LEFT, padx=5)
  
        # 结果显示
        result_frame = ttk.LabelFrame(self.file_tab, text="计算结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
  
        self.result_text = tk.Text(result_frame, height=8, wrap=tk.WORD, font=("Consolas", 9))
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
         
        # 比对信息
        compare_frame = ttk.LabelFrame(self.file_tab, text="哈希比对", padding="10")
        compare_frame.pack(fill=tk.X, pady=5)
         
        # 创建一个框架来容纳输入框和结果
        compare_content_frame = ttk.Frame(compare_frame)
        compare_content_frame.pack(fill=tk.X, expand=True)
         
        # 比对输入框 - 自适应大小
        self.compare_var = tk.StringVar(value="请输入哈希值，哈希值将与计算结果比对。")
        self.compare_entry = ttk.Entry(compare_content_frame, textvariable=self.compare_var)
        self.compare_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
         
        # 绑定事件
        self.compare_entry.bind("<FocusIn>", self._on_compare_focus_in)
        self.compare_entry.bind("<FocusOut>", self._on_compare_focus_out)
        self.compare_entry.bind("<KeyRelease>", self._compare_hash)
         
        # 结果显示 - 图片和文本
        self.compare_result_frame = ttk.Frame(compare_content_frame)
        self.compare_result_frame.pack(side=tk.LEFT, padx=5, fill=tk.Y)
         
        # 结果图片标签
        self.compare_image_label = ttk.Label(self.compare_result_frame)
        self.compare_image_label.pack(side=tk.LEFT, padx=2)
         
        # 结果文本标签
        self.compare_text_label = ttk.Label(self.compare_result_frame, text="")
        self.compare_text_label.pack(side=tk.LEFT, padx=2)
         
        # 加载图片
        self.correct_image = tk.PhotoImage(file="icons/correct.png")
        self.error_image = tk.PhotoImage(file="icons/error.png")
 
        # 文件信息
        self.info_frame = ttk.Frame(self.file_tab)
        self.info_frame.pack(fill=tk.X, pady=5)
  
        self.info_label = ttk.Label(self.info_frame, text="", style="Result.TLabel")
        self.info_label.pack(anchor=tk.W)
  
    def setup_text_tab(self):
        # 文本输入
        input_frame = ttk.LabelFrame(self.text_tab, text="输入文本", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=5)
  
        self.text_input = tk.Text(input_frame, height=8, wrap=tk.WORD)
        self.text_input.pack(fill=tk.BOTH, expand=True)
  
        # 按钮和算法选择
        control_frame = ttk.Frame(self.text_tab)
        control_frame.pack(fill=tk.X, pady=10)
  
        ttk.Label(control_frame, text="算法:").pack(side=tk.LEFT, padx=(0, 10))
        self.text_algo_var = tk.StringVar(value="MD5")
        text_algo_combo = ttk.Combobox(control_frame, textvariable=self.text_algo_var,
                                       values=["MD5", "SHA-1", "SHA-256", "SHA-512"], state="readonly")
        text_algo_combo.pack(side=tk.LEFT, padx=(0, 20))
  
        ttk.Button(control_frame, text="计算哈希", command=self.calculate_text_hash).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="复制结果", command=self.copy_text_hash).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="清空", command=self.clear_text).pack(side=tk.LEFT, padx=5)
  
        # 结果显示
        text_result_frame = ttk.LabelFrame(self.text_tab, text="哈希结果", padding="10")
        text_result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
  
        self.text_result = tk.Text(text_result_frame, height=4, wrap=tk.WORD, font=("Consolas", 10))
        self.text_result.pack(fill=tk.BOTH, expand=True)
  
    def setup_batch_tab(self):
        # 文件列表
        list_frame = ttk.LabelFrame(self.batch_tab, text="文件列表", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
  
        # 列表和滚动条
        list_control_frame = ttk.Frame(list_frame)
        list_control_frame.pack(fill=tk.X, pady=(0, 5))
  
        ttk.Button(list_control_frame, text="添加文件", command=self.add_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(list_control_frame, text="添加文件夹", command=self.add_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(list_control_frame, text="清空列表", command=self.clear_list).pack(side=tk.LEFT, padx=5)
  
        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED)
        list_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=list_scrollbar.set)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
  
        # 算法选择和计算按钮
        batch_control_frame = ttk.Frame(self.batch_tab)
        batch_control_frame.pack(fill=tk.X, pady=10)
  
        ttk.Label(batch_control_frame, text="算法:").pack(side=tk.LEFT, padx=(0, 10))
        self.batch_algo_var = tk.StringVar(value="MD5")
        batch_algo_combo = ttk.Combobox(batch_control_frame, textvariable=self.batch_algo_var,
                                        values=["MD5", "SHA-1", "SHA-256", "SHA-512"], state="readonly")
        batch_algo_combo.pack(side=tk.LEFT, padx=(0, 20))
  
        ttk.Button(batch_control_frame, text="开始计算", command=self.start_batch_calculation).pack(side=tk.LEFT,
                                                                                                    padx=5)
        ttk.Button(batch_control_frame, text="导出结果", command=self.export_results).pack(side=tk.LEFT, padx=5)
  
        # 批量计算结果
        batch_result_frame = ttk.LabelFrame(self.batch_tab, text="批量计算结果", padding="10")
        batch_result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
  
        self.batch_result = tk.Text(batch_result_frame, height=6, wrap=tk.WORD, font=("Consolas", 9))
        batch_scrollbar = ttk.Scrollbar(batch_result_frame, orient=tk.VERTICAL, command=self.batch_result.yview)
        self.batch_result.configure(yscrollcommand=batch_scrollbar.set)
        self.batch_result.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        batch_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
  
    def calculate_hash(self, file_path, algorithm="MD5"):
        """计算文件的哈希值"""
        # 算法名称映射，处理带连字符的算法名
        algo_map = {
            "sha-1": "sha1",
            "sha-256": "sha256",
            "sha-512": "sha512"
        }
        algo_name = algorithm.lower()
        # 如果算法名在映射中存在，则使用映射后的值
        if algo_name in algo_map:
            algo_name = algo_map[algo_name]
        hash_func = getattr(hashlib, algo_name)()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception as e:
            return f"错误: {str(e)}"
  
    def calculate_text_hash(self):
        """计算文本的哈希值"""
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("警告", "请输入要计算哈希的文本")
            return
 
        algorithm = self.text_algo_var.get()
        # 算法名称映射，处理带连字符的算法名
        algo_map = {
            "sha-1": "sha1",
            "sha-256": "sha256",
            "sha-512": "sha512"
        }
        algo_name = algorithm.lower()
        # 如果算法名在映射中存在，则使用映射后的值
        if algo_name in algo_map:
            algo_name = algo_map[algo_name]
        hash_func = getattr(hashlib, algo_name)()
        hash_func.update(text.encode('utf-8'))
        result = hash_func.hexdigest()
  
        self.text_result.delete("1.0", tk.END)
        self.text_result.insert("1.0", f"{algorithm} 哈希: {result}")
  
    def on_drop(self, event):
        """处理文件拖放事件"""
        file_path = event.data.strip('{}')
        self.process_file(file_path)
  
    def open_file_dialog(self):
        """打开文件选择对话框"""
        file_path = filedialog.askopenfilename()
        if file_path:
            self.process_file(file_path)
  
    def process_file(self, file_path):
        """处理单个文件并计算哈希"""
        self.current_file = file_path
        self.status_var.set(f"正在计算 {os.path.basename(file_path)} 的哈希值...")
  
        # 在单独的线程中计算哈希，避免界面冻结
        thread = threading.Thread(target=self._calculate_and_display, args=(file_path,))
        thread.daemon = True
        thread.start()
  
    def _calculate_and_display(self, file_path):
        """在后台线程中计算并显示结果"""
        algorithm = self.algo_var.get()
        hash_value = self.calculate_hash(file_path, algorithm)
  
        # 获取文件信息
        file_size = os.path.getsize(file_path)
        mod_time = os.path.getmtime(file_path)
        mod_time_str = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M:%S")
  
        # 在主线程中更新UI
        self.root.after(0, self._update_display, file_path, hash_value, algorithm, file_size, mod_time_str)
  
    def _update_display(self, file_path, hash_value, algorithm, file_size, mod_time):
        """更新显示结果"""
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", f"文件: {file_path}\n")
        self.result_text.insert(tk.END, f"{algorithm} 哈希: {hash_value}\n")
         
        # 保存当前计算的哈希值，用于比对
        self.current_hash_value = hash_value.lower()
 
        self.info_label.config(text=f"大小: {self.format_file_size(file_size)} | 修改时间: {mod_time}")
 
        self.copy_button.config(state=tk.NORMAL)
        self.status_var.set(f"已完成 {os.path.basename(file_path)} 的哈希计算")
         
        # 如果比对输入框不为空且不是提示文本，则进行比对
        if self.compare_var.get().strip() and self.compare_var.get() != "请输入哈希值，哈希值将与计算结果比对。":
            self._compare_hash(None)
  
    def format_file_size(self, size):
        """格式化文件大小显示"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"
  
    def copy_hash(self):
        """复制哈希值到剪贴板"""
        result = self.result_text.get("1.0", tk.END).strip()
        if "哈希:" in result:
            lines = result.split("\n")
            for line in lines:
                if "哈希:" in line:
                    hash_value = line.split("哈希:")[1].strip()
                    self.root.clipboard_clear()
                    self.root.clipboard_append(hash_value)
                    messagebox.showinfo("成功", "哈希值已复制到剪贴板！")
                    break
  
    def copy_text_hash(self):
        """复制文本哈希值到剪贴板"""
        result = self.text_result.get("1.0", tk.END).strip()
        if "哈希:" in result:
            hash_value = result.split("哈希:")[1].strip()
            self.root.clipboard_clear()
            self.root.clipboard_append(hash_value)
            messagebox.showinfo("成功", "哈希值已复制到剪贴板！")
  
    def clear_result(self):
        """清空文件哈希结果"""
        self.result_text.delete("1.0", tk.END)
        self.info_label.config(text="")
        self.copy_button.config(state=tk.DISABLED)
        self.current_file = None
        self.current_hash_value = None
        # 重置比对输入框
        self.compare_var.set("请输入哈希值，哈希值将与计算结果比对。")
        self.compare_image_label.config(image="")
        self.compare_text_label.config(text="")
         
    def _on_compare_focus_in(self, event):
        """当比对输入框获得焦点时"""
        if self.compare_var.get() == "请输入哈希值，哈希值将与计算结果比对。":
            self.compare_var.set("")
            # 清空图片和文本
            self.compare_image_label.config(image="")
            self.compare_text_label.config(text="")
     
    def _on_compare_focus_out(self, event):
        """当比对输入框失去焦点时"""
        if not self.compare_var.get().strip():
            self.compare_var.set("请输入哈希值，哈希值将与计算结果比对。")
            # 清空图片和文本
            self.compare_image_label.config(image="")
            self.compare_text_label.config(text="")
     
    def _compare_hash(self, event):
        """比对输入的哈希值与计算结果"""
        # 如果没有当前计算的哈希值或输入框为空或为提示文本，则不进行比对
        if not hasattr(self, 'current_hash_value') or not self.current_hash_value:
            self.compare_image_label.config(image="")
            self.compare_text_label.config(text="")
            return
         
        # 获取输入并去除所有空格
        input_text = self.compare_var.get().strip().lower()
        if not input_text or input_text == "请输入哈希值，哈希值将与计算结果比对。":
            self.compare_image_label.config(image="")
            self.compare_text_label.config(text="")
            return
         
        # 去除所有空格（包括中间的空格）
        input_hash = input_text.replace(" ", "")
         
        # 比对哈希值
        if input_hash == self.current_hash_value:
            self.compare_image_label.config(image=self.correct_image)
            self.compare_text_label.config(text="哈希值匹配")
        else:
            self.compare_image_label.config(image=self.error_image)
            self.compare_text_label.config(text="哈希值不匹配")
  
    def clear_text(self):
        """清空文本输入和结果"""
        self.text_input.delete("1.0", tk.END)
        self.text_result.delete("1.0", tk.END)
  
    def add_files(self):
        """添加文件到批量计算列表"""
        files = filedialog.askopenfilenames()
        for file in files:
            self.file_listbox.insert(tk.END, file)
  
    def add_folder(self):
        """添加文件夹中的所有文件到批量计算列表"""
        folder = filedialog.askdirectory()
        if folder:
            for root_dir, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root_dir, file)
                    self.file_listbox.insert(tk.END, file_path)
  
    def clear_list(self):
        """清空文件列表"""
        self.file_listbox.delete(0, tk.END)
  
    def start_batch_calculation(self):
        """开始批量计算"""
        if self.file_listbox.size() == 0:
            messagebox.showwarning("警告", "请先添加要计算的文件")
            return
  
        self.batch_result.delete("1.0", tk.END)
        self.status_var.set("正在进行批量计算...")
  
        # 在后台线程中进行批量计算
        thread = threading.Thread(target=self._batch_calculate)
        thread.daemon = True
        thread.start()
  
    def _batch_calculate(self):
        """在后台线程中进行批量计算"""
        algorithm = self.batch_algo_var.get()
        results = []
  
        for i in range(self.file_listbox.size()):
            file_path = self.file_listbox.get(i)
            file_name = os.path.basename(file_path)
  
            # 更新状态
            self.root.after(0, lambda: self.status_var.set(f"正在计算: {file_name}"))
  
            # 计算哈希
            hash_value = self.calculate_hash(file_path, algorithm)
            results.append(f"{file_name}\t{hash_value}\n")
  
            # 更新结果显示
            self.root.after(0, self._update_batch_result, file_name, hash_value, algorithm)
  
        # 计算完成
        self.root.after(0, lambda: self.status_var.set(f"批量计算完成，共计算了 {len(results)} 个文件"))
  
    def _update_batch_result(self, file_name, hash_value, algorithm):
        """更新批量计算结果显示"""
        self.batch_result.insert(tk.END, f"{file_name}\n")
        self.batch_result.insert(tk.END, f"  {algorithm}: {hash_value}\n\n")
        self.batch_result.see(tk.END)
  
    def export_results(self):
        """导出批量计算结果到文件"""
        if not self.batch_result.get("1.0", tk.END).strip():
            messagebox.showwarning("警告", "没有可导出的结果")
            return
  
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
  
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.batch_result.get("1.0", tk.END))
                messagebox.showinfo("成功", f"结果已导出到: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {str(e)}")
  
  
def main():
    root = TkinterDnD.Tk()
    app = MD5Calculator(root)
    root.mainloop()
  
  
if __name__ == "__main__":
    main()
