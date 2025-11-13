import streamlit as st
from PIL import Image
import numpy as np
import cv2
from lp_reader.pipeline import PlateReader
from lp_reader.utils import bytes_to_bgr_image

st.set_page_config(page_title="License Plate Reader (TH/EN)", layout="centered")
st.title("อ่านป้ายทะเบียน (ไทย/อังกฤษ)")

reader = PlateReader()

tab1, tab2 = st.tabs(["อัปโหลดรูป", "ถ่ายจากกล้อง"])

with tab1:
    uploaded = st.file_uploader("อัปโหลดไฟล์รูป", type=["jpg", "jpeg", "png", "webp"])
    if uploaded:
        content = uploaded.read()
        bgr = bytes_to_bgr_image(content)
        result = reader.read(bgr)

        st.subheader("ผลลัพธ์")
        if result["candidates"]:
            for c in result["candidates"]:
                st.write(f"- {c['text']} (conf={c['confidence']:.2f}, score={c['score']:.2f})")
        else:
            st.info("ไม่พบรูปแบบที่น่าเป็นป้ายทะเบียน")

        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        st.image(rgb, caption="ภาพที่อัปโหลด", use_column_width=True)

with tab2:
    img = st.camera_input("ถ่ายภาพจากกล้อง")
    if img is not None:
        content = img.getvalue()
        bgr = bytes_to_bgr_image(content)
        result = reader.read(bgr)

        st.subheader("ผลลัพธ์")
        if result["candidates"]:
            for c in result["candidates"]:
                st.write(f"- {c['text']} (conf={c['confidence']:.2f}, score={c['score']:.2f})")
        else:
            st.info("ไม่พบรูปแบบที่น่าเป็นป้ายทะเบียน")

        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        st.image(rgb, caption="ภาพจากกล้อง", use_column_width=True)
