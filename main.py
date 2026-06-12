from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# السماح لصفحة Netlify بالاتصال بالسيرفر بأمان بدون حظر CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "409686d69fmsh442fa7d8b51ad56p11af54jsn688d0038401b"
API_HOST = "://rapidapi.com"

@app.get("/")
def home():
    return {"status": "running", "message": "TikTok Downloader API is ready!"}

@app.get("/api/download")
def download_tiktok(url: str):
    # استخدام الرابط المباشر للـ API الخاص بك
    api_url = f"https://{API_HOST}/"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    # إرسال الرابط كـ Query Parameter كما يطلب الـ API تماماً
    params = {"url": url, "hd": "1"}
    
    try:
        response = requests.get(api_url, headers=headers, params=params)
        data = response.json()
        
        # فحص استجابة الـ API واستخراج رابط الفيديو النظيف
        if data and "data" in data and "play" in data["data"]:
            return {
                "success": True,
                "title": data["data"].get("title", "TikTok Video"),
                "video_url": data["data"]["play"] # رابط الفيديو بدون علامة مائية
            }
        else:
            return {
                "success": False,
                "error": "تعذر العثور على رابط الفيديو، قد يكون المقطع خاصاً أو محذوفاً"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
