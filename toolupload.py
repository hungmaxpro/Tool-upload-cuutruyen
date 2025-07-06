import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
import time
import sys
import subprocess
from urllib.parse import urlparse
import webbrowser

# ===================================================================
# KHỐI KIỂM TRA VÀ TỰ ĐỘNG CÀI ĐẶT THƯ VIỆN
# ===================================================================
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Thông báo", "Phát hiện chưa có thư viện cần thiết.\n"
                                     "Vui lòng chờ trong giây lát để tool tự động cài đặt.")
    try:
        creation_flags = 0
        if sys.platform == "win32":
            creation_flags = subprocess.CREATE_NO_WINDOW
        
        # Cài đặt cả hai thư viện nếu thiếu
        subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium", "webdriver-manager"], creationflags=creation_flags)
        
        messagebox.showinfo("Thành công", "Đã cài đặt thư viện thành công!\n"
                                          "Vui lòng đóng và chạy lại ứng dụng.")
    except Exception as e:
        messagebox.showerror("Lỗi cài đặt", f"Không thể tự động cài đặt. Lỗi: {e}\n"
                                             "Vui lòng mở Command Prompt và gõ 'pip install selenium webdriver-manager'")
    finally:
        sys.exit()

# === HÀM TÌM KIẾM THƯ MỤC CHƯƠNG ===
def find_chapter_folder(root_path, chapter_num):
    chapter_num_str = str(chapter_num)
    possible_names = [f"chapter-{chapter_num_str}",f"chuong-{chapter_num_str}",f"chap-{chapter_num_str}",f"chapter {chapter_num_str}",f"chuong {chapter_num_str}",f"chap {chapter_num_str}",f"chapter{chapter_num_str}",f"chuong{chapter_num_str}",f"chap{chapter_num_str}",chapter_num_str]
    try:
        sub_dirs = [d for d in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, d))]
        for dir_name in sub_dirs:
            if dir_name.lower() in possible_names:
                return os.path.join(root_path, dir_name)
    except FileNotFoundError: return None
    return None

# ===================================================================
# HÀM LOGIC UPLOAD
# ===================================================================
def batch_upload_logic(login_info, chapter_info, status_label, upload_button):
    # ... (Khai báo biến)
    USERNAME = login_info['username']
    PASSWORD = login_info['password']
    LOGIN_URL = login_info['login_url']
    UPLOAD_URL = chapter_info['upload_url']
    ROOT_FOLDER_PATH = chapter_info['root_folder']
    START_CHAPTER = chapter_info['start_num']
    END_CHAPTER = chapter_info['end_num']

    driver = None
    try:
        status_label.config(text="Trạng thái: Đang kiểm tra/tải về driver...", fg="blue")
        
        # === KHỞI ĐỘNG DRIVER TỰ ĐỘNG ===
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        # =============================================
        
        driver.implicitly_wait(10)

        # ... (logic đăng nhập và upload )
        status_label.config(text=f"Trạng thái: Đang đăng nhập tại {LOGIN_URL}...")
        driver.get(LOGIN_URL)
        ID_O_TEN_DANG_NHAP = "username"
        ID_O_MAT_KHAU = "password"
        driver.find_element(By.ID, ID_O_TEN_DANG_NHAP).send_keys(USERNAME)
        driver.find_element(By.ID, ID_O_MAT_KHAU).send_keys(PASSWORD)
        driver.find_element(By.ID, ID_O_MAT_KHAU).send_keys(Keys.RETURN)
        time.sleep(7)

        status_label.config(text="Trạng thái: Đang 'làm nóng' trang upload...")
        first_chap_folder = find_chapter_folder(ROOT_FOLDER_PATH, START_CHAPTER)
        if first_chap_folder and any(f.endswith(('.jpg', '.jpeg', '.png')) for f in os.listdir(first_chap_folder)):
            driver.get(UPLOAD_URL)
            time.sleep(2)
            first_image = sorted([os.path.join(first_chap_folder, f) for f in os.listdir(first_chap_folder) if f.endswith(('.jpg', '.jpeg', '.png'))])[0]
            try:
                driver.find_element(By.ID, "fileInput").send_keys(first_image)
            except Exception as e:
                print(f"Lỗi dự kiến trong lúc làm nóng (có thể bỏ qua): {e}")
            status_label.config(text="Trạng thái: Chờ trang ổn định...")
            time.sleep(5)

        total_chapters = END_CHAPTER - START_CHAPTER + 1
        for i, chapter_num in enumerate(range(START_CHAPTER, END_CHAPTER + 1)):
            current_chapter_str = str(chapter_num)
            status_label.config(text=f"Trạng thái: Chuẩn bị đăng chương {current_chapter_str} ({i+1}/{total_chapters})")
            
            current_image_folder = find_chapter_folder(ROOT_FOLDER_PATH, chapter_num)
            if current_image_folder is None:
                print(f"Bỏ qua chương {current_chapter_str}: không tìm thấy thư mục phù hợp.")
                continue

            driver.get(UPLOAD_URL)
            time.sleep(2)

            image_files = sorted([os.path.join(current_image_folder, f) for f in os.listdir(current_image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))])
            if not image_files:
                print(f"Bỏ qua chương {current_chapter_str}: thư mục không có ảnh.")
                continue
            
            chapter_number_field = driver.find_element(By.ID, "chapterNumber")
            chapter_number_field.clear()
            chapter_number_field.send_keys(current_chapter_str)
            
            status_label.config(text=f"Trạng thái: Đang gửi {len(image_files)} ảnh...")
            file_input = driver.find_element(By.ID, "fileInput")
            file_input.send_keys("\n".join(image_files))
            
            wait_time = 5 + (len(image_files) * 1.0)
            status_label.config(text=f"Trạng thái: Chờ xử lý ảnh trong {wait_time:.1f} giây...")
            time.sleep(wait_time)
            
            submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Thêm chương')]")
            driver.execute_script("arguments[0].click();", submit_button)
            
            status_label.config(text=f"Trạng thái: Đã gửi xong chương {current_chapter_str}. Chờ 5 giây...", fg="orange")
            time.sleep(5)

        status_label.config(text="Trạng thái: HOÀN TẤT TOÀN BỘ!", fg="green")
        messagebox.showinfo("Hoàn tất", f"Đã đăng xong các chương từ {START_CHAPTER} đến {END_CHAPTER}!")

    except Exception as e:
        error_message = f"Lỗi nghiêm trọng: {str(e)}"
        status_label.config(text=f"Trạng thái: {error_message}", fg="red")
        messagebox.showerror("Đã xảy ra lỗi", error_message)
    finally:
        if driver:
            driver.quit()
        upload_button.config(state=tk.NORMAL)

# ===================================================================
# PHẦN GIAO DIỆN (GUI) 
# ===================================================================
class App:
    def __init__(self, root):
        self.root = root
        root.title("Tool Upload Truyện Tự Động (vPro)")
        root.geometry("550x480")
        login_frame = tk.LabelFrame(root, text="Thông Tin Đăng Nhập", padx=10, pady=10)
        login_frame.pack(padx=10, pady=10, fill="x")
        tk.Label(login_frame, text="Tên đăng nhập:").grid(row=0, column=0, sticky="w", pady=2)
        self.username_entry = tk.Entry(login_frame, width=50)
        self.username_entry.grid(row=0, column=1, sticky="w")
        tk.Label(login_frame, text="Mật khẩu:").grid(row=1, column=0, sticky="w", pady=2)
        self.password_entry = tk.Entry(login_frame, show="*", width=50)
        self.password_entry.grid(row=1, column=1, sticky="w")
        chapter_frame = tk.LabelFrame(root, text="Thông Tin Đăng Chương Hàng Loạt", padx=10, pady=10)
        chapter_frame.pack(padx=10, pady=10, fill="x")
        tk.Label(chapter_frame, text="Link Đăng Chương Mới:").grid(row=0, column=0, columnspan=2, sticky="w", pady=2)
        self.upload_url_entry = tk.Entry(chapter_frame, width=70)
        self.upload_url_entry.grid(row=1, column=0, columnspan=2, sticky="w")
        tk.Label(chapter_frame, text="Thư mục gốc chứa chương:").grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 2))
        self.folder_path_label = tk.Label(chapter_frame, text="Chưa chọn thư mục...", fg="grey", anchor='w')
        self.folder_path_label.grid(row=4, column=0, columnspan=2, sticky="w")
        tk.Button(chapter_frame, text="Chọn Thư Mục Gốc", command=self.select_folder).grid(row=3, column=0, columnspan=2, pady=5)
        tk.Label(chapter_frame, text="Đăng từ chương số:").grid(row=5, column=0, sticky="w", pady=(10, 2))
        self.start_chapter_entry = tk.Entry(chapter_frame, width=10)
        self.start_chapter_entry.grid(row=5, column=1, sticky="w", pady=(10, 2))
        tk.Label(chapter_frame, text="Đến chương số:").grid(row=6, column=0, sticky="w", pady=2)
        self.end_chapter_entry = tk.Entry(chapter_frame, width=10)
        self.end_chapter_entry.grid(row=6, column=1, sticky="w")
        self.upload_button = tk.Button(root, text="BẮT ĐẦU ĐĂNG HÀNG LOẠT", font=("Helvetica", 12, "bold"), bg="darkred", fg="white", command=self.start_upload)
        self.upload_button.pack(pady=10, fill="x", padx=10, ipady=5)
        
        credit_frame = tk.Frame(root)
        credit_frame.pack(pady=5)
        tk.Label(credit_frame, text="credit: ").pack(side=tk.LEFT)
        link = tk.Label(credit_frame, text="https://www.facebook.com/odaycoduong/", fg="blue", cursor="hand2")
        link.pack(side=tk.LEFT)
        link.bind("<Button-1>", lambda e: self.open_link("https://www.facebook.com/odaycoduong/"))
        tk.Label(credit_frame, text=" donate MB bank: 0345279983").pack(side=tk.LEFT)
        
        self.status_label = tk.Label(root, text="Trạng thái: Sẵn sàng", bd=1, relief=tk.SUNKEN, anchor='w')
        self.status_label.pack(side=tk.BOTTOM, fill="x")

    def open_link(self, url):
        webbrowser.open_new(url)

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path_label.config(text=folder_selected, fg="black")

    def start_upload(self):
        upload_url = self.upload_url_entry.get()
        if not upload_url:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Link Đăng Chương Mới!")
            return
        try:
            parsed_url = urlparse(upload_url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            login_url = f"{base_url}/login"
        except Exception:
            messagebox.showerror("Lỗi", "Link Đăng Chương Mới không hợp lệ!")
            return
        login_info = {"username": self.username_entry.get(), "password": self.password_entry.get(), "login_url": login_url}
        try:
            chapter_info = { "upload_url": upload_url, "root_folder": self.folder_path_label.cget("text"), "start_num": int(self.start_chapter_entry.get()), "end_num": int(self.end_chapter_entry.get()) }
        except ValueError:
            messagebox.showwarning("Lỗi", "Số chương phải là dạng số nguyên!")
            return
        if not login_info['username'] or not login_info['password'] or "Chưa chọn" in chapter_info['root_folder']:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ tất cả các trường!")
            return
        if chapter_info['start_num'] > chapter_info['end_num']:
            messagebox.showwarning("Lỗi", "Số chương bắt đầu không thể lớn hơn số chương kết thúc!")
            return
        self.upload_button.config(state=tk.DISABLED)
        threading.Thread(target=batch_upload_logic, args=(login_info, chapter_info, self.status_label, self.upload_button)).start()


if __name__ == "__main__":
    app_root = tk.Tk()
    app = App(app_root)
    app_root.mainloop()
