from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

# Allow frontend (Vercel) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict to your Vercel domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Add this route
@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/download")
async def download_video(request: Request):
    data = await request.json()
    url = data.get("url")

    if not url:
        return {"error": "No URL provided"}

    try:
        ydl_opts = {"quiet": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = info.get("formats", [])
        download_url = None
        for f in formats:
            if f.get("ext") == "mp4" and f.get("url"):
                download_url = f["url"]
                break

        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "download_url": download_url or "No direct link found"
        }

    except Exception as e:
        return {"error": str(e)}
