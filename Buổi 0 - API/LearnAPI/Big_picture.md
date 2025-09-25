Below is a deep‑dive primer on APIs for a budding data engineer, complete with imaginative examples and practical guidance. I’ll cover:

1. **What is an API?**
2. **API outputs (formats)**
3. **How to call an API**
4. **Common API‑related issues**
5. **Other ways to ingest data beyond APIs**

---

## 1. What Is an API?

* **API** là viết tắt của *Application Programming Interface* (Giao diện lập trình ứng dụng).
* Nó định nghĩa cách hai hệ thống (ví dụ client và server) “nói chuyện” với nhau.
* **Ví dụ tưởng tượng**: Bạn ở trong một nhà hàng (client) và gọi món với bồi bàn (API). Bồi bàn hiểu yêu cầu, truyền cho bếp (server), rồi mang món ăn (response) về cho bạn.

---

## 2. API Outputs (Các định dạng kết quả)

Khi gọi API, server có thể trả về dữ liệu ở nhiều “định dạng” khác nhau:

1. **JSON** (JavaScript Object Notation)

   ```json
   {
     "temperature": 28.5,
     "unit": "°C",
     "location": "Ho Chi Minh City"
   }
   ```
2. **XML**

   ```xml
   <weather>
     <temperature unit="°C">28.5</temperature>
     <location>Ho Chi Minh City</location>
   </weather>
   ```
3. **CSV** (comma‑separated values)

   ```
   temperature,unit,location
   28.5,°C,Ho Chi Minh City
   ```
4. **Plain Text** hoặc **HTML** (thường ít dùng cho data‑engineering)

   ```
   Current temp in HCMC is 28.5 °C
   ```

---

## 3. How to Call an API (Lấy API bằng cách gì)

1. **HTTP Methods**

   * `GET` để lấy dữ liệu
   * `POST` để tạo dữ liệu
   * `PUT/PATCH` để cập nhật
   * `DELETE` để xoá

2. **Endpoint**

   * URL nơi bạn gõ yêu cầu, ví dụ:

     ```
     https://api.openweathermap.org/data/2.5/weather
     ```

3. **Authentication**

   * **API Key**: Chuỗi ký tự do provider cấp, gắn vào query hoặc header.

     ```bash
     GET https://api.example.com/data?api_key=YOUR_KEY
     ```
   * **OAuth 2.0**: Thường dùng cho các dịch vụ cần bảo mật cao (Google, Facebook).

4. **Query Parameters**

   * Thêm vào sau dấu `?`, ví dụ:

     ```
     ?city=Hanoi&units=metric
     ```

5. **Tools & Libraries**

   * **curl** (command‑line)

     ```bash
     curl "https://api.example.com/data?city=Hanoi&api_key=KEY"
     ```
   * **Postman** (GUI để test)
   * **Python (requests)**

     ```python
     import requests

     url = "https://api.example.com/data"
     params = {"city": "Hanoi", "api_key": "YOUR_KEY"}
     resp = requests.get(url, params=params)
     data = resp.json()
     print(data)
     ```

---

## 4. Common API‑Related Issues (Các vấn đề liên quan API)

| Vấn đề                      | Mô tả                                      | Cách xử lý                                                     |
| --------------------------- | ------------------------------------------ | -------------------------------------------------------------- |
| **Rate Limiting**           | Bị giới hạn số request trên phút/giờ/ngày  | Thêm cơ chế back‑off; cache dữ liệu                            |
| **Authentication Failures** | Sai key, token hết hạn                     | Kiểm tra key, refresh token (OAuth)                            |
| **Pagination**              | Dữ liệu quá nhiều cần chia trang           | Xử dụng `page`/`limit` params, lặp qua tất cả pages            |
| **Error Handling**          | HTTP 4xx, 5xx responses                    | Bắt exception, log chi tiết, retry khi phù hợp                 |
| **Data Format Changes**     | Provider thay đổi schema (thêm/bớt trường) | Viết code linh hoạt, kiểm tra tồn tại field trước khi truy cập |
| **CORS (Frontend)**         | Browser chặn request do khác domain        | Thiết lập `Access-Control-Allow-Origin` tại server             |
| **Versioning**              | Thay đổi API không tương thích ngược       | Luôn gọi rõ version: `/v1/users` vs. `/v2/users`               |

---

## 5. Other Ways to Ingest Data (Ngoài API thì còn gì nữa?)

1. **Database Connection**

   * **JDBC/ODBC**: Kết nối trực tiếp đến SQL Server, MySQL, PostgreSQL…
   * **Example**: Dùng Python’s `psycopg2` lấy trực tiếp từ PostgreSQL.

2. **Flat Files**

   * **CSV, Parquet, JSON files** đặt trên S3/GCS/Local.
   * Dùng Spark, Pandas, hoặc Azure Data Factory để load.

3. **Message Queues / Streaming**

   * **Apache Kafka, AWS Kinesis**: Dữ liệu streaming (log, sensor data).

4. **Web Scraping**

   * Khi không có API, dùng **BeautifulSoup**, **Selenium** để ghép dữ liệu từ HTML.

5. **Third‑Party Connectors**

   * **Airflow Operators**, **Fivetran**, **Stitch**: kết nối sẵn với CRM, ERP, SaaS apps.

6. **Change Data Capture (CDC)**

   * Bắt sự kiện thay đổi trong DB (binlog, Debezium) để stream vào kho dữ liệu.

---

### Imaginative End‑to‑End Example: “Smart Café”

* **Use Case**: Tự động tổng hợp doanh thu, bình chọn món “hot” nhất.
* **API**: Quản lý order app cung cấp endpoint `GET /orders?date=2025-07-28`. Trả JSON list of orders.
* **Database**: Thông tin menu lưu trong PostgreSQL, kết nối JDBC.
* **Streaming**: Order mới gửi vào Kafka topic `orders`.
* **Ingestion Pipeline**:

  1. **Spark Streaming** đọc Kafka → tính tổng doanh thu real‑time.
  2. **Batch Job** hằng giờ gọi API để backfill đơn offline.
  3. **CDC** bắt thay đổi giá menu từ PostgreSQL, cập nhật BI dashboards.

---

### Next Steps for You

1. **Hands‑On**: Sign up for a free API (e.g. OpenWeatherMap), practice `GET`/`POST` with curl and Python.
2. **Build a Mini‑Pipeline**:

   * Ingest orders via API + Kafka.
   * Store raw JSON in S3.
   * Transform with Spark into Parquet.
   * Load into a data warehouse (e.g. PostgreSQL).
3. **Explore**: CDC tools (Debezium), orchestration (Airflow), containerize your services (Docker).

Chúc bạn học tập vui vẻ và nhanh chóng tiến lên Data Engineer! Nếu có câu hỏi cụ thể nào, cứ hỏi tiếp nhé.
