# E-commerce Price Scraper with Airflow

![Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-45ba4b?style=for-the-badge&logo=Playwright&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

ระบบเปรียบเทียบราคาสินค้ามือถืออัตโนมัติจากเว็บ jaymart และ advice พร้อมอัปโหลดผลลัพธ์ไปยัง Google Drive ทุกวัน

## คุณสมบัติหลัก

- ดึงข้อมูลสินค้ามือถือจาก jaymart และ advice
- เปรียบเทียบราคาสินค้าระหว่างเว็บไซต์
- บันทึกผลลัพธ์เป็นไฟล์ Excel
- อัปโหลดไปยัง Google Drive อัตโนมัติ
- ทำงานตามเวลาที่กำหนดด้วย Airflow
- พร้อมใช้งานใน Docker Container

## การติดตั้ง

1. คัดลอกโปรเจกต์

```bash
git clone https://github.com/yourusername/ecommerce-scraper.git
cd ecommerce-scraper
```

2. สร้างและรัน containers

```bash
docker-compose up -d --build
```

3. เปิด Airflow UI ที่ http://localhost:8080

- Username: admin

- Password: admin

