from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
import json
from video_generator import generate_video

app = FastAPI()

@app.get("health")
async def health():
    return "it works "

@app.post("/generate")
async def generate(prompt_file: UploadFile):
    prompt_json = json.loads(await prompt_file.read())
    video_path = generate_video(prompt_json)
    return FileResponse(video_path, media_type="video/mp4", filename="generated_video.mp4")
