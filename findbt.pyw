import os, re, webbrowser, requests, base64
import customtkinter as ctk
import tkinter.ttk as ttk
from tkinter import messagebox
import threading

GITHUB_REPO = "Songjag/LTO-UTC"
GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}/contents"

def extract_comment(line, ext):
    """Lấy phần comment trong một dòng code."""
    if ext == ".py":
        if "#" in line:
            return line.split("#", 1)[1].strip()
    elif ext in (".c", ".cpp", ".h"):
        if "//" in line:
            return line.split("//", 1)[1].strip()
        if "/*" in line and "*/" in line:
            return line.split("/*", 1)[1].split("*/", 1)[0].strip()
    return None

def get_base_folders():
    """Lấy thư mục chứa script và 2 thư mục python, c."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    folders = {
        "python": os.path.join(script_dir, "python"),
        "c": os.path.join(script_dir, "c")
    }
    
    # Tạo thư mục nếu chưa tồn tại
    for path in folders.values():
        os.makedirs(path, exist_ok=True)
    
    return folders

def download_file_from_github(file_url, local_path):
    """Tải file từ GitHub về local."""
    try:
        response = requests.get(file_url)
        response.raise_for_status()
        
        # GitHub API trả về file dạng base64
        content = response.json()
        if 'content' in content:
            file_content = base64.b64decode(content['content']).decode('utf-8')
            
            # Tạo thư mục cha nếu chưa tồn tại
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Ghi file
            with open(local_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            return True
        return False
    except Exception as e:
        print(f"Lỗi tải file {file_url}: {e}")
        return False

def sync_folder_from_github(github_path, local_base_path, folder_name, progress_callback=None):
    """Đồng bộ một thư mục từ GitHub về local."""
    try:
        url = f"{GITHUB_API}/{github_path}"
        response = requests.get(url)
        response.raise_for_status()
        
        items = response.json()
        total_files = 0
        downloaded = 0
        
        # Đếm số file cần tải
        for item in items:
            if item['type'] == 'file':
                ext = os.path.splitext(item['name'])[1]
                if ext in ['.py', '.c', '.cpp', '.h']:
                    total_files += 1
        
        # Tải các file
        for item in items:
            if item['type'] == 'file':
                ext = os.path.splitext(item['name'])[1]
                if ext in ['.py', '.c', '.cpp', '.h']:
                    # Lấy đường dẫn tương đối
                    rel_path = item['path'].replace(f"{folder_name}/", "")
                    local_path = os.path.join(local_base_path, rel_path)
                    
                    if download_file_from_github(item['url'], local_path):
                        downloaded += 1
                        if progress_callback:
                            progress_callback(downloaded, total_files, item['name'])
            
            elif item['type'] == 'dir':
                # Đệ quy tải thư mục con
                sync_folder_from_github(item['path'], local_base_path, folder_name, progress_callback)
        
        return downloaded
    except Exception as e:
        print(f"Lỗi đồng bộ {github_path}: {e}")
        return 0

def sync_from_github():
    """Đồng bộ code từ GitHub."""
    sync_btn.configure(state="disabled", text="Đang đồng bộ...")
    progress_label.configure(text="Đang kết nối đến GitHub...")
    
    def sync_thread():
        try:
            folders = get_base_folders()
            total_downloaded = 0
            
            # Đồng bộ thư mục python
            if "python" in folders:
                progress_label.configure(text="📥 Đang tải thư mục python...")
                main.update()
                
                def python_progress(current, total, filename):
                    progress_label.configure(
                        text=f"📥 Python: {current}/{total} - {filename}"
                    )
                    main.update()
                
                downloaded = sync_folder_from_github("python", folders["python"], "python", python_progress)
                total_downloaded += downloaded
            
            # Đồng bộ thư mục c
            if "c" in folders:
                progress_label.configure(text="📥 Đang tải thư mục c...")
                main.update()
                
                def c_progress(current, total, filename):
                    progress_label.configure(
                        text=f"📥 C: {current}/{total} - {filename}"
                    )
                    main.update()
                
                downloaded = sync_folder_from_github("c", folders["c"], "c", c_progress)
                total_downloaded += downloaded
            
            # Hoàn thành
            progress_label.configure(
                text=f"✅ Đã tải {total_downloaded} file từ GitHub!"
            )
            messagebox.showinfo("Thành công", f"Đã đồng bộ {total_downloaded} file từ GitHub!")
            
        except Exception as e:
            progress_label.configure(text=f"❌ Lỗi: {str(e)}")
            messagebox.showerror("Lỗi", f"Không thể đồng bộ từ GitHub:\n{str(e)}")
        
        finally:
            sync_btn.configure(state="normal", text="🔄 Đồng bộ từ GitHub")
            check_folders()
    
    # Chạy trong thread riêng để không block UI
    thread = threading.Thread(target=sync_thread, daemon=True)
    thread.start()

def search_by_url(search_url):
    """Tìm file chứa URL được chỉ định."""
    if not search_url.strip():
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập URL cần tìm!")
        return []
    
    folders = get_base_folders()
    
    exts = {
        ".py": "Python",
        ".c": "C",
        ".cpp": "C++",
        ".h": "C Header"
    }
    
    results = []
    file_count = 0
    search_url_lower = search_url.strip().lower()
    
    for folder_name, folder_path in folders.items():
        if not os.path.exists(folder_path):
            continue
            
        for dirpath, _, files in os.walk(folder_path):
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in exts:
                    file_count += 1
                    path = os.path.join(dirpath, file)
                    
                    rel_path = os.path.relpath(path, folder_path)
                    
                    try:
                        with open(path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            lines = content.split('\n')
                            
                            for lineno, line in enumerate(lines, 1):
                                comment = extract_comment(line, ext)
                                if comment and search_url_lower in comment.lower():
                                    parent_dir = os.path.basename(os.path.dirname(path))
                                    if parent_dir == folder_name:
                                        parent_dir = "root"
                                    
                                    results.append({
                                        "path": path,
                                        "rel_path": rel_path,
                                        "lineno": lineno,
                                        "line": line.strip(),
                                        "type": exts[ext],
                                        "ext": ext,
                                        "content": content,
                                        "folder": folder_name,
                                        "subfolder": parent_dir,
                                        "filename": file
                                    })
                                    break
                    except Exception as e:
                        print(f"Lỗi khi đọc {path}: {e}")
    
    status_label.configure(
        text=f"Đã quét {file_count} file trong {len(folders)} thư mục, tìm thấy {len(results)} kết quả"
    )
    return results

def show_results():
    """Hiển thị kết quả tìm kiếm."""
    search_url = url_entry.get().strip()
    
    if not search_url:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập URL cần tìm!")
        return
    
    for i in tree.get_children():
        tree.delete(i)
    
    code_text.delete("1.0", "end")
    
    results = search_by_url(search_url)
    
    if not results:
        messagebox.showinfo("Thông báo", "Không tìm thấy file nào chứa URL này!")
        return
    
    for item in results:
        tree.insert(
            "", "end",
            values=(item["filename"], item["folder"], item["subfolder"], item["lineno"], item["type"]),
            tags=(item["ext"],)
        )
    
    tree.tag_configure(".py", foreground="green")
    tree.tag_configure(".c", foreground="blue")
    tree.tag_configure(".cpp", foreground="darkblue")
    tree.tag_configure(".h", foreground="purple")
    
    tree.results = results

def on_file_select(event):
    """Hiển thị nội dung file khi chọn."""
    selection = tree.selection()
    if selection and hasattr(tree, 'results'):
        idx = tree.index(selection[0])
        result = tree.results[idx]
        
        code_text.delete("1.0", "end")
        code_text.insert("1.0", result["content"])
        
        code_text.tag_remove("highlight", "1.0", "end")
        line_pos = f"{result['lineno']}.0"
        line_end = f"{result['lineno']}.end"
        code_text.tag_add("highlight", line_pos, line_end)
        code_text.tag_config("highlight", background="yellow", foreground="black")
        
        code_text.see(line_pos)
        
        file_label.configure(text=f"📄 {result['rel_path']}")

def open_file_location(event):
    """Mở thư mục chứa file."""
    selection = tree.selection()
    if selection and hasattr(tree, 'results'):
        idx = tree.index(selection[0])
        result = tree.results[idx]
        folder = os.path.dirname(result["path"])
        
        try:
            if os.name == 'nt':
                os.startfile(folder)
            elif os.name == 'posix':
                import subprocess
                if os.uname().sysname == 'Darwin':
                    subprocess.run(['open', folder])
                else:
                    subprocess.run(['xdg-open', folder])
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở thư mục: {e}")

def check_folders():
    """Kiểm tra và hiển thị thông tin thư mục."""
    folders = get_base_folders()
    
    # Đếm số file
    total_files = 0
    for folder_path in folders.values():
        if os.path.exists(folder_path):
            for dirpath, _, files in os.walk(folder_path):
                total_files += len([f for f in files if os.path.splitext(f)[1] in ['.py', '.c', '.cpp', '.h']])
    
    folder_names = ", ".join(folders.keys())
    info_label.configure(
        text=f"✅ Thư mục: {folder_names} | 📄 {total_files} files",
        text_color="green"
    )

# Tạo giao diện
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

main = ctk.CTk()
main.title("Tìm Bài Tập Qua URL + Đồng Bộ GitHub")
main.geometry("1200x750")

# Frame đồng bộ GitHub
github_frame = ctk.CTkFrame(main, fg_color="#1a1a2e")
github_frame.pack(pady=10, padx=15, fill="x")

github_label = ctk.CTkLabel(
    github_frame, 
    text=f"📦 GitHub: {GITHUB_REPO}", 
    font=("Arial", 12, "bold")
)
github_label.pack(side="left", padx=10, pady=10)

sync_btn = ctk.CTkButton(
    github_frame, 
    text="🔄 Đồng bộ từ GitHub", 
    width=150, 
    height=35,
    command=sync_from_github,
    fg_color="#0d7377",
    hover_color="#14a085"
)
sync_btn.pack(side="left", padx=10, pady=10)

progress_label = ctk.CTkLabel(
    github_frame, 
    text="Sẵn sàng đồng bộ", 
    font=("Arial", 10),
    text_color="gray"
)
progress_label.pack(side="left", padx=10, pady=10)

# Frame tìm kiếm
search_frame = ctk.CTkFrame(main)
search_frame.pack(pady=10, padx=15, fill="x")

info_label = ctk.CTkLabel(search_frame, text="Đang kiểm tra...", font=("Arial", 10))
info_label.grid(row=0, column=0, columnspan=3, pady=5)

url_label = ctk.CTkLabel(search_frame, text="🔗 Nhập URL:", font=("Arial", 14, "bold"))
url_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

url_entry = ctk.CTkEntry(
    search_frame, 
    width=600, 
    height=40,
    placeholder_text="Ví dụ: https://laptrinhonline.club/problem/basic2",
    font=("Arial", 12)
)
url_entry.grid(row=1, column=1, padx=10, pady=10)

search_btn = ctk.CTkButton(
    search_frame, 
    text="🔍 Tìm kiếm", 
    width=120, 
    height=40,
    command=show_results, 
    font=("Arial", 12, "bold"),
    fg_color="green", 
    hover_color="darkgreen"
)
search_btn.grid(row=1, column=2, padx=10, pady=10)

url_entry.bind("<Return>", lambda e: show_results())

status_label = ctk.CTkLabel(main, text="Sẵn sàng tìm kiếm...", font=("Arial", 10))
status_label.pack(pady=5)

# Container
container = ctk.CTkFrame(main)
container.pack(fill="both", expand=True, padx=15, pady=(0, 15))

# Panel trái
left_panel = ctk.CTkFrame(container, width=450)
left_panel.pack(side="left", fill="both", expand=False, padx=(0, 5))
left_panel.pack_propagate(False)

list_label = ctk.CTkLabel(left_panel, text="📋 Kết quả tìm kiếm", font=("Arial", 12, "bold"))
list_label.pack(pady=5)

tree_frame = ctk.CTkFrame(left_panel)
tree_frame.pack(fill="both", expand=True, padx=5, pady=5)

scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

tree = ttk.Treeview(
    tree_frame,
    columns=("File", "Folder", "Sub", "Line", "Type"),
    show="headings",
    yscrollcommand=scrollbar.set
)
tree.heading("File", text="📄 File")
tree.heading("Folder", text="📁 Folder")
tree.heading("Sub", text="📂 Sub")
tree.heading("Line", text="🔢")
tree.heading("Type", text="📝")

tree.column("File", width=120)
tree.column("Folder", width=60)
tree.column("Sub", width=50)
tree.column("Line", width=40)
tree.column("Type", width=60)

tree.pack(fill="both", expand=True)
scrollbar.config(command=tree.yview)

tree.bind("<<TreeviewSelect>>", on_file_select)
tree.bind("<Double-1>", open_file_location)

# Panel phải
right_panel = ctk.CTkFrame(container)
right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))

file_label = ctk.CTkLabel(right_panel, text="📄 Nội dung file", font=("Arial", 12, "bold"))
file_label.pack(pady=5)

code_frame = ctk.CTkFrame(right_panel)
code_frame.pack(fill="both", expand=True, padx=5, pady=5)

code_scrollbar = ctk.CTkScrollbar(code_frame)
code_scrollbar.pack(side="right", fill="y")

code_text = ctk.CTkTextbox(
    code_frame, 
    font=("Consolas", 11),
    yscrollcommand=code_scrollbar.set
)
code_text.pack(fill="both", expand=True)
code_scrollbar.configure(command=code_text.yview)

# Hướng dẫn
help_label = ctk.CTkLabel(
    main,
    text="💡 Nhấn 'Đồng bộ từ GitHub' để tải code mới nhất | Click để xem | Double-click để mở thư mục",
    font=("Arial", 10),
    text_color="gray"
)
help_label.pack(pady=(0, 10))

main.after(100, check_folders)

main.mainloop()