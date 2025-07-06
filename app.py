import streamlit as st
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import tempfile

st.title("사진 업로드")

uploaded_file = st.file_uploader("사진을 업로드하세요", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="업로드된 이미지", use_container_width=True)

    # 임시 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        tmp_file_path = tmp_file.name

    # Google Drive 업로드
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    file_drive = drive.CreateFile({'title': uploaded_file.name})
    file_drive.SetContentFile(tmp_file_path)
    file_drive.Upload()

    st.success("Google Drive에 업로드 완료!")