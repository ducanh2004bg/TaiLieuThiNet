import os

try:
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    import base64
    from bs4 import BeautifulSoup
except ImportError:
    os.system("pip install google-api-python-client")
    os.system("pip install google-auth-oauthlib")
    os.system("pip install beautifulsoup4")
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    import base64
    from bs4 import BeautifulSoup

path = input(r"Nhập đường dẫn chứa file 'credentials.json': ")
# Cấp quyền truy cập
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
flow = InstalledAppFlow.from_client_secrets_file(
    path,
    SCOPES,
)
creds = flow.run_local_server(port=0)

service = build("gmail", "v1", credentials=creds)


# Hàm để lấy nội dung email
def get_email_content(msg_data):
    try:
        # Kiểm tra nếu 'data' có trực tiếp trong 'body'
        if "data" in msg_data["payload"]["body"]:
            return base64.urlsafe_b64decode(msg_data["payload"]["body"]["data"]).decode(
                "utf-8"
            )

        # Nếu không, kiểm tra trong 'parts'
        elif "parts" in msg_data["payload"]:
            parts = msg_data["payload"]["parts"]
            for part in parts:
                if part["mimeType"] == "text/html" and "data" in part["body"]:
                    return base64.urlsafe_b64decode(part["body"]["data"]).decode(
                        "utf-8"
                    )
                elif part["mimeType"] == "text/plain" and "data" in part["body"]:
                    return base64.urlsafe_b64decode(part["body"]["data"]).decode(
                        "utf-8"
                    )
    except Exception as e:
        print(f"Error while decoding email content: {e}")
    return None


# Hàm để trích xuất các liên kết từ HTML
def extract_links_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    links = []
    for a_tag in soup.find_all("a", href=True):
        links.append(a_tag["href"])
    return links


# Hàm để lưu các liên kết vào tệp
def save_links_to_file(links, filename="links.txt"):
    try:
        with open(filename, "a", encoding="utf-8") as file:
            for link in links:
                file.write(link + "\n")
        print(f"Đã lưu {len(links)} liên kết vào tệp {filename}")
    except Exception as e:
        print(f"Lỗi khi lưu liên kết vào tệp: {e}")


# Lấy danh sách toàn bộ email với pagination
def get_all_emails():
    all_messages = []
    page_token = None

    while True:
        results = (
            service.users()
            .messages()
            .list(userId="me", labelIds=["CATEGORY_PERSONAL"], pageToken=page_token)
            .execute()
        )
        messages = results.get("messages", [])
        all_messages.extend(messages)

        page_token = results.get("nextPageToken")
        if not page_token:
            break  # Nếu không còn token nào nữa, thoát vòng lặp

    return all_messages


# Lấy tất cả các email
all_messages = get_all_emails()
print(f"Tổng số email lấy được: {len(all_messages)}")

# Trích xuất và lưu liên kết
all_links = []
for msg in all_messages:
    msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
    email_content = get_email_content(msg_data)
    if email_content:
        links = extract_links_from_html(email_content)
        all_links.extend(links)
        for link in links:
            print(link)

# Lưu toàn bộ liên kết vào tệp
save_links_to_file(all_links, filename="links.txt")
