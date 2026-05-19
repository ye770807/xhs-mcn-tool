import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime
from tkcalendar import DateEntry
import time


class XHSQueryTool:
    def __init__(self, root):
        self.root = root
        self.root.title("小红书MCN博主邀约工具")
        self.root.geometry("1200x900")
        self.root.minsize(1100, 800)
        self.root.configure(bg='#f5f5f7')
        
        # 存储查询到的用户信息
        self.current_user_id = None
        
        # 配色方案
        self.colors = {
            'bg': '#f5f5f7',
            'card_bg': '#ffffff',
            'primary': '#ff2442',  # 小红书红
            'primary_hover': '#e0203c',
            'secondary': '#6c757d',
            'success': '#28a745',
            'text': '#1d1d1f',
            'text_secondary': '#86868b',
            'border': '#d2d2d7',
            'input_bg': '#fbfbfd'
        }
        
        self.create_widgets()
    
    def create_widgets(self):
        # 主容器
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # ===== 头部区域 =====
        header_frame = tk.Frame(main_container, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Logo和标题
        title_container = tk.Frame(header_frame, bg=self.colors['bg'])
        title_container.pack(side=tk.LEFT)
        
        # 小红书风格Logo
        logo_frame = tk.Frame(title_container, bg=self.colors['primary'], width=40, height=40)
        logo_frame.pack(side=tk.LEFT, padx=(0, 15))
        logo_frame.pack_propagate(False)
        
        logo_label = tk.Label(logo_frame, text="红", font=('微软雅黑', 18, 'bold'), 
                              bg=self.colors['primary'], fg='white')
        logo_label.place(relx=0.5, rely=0.5, anchor='center')
        
        title_label = tk.Label(title_container, text="小红书MCN博主邀约工具", 
                               font=('微软雅黑', 22, 'bold'), bg=self.colors['bg'], 
                               fg=self.colors['text'])
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(header_frame, text="专业版 v2.0", 
                                  font=('微软雅黑', 11), bg=self.colors['bg'], 
                                  fg=self.colors['text_secondary'])
        subtitle_label.pack(side=tk.RIGHT, pady=(10, 0))
        
        # ===== 内容区域（左右分栏） =====
        content_frame = tk.Frame(main_container, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        content_frame.columnconfigure(0, weight=3)
        content_frame.columnconfigure(1, weight=2)
        content_frame.rowconfigure(0, weight=1)
        
        # ===== 左侧区域 =====
        left_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        # 查询卡片
        query_card = self.create_card(left_frame, "博主信息查询")
        query_card.pack(fill=tk.X, pady=(0, 15))
        
        # ID输入区域
        input_frame = tk.Frame(query_card, bg=self.colors['card_bg'])
        input_frame.pack(fill=tk.X, padx=20, pady=15)
        
        id_label = tk.Label(input_frame, text="博主ID", font=('微软雅黑', 12, 'bold'),
                           bg=self.colors['card_bg'], fg=self.colors['text'])
        id_label.pack(anchor=tk.W, pady=(0, 8))
        
        id_input_frame = tk.Frame(input_frame, bg=self.colors['card_bg'])
        id_input_frame.pack(fill=tk.X)
        
        self.id_entry = tk.Entry(id_input_frame, font=('微软雅黑', 13), 
                                 bg=self.colors['input_bg'], fg=self.colors['text'],
                                 relief=tk.FLAT, bd=10, highlightthickness=1,
                                 highlightbackground=self.colors['border'],
                                 highlightcolor=self.colors['primary'])
        self.id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.add_context_menu(self.id_entry)
        
        self.query_btn = tk.Button(id_input_frame, text="获取", font=('微软雅黑', 12, 'bold'),
                                   bg=self.colors['primary'], fg='white',
                                   relief=tk.FLAT, bd=0, padx=25, pady=8,
                                   cursor='hand2', command=self.query_user,
                                   activebackground=self.colors['primary_hover'],
                                   activeforeground='white')
        self.query_btn.pack(side=tk.RIGHT)
        
        # 查询结果卡片
        result_card = self.create_card(left_frame, "查询结果")
        result_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 结果文本区域
        result_container = tk.Frame(result_card, bg=self.colors['card_bg'])
        result_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        self.result_text = tk.Text(result_container, font=('微软雅黑', 12), 
                                   wrap=tk.WORD, state=tk.DISABLED, height=6,
                                   bg=self.colors['input_bg'], fg=self.colors['text'],
                                   relief=tk.FLAT, padx=10, pady=10,
                                   highlightthickness=1,
                                   highlightbackground=self.colors['border'])
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.add_context_menu(self.result_text)
        
        result_scrollbar = tk.Scrollbar(result_container, command=self.result_text.yview,
                                        bg=self.colors['border'], troughcolor=self.colors['card_bg'],
                                        relief=tk.FLAT)
        result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=result_scrollbar.set)
        
        # 使用说明卡片
        help_card = self.create_card(left_frame, "使用说明")
        help_card.pack(fill=tk.X)
        
        help_content = tk.Frame(help_card, bg=self.colors['card_bg'])
        help_content.pack(fill=tk.X, padx=20, pady=15)
        
        steps = [
            ("1", "填写博主ID、姓名、电话等信息"),
            ("2", "点击「获取」按钮获取博主信息"),
            ("3", "设置挂靠时间后点击「挂靠」按钮")
        ]
        
        for num, text in steps:
            step_frame = tk.Frame(help_content, bg=self.colors['card_bg'])
            step_frame.pack(fill=tk.X, pady=5)
            
            num_label = tk.Label(step_frame, text=num, font=('微软雅黑', 11, 'bold'),
                                bg=self.colors['primary'], fg='white',
                                width=2, height=1)
            num_label.pack(side=tk.LEFT, padx=(0, 12))
            
            text_label = tk.Label(step_frame, text=text, font=('微软雅黑', 11),
                                 bg=self.colors['card_bg'], fg=self.colors['text_secondary'])
            text_label.pack(side=tk.LEFT)
        
        # ===== 右侧区域 =====
        right_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        right_frame.grid(row=0, column=1, sticky="nsew")
        
        # UID列表卡片
        uid_card = self.create_card(right_frame, "UID列表")
        uid_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        uid_container = tk.Frame(uid_card, bg=self.colors['card_bg'])
        uid_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        self.uid_text = tk.Text(uid_container, font=('微软雅黑', 14), 
                                wrap=tk.WORD, bg=self.colors['input_bg'], height=6,
                                fg=self.colors['text'], relief=tk.FLAT,
                                padx=10, pady=10, highlightthickness=1,
                                highlightbackground=self.colors['border'])
        self.uid_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.add_context_menu(self.uid_text)
        
        uid_scrollbar = tk.Scrollbar(uid_container, command=self.uid_text.yview,
                                     bg=self.colors['border'], troughcolor=self.colors['card_bg'],
                                     relief=tk.FLAT)
        uid_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.uid_text.config(yscrollcommand=uid_scrollbar.set)
        
        # UID按钮
        uid_btn_frame = tk.Frame(uid_card, bg=self.colors['card_bg'])
        uid_btn_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self.clear_uid_btn = tk.Button(uid_btn_frame, text="清空列表", 
                                       font=('微软雅黑', 11), bg=self.colors['secondary'],
                                       fg='white', relief=tk.FLAT, bd=0, padx=20, pady=8,
                                       cursor='hand2', command=self.clear_uid_list,
                                       activebackground='#5a6268')
        self.clear_uid_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.copy_uid_btn = tk.Button(uid_btn_frame, text="复制全部", 
                                      font=('微软雅黑', 11), bg=self.colors['success'],
                                      fg='white', relief=tk.FLAT, bd=0, padx=20, pady=8,
                                      cursor='hand2', command=self.copy_uid_list,
                                      activebackground='#218838')
        self.copy_uid_btn.pack(side=tk.LEFT)
        
        # 挂靠信息卡片
        attach_card = self.create_card(right_frame, "挂靠信息")
        attach_card.pack(fill=tk.X)
        
        attach_content = tk.Frame(attach_card, bg=self.colors['card_bg'])
        attach_content.pack(fill=tk.X, padx=20, pady=15)
        
        # 姓名
        name_frame = tk.Frame(attach_content, bg=self.colors['card_bg'])
        name_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(name_frame, text="姓名", font=('微软雅黑', 11, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 6))
        
        self.name_entry = tk.Entry(name_frame, font=('微软雅黑', 12),
                                   bg=self.colors['input_bg'], fg=self.colors['text'],
                                   relief=tk.FLAT, bd=8, highlightthickness=1,
                                   highlightbackground=self.colors['border'],
                                   highlightcolor=self.colors['primary'])
        self.name_entry.pack(fill=tk.X)
        self.add_context_menu(self.name_entry)
        
        # 电话
        phone_frame = tk.Frame(attach_content, bg=self.colors['card_bg'])
        phone_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(phone_frame, text="电话", font=('微软雅黑', 11, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 6))
        
        phone_input_frame = tk.Frame(phone_frame, bg=self.colors['card_bg'])
        phone_input_frame.pack(fill=tk.X)
        
        self.area_code_var = tk.StringVar(value="+86")
        area_codes = ["+86", "+852", "+853", "+886", "+1", "+44", "+81", "+82", "+65", "+61"]
        self.area_code_combo = ttk.Combobox(phone_input_frame, textvariable=self.area_code_var,
                                            values=area_codes, width=6, font=('微软雅黑', 11),
                                            state='readonly')
        self.area_code_combo.pack(side=tk.LEFT, padx=(0, 8))
        
        self.phone_entry = tk.Entry(phone_input_frame, font=('微软雅黑', 12),
                                    bg=self.colors['input_bg'], fg=self.colors['text'],
                                    relief=tk.FLAT, bd=8, highlightthickness=1,
                                    highlightbackground=self.colors['border'],
                                    highlightcolor=self.colors['primary'])
        self.phone_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.add_context_menu(self.phone_entry)
        
        # 时间选择
        time_frame = tk.Frame(attach_content, bg=self.colors['card_bg'])
        time_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(time_frame, text="挂靠时间", font=('微软雅黑', 11, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 6))
        
        time_input_frame = tk.Frame(time_frame, bg=self.colors['card_bg'])
        time_input_frame.pack(fill=tk.X)
        
        tk.Label(time_input_frame, text="开始", font=('微软雅黑', 10),
                bg=self.colors['card_bg'], fg=self.colors['text_secondary']).pack(side=tk.LEFT)
        
        self.start_date = DateEntry(time_input_frame, width=12, font=('微软雅黑', 11),
                                    date_pattern='yyyy-mm-dd', locale='zh_CN',
                                    relief=tk.FLAT, borderwidth=1)
        self.start_date.pack(side=tk.LEFT, padx=(5, 15))
        
        tk.Label(time_input_frame, text="结束", font=('微软雅黑', 10),
                bg=self.colors['card_bg'], fg=self.colors['text_secondary']).pack(side=tk.LEFT)
        
        self.end_date = DateEntry(time_input_frame, width=12, font=('微软雅黑', 11),
                                  date_pattern='yyyy-mm-dd', locale='zh_CN',
                                  relief=tk.FLAT, borderwidth=1)
        self.end_date.pack(side=tk.LEFT, padx=5)
        self.end_date.set_date(datetime(2028, 5, 15))
        
        # ===== 底部操作栏 =====
        bottom_frame = tk.Frame(main_container, bg=self.colors['bg'])
        bottom_frame.pack(fill=tk.X, pady=(20, 0))
        
        # 状态显示
        self.status_frame = tk.Frame(bottom_frame, bg=self.colors['card_bg'],
                                     highlightthickness=1, highlightbackground=self.colors['border'])
        self.status_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        
        self.status_label = tk.Label(self.status_frame, text="就绪", font=('微软雅黑', 12),
                                     bg=self.colors['card_bg'], fg=self.colors['text_secondary'],
                                     padx=20, pady=12)
        self.status_label.pack()
        
        # 挂靠按钮
        self.attach_btn = tk.Button(bottom_frame, text="确认挂靠", 
                                    font=('微软雅黑', 14, 'bold'),
                                    bg=self.colors['primary'], fg='white',
                                    relief=tk.FLAT, bd=0, padx=50, pady=12,
                                    cursor='hand2', command=self.attach_user,
                                    activebackground=self.colors['primary_hover'])
        self.attach_btn.pack(side=tk.RIGHT)
    
    def create_card(self, parent, title):
        """创建卡片式容器"""
        card = tk.Frame(parent, bg=self.colors['card_bg'], 
                       highlightthickness=1, highlightbackground=self.colors['border'])
        
        # 卡片标题
        title_frame = tk.Frame(card, bg=self.colors['card_bg'])
        title_frame.pack(fill=tk.X, padx=20, pady=(15, 0))
        
        # 左侧装饰线
        line = tk.Frame(title_frame, bg=self.colors['primary'], width=4, height=20)
        line.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = tk.Label(title_frame, text=title, font=('微软雅黑', 14, 'bold'),
                              bg=self.colors['card_bg'], fg=self.colors['text'])
        title_label.pack(side=tk.LEFT)
        
        return card
    
    def add_context_menu(self, widget):
        """为控件添加上下文菜单"""
        menu = tk.Menu(self.root, tearoff=0, bg=self.colors['card_bg'], 
                      fg=self.colors['text'], font=('微软雅黑', 10),
                      activebackground=self.colors['primary'], activeforeground='white')
        menu.add_command(label="撤销", command=lambda: self.edit_command(widget, 'undo'))
        menu.add_separator()
        menu.add_command(label="剪切", command=lambda: self.edit_command(widget, 'cut'))
        menu.add_command(label="复制", command=lambda: self.edit_command(widget, 'copy'))
        menu.add_command(label="粘贴", command=lambda: self.edit_command(widget, 'paste'))
        menu.add_separator()
        menu.add_command(label="全选", command=lambda: self.edit_command(widget, 'select_all'))
        
        def show_menu(event):
            widget.focus_set()
            menu.post(event.x_root, event.y_root)
        
        widget.bind('<Button-3>', show_menu)
        
        # 绑定键盘快捷键
        def bind_shortcut(key, cmd):
            def handler(event):
                return self.edit_command(widget, cmd)
            widget.bind(key, handler)
        
        bind_shortcut('<Control-a>', 'select_all')
        bind_shortcut('<Control-A>', 'select_all')
        bind_shortcut('<Control-c>', 'copy')
        bind_shortcut('<Control-C>', 'copy')
        bind_shortcut('<Control-v>', 'paste')
        bind_shortcut('<Control-V>', 'paste')
        bind_shortcut('<Control-x>', 'cut')
        bind_shortcut('<Control-X>', 'cut')
        bind_shortcut('<Control-z>', 'undo')
        bind_shortcut('<Control-Z>', 'undo')
    
    def edit_command(self, widget, command):
        """执行编辑命令"""
        try:
            widget_type = widget.winfo_class()
            
            if command == 'select_all':
                if widget_type == 'Text':
                    widget.tag_add(tk.SEL, 1.0, tk.END)
                    widget.mark_set(tk.INSERT, 1.0)
                    widget.see(tk.INSERT)
                else:
                    widget.select_range(0, tk.END)
                    widget.icursor(tk.END)
                widget.focus_force()
                return 'break'
            elif command == 'undo':
                if widget_type == 'Text':
                    try:
                        widget.edit_undo()
                    except:
                        pass
                else:
                    # Entry控件的撤销
                    try:
                        widget.event_generate('<<Undo>>')
                    except:
                        pass
                return 'break'
            elif command == 'cut':
                widget.event_generate('<<Cut>>')
                return 'break'
            elif command == 'copy':
                widget.event_generate('<<Copy>>')
                return 'break'
            elif command == 'paste':
                widget.event_generate('<<Paste>>')
                return 'break'
        except tk.TclError:
            pass
        return None
    
    def set_status(self, text, status_type='normal'):
        """设置状态显示"""
        self.status_label.config(text=text)
        if status_type == 'success':
            self.status_label.config(fg=self.colors['success'])
            self.status_frame.config(highlightbackground=self.colors['success'])
        elif status_type == 'error':
            self.status_label.config(fg=self.colors['primary'])
            self.status_frame.config(highlightbackground=self.colors['primary'])
        elif status_type == 'processing':
            self.status_label.config(fg='#007bff')
            self.status_frame.config(highlightbackground='#007bff')
        else:
            self.status_label.config(fg=self.colors['text_secondary'])
            self.status_frame.config(highlightbackground=self.colors['border'])
        self.root.update()
    
    def query_user(self):
        user_id = self.id_entry.get().strip()
        
        if not user_id:
            self.set_status("请输入博主ID", 'error')
            return
        
        if not user_id.isdigit():
            self.set_status("博主ID必须是数字", 'error')
            return
        
        # 清空之前的结果
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        self.current_user_id = None
        
        # 发送请求
        self.query_btn.config(state=tk.DISABLED)
        self.set_status("查询中...", 'processing')
        self.root.update()
        
        try:
            result = self.fetch_user_info(user_id)
            if result:
                self.display_result(result)
                self.current_user_id = result.get('userId')
                self.add_uid_to_list(self.current_user_id)
                self.set_status("查询成功", 'success')
            else:
                self.set_status("未找到该博主信息", 'error')
        except Exception as e:
            self.set_status("查询失败", 'error')
        finally:
            self.query_btn.config(state=tk.NORMAL)
    
    def display_result(self, result):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        result_str = f"博主ID：{result.get('userId', '')}\n\n"
        result_str += f"博主昵称：{result.get('userName', '')}\n\n"
        result_str += f"粉丝数量：{result.get('fansNum', '')}"
        self.result_text.insert(tk.END, result_str)
        self.result_text.config(state=tk.DISABLED)
    
    def add_uid_to_list(self, uid):
        """添加UID到列表"""
        if uid:
            current_text = self.uid_text.get(1.0, tk.END).strip()
            if current_text:
                self.uid_text.insert(tk.END, f"\n{uid}")
            else:
                self.uid_text.insert(tk.END, uid)
            self.uid_text.see(tk.END)
    
    def clear_uid_list(self):
        """清空UID列表"""
        self.uid_text.delete(1.0, tk.END)
        self.set_status("已清空", 'normal')
    
    def copy_uid_list(self):
        """复制UID列表到剪贴板"""
        uid_text = self.uid_text.get(1.0, tk.END).strip()
        if uid_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(uid_text)
            self.set_status("已复制到剪贴板", 'success')
        else:
            self.set_status("UID列表为空", 'error')
    
    def fetch_user_info(self, user_id):
        url = f"https://creator.xiaohongshu.com/api/galaxy/sign/user/search?keyword={user_id}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 QQBrowser/21.1.8531.400",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "sec-ch-ua": "\"Chromium\";v=\"123\", \"Not:A-Brand\";v=\"8\"",
            "x-t": "1778828517578",
            "x-b3-traceid": "4fcf7b30fc27f6dd",
            "sec-ch-ua-mobile": "?0",
            "authorization": "",
            "x-s-common": "2UQAPsHC+aIjqArjwjHjNsQhPsHCH0rjNsQhPaHCH0c1PUhMHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQM89PjNsQh+sHCH0r1P/Z1PsHVHdWMH0ijP/Sj+0cIweb08n8A2nSxq7YA4BplG0Qlq9PAq9kA87i9wgYx8A+DwBWMPeZIPerF+ArhPUHVHdW9H0ijHjIj2eqjwjHjNsQhwsHCHDDAwoQH8B4AyfRI8FS98g+Dpd4daLP3JFSb/BMsn0pSPM87nrldzSzQ2bPAGdb7zgQB8nph8emSy9E0cgk+zSS1qgzianYt8p+1/LzN4gzaa/+NqMS6qS4HLozoqfQnPbZEp98QyaRSp9P98pSl4oSzcgmca/P78nTTL0bz/sVManD9q9z18np/8db8aob7JeQl4epsPrzsagW3Lr4ryaRApdz3agYDq7YM47HFqgzkanYMGLSbP9LA/bGIa/+nprSe+9LI4gzVPDbrJg+P4fprLFTALMm7+LSb4d+kpdzt/7b7wrQM498cqBzSpr8g/FSh+bzQygL9nSm7qSmM4epQ4flY/BQdqA+l4oYQ2BpAPp87arS34nMQyFSE8nkdqMD6pMzd8/4SL7bF8aRr+7+rG7mkqBpD8pSUzozQcA8Szb87PDSb/d+/qgzVJfl/4LExpdzQ4fRSy7bFP9+y+7+nJAzdaLp/2LSizL4zcdbMagYiJdbCwB4QyFSfJ7b7yFSeqS4o8e+A8BlO8p8c4A+Q4DbSPB8d8nzryo4QzLRAPpq3zdSl4bYQye+SPnzm8/+B/7+nLo4O8n8OqMSl4e+Q2bzA8ML9qM+M4ApP+FTA8S878FDALdkQP7m/qdp7aokc47SsydH6wBQNq9zS+7+nqgq3anTN8LcIcg+n/bQsagGM8gWI8BpDaaTsaL+dq98c4FYQ4DSBLpm7abmn4rbQ2epS+dpF4DS38nL94gzAa/+D8/bn47+1pdzV2gbFqFS3LFlQcFYUP04VyAQQ8nLl4gzeaLp/4FSb+d+xqgz12DSCqf+1/d+8ySSManSi/r4M4okU4gzVagGM8nTl4bpOqrTAPgQw8gYy4g+Qyo8SngkmqAbl4Fls4gz7agY68p4n4e4Qy94S2Bka4FS98np/8sRS8S8FLFSha7P9pd4pz94/GLSbaeQQ4fpAyFlS8p868nLIz0+A8b8F2DSkLebQ4fMindbFJFSeJBkQzg8APFzrnoc6P7PILozyanYLt9Mc4rLFanRAzBHA8p+M4Fk6LozEaLPFzDS3G7+0Lo4FaM8FGDSh89p///mApSmFqoQn4o8Q4dk3JgpF/DDAab4HJDMAa/P6qAmxcg+8c04Sp7b7nBQl4b8Q2rYianD9q9kc4okQc9RS2BqhqLSbGfY7qUT+anYIpDSb89pfLo4zadbFcnRn4BpQyF81agGAqAmVPBp84gqI/BQULDS9LBzo4gzT/MmFwrShpdYQP9MhanSbyDSi8Bp3/e+ApD8/8pkc47QQcFznPSm7qpkM49lQcURSy98rNFDAzf8oqf4SPobFnbkM4b8y2f+dn0SlJrShGd+d4gqMa/+9qM4yzLkQygkLJMm7JrS3Lf+F4gcIJ7pF4FSiy/pQyezwag8Iq9pc4MmQyLSlanYwqA8n4URUp9T9anYBpDSe/7+889RA+Sm7tFSi2DpQcFlHN7kQyrSiJb8dJgHEanYSq98r+npgpd46anYmq9Sl4omQzL4IaLLIq9zM4FkQcFp14ob7/FS9ad+DqFllNMmFpfpc4r4Q4fRSp7pF8LSi4dPI8ez/aLpmqMS/a7PlLoz7aeZIqM+n4FzzqBRAPbmFpLSk87PAN94SpS8FnDSeLBpQ2bb0nS87JdQTJpQQyAmSySm7/7QC/fphaLFIqSmFPDS3LMmQyn4Apok+GLDAad+xqg41anYnwLSicnphwpDManYi+LSkyrqhzdk1aLPI8n8YqL+QybSganTQz1778828517578",
            "x-s": "XYS_2UQhPsHCH0c1PUhMHjIj2erjwjQM89PjNsQhPjHCHS4kJfz647PjNsQhPUHCHfM1qAZlPebK/MSB8LLAc7i7LgprzdkQafpi4dc9NM+taMbPzUVha/LEabc9anEzPrYQJ/bccD+1zpm/aD8i4DEY47zSpBYg8fW3nD8/t9kN+rcU4ASs+p4FnfQ9zAPIcFzyzr8SLn8B4emE/Ar78oSy+n+azpDF4okfnpSyG9R88AmCLnELaBQrnB8Bwoza2oYtPgSr+AYY8eS1woZl+n8xLgWU//GU4gmkapQep98cyB8D8UuFne8T/rl/8fzQPSk7y0qjNsQh+sHCHjQR",
            "x-xray-traceid": "cf1538905f0a2532f8aaad174ff83292",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://creator.xiaohongshu.com/newmcn/contract-search?searchText=752457210",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": "a1=19b64081cefsyijsxsteqb2qsc3sjsgz69xjg3d8h50000147183; webId=c7d755ae247ecb8aae4f366d5d112ae7; gid=yjDK48YJ2qKYyjDK48YySjqfdiMv3VMCM9dACYxDJAMSqV28MVMkuk888y4WyYq8dSyYii40; customerClientId=760937489878821; xsecappid=ugc; x-user-id-creator.xiaohongshu.com=6774c59b0000000018017df0; ets=1777551621268; access-token-creator.xiaohongshu.com=customer.creator.AT-68c5176349289429491220536pixi3sylcjalp07; galaxy_creator_session_id=c036p5BSE4zNPymAki4HCq5AIJf8gQtSNyWP; galaxy.creator.beaker.session.id=1777645420957068860002; acw_tc=0a0d0e0317788279624497113eb19b8eb4ae7007c39602e5dbb81d23cf3fd9; loadts=1778827964764; websectiga=3fff3a6f9f07284b62c0f2ebf91a3b10193175c06e4f71492b60e056edcdebb2; sec_poison_id=6749f0c9-3811-4966-90a5-b9e28c5f9d5b"
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            raise Exception(f"HTTP错误：{response.status_code}")
        
        data = response.json()
        
        if data.get('code') == 0 and data.get('data'):
            data_obj = data['data']
            
            if isinstance(data_obj, dict) and 'users' in data_obj:
                users_list = data_obj['users']
                if isinstance(users_list, list) and len(users_list) > 0:
                    user_info = users_list[0]
                    return {
                        'userId': user_info.get('userId', ''),
                        'userName': user_info.get('userName', ''),
                        'fansNum': user_info.get('fansNum', ''),
                        'noteNum': user_info.get('noteNum', '')
                    }
        
        return None
    
    def attach_user(self):
        if not self.current_user_id:
            self.set_status("请先查询博主信息", 'error')
            return
        
        name = self.name_entry.get().strip()
        area_code = self.area_code_var.get()
        phone_number = self.phone_entry.get().strip()
        
        if not name:
            self.set_status("请输入姓名", 'error')
            return
        
        if not phone_number:
            self.set_status("请输入电话号码", 'error')
            return
        
        phone = f"{area_code}{phone_number}"
        
        start_date = self.start_date.get_date()
        end_date = self.end_date.get_date()
        
        try:
            current_timestamp = int(time.time() * 1000)
        except Exception as e:
            current_timestamp = int(datetime.now().timestamp() * 1000)
        
        end_datetime = datetime.combine(end_date, datetime.max.time().replace(hour=23, minute=59, second=59, microsecond=0))
        end_timestamp = int(end_datetime.timestamp() * 1000)
        
        self.attach_btn.config(state=tk.DISABLED)
        self.set_status("挂靠中...", 'processing')
        self.root.update()
        
        try:
            result = self.send_attach_request(current_timestamp, end_timestamp, name, phone)
            
            if result.get('code') == 0 or result.get('success') == True:
                self.set_status("挂靠成功", 'success')
            else:
                error_msg = result.get('msg', '')
                if '用户手机号填写错误' in error_msg:
                    self.set_status("手机号错误请检查", 'error')
                elif '与博主真实姓名不符' in error_msg:
                    self.set_status("姓名错误请检查", 'error')
                else:
                    self.set_status("挂靠失败", 'error')
        except Exception as e:
            self.set_status("挂靠失败", 'error')
        finally:
            self.attach_btn.config(state=tk.NORMAL)
    
    def send_attach_request(self, start_time, end_time, name, phone):
        url = "https://creator.xiaohongshu.com/api/galaxy/sign/apply"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 QQBrowser/21.1.8531.400",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/json",
            "sec-ch-ua": "\"Chromium\";v=\"123\", \"Not:A-Brand\";v=\"8\"",
            "x-t": "1778828414070",
            "x-b3-traceid": "2acf1bdb27a0fded",
            "sec-ch-ua-mobile": "?0",
            "authorization": "",
            "x-s-common": "2UQAPsHC+aIjqArjwjHjNsQhPsHCH0rjNsQhPaHCH0c1PUhMHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQM89PjNsQh+sHCH0r1P/Z1PsHVHdWMH0ijP/Sj+0cIweb08n8A2nSxq7YA4BplG0Qlq9PAq9kA87i9wgYx8A+DwBWMPeZIPerF+ArhPUHVHdW9H0ijHjIj2eqjwjHjNsQhwsHCHDDAwoQH8B4AyfRI8FS98g+Dpd4daLP3JFSb/BMsn0pSPM87nrldzSzQ2bPAGdb7zgQB8nph8emSy9E0cgk+zSS1qgzianYt8p+1/LzN4gzaa/+NqMS6qS4HLozoqfQnPbZEp98QyaRSp9P98pSl4oSzcgmca/P78nTTL0bz/sVManD9q9z18np/8db8aob7JeQl4epsPrzsagW3Lr4ryaRApdz3agYDq7YM47HFqgzkanYMGLSbP9LA/bGIa/+nprSe+9LI4gzVPDbrJg+P4fprLFTALMm7+LSb4d+kpdzt/7b7wrQM498cqBzSpr8g/FSh+bzQygL9nSm7qSmM4epQ4flY/BQdqA+l4oYQ2BpAPp87arS34nMQyFSE8nkdqMD6pMzd8/4SL7bF8aRr+7+rG7mkqBpD8pSUzozQcA8Szb87PDSb/d+/qgzVJfl/4LExpdzQ4fRSy7bFP9+y+7+nJAzdaLp/2LSizL4zcdbMagYiJdbCwB4QyFSfJ7b7yFSeqS4o8e+A8BlO8p8c4A+Q4DbSPB8d8nzryo4QzLRAPpq3zdSl4bYQye+SPnzm8/+B/7+nLo4O8n8OqMSl4e+Q2bzA8ML9qM+M4ApP+FTA8S878FDALdkQP7m/qdp7aokc4FksydH6aDMwq9zS+7+nqgq3anTN8LcIcg+n/bQsagGM8gWI8BpDaaTsaL+dq98c4FYQ4DSBLpm7abmn4rbQ2epS+dpF4DS38nL94gzAa/+D8/bn47+1pdzV2gbFqFS3LFlQcFYUP04VyAQQ8nLl4gzeaLp/4FSb+d+xqgz12DSCqf+1/d+8ySSManSi/r4M4okU4gzVagGM8nTl4bpOqrTAPgQw8gYy4g+Qyo8SngkmqAbl4Fls4gz7agY68p4n4e4Qy94S2Bka4FS98np/8sRS8S8FLFShPoPl4g4pz948GLSbqgbQcA8A+Dc98gWE+9LIzBpAnpmFaFSk/L8QPFMMqS8FaFS92DpQzLkApdmc4aTp8gPILozlaLpa/FQl4r8tnLEAyDGMqAml47+SLo4yaL+8zrS3GFl0Loz02p8FqrS9+np//emSPob7P/Yl4okQcFMEt7pF/rSewBbOPrpsanV6qFz+cg+h/rESLM87zo+M4bQQP7phanV7q9kl4BMQcA4SpBchqDSb2DpHqFF7aLpIyFSbPBpf4g4P2gbFpg+c4BbQyn+Eag8mq9TmcnLl4gqAJDQynLSeyncULozoJpmFqDS3z0bQP9QtanSLzrSi8nL9+FbAyDGFLDEM49TQcFznqop7yDQn4M+QcURSzBRUNFDAzfSd80+SypmFpBQn4Bp6nSZ6Lr8kzLShLDTtpd46anTwq9TSGdbQypPUcS87yFSkpez7pdzrndbF4LSeLBlQ4S+raLp8/9Rl4M4Qy9+xanYwq9SM4A+ScnIManYQnDS9N7+Lqe4Apbm7tFSi204Qzp8Dz9MUyFSeJL8onL4Qag89qM4U4fp8qg4sanW7q7Yn4b+QyobdagG6q9kc4A+QybrU4ob7/FS9Po+kp9SV2dbF/g4l4okQ408SpM8FLDSiN7+x/pziaLpOq98P+gP9Lozsqf+wqAmn4Fz7cf4APgbFwLSh8g+kGLkSzb8FPrSiaeSQypQLJp87nnM8LfRQPFRSP7b7/9Qp+9phn0Y6JgbFnDS3weQQy9RAzrzkqrSkcnpkLocUanYnwLSbPBp8cSSBanYQGDSka/Qtqezaag8O8nk8ygkQznVEagYHc1778828414070",
            "x-s": "XYS_2UQhPsHCH0c1PUhMHjIj2erjwjQM89PjNsQhPjHCHS4kJfz647PjNsQhPUHCHfM1qAZlPebK/MSB8LLAaSH6nnlk+gY92rh7qe8YJF+yyn8YLpzr8/m8+/8k+Amzp9hE/g4g4nY64bi7zB8NaBuA4rkL8fWE4bQzyMQDcSYic0pCLL884piILDkwN78Iagzf8Mm0/LMGzA4IJ0WIzebbL/YCapS3/F4+JnMPpMY6GUTi+fpYzDl9/BWI+fYapF4x8A8EqB+Dnr8yG9keprTkcdm1/LSCnbZ9L/QH8gkcPni7L/Y9cMZM//4jnfRd+fihGgDjNsQh+sHCHfRjyfp04sQR",
            "x-xray-traceid": "cf1537c6360a2513c9795e56df0fb34c",
            "sec-ch-ua-platform": "\"Windows\"",
            "origin": "https://creator.xiaohongshu.com",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://creator.xiaohongshu.com/newmcn/contract-edit/5df3991e000000000100712b/create/1",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": "a1=19b64081cefsyijsxsteqb2qsc3sjsgz69xjg3d8h50000147183; webId=c7d755ae247ecb8aae4f366d5d112ae7; gid=yjDK48YJ2qKYyjDK48YySjqfdiMv3VMCM9dACYxDJAMSqV28MVMkuk888y4WyYq8dSyYii40; customerClientId=760937489878821; xsecappid=ugc; x-user-id-creator.xiaohongshu.com=6774c59b0000000018017df0; ets=1777551621268; access-token-creator.xiaohongshu.com=customer.creator.AT-68c5176349289429491220536pixi3sylcjalp07; galaxy_creator_session_id=c036p5BSE4zNPymAki4HCq5AIJf8gQtSNyWP; galaxy.creator.beaker.session.id=1777645420957068860002; acw_tc=0a0d0e0317788279624497113eb19b8eb4ae7007c39602e5dbb81d23cf3fd9; loadts=1778827964764; websectiga=3fff3a6f9f07284b62c0f2ebf91a3b10193175c06e4f71492b60e056edcdebb2; sec_poison_id=6749f0c9-3811-4966-90a5-b9e28c5f9d5b"
        }
        
        payload = {
            "startTime": start_time,
            "endTime": end_time,
            "kolAgreement": None,
            "terminateAgreement": None,
            "userId": self.current_user_id,
            "businessType": 1,
            "kolRealName": name,
            "kolPhone": phone
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            raise Exception(f"HTTP错误：{response.status_code}")
        
        return response.json()


if __name__ == "__main__":
    root = tk.Tk()
    app = XHSQueryTool(root)
    root.mainloop()
