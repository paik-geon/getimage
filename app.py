import streamlit as st
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import tempfile

FOLDER_ID = "1rOJG4knmnlOruo0j720UMdRaqV8bVP1L"

def google_drive_auth():
    gauth = GoogleAuth()
    gauth.ServiceAuth()  # settings.yaml + credentials.json 기반 인증
    return GoogleDrive(gauth)

st.title("사진 업로드")

uploaded_file = st.file_uploader("사진을 업로드하세요", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="업로드된 이미지", use_container_width=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        tmp_file_path = tmp_file.name

    drive = google_drive_auth()
    file_drive = drive.CreateFile({
        'title': uploaded_file.name,
        'parents': [{'id': FOLDER_ID}]
    })
    file_drive.SetContentFile(tmp_file_path)
    file_drive.Upload()

    st.success("✅ Google Drive에 업로드 완료!")
