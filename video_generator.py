import os
import json
from moviepy.editor import ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip

# from moviepy.video.io.ImageSequenceClip import ImageClip
# from moviepy.video.compositing.concatenate import concatenate_videoclips
# from moviepy.video.VideoClip import TextClip
# from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
# from moviepy.audio.io.AudioFileClip import AudioFileClip
from TTS.api import TTS
from diffusers import StableDiffusionPipeline
import torch

output_dir = "assets"
os.makedirs(output_dir, exist_ok=True)

# Load models once
tts_model = TTS("tts_models/en/ljspeech/tacotron2-DDC")
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
pipe.to("cuda")

def generate_video(prompt_json):
    video_clips = []

    for idx, scene in enumerate(prompt_json['scenes']):
        image_path = f"{output_dir}/scene_{idx}.png"
        audio_path = f"{output_dir}/scene_{idx}.wav"

        # Generate image
        image = pipe(scene['imagePrompt']).images[0]
        image.save(image_path)

        # Generate audio
        tts_model.tts_to_file(text=scene['voiceOverText'], file_path=audio_path)

        # Create video clip
        image_clip = ImageClip(image_path).set_duration(5)
        audio_clip = AudioFileClip(audio_path)
        image_clip = image_clip.set_audio(audio_clip)

        # Add overlaid text
        txt_clip = TextClip(scene['overlaidText'], fontsize=30, color='white').set_position('bottom').set_duration(5)
        video = CompositeVideoClip([image_clip, txt_clip])
        video_clips.append(video)

    final_video = concatenate_videoclips(video_clips)
    final_path = f"{output_dir}/final_video.mp4"
    final_video.write_videofile(final_path, fps=24)

    return final_path
