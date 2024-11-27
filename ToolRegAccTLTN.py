import os

try:
    import requests
    from bs4 import BeautifulSoup
    import random
except ImportError:
    os.system("pip install requests")
    os.system("pip install beautifulsoup4")
    import requests
    from bs4 import BeautifulSoup
    import random


# Danh sách các họ, tên đệm và tên chính phổ biến
ho = [
    "Nguyen",
    "Tran",
    "Le",
    "Pham",
    "Hoang",
    "Bui",
    "Vo",
    "Do",
    "Mai",
    "Dang",
    "Kim",
    "Vu",
    "Ngo",
    "Truong",
    "Dinh",
    "Than",
]
ten_dem = [
    "Van",
    "Thi",
    "Minh",
    "Quoc",
    "Anh",
    "Duy",
    "Ngoc",
    "Huu",
    "Gia",
    "Thanh",
    "Phuong",
    "Xuan",
    "Thao",
    "Bich",
    "Khanh",
]
ten_chinh = [
    "Hung",
    "An",
    "Binh",
    "Lan",
    "Hoa",
    "Trang",
    "Khang",
    "Tu",
    "Duc",
    "Hien",
    "Linh",
    "Nhi",
    "Quynh",
    "Vu",
    "Vy",
    "Phat",
    "Nhan",
]


def random_ten():
    """Random hóa tên."""
    return f"{random.choice(ho)} {random.choice(ten_dem)} {random.choice(ten_chinh)}"


def random_email_alias(base_email):
    """Random hóa email dạng alias."""
    return f"{base_email}+a{random.randint(10000, 99999999)}@gmail.com"


def random_sdt():
    """Random hóa số điện thoại."""
    return f"0{random.randint(100000000, 999999999)}"


# Người dùng nhập số lượng tài khoản cần tạo và email cơ bản
so_luong_tai_khoan = int(input("Nhập số lượng tài khoản cần tạo: "))
base_email = input("Nhập email Google cơ bản (chỉ phần trước @gmail.com): ")
code_ref = int(input("Code REF: "))

# Khởi tạo session requests
session = requests.Session()

# Thực hiện vòng lặp để tạo tài khoản
so_tai_khoan_tao = 0
ref_url = f"https://tailieuthi.net/?ref={code_ref}"
try:
    response_ref = session.get(ref_url)
    response_ref.raise_for_status()
    print(f"Đã ghé qua link giới thiệu: {ref_url}")
except requests.exceptions.RequestException as e:
    print("Không thể ghé qua link giới thiệu:", e)
    # Thử lại nếu không truy cập được
while so_tai_khoan_tao < so_luong_tai_khoan:
    # Bước 1: Ghé qua link giới thiệu

    # Bước 2: Lấy CSRF Token
    url_get = "https://tailieuthi.net/register"
    try:
        response = session.get(url_get)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Không thể truy cập trang đăng ký:", e)
        continue

    # Phân tích token từ HTML
    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("input", {"name": "_token"})["value"]
    # print("CSRF Token đã lấy:", csrf_token)

    # Bước 3: Chuẩn bị dữ liệu đăng ký
    url_post = "https://tailieuthi.net/register"
    payload = {
        "_token": csrf_token,
        "name": random_ten(),
        "username": f"zuser_{random.randint(10000, 99999)}",
        "email": random_email_alias(base_email),
        "user_phone": random_sdt(),
        "password": "Ducanhbg123@",
        "password_confirmation": "Ducanhbg123@",
        "user_type": "eyJpdiI6Ild5M2hwb1B5VGdyQnF3NWZlRWMzOXc9PSIsInZhbHVlIjoiK1lWdmYxS1ZHTEFwcjkxcWJaRFA0UT09IiwibWFjIjoiMDZlNDlkYjQwOTUzN2M4MGFiNDBlNGY3MjIwZmY3MmIzN2ZjOTZiMzdjMzBmZGQxNTZiMTU1MGI2OTJkM2I1ZCIsInRhZyI6IiJ9",
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Referer": "https://tailieuthi.net/register",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://tailieuthi.net",
    }

    # Bước 4: Gửi yêu cầu đăng ký
    try:
        response_post = session.post(url_post, data=payload, headers=headers)
        if response_post.status_code == 200:
            print(
                f"[{so_tai_khoan_tao+1}/{so_luong_tai_khoan}] Đăng ký thành công! Email: {payload['email']}"
            )
            so_tai_khoan_tao += 1
        else:
            print(f"Lỗi đăng ký! Mã phản hồi: {response_post.status_code}")
    except requests.exceptions.RequestException as e:
        print("Lỗi khi gửi yêu cầu đăng ký:", e)

print(f"\nĐã tạo xong {so_tai_khoan_tao}/{so_luong_tai_khoan} tài khoản.")
