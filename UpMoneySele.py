import os

try:
    import time
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import seleniumbase
except ImportError:
    os.system("pip install selenium")
    os.system("pip install seleniumbase")
    os.system("pip install time")
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import seleniumbase
    import time


# file_path = r"links.txt"
file_path = input(r"Nhập đường dẫn file chứa list danh sách link Verify: ")

# Đếm số dòng trong file
with open(file_path, "r") as file:
    urls = [line.strip() for line in file.readlines() if line.strip()]
    num_lines = len(urls)  # Đếm số dòng

print(f"Tổng LinkVeriAcc trong file: {num_lines}")
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

coin = int(input("Số tiền hiện tại của bạn: "))
timing = float(input("Thời gian chạy từng link (giây): "))
# Khởi tạo ChromeOptions
chrome_options = Options()
chrome_options.page_load_strategy = "none"
chrome_options.add_argument("--headless")  # Chạy trình duyệt không giao diện

driver = webdriver.Chrome(options=chrome_options)
# Danh sách lưu lại các link đã truy cập
remaining_urls = urls.copy()

# Xử lý các link
i = 1
for url in remaining_urls:
    try:
        driver.get(url)  # Truy cập vào link
        coin += 10  # Cộng tiền
        print(f"[{i}] - - > Success [+10$] Coin: {coin}")
        time.sleep(timing)  # Thời gian chờ
        i += 1
    except Exception as e:
        print(f"[{i}] - Lỗi khi truy cập link {url}: {e}")
        i += 1

# Cập nhật danh sách còn lại và ghi lại vào tệp sau khi xử lý xong
remaining_urls = remaining_urls[i - 1 :]  # Lọc những link đã xử lý
with open(file_path, "w") as file:
    for link in remaining_urls:
        file.write(link + "\n")

print(f"Tiền hiện tại của bạn là {coin} khi chạy {i-1} acc!")

# Đóng driver sau khi hoàn thành
driver.quit()
