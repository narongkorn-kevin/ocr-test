## โครงการอ่านป้ายทะเบียน (Thai/EN) จากกล้องหรือรูปภาพ

โปรเจ็กต์นี้เป็นตัวอย่างครบชุดสำหรับอ่านป้ายทะเบียนรถจาก:
- รูปภาพ (อัปโหลดผ่าน API หรือ UI)
- กล้องเว็บแคม/กล้องโน้ตบุ๊ก (ผ่าน CLI demo หรือ UI)

สถาปัตยกรรมเบื้องต้น:
- ตรวจอักขระด้วย EasyOCR (`th`, `en`) เพื่อรองรับอักษรไทยและอังกฤษ
- กรองข้อความด้วยกฎ/regex ให้เป็นรูปแบบที่มีแนวโน้มเป็นป้ายทะเบียน
- ให้บริการผ่าน FastAPI และมี UI แบบ Streamlit
- มี CLI demo สำหรับทดสอบเร็ว

หมายเหตุ: โค้ดนี้เป็น prototype ที่ให้ความสมดุลระหว่างความง่ายในการติดตั้งกับความแม่นยำ หากต้องการความแม่นยำสูงขึ้น แนะนำต่อยอดด้วยโมเดลตรวจจับป้าย (เช่น YOLO) เพื่อครอปเฉพาะบริเวณแผ่นป้าย ก่อนส่งเข้า OCR

### การติดตั้ง

ต้องการ Python 3.9+ (แนะนำ 3.10/3.11) บน macOS (รองรับ darwin 24.x)

1) สร้างและเปิดใช้งาน virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) ติดตั้ง dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

ครั้งแรกที่รัน EasyOCR จะดาวน์โหลดโมเดลอัตโนมัติ (ต้องมีอินเทอร์เน็ต)

### การใช้งานแบบ CLI (ทดสอบเร็ว)

อ่านจากไฟล์รูป:
```bash
python demo.py --image /absolute/path/to/image.jpg
```

เปิดกล้องและอ่านแบบเรียลไทม์:
```bash
python demo.py --camera 0
```

กด `q` เพื่อออก

### การใช้งานผ่าน API (FastAPI)

รันเซิร์ฟเวอร์:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

ทดสอบอัปโหลดรูป:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/absolute/path/to/image.jpg"
```

Swagger UI:
- เปิดเบราว์เซอร์ไปที่ `http://localhost:8000/docs`

### การใช้งานผ่าน UI (Streamlit)

```bash
streamlit run ui_streamlit.py
```

ภายใน UI:
- อัปโหลดรูป เพื่ออ่านป้ายทะเบียน
- หรือใช้กล้องถ่ายภาพครั้งเดียว (streamlit camera_input)

### โครงสร้างโปรเจ็กต์

```
.
├── app.py                # FastAPI
├── demo.py               # CLI demo (ภาพ/กล้อง)
├── ui_streamlit.py       # Streamlit UI
├── lp_reader/
│   ├── __init__.py
│   ├── ocr.py            # EasyOCR service
│   ├── patterns.py       # Plate regex + ฟังก์ชันตรวจความเป็นไปได้
│   ├── pipeline.py       # รวม OCR + คัดกรอง/ทำความสะอาดผลลัพธ์
│   └── utils.py          # ยูทิลิตี้ (อ่านไฟล์, แปลงภาพ, ฯลฯ)
├── requirements.txt
└── README.md
```

### หมายเหตุเรื่องความแม่นยำ
- Prototype นี้พึ่งพา OCR ตรงจากทั้งภาพ ซึ่งอาจอ่านสิ่งอื่นๆ ที่ไม่ใช่ป้าย ถ้าพื้นหลังวุ่นวาย
- สำหรับงานโปรดักชัน แนะนำ:
  - ใช้โมเดลตรวจจับป้าย (YOLO ฯลฯ) เพื่อตัดเฉพาะป้าย -> OCR
  - ใช้การติดตามผลลัพธ์บนวิดีโอ (temporal smoothing / majority vote)
  - เพิ่ม rules เฉพาะรูปแบบป้ายของไทย/ENG และ post-processing (เช่น map O↔0, I↔1)

### ใบอนุญาต
MIT License (อิสระในการใช้งาน/แก้ไข/แจกจ่าย)
