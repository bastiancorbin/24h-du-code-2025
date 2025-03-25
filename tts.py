from kokoro import KPipeline
import soundfile as sf
import torch

def generate_audio(langue, text, speed):

    if(langue == "en"):
        pipeline = KPipeline(lang_code='a')
        voice = 'am_michael'
    elif(langue == "fr"):
        pipeline = KPipeline(lang_code='f')
        voice = 'im_nicola'

    text = text.replace("\n", " ")

    generator = pipeline(text, voice=voice, speed=speed)
    for i, (gs, ps, audio) in enumerate(generator):
        sf.write('static/audio/response.wav', audio, 24000)