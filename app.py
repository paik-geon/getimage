import streamlit as st
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import tempfile
import json

FOLDER_ID = "1rOJG4knmnlOruo0j720UMdRaqV8bVP1L"

# credentials.json을 임시 생성
with open("temp_credentials.json", "w") as f:
    f.write(st.secrets["GOOGLE_SERVICE_KEY"])
try:
    creds = json.loads(st.secrets["GOOGLE_SERVICE_KEY"])
    st.write("✅ client_email:", creds["client_email"])
except Exception as e:
    st.error("❌ st.secrets 로딩 실패: " + str(e))

# PyDrive2 인증
def google_drive_auth():
    gauth = GoogleAuth()
    gauth.settings["client_config_backend"] = "service"
    gauth.settings["service_config"] = {
        "client_json_file_path": "temp_credentials.json"
    }
    gauth.ServiceAuth()
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
