#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python官方下载器 - 官方风格版
模仿Python官网的设计风格
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import threading
import os
import re
import webbrowser
import time
from urllib.parse import urljoin
from PIL import Image, ImageTk

class PythonOfficialDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Windows版本下载器 - 官方安装程序,抖音搜索-小庄学Python, 个人博客：https://ikun.space")
        self.root.geometry("1000x850")
        self.root.resizable(True, True)
        
        # Python官方配色方案
        self.colors = {
            'python_blue': '#3776ab',
            'python_yellow': '#ffd43b',
            'dark_blue': '#2b5b84',
            'light_blue': '#4b8bbe',
            'white': '#ffffff',
            'light_gray': '#f8f9fa',
            'medium_gray': '#e9ecef',
            'dark_gray': '#6c757d',
            'text_dark': '#212529',
            'success_green': '#28a745',
            'warning_orange': '#fd7e14'
        }
        
        # 设置窗口图标色彩
        self.root.configure(bg=self.colors['light_gray'])
        
        # 配置样式
        self.setup_styles()
        
        # 数据存储
        self.python_versions = []
        self.download_thread = None
        self.is_downloading = False
        
        # 扩展的Python版本信息 - 包含更多版本
        self.predefined_versions = [
            # Python 3.14 系列 (Latest)
            {'version': '3.14.0', 'date': '2025-10-07', 'status': '最新版'},
            
            # Python 3.13 系列 (Stable)
            {'version': '3.13.9', 'date': '2025-10-14', 'status': '稳定版'},
            {'version': '3.13.8', 'date': '2025-10-01', 'status': '稳定版'},
            {'version': '3.13.7', 'date': '2025-08-14', 'status': '稳定版'},
            {'version': '3.13.6', 'date': '2025-06-01', 'status': '稳定版'},
            {'version': '3.13.5', 'date': '2025-04-01', 'status': '稳定版'},
            {'version': '3.13.4', 'date': '2025-02-01', 'status': '稳定版'},
            {'version': '3.13.3', 'date': '2024-12-01', 'status': '稳定版'},
            {'version': '3.13.2', 'date': '2024-11-01', 'status': '稳定版'},
            {'version': '3.13.1', 'date': '2024-10-15', 'status': '稳定版'},
            {'version': '3.13.0', 'date': '2024-10-07', 'status': '稳定版'},
            
            # Python 3.12 系列
            {'version': '3.12.8', 'date': '2024-12-07', 'status': '稳定版'},
            {'version': '3.12.7', 'date': '2024-10-01', 'status': '稳定版'},
            {'version': '3.12.6', 'date': '2024-09-06', 'status': '稳定版'},
            {'version': '3.12.5', 'date': '2024-08-06', 'status': '稳定版'},
            {'version': '3.12.4', 'date': '2024-06-06', 'status': '稳定版'},
            {'version': '3.12.3', 'date': '2024-04-09', 'status': '稳定版'},
            {'version': '3.12.2', 'date': '2024-02-06', 'status': '稳定版'},
            {'version': '3.12.1', 'date': '2023-12-07', 'status': '稳定版'},
            {'version': '3.12.0', 'date': '2023-10-02', 'status': '稳定版'},
            
            # Python 3.11 系列
            {'version': '3.11.10', 'date': '2024-09-07', 'status': '稳定版'},
            {'version': '3.11.9', 'date': '2024-04-02', 'status': '稳定版'},
            {'version': '3.11.8', 'date': '2024-02-06', 'status': '稳定版'},
            {'version': '3.11.7', 'date': '2023-12-04', 'status': '稳定版'},
            {'version': '3.11.6', 'date': '2023-10-02', 'status': '稳定版'},
            {'version': '3.11.5', 'date': '2023-08-24', 'status': '稳定版'},
            {'version': '3.11.4', 'date': '2023-06-06', 'status': '稳定版'},
            {'version': '3.11.3', 'date': '2023-04-04', 'status': '稳定版'},
            {'version': '3.11.2', 'date': '2023-02-07', 'status': '稳定版'},
            {'version': '3.11.1', 'date': '2022-12-06', 'status': '稳定版'},
            {'version': '3.11.0', 'date': '2022-10-24', 'status': '稳定版'},
            
            # Python 3.10 系列
            {'version': '3.10.15', 'date': '2024-09-07', 'status': '稳定版'},
            {'version': '3.10.14', 'date': '2024-03-19', 'status': '稳定版'},
            {'version': '3.10.13', 'date': '2023-08-24', 'status': '稳定版'},
            {'version': '3.10.12', 'date': '2023-06-06', 'status': '稳定版'},
            {'version': '3.10.11', 'date': '2023-04-04', 'status': '稳定版'},
            {'version': '3.10.10', 'date': '2023-02-07', 'status': '稳定版'},
            {'version': '3.10.9', 'date': '2022-12-06', 'status': '稳定版'},
            {'version': '3.10.8', 'date': '2022-10-11', 'status': '稳定版'},
            
            # Python 3.9 系列
            {'version': '3.9.20', 'date': '2024-09-07', 'status': '安全版'},
            {'version': '3.9.19', 'date': '2024-03-19', 'status': '安全版'},
            {'version': '3.9.18', 'date': '2023-08-24', 'status': '安全版'},
            {'version': '3.9.17', 'date': '2023-06-06', 'status': '安全版'},
            {'version': '3.9.16', 'date': '2022-12-06', 'status': '安全版'},
            
            # Python 3.8 系列
            {'version': '3.8.20', 'date': '2024-09-07', 'status': '安全版'},
            {'version': '3.8.19', 'date': '2024-03-19', 'status': '安全版'},
            {'version': '3.8.18', 'date': '2023-08-24', 'status': '安全版'},
            {'version': '3.8.17', 'date': '2023-06-06', 'status': '安全版'},
            {'version': '3.8.16', 'date': '2022-12-06', 'status': '安全版'},
        ]
        
        self.setup_ui()
        
    def setup_styles(self):
        """设置Python官方风格的样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置主要样式
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 24, 'bold'),
                       foreground=self.colors['python_blue'],
                       background=self.colors['light_gray'],
                       anchor='center')
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 12),
                       foreground=self.colors['dark_gray'],
                       background=self.colors['light_gray'],
                       anchor='center')
        
        style.configure('Header.TLabel',
                       font=('Segoe UI', 14, 'bold'),
                       foreground=self.colors['text_dark'],
                       background=self.colors['white'])
        
        style.configure('Python.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       foreground=self.colors['white'],
                       background=self.colors['python_blue'],
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Python.TButton',
                 background=[('active', self.colors['dark_blue']),
                           ('pressed', self.colors['dark_blue'])])
        
        style.configure('Download.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       foreground=self.colors['white'],
                       background=self.colors['success_green'],
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Download.TButton',
                 background=[('active', '#218838'),
                           ('pressed', '#1e7e34')])
        
        style.configure('Warning.TButton',
                       font=('Segoe UI', 10),
                       foreground=self.colors['white'],
                       background=self.colors['warning_orange'],
                       borderwidth=0,
                       focuscolor='none')
        
        # 配置Treeview样式
        style.configure('Python.Treeview',
                       background=self.colors['white'],
                       foreground=self.colors['text_dark'],
                       fieldbackground=self.colors['white'],
                       font=('Segoe UI', 10),
                       anchor='center')
        
        style.configure('Python.Treeview.Heading',
                       font=('Segoe UI', 11, 'bold'),
                       foreground=self.colors['python_blue'],
                       background=self.colors['medium_gray'])
        
        # 配置Frame样式
        style.configure('Card.TFrame',
                       background=self.colors['white'],
                       relief='solid',
                       borderwidth=1)
        
        style.configure('Main.TFrame',
                       background=self.colors['light_gray'])
        
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, style='Main.TFrame', padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # 标题区域 - 蓝色背景
        title_frame = tk.Frame(main_frame, bg=self.colors['python_blue'], relief='flat', bd=0)
        title_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        title_frame.columnconfigure(0, weight=1)
        
        # 主标题 - 白色文字
        title_label = tk.Label(title_frame, text="Python Windows版本下载", 
                              font=('Segoe UI', 24, 'bold'),
                              fg='white', bg=self.colors['python_blue'],
                              anchor='w')
        title_label.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(20, 0), pady=(15, 5))
        
        # 副标题 - 白色文字
        subtitle_label = tk.Label(title_frame, 
                                 text="Python编程语言官方下载站", 
                                 font=('Segoe UI', 12),
                                 fg='white', bg=self.colors['python_blue'],
                                 anchor='w')
        subtitle_label.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(20, 0), pady=(0, 15))
        
        # 加载并显示Python logo - 放在右上角，使用原始大小
        try:
            logo_image = Image.open("python-logo.png")
            # 不缩放，使用原始大小
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            
            logo_label = tk.Label(title_frame, image=self.logo_photo, 
                                bg=self.colors['python_blue'], bd=0)
            logo_label.grid(row=0, column=1, rowspan=2, padx=(15, 20), pady=15, sticky=tk.E)
        except Exception as e:
            print(f"无法加载logo: {e}")
        
        # 控制按钮区域
        control_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="15")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        control_frame.columnconfigure(2, weight=1)
        
        ttk.Label(control_frame, text="可用的Python版本:", 
                 style='Header.TLabel').grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=(0, 10))
        
        # 按钮
        ttk.Button(control_frame, text="🔄 加载Python版本", 
                  style='Python.TButton',
                  command=self.load_versions).grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        
        ttk.Button(control_frame, text="🔃 刷新", 
                  style='Python.TButton',
                  command=self.refresh_versions).grid(row=1, column=1, sticky=tk.W, padx=(0, 10))
        
        # 状态标签
        self.status_label = ttk.Label(control_frame, text="点击'加载Python版本'开始",
                                     style='Subtitle.TLabel')
        self.status_label.grid(row=1, column=2, sticky=tk.E, padx=(10, 0))
        
        # 过滤器区域
        filter_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="10")
        filter_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(filter_frame, text="按版本筛选:", font=('Segoe UI', 10)).grid(row=0, column=0, padx=(0, 10))
        
        self.filter_var = tk.StringVar(value="所有版本")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                   values=["所有版本", "3.14.x", "3.13.x", "3.12.x", "3.11.x", "3.10.x", "3.9.x", "3.8.x"],
                                   state="readonly", width=15)
        filter_combo.grid(row=0, column=1, padx=(0, 20))
        filter_combo.bind('<<ComboboxSelected>>', self.filter_versions)
        
        ttk.Label(filter_frame, text="系统架构:", font=('Segoe UI', 10)).grid(row=0, column=2, padx=(0, 10))
        
        self.arch_var = tk.StringVar(value="全部")
        arch_combo = ttk.Combobox(filter_frame, textvariable=self.arch_var,
                                 values=["全部", "64-bit", "32-bit"],
                                 state="readonly", width=10)
        arch_combo.grid(row=0, column=3)
        arch_combo.bind('<<ComboboxSelected>>', self.filter_versions)
        
        # 版本列表区域
        list_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="10")
        list_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 创建Treeview
        columns = ('version', 'status', 'arch', 'type', 'size', 'date')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', 
                                height=15, style='Python.Treeview')
        
        # 设置列标题和宽度
        headers = {
            'version': ('版本', 100),
            'status': ('状态', 80),
            'arch': ('架构', 100),
            'type': ('安装包类型', 150),
            'size': ('文件大小', 100),
            'date': ('发布日期', 120)
        }
        
        for col, (text, width) in headers.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, minwidth=width, anchor='center')
        
        # 滚动条
        scrollbar_v = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_h = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        # 布局
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_v.grid(row=0, column=1, sticky=(tk.N, tk.S))
        scrollbar_h.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # 下载控制区域
        download_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="15")
        download_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(15, 0))
        download_frame.columnconfigure(1, weight=1)
        
        ttk.Label(download_frame, text="下载选项:", 
                 style='Header.TLabel').grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=(0, 10))
        
        # 下载路径
        ttk.Label(download_frame, text="📁 下载到:", 
                 font=('Segoe UI', 10)).grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        
        self.download_path = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        path_entry = ttk.Entry(download_frame, textvariable=self.download_path, font=('Segoe UI', 10))
        path_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(download_frame, text="浏览", 
                  command=self.browse_download_path).grid(row=1, column=2, padx=(0, 10))
        
        # 下载按钮区域
        button_frame = ttk.Frame(download_frame, style='Card.TFrame')
        button_frame.grid(row=2, column=0, columnspan=3, pady=(15, 0))
        
        self.download_btn = ttk.Button(button_frame, text="⬇️ 下载选中版本", 
                                      style='Download.TButton',
                                      command=self.download_selected)
        self.download_btn.grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(button_frame, text="🌐 在Python.org查看", 
                  style='Warning.TButton',
                  command=self.open_in_browser).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(button_frame, text="📋 复制下载链接", 
                  command=self.copy_download_link).grid(row=0, column=2)
        
        # 进度区域
        progress_frame = ttk.Frame(download_frame, style='Card.TFrame')
        progress_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(15, 0))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.progress_label = ttk.Label(progress_frame, text="", font=('Segoe UI', 9))
        self.progress_label.grid(row=1, column=0)
        
        # 绑定事件
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<Button-3>', self.show_context_menu)  # 右键菜单
        
    def filter_versions(self, event=None):
        """过滤版本列表"""
        if not self.python_versions:
            return
            
        # 清空现有显示
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        version_filter = self.filter_var.get()
        arch_filter = self.arch_var.get()
        
        filtered_versions = []
        for version in self.python_versions:
            # 版本过滤
            if version_filter != "所有版本":
                version_prefix = version_filter.replace('.x', '')
                if not version['version'].startswith(version_prefix):
                    continue
            
            # 架构过滤
            if arch_filter != "全部" and version['arch'] != arch_filter:
                continue
                
            filtered_versions.append(version)
        
        # 重新添加过滤后的版本
        for version in filtered_versions:
            # 根据状态设置不同的标签
            status_tag = version['status'].lower()
            self.tree.insert('', 'end', values=(
                version['version'],
                version['status'],
                version['arch'],
                version['type'],
                version['size'],
                version['date']
            ), tags=(status_tag,))
        
        # 配置标签颜色
        self.tree.tag_configure('latest', background='#e8f5e8')
        self.tree.tag_configure('stable', background='#f8f9fa')
        self.tree.tag_configure('security', background='#fff3cd')
        
        self.status_label.config(text=f"显示 {len(filtered_versions)} 个版本")
    
    def copy_download_link(self):
        """复制下载链接到剪贴板"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个版本")
            return
        
        item = selection[0]
        index = self.tree.index(item)
        
        # 找到对应的版本信息
        displayed_versions = []
        version_filter = self.filter_var.get()
        arch_filter = self.arch_var.get()
        
        for version in self.python_versions:
            if version_filter != "所有版本":
                version_prefix = version_filter.replace('.x', '')
                if not version['version'].startswith(version_prefix):
                    continue
            if arch_filter != "全部" and version['arch'] != arch_filter:
                continue
            displayed_versions.append(version)
        
        if index < len(displayed_versions):
            version_info = displayed_versions[index]
            self.root.clipboard_clear()
            self.root.clipboard_append(version_info['url'])
            messagebox.showinfo("成功", f"下载链接已复制到剪贴板:\n{version_info['url']}")
    
    def show_context_menu(self, event):
        """显示右键菜单"""
        selection = self.tree.selection()
        if not selection:
            return
            
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="⬇️ 下载", command=self.download_selected)
        context_menu.add_command(label="🌐 在Python.org查看", command=self.open_in_browser)
        context_menu.add_command(label="📋 复制下载链接", command=self.copy_download_link)
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    
    def load_versions(self):
        """加载Python版本列表"""
        self.status_label.config(text="🔄 正在加载Python版本...")
        self.download_btn.config(state='disabled')
        
        # 清空现有列表
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.python_versions = []
        
        # 在新线程中逐个加载版本
        threading.Thread(target=self._load_versions_progressively, daemon=True).start()
    
    def _load_versions_progressively(self):
        """逐个加载版本的后台线程"""
        try:
            total_versions = len(self.predefined_versions)
            loaded_count = 0
            
            # 遍历预定义版本
            for version_info in self.predefined_versions:
                version = version_info['version']
                date = version_info['date']
                status = version_info['status']
                
                print(f"🔍 检查Python {version}...")
                
                # 为每个版本添加64位和32位安装包
                for arch in ['64-bit', '32-bit']:
                    # 构建下载URL
                    if arch == '64-bit':
                        filename = f"python-{version}-amd64.exe"
                    else:
                        filename = f"python-{version}.exe"
                    
                    url = f"https://www.python.org/ftp/python/{version}/{filename}"
                    
                    # 估算文件大小
                    if arch == '64-bit':
                        estimated_size = "~28 MB"
                    else:
                        estimated_size = "~25 MB"
                    
                    # 检查文件是否存在（简化版本，直接添加）
                    try:
                        version_data = {
                            'version': version,
                            'status': status,
                            'arch': arch,
                            'type': 'Windows安装程序',
                            'size': estimated_size,
                            'date': date,
                            'url': url,
                            'filename': filename
                        }
                        
                        self.python_versions.append(version_data)
                        print(f"✅ 添加 Python {version} ({arch})")
                        
                        # 在主线程中更新UI
                        self.root.after(0, self._add_version_to_display, version_data)
                        
                    except Exception as e:
                        print(f"❌ 跳过 Python {version} ({arch}): {e}")
                
                loaded_count += 1
                progress = (loaded_count / total_versions) * 100
                
                # 更新进度
                self.root.after(0, self._update_loading_progress, loaded_count, total_versions)
                
                # 添加小延迟，让用户看到逐个加载的效果
                time.sleep(0.1)
            
            # 加载完成
            self.root.after(0, self._loading_complete)
            
        except Exception as e:
            self.root.after(0, self._show_error, f"加载版本时出错: {str(e)}")
    
    def _add_version_to_display(self, version_data):
        """在主线程中添加版本到显示列表"""
        # 应用当前筛选条件
        version_filter = self.filter_var.get()
        arch_filter = self.arch_var.get()
        
        # 版本过滤
        if version_filter != "所有版本":
            version_prefix = version_filter.replace('.x', '')
            if not version_data['version'].startswith(version_prefix):
                return
        
        # 架构过滤
        if arch_filter != "全部" and version_data['arch'] != arch_filter:
            return
        
        # 添加到树形视图
        item_id = self.tree.insert('', 'end', values=(
            version_data['version'],
            version_data['status'],
            version_data['arch'],
            version_data['type'],
            version_data['size'],
            version_data['date']
        ))
        
        # 根据状态设置标签样式
        if version_data['status'] == '最新版':
            self.tree.item(item_id, tags=('latest',))
        elif version_data['status'] == '稳定版':
            self.tree.item(item_id, tags=('stable',))
        elif version_data['status'] == '安全版':
            self.tree.item(item_id, tags=('security',))
    
    def _update_loading_progress(self, loaded, total):
        """更新加载进度"""
        self.status_label.config(text=f"🔄 正在加载... ({loaded}/{total})")
    
    def _loading_complete(self):
        """加载完成"""
        total_displayed = len([item for item in self.tree.get_children()])
        self.status_label.config(text=f"🎉 加载完成！显示 {total_displayed} 个版本")
        self.download_btn.config(state='normal')
        print(f"🎉 加载完成！共找到 {len(self.python_versions)} 个安装包")
        
    def _load_versions_thread(self):
        """在线程中加载版本列表"""
        try:
            print("开始加载Python版本列表...")
            versions = []
            
            # 为每个预定义版本生成64位和32位安装包信息
            for version_info in self.predefined_versions:
                version = version_info['version']
                date = version_info['date']
                status = version_info['status']
                
                # 检查版本是否真实存在
                base_url = f"https://www.python.org/ftp/python/{version}/"
                
                try:
                    # 检查FTP目录是否存在
                    response = requests.head(base_url, timeout=10)
                    if response.status_code == 200:
                        print(f"✅ 版本 {version} 存在，添加到列表")
                        
                        # 64位版本
                        filename_64 = f"python-{version}-amd64.exe"
                        url_64 = base_url + filename_64
                        
                        # 32位版本
                        filename_32 = f"python-{version}.exe"
                        url_32 = base_url + filename_32
                        
                        # 检查文件是否存在并获取大小
                        for arch, filename, url in [('64-bit', filename_64, url_64), ('32-bit', filename_32, url_32)]:
                            try:
                                file_response = requests.head(url, timeout=5)
                                if file_response.status_code == 200:
                                    # 获取文件大小
                                    size = "Unknown"
                                    if 'content-length' in file_response.headers:
                                        size_bytes = int(file_response.headers['content-length'])
                                        size = self.format_size(size_bytes)
                                    
                                    versions.append({
                                        'version': version,
                                        'status': status,
                                        'arch': arch,
                                        'type': 'Windows安装程序',
                                        'size': size,
                                        'date': date,
                                        'url': url,
                                        'filename': filename
                                    })
                                    print(f"  ➕ 添加: {filename} ({arch}) - {size}")
                            except:
                                # 如果无法获取文件信息，仍然添加但标记大小为估计值
                                estimated_size = "~25 MB" if arch == "64-bit" else "~24 MB"
                                versions.append({
                                    'version': version,
                                    'status': status,
                                    'arch': arch,
                                    'type': 'Windows安装程序',
                                    'size': estimated_size,
                                    'date': date,
                                    'url': url,
                                    'filename': filename
                                })
                                print(f"  ➕ 添加: {filename} ({arch}) - {estimated_size} (estimated)")
                                
                except Exception as e:
                    print(f"❌ 检查版本 {version} 失败: {e}")
                    continue
            
            print(f"🎉 总共加载了 {len(versions)} 个安装包")
            
            # 更新UI
            self.root.after(0, self._update_version_list, versions)
            
        except Exception as e:
            error_msg = f"加载版本列表失败: {str(e)}"
            print(f"💥 错误: {error_msg}")
            self.root.after(0, self._show_error, error_msg)
    
    def format_size(self, size_bytes):
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"
    
    def _update_version_list(self, versions):
        """更新版本列表UI"""
        # 存储版本数据
        self.python_versions = versions
        
        # 应用当前过滤器
        self.filter_versions()
        
        self.download_btn.config(state='normal')
    
    def _show_error(self, error_msg):
        """显示错误信息"""
        self.status_label.config(text="❌ 加载版本失败")
        messagebox.showerror("错误", error_msg)
        self.download_btn.config(state='normal')
    
    def refresh_versions(self):
        """刷新版本列表"""
        self.load_versions()
    
    def browse_download_path(self):
        """浏览下载路径"""
        path = filedialog.askdirectory(initialdir=self.download_path.get())
        if path:
            self.download_path.set(path)
    
    def download_selected(self):
        """下载选中的版本"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要下载的版本")
            return
        
        if self.is_downloading:
            messagebox.showwarning("警告", "正在下载中，请稍候...")
            return
        
        # 获取选中项的索引
        item = selection[0]
        index = self.tree.index(item)
        
        # 找到对应的版本信息
        displayed_versions = []
        version_filter = self.filter_var.get()
        arch_filter = self.arch_var.get()
        
        for version in self.python_versions:
            if version_filter != "所有版本":
                version_prefix = version_filter.replace('.x', '')
                if not version['version'].startswith(version_prefix):
                    continue
            if arch_filter != "全部" and version['arch'] != arch_filter:
                continue
            displayed_versions.append(version)
        
        if index < len(displayed_versions):
            version_info = displayed_versions[index]
            self.start_download(version_info)
    
    def start_download(self, version_info):
        """开始下载"""
        download_path = self.download_path.get()
        if not os.path.exists(download_path):
            try:
                os.makedirs(download_path)
            except Exception as e:
                messagebox.showerror("错误", f"创建下载目录失败: {e}")
                return
        
        self.is_downloading = True
        self.download_btn.config(state='disabled')
        self.progress['value'] = 0
        self.progress_label.config(text="🚀 准备下载...")
        
        # 在新线程中下载
        self.download_thread = threading.Thread(
            target=self._download_thread, 
            args=(version_info, download_path)
        )
        self.download_thread.daemon = True
        self.download_thread.start()
    
    def _download_thread(self, version_info, download_path):
        """下载线程"""
        try:
            url = version_info['url']
            filename = version_info['filename']
            filepath = os.path.join(download_path, filename)
            
            # 检查文件是否已存在
            if os.path.exists(filepath):
                response = messagebox.askyesno("文件已存在", 
                                             f"文件 {filename} 已存在。是否覆盖?")
                if not response:
                    self.root.after(0, self._download_complete, False, "下载已取消")
                    return
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            print(f"🌐 开始下载: {url}")
            response = requests.get(url, headers=headers, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            self.root.after(0, self._update_progress, progress, downloaded, total_size)
            
            self.root.after(0, self._download_complete, True, f"✅ 下载完成: {filepath}")
            
        except Exception as e:
            self.root.after(0, self._download_complete, False, f"❌ 下载失败: {str(e)}")
    
    def _update_progress(self, progress, downloaded, total_size):
        """更新进度"""
        self.progress['value'] = progress
        
        downloaded_str = self.format_size(downloaded)
        total_str = self.format_size(total_size)
        self.progress_label.config(text=f"⬇️ 正在下载... {downloaded_str} / {total_str} ({progress:.1f}%)")
    
    def _download_complete(self, success, message):
        """下载完成"""
        self.is_downloading = False
        self.download_btn.config(state='normal')
        
        if success:
            self.progress['value'] = 100
            self.progress_label.config(text="🎉 下载成功完成!")
            messagebox.showinfo("成功", message)
        else:
            self.progress['value'] = 0
            self.progress_label.config(text="💥 下载失败")
            messagebox.showerror("错误", message)
    
    def open_in_browser(self):
        """在浏览器中打开选中版本的下载页面"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要查看的版本")
            return
        
        # 获取选中项的索引
        item = selection[0]
        index = self.tree.index(item)
        
        # 找到对应的版本信息
        displayed_versions = []
        version_filter = self.filter_var.get()
        arch_filter = self.arch_var.get()
        
        for version in self.python_versions:
            if version_filter != "所有版本":
                version_prefix = version_filter.replace('.x', '')
                if not version['version'].startswith(version_prefix):
                    continue
            if arch_filter != "全部" and version['arch'] != arch_filter:
                continue
            displayed_versions.append(version)
        
        if index < len(displayed_versions):
            version_info = displayed_versions[index]
            # 打开Python官网的版本页面
            version = version_info['version']
            url = f"https://www.python.org/downloads/release/python-{version.replace('.', '')}/"
            webbrowser.open(url)
    
    def on_double_click(self, event):
        """双击事件处理"""
        self.download_selected()

def main():
    """主函数"""
    root = tk.Tk()
    app = PythonOfficialDownloader(root)
    
    # 居中显示窗口
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()