from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# السماح لصفحة الموقع بالاتصال بالسيرفر بأمان
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "409686d69fmsh442fa7d8b51ad56p11af54jsn688d0038401b"
API_HOST = "://rapidapi.com"

@app.get("/api/download")
def download_tiktok(url: str):
    # الرابط الصحيح لجلب معلومات الفيديو بدون حقوق
    api_url = f"https://{API_HOST}/"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    params = {"url": url, "hd": "1"}
    
    try:
        response = requests.get(api_url, headers=headers, params=params)
        data = response.json()
        
        if data.get("code") == 0 and "data" in data:
            return {
                "success": True,
                "title": data["data"].get("title", "TikTok Video"),
                "video_url": data["data"].get("play") # رابط الفيديو بدون علامة مائية
            }
        else:
            raise HTTPException(status_code=400, detail="تعذر استخراج رابط الفيديو، تأكد من صحة الرابط")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
