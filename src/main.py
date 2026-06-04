import tkinter as tk
from tkinter import messagebox, filedialog
import yt_dlp
import os
import threading

# โค้ดสั่งให้แอปบน Mac มองเห็น FFmpeg ของ Homebrew เสมอ
import sys
os.environ["PATH"] = os.environ.get("PATH", "") + os.pathsep + "/opt/homebrew/bin" + os.pathsep + "/usr/local/bin"

# ตัวแปรสถานะควบคุมเพื่อป้องกันการกดปุ่มซ้ำตอนกำลังดาวน์โหลด
is_downloading = False

# ==========================================
# ฟังก์ชันการทำงานของระบบ
# ==========================================
def browse_path(event):
    selected_dir = filedialog.askdirectory(initialdir=path_entry.get())
    if selected_dir:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, selected_dir)

def on_download_click(event):
    # ฟังก์ชันรองรับการคลิกที่ตัวปุ่มแบบ Label
    download_video()

def download_video():
    global is_downloading
    if is_downloading: # ถ้ากำลังดาวน์โหลดอยู่ จะไม่ทำงานซ้ำ
        return
        
    url = url_entry.get()
    save_dir = path_entry.get()
    
    if not url.strip():
        status_label.config(text="⚠️ กรุณาวาง Youtube URL ก่อนครับ", fg="#FF0000")
        return
    
    if not save_dir.strip() or not os.path.exists(save_dir):
        status_label.config(text="⚠️ กรุณาระบุ Path ที่ถูกต้องครับ", fg="#FF0000")
        return
        
    status_label.config(text="⏳ กำลังดาวน์โหลด...", fg="#FFFFFF")
    
    # ล็อกสถานะปุ่มชั่วคราว เปลี่ยนเป็นสีแดงเข้ม (แสดงว่ากำลังทำงาน)
    is_downloading = True
    download_btn.config(bg="#550000", cursor="arrow")
    
    fmt = selected_format.get()
    qual = selected_quality.get()
    
    threading.Thread(target=process_download, args=(url, fmt, qual, save_dir)).start()

def process_download(url, fmt, qual, save_dir):
    download_path = os.path.join(save_dir, '%(title)s.%(ext)s')
    
    quality_map = {
        '4K': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]/best',
        '1080P': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/best',
        '720P': 'bestvideo[height<=720]+bestaudio/best[height<=720]/best',
        '480P': 'bestvideo[height<=480]+bestaudio/best[height<=480]/best'
    }
    
    ydl_opts = {
        'format': quality_map.get(qual, 'best'),
        'outtmpl': download_path,
        'quiet': True,
        'nocheckcertificate': True,
    }

    if fmt.upper() == 'MP4':
        ydl_opts['merge_output_format'] = 'mp4'
    else:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': fmt.lower()
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        window.after(0, lambda: status_label.config(text=f"🎉 สำเร็จ! ไฟล์อยู่ในโฟลเดอร์ที่เลือกแล้ว", fg="#00FF00"))
        window.after(0, lambda: url_entry.delete(0, tk.END))
    except Exception as e:
        window.after(0, lambda: status_label.config(text="❌ เกิดข้อผิดพลาด! (โปรดเช็ค Link หรือ FFmpeg)", fg="#FF0000"))
    finally:
        # ปลดล็อกปุ่มให้กลับมาเป็นสีแดงสดเมื่อทำงานเสร็จ
        window.after(0, reset_button_ui)

def reset_button_ui():
    global is_downloading
    is_downloading = False
    download_btn.config(bg="#FF0000", cursor="hand2")

# ==========================================
# ส่วนของการออกแบบหน้าต่าง GUI ตามดีไซน์ใหม่
# ==========================================
window = tk.Tk()
window.title("YouTube Downloader")
window.geometry("750x520")
window.configure(bg="#050505")
window.eval('tk::PlaceWindow . center')

selected_format = tk.StringVar(value="MP4")
selected_quality = tk.StringVar(value="1080P")

# --- ส่วนหัว (Header) ---
header_frame = tk.Frame(window, bg="#050505")
header_frame.pack(anchor="w", padx=40, pady=(30, 20))

title_main = tk.Label(header_frame, text="YOUTUBE\nDOWNLOADER", font=("Helvetica", 36, "bold"), fg="#FF0000", bg="#050505", justify="left")
title_main.pack(side="left", anchor="sw")

title_sub = tk.Label(header_frame, text="BY PFC. BANK", font=("Helvetica", 14, "bold"), fg="#FF0000", bg="#050505")
title_sub.pack(side="left", anchor="sw", padx=(10, 0), pady=(0, 6))

# --- ฟังก์ชันสร้างแถวข้อมูล (URL & Path) ---
def create_input_row(label_text, default_value=""):
    row_frame = tk.Frame(window, bg="#050505")
    row_frame.pack(fill="x", padx=40, pady=8)
    
    tk.Label(row_frame, text=label_text, font=("Helvetica", 16, "bold"), fg="#FFFFFF", bg="#050505", width=12, anchor="w").pack(side="left")
    
    entry_border = tk.Frame(row_frame, bg="#FF0000", bd=1)
    entry_border.pack(side="left", fill="x", expand=True)
    
    entry = tk.Entry(entry_border, font=("Helvetica", 13), bg="#050505", fg="#FFFFFF", insertbackground="#FF0000", relief="flat")
    entry.pack(fill="both", expand=True, padx=1, pady=1)
    if default_value:
        entry.insert(0, default_value)
    return entry

url_entry = create_input_row("Youtube URL")

# --- ส่วนเลือก Format และ Quality ---
def create_option_group(label_text, options_list, variable):
    row_frame = tk.Frame(window, bg="#050505")
    row_frame.pack(fill="x", padx=40, pady=8)
    
    tk.Label(row_frame, text=label_text, font=("Helvetica", 16, "bold"), fg="#FFFFFF", bg="#050505", width=12, anchor="w").pack(side="left")
    
    buttons = []
    def update_ui():
        for val, border, lbl in buttons:
            if variable.get() == val:
                lbl.config(bg="#FF0000", fg="#FFFFFF")
            else:
                lbl.config(bg="#050505", fg="#FF0000")
                
    for opt in options_list:
        opt_border = tk.Frame(row_frame, bg="#FF0000")
        opt_border.pack(side="left", padx=(0, 15))
        
        opt_lbl = tk.Label(opt_border, text=opt, font=("Helvetica", 13), width=6, pady=4, cursor="hand2")
        opt_lbl.pack(padx=1, pady=1)
        
        opt_lbl.bind("<Button-1>", lambda e, val=opt: (variable.set(val), update_ui()))
        buttons.append((opt, opt_border, opt_lbl))
    update_ui()

create_option_group("File Type", ["MP4", "MOV", "WMV"], selected_format)
create_option_group("Quality", ["4K", "1080P", "720P", "480P"], selected_quality)

# --- ส่วนรับ Path ---
default_path = os.path.join(os.path.expanduser('~'), 'Downloads')
path_entry = create_input_row("Path", default_path)
path_entry.bind("<Double-Button-1>", browse_path)

# --- แถบล่างสุด: ปุ่ม Download สีแดงสด และข้อความสถานะ ---
action_frame = tk.Frame(window, bg="#050505")
action_frame.pack(fill="x", padx=40, pady=(25, 0))

# *** เปลี่ยนเป็น tk.Label เพื่อแก้ปัญหาเรื่องสีบน Mac ให้เป็นสีแดงสดตามภาพต้นฉบับสำเร็จค่ะ ***
download_btn = tk.Label(
    action_frame, 
    text="Download", 
    font=("Helvetica", 15, "bold"), 
    bg="#FF0000", # แดงสดเต็มพื้นที่
    fg="#FFFFFF", # ตัวหนังสือสีขาวเด่นชัด
    padx=30,
    pady=8,
    cursor="hand2"
)
download_btn.pack(side="left")
download_btn.bind("<Button-1>", on_download_click) # ผูกฟังก์ชันคลิกให้ใช้งานได้เหมือนปุ่มปกติ

status_label = tk.Label(action_frame, text="*ดับเบิลคลิกที่ช่อง Path เพื่อเปลี่ยนโฟลเดอร์ได้ครับ", font=("Helvetica", 11), bg="#050505", fg="#888888")
status_label.pack(side="left", padx=20)

# --- Footer ---
footer = tk.Label(window, text="License by Thatthap Tientavorn 2026.", font=("Helvetica", 10), bg="#050505", fg="#555555")
footer.pack(side="bottom", anchor="e", padx=20, pady=10)

window.mainloop()