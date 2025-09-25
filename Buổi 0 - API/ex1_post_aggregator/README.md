# Exercise 1: Post Aggregator

## Mục tiêu
Lấy dữ liệu từ JSONPlaceholder, đếm số post theo user, xuất CSV, và gửi bản tóm tắt qua email. Hỗ trợ nhiều client đồng thời, cache, retry, và full test suite.

## Cài đặt
```bash
python -m venv .venv
source .venv/bin/activate        # hoặc .venv\Scripts\activate trên Windows
pip install -r requirements.txt  # nếu dùng requirements.txt
# hoặc nếu xài pyproject.toml:
pip install .
pip install -r <(echo "pytest\npytest-asyncio\npython-dotenv\nmypy\nflake8")




## **Dễ (2 bài)**

### **1. Post Aggregator từ JSONPlaceholder**

**Đề bài:**
Từ API giả lập `https://jsonplaceholder.typicode.com/posts` lấy tất cả bài đăng, tính số bài mỗi user (userId), lưu kết quả thành CSV và gửi email tóm tắt (ví dụ: “User 1: 10 posts”, ...).

**API:**
`GET https://jsonplaceholder.typicode.com/posts` (không cần key)

**Expected outcome:**

* File `posts_per_user.csv` chứa hai cột: `userId`, `post_count`.
* Email gửi báo cáo summary (top 3 user có nhiều post nhất).
* Code theo OOP: có class `PostClient`, `PostAggregator`, `EmailReporter`.
* Unit test:

  * Mock API trả về sample posts, kiểm tra `PostAggregator.count_per_user()` đúng.
  * Test formatting email summary.
  * Test CSV write (có thể dùng temp file / tmpdir).

**Gợi ý mở rộng:**

* Thêm retry với exponential backoff khi gọi API thất bại.
* Có lớp `Cache` giữ kết quả cũ để không gọi lại nếu vẫn “fresh” trong cùng ngày.
