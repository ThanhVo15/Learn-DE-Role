# Step 1: choose specific one base image
FROM python:3.9-slim

# Step 2: Đặt thư mục làm việc trong container
WORKDIR /app

# Step 3: Sao chép file requirements.txt trước và cài đặt các depencies
# Tận dụng caching của Docker: Bước này chỉ chạy các thứ có thay đổi
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#Step 4: sao chép toàn bộ code vào hệ thống
COPY .env .env
COPY app.py app.py

# Bước 5: Chỉ định lệnh sẽ được chạy khi container khởi động
CMD ["python", "app.py"]