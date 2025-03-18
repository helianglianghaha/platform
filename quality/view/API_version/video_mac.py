from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.http import FileResponse
from django.http import HttpResponse
import os
import uuid
from moviepy import *
import os, re
import srt,json
import copy
from datetime import timedelta
from django.conf import settings
from django.http import StreamingHttpResponse
import zipfile
import hashlib
import asyncio
import edge_tts
import asyncio

# video_dir = r"C:\Users\Administrator\Desktop\视频处理\video"
# subtitle_dir = r"C:\Users\Administrator\Desktop\视频处理\font\output"  # 修改字幕路径
# sas_subtitle_dir=r"C:\Users\Administrator\Desktop\视频处理\font\sasFont"
# final_output = r"C:\Users\Administrator\Desktop\视频处理\final_output.mp4"  # 修改最终合成视频的存放位置
# output_dir=r"C:\Users\Administrator\Desktop\视频处理\outputVideo"
# file_dir=r"C:\Users\Administrator\Desktop\视频处理"

video_dir = r"/Users/hll/Desktop/视频处理/video"
subtitle_dir = r"/Users/hll/Desktop/视频处理/font/output"  # 修改字幕路径
sas_subtitle_dir=r"/Users/hll/Desktop/视频处理/font/sasFont"
final_output = r"/Users/hll/Desktop/视频处理/final_output.mp4"  # 修改最终合成视频的存放位置
output_dir=r"/Users/hll/Desktop/视频处理/outputVideo"
file_dir=r"/Users/hll/Desktop/视频处理"
font_path=os.path.join(os.getcwd(),'media','font','NotoSerifSC-VariableFont_wght.ttf')

from gtts import gTTS
AUDIO_SAVE_PATH = "media/tts_audio"

def musicFilesUpload(request):
    '''xmind文件上传'''
    data=[]
    req = request.FILES.get('file')
    content = {}

    #测试
    # path="/Users/hll/Desktop/git/platform/media/xmind"

    #线上
    path="/Users/hll/Desktop/git/platform/media/music"
    fileName=os.path.join(path, req.name)
    # 打开特定的文件进行二进制的写操作
    destination = open(fileName, 'wb+')
    for chunk in req.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    content["name"]=req.name
    content["url"]=fileName

    #返回状态信息
    data.append(content)
    return JsonResponse(data, safe=False)

def videoFilesUpload(request):
    '''xmind文件上传'''
    data=[]
    req = request.FILES.get('file')
    content = {}

    #测试
    # path="/Users/hll/Desktop/git/platform/media/xmind"

    #线上
    path="/Users/hll/Desktop/git/platform/media/uploads"
    fileName=os.path.join(path, req.name)
    # 打开特定的文件进行二进制的写操作
    destination = open(fileName, 'wb+')
    for chunk in req.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    content["name"]=req.name
    content["url"]=fileName

    #返回状态信息
    data.append(content)
    return JsonResponse(data, safe=False)

def get_music_list(request):
    music_directory = os.path.join(settings.MEDIA_ROOT, "music")  # 获取 media/music 目录++
    print(music_directory)
    musicList = []

    if os.path.exists(music_directory):
        for filename in os.listdir(music_directory):
            print(filename)
            if filename.endswith((".mp3", ".wav", ".ogg")):  # 只获取音频文件
                # formatted_name = os.path.splitext(filename)[0]  # 去掉文件扩展名
                file_url = os.path.join("http://127.0.0.1:8090","media","music",filename)  # 生成文件路径
                # file_url=os.path.normpath(file_url)
                musicList.append({"label": filename, "value": file_url})  # 添加到列表中

    return JsonResponse({"musicList": musicList})

# UPLOADS_DIR = os.path.join(settings.MEDIA_ROOT, 'uploads')
def add_dynamic_watermark(input_video: str, 
                          output_video: str, 
                          text="@泥鳅炖土豆",
                          fontsize=30, 
                          fontcolor="white",
                          font_path=font_path
                            ): #添加水印
    """
    使用 FFmpeg 给视频添加动态水印
    :param input_video: 输入视频文件路径
    :param output_video: 输出视频文件路径
    :param text: 水印文本
    :param fontsize: 文字大小
    :param fontcolor: 文字颜色
    """
    if os.path.exists(output_video):  # 判断文件是否存在
        os.remove(output_video)  # 删除文件
        print(f"{output_video} 已删除")
    else:
        print(f"{output_video} 不存在")

    cmd = '''ffmpeg -i "{}" -vf "drawtext=text='{}':fontfile='{}':fontcolor={}:fontsize={}:x=w*mod(t\,10)/10:y=h*mod(t\,10)/10" -c:a copy "{}"'''.format(
    input_video, text,font_path, fontcolor, fontsize, output_video)
    print('==视频新增水印==',cmd)

    print("执行命令:", cmd)
    os.system(cmd)
def get_voice_roles(request): #获取音色列表
    voices = asyncio.run(edge_tts.list_voices())
    voice_roles = []
    for v in voices:
        name = v["Name"]
        match = re.search(r'\(([^,]+), ([^)]+)\)', name)
        if match:
            formatted_name = f"{match.group(1)}-{match.group(2)}"
        else:
            formatted_name = name  # Fallback in case the format is unexpected
        
        voice_roles.append({"label": formatted_name, "value": formatted_name})
    
    return JsonResponse({"voiceRoles": voice_roles})
async def synthesize_speech(text, voice, speech_rate, file_path):
    """
    异步语音合成，支持自定义语速
    """
    # 语速处理，确保为整数
    try:
        speech_rate = int(speech_rate)  # 将语速转换为整数
    except ValueError:
        return JsonResponse({"error": "Invalid speech rate value"}, status=400)

    # 确保语速在有效范围内
    if speech_rate < -100 or speech_rate > 100:
        return JsonResponse({"error": "Speech rate must be between -100 and 100"}, status=400)

    rate_option = f"+{speech_rate}%" if speech_rate >= 0 else f"{speech_rate}%"

    tts = edge_tts.Communicate(text, voice, rate=rate_option)
    await tts.save(file_path) 
def generate_speech(request): #生成视频配音
    # 解析前端传递的 JSON 数据
    responseData = json.loads(request.body)
    print(responseData)

    text = responseData['params']['text']
    voice = responseData['params']['role']  # 语音角色（男声/女声）
    speech_rate = responseData['params']['speechRate']  # 语速（-100 ~ +100）

    print("语音角色:", voice)
    print("语速:", speech_rate)

    if not text:
        return JsonResponse({"error": "Text is required"}, status=400)

    # 生成文件名（防止特殊字符）
    safe_text = "".join(c for c in text if c.isalnum() or c in " _-").strip()
    file_path = os.path.join(os.getcwd(),AUDIO_SAVE_PATH, f"{safe_text}.mp3")

    # 先删除旧文件
    if os.path.exists(file_path):
        os.remove(file_path)

    # 生成新语音
    asyncio.run(synthesize_speech(text, voice, speech_rate, file_path))

    return JsonResponse({"audioUrl": f"http://127.0.0.1:8090/media/tts_audio/{safe_text}.mp3"})

def check_final_video(request):
    """
    检查字幕视频是否已生成
    """
    responseData=json.loads(request.body)
    video_url = responseData["videoUrl"]
    print(video_url)

    video_name=video_url.split('/')[-1]
    print(video_name)
    video_first_name=video_name.split('.')[0]

    # 生成字幕视频的路径（示例，需根据实际情况修改）
    video_path = os.path.join(os.getcwd(),'media','uploads',video_first_name,video_first_name+'_finally.mp4')
    print(video_path)
    # final_video_url = final_video_path.replace("\\", "/")  # 确保路径格式正确


    # 判断文件是否存在
    if os.path.exists(video_path):
        final_video_url=os.path.join('http://127.0.0.1:8090','media','uploads',video_first_name,video_first_name+'_finally.mp4')
        final_video_url=final_video_url.replace('\\','/')
        return JsonResponse({"exists": True, "finalVideoUrl": final_video_url})
    
    return JsonResponse({"exists": False})
def download_all_videos(request):
    zip_filename = 'videos.zip'
    zip_path = os.path.join(settings.MEDIA_ROOT, zip_filename)

    # 创建 ZIP 文件
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for folder_name in os.listdir(UPLOADS_DIR):
            folder_path = os.path.join(UPLOADS_DIR, folder_name)
            if os.path.isdir(folder_path):
                for file_name in os.listdir(folder_path):
                    if file_name.endswith('.mp4'):
                        file_path = os.path.join(folder_path, file_name)
                        zipf.write(file_path, arcname=file_name)

    # 使用 FileResponse 让 Django 负责文件流式传输
    response = FileResponse(open(zip_path, 'rb'), as_attachment=True, filename=zip_filename)

    return response
def ensure_paths(): #没有文件夹创建文件夹
    """确保所需的文件夹和文件存在，不存在则创建"""
    # 定义文件夹路径
    video_dir = "C:\\Users\\Administrator\\Desktop\\视频处理\\video"
    subtitle_dir = "C:\\Users\\Administrator\\Desktop\\视频处理\\font\\output"
    sas_subtitle_dir = "C:\\Users\\Administrator\\Desktop\\视频处理\\font\\sasFont"
    output_dir = "C:\\Users\\Administrator\\Desktop\\视频处理\\outputVideo"

    # 需要创建的文件夹列表
    folders = [video_dir, subtitle_dir, sas_subtitle_dir, output_dir]

    # 遍历文件夹路径，若不存在则创建
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            # print(f"文件夹已创建: {folder}")
        else:
            print(f"文件夹已存在: {folder}")

    # # 定义最终合成视频的存放路径（这个是文件，不是文件夹）
    # final_output = r"C:\Users\Administrator\Desktop\视频处理\final_output.mp4"

    # # 如果最终合成视频文件不存在，可以提前创建一个空文件
    # if not os.path.exists(final_output):
    #     open(final_output, 'w').close()
    #     print(f"文件已创建: {final_output}")
    # else:
    #     print(f"文件已存在: {final_output}")
def text_to_individual_srt(text, output_dir,sas_subtitle_dir, duration_per_sentence=19):# 将文本转换为多个单独的 SRT 字幕文件
    """
    将文本转换为多个单独的 SRT 字幕文件
    """
    os.makedirs(output_dir, exist_ok=True)
    sentences = [s.strip() for s in text.replace("\n", "").split("。") if s]
    
    
    for index, sentence in enumerate(sentences, start=1):
        start_time = 0.0
        end_time = start_time + duration_per_sentence
        subtitle = srt.Subtitle(
            index=index,
            start=timedelta(seconds=start_time),
            end=timedelta(seconds=end_time),
            content=sentence + "。"
        )
        filename = f"subtitle_{index:03d}.srt"
        output_srt = os.path.join(output_dir, filename)
        print('====start_time=====',start_time)
        print('====end_time=====',end_time)
        print(output_srt)
        
        with open(output_srt, "w", encoding="utf-8") as f:
            f.write(srt.compose([subtitle]))
        
        # print(f"✅ 生成：{output_srt}")
        # start_time = end_time
    # 转化所有的字幕
    subtitle_files = sorted([f for f in os.listdir(subtitle_dir) if f.endswith(".srt")], 
                            key=lambda x: int(re.search(r'\d+', x).group()))
    print(subtitle_files)
    
    print('===sas_subtitle_dir===',sas_subtitle_dir)
    
    for  i in range(len(subtitle_files)):
        srt_file = subtitle_files[i]
        
        srt_path = os.path.join(subtitle_dir, srt_file)
        ass_path = os.path.join(sas_subtitle_dir, subtitle_files[i].replace(".srt", ".ass"))
        convert_srt_to_ass(srt_path, ass_path) 
def singleText_to_individual_srt(text,video_name, duration_per_sentence=19):# 将文本转换为多个单独的 SRT 字幕文件
    """
    将文本转换为多个单独的 SRT 字幕文件
    """
    sentences = [s.strip() for s in text.replace("\n", "").split("。") if s]
    
    
    for index, sentence in enumerate(sentences, start=1):
        start_time = 0.0
        end_time = start_time + duration_per_sentence
        subtitle = srt.Subtitle(
            index=index,
            start=timedelta(seconds=start_time),
            end=timedelta(seconds=end_time),
            content=sentence + "。"
        )
        filename = f"subtitle_{video_name}.srt"
        output_dir = os.path.join(os.getcwd(), 'media', 'uploads', video_name)
        print(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        output_srt = os.path.join(output_dir, filename)
        
        with open(output_srt, "w", encoding="utf-8") as f:
            f.write(srt.compose([subtitle]))
        
        # print(f"✅ 生成：{output_srt}")
        # start_time = end_time
    # 转化所有的字幕
    ass_path = output_srt.replace(".srt", ".ass")
    convert_singleSrt_to_ass(output_srt, ass_path) 
def convert_srt_to_ass(srt_path, ass_path): #srt 字幕转sas
    """
    将 SRT 字幕转换为 ASS，并优化样式以适应视频播放。
    """
    # print(srt_path)
    # print(ass_path)
    # input()
    ass_header = """[Script Info]
                Title: Converted Subtitle
                ScriptType: v4.00+
                Collisions: Normal
                PlayDepth: 0
                Timer: 100.0000

                [V4+ Styles]
                Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing,
                Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
               Style: Default,Arial,15,&H00FFFFFF,&H000000FF,&H80000000,&H80808080,0,0,0,0,100,100,0,0,1,3,2,5,2,20,20,2,1
                [Events]
                Format: Layer, Start, End, Style, Name,BackColour, MarginL, MarginR, MarginV, Effect, Text
                """
    
    
    with open(srt_path, "r", encoding="utf-8") as srt_file, open(ass_path, "w", encoding="utf-8") as ass_file:
        ass_file.write(ass_header)
        lines = srt_file.readlines()
        i = 0
        while i < len(lines):
            if re.match(r"^\d+$", lines[i].strip()):  # 跳过索引行
                i += 1
                continue
            
            
            if "-->" in lines[i]:  # 时间轴行
                start, end = lines[i].strip().split(" --> ")
                start = start.replace(",", ".")
                end = end.replace(",", ".")
                i += 1
                # print("=======333333===")
                
                # 读取字幕内容
                content = []
                while i < len(lines) and lines[i].strip():
                    data=lines[i].strip()
                    dataList=data.split('，')
                    dataList.reverse()
                    for j in dataList:

                        j=j[0:]
                        # print(j)
                        # input()
                        # content.append(lines[i].strip())
                        ass_file.write(f"Dialogue: 0,{start},{end},Default,,&H80808080,10,50,5,0,{j}\n")
                    i += 1
                # print(content)
                # input()
                # # ass_text = r"\\N".join(content)  # 处理换行
                # ass_text = content[0].replace("，", "\\N")
                # print(ass_text) 
            i += 1
def convert_singleSrt_to_ass(srt_path, ass_path): #单条文字字幕转sas
    """
    将 SRT 字幕转换为 ASS，并优化样式以适应视频播放。
    """
    # print(srt_path)
    # print(ass_path)
    # input()
    ass_header = """[Script Info]
                Title: Converted Subtitle
                ScriptType: v4.00+
                Collisions: Normal
                PlayDepth: 0
                Timer: 100.0000

                [V4+ Styles]
                Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing,
                Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
               Style: Default,Arial,10,&H00FFFFFF,&H000000FF,&H80000000,&H80808080,0,0,0,0,100,100,0,0,1,3,2,5,2,20,20,2,1
                [Events]
                Format: Layer, Start, End, Style, Name,BackColour, MarginL, MarginR, MarginV, Effect, Text
                """
    
    
    with open(srt_path, "r", encoding="utf-8") as srt_file, open(ass_path, "w", encoding="utf-8") as ass_file:
        ass_file.write(ass_header)
        lines = srt_file.readlines()
        i = 0
        while i < len(lines):
            if re.match(r"^\d+$", lines[i].strip()):  # 跳过索引行
                i += 1
                continue
            
            
            if "-->" in lines[i]:  # 时间轴行
                start, end = lines[i].strip().split(" --> ")
                start = start.replace(",", ".")
                end = end.replace(",", ".")
                i += 1
                # print("=======333333===")
                
                # 读取字幕内容
                content = []
                while i < len(lines) and lines[i].strip():
                    data=lines[i].strip()
                    dataList=data.split('，')
                    dataList.reverse()
                    for j in dataList:
                        j=j[0:]
                        ass_file.write(f"Dialogue: 0,{start},{end},Default,,&H80808080,10,50,10,0,{j}\n")
                    i += 1
            i += 1
def add_subtitles_to_videos(video_dir, subtitle_dir,output_dir,sas_subtitle_dir): #字幕添加到文本
    """
    遍历视频目录，为所有视频合成字幕（字幕来自 subtitle_dir）
    """
    video_files = sorted([f for f in os.listdir(video_dir) if f.endswith(".mp4")])
    subtitle_files = sorted([f for f in os.listdir(subtitle_dir) if f.endswith(".srt")], 
                            key=lambda x: int(re.search(r'\d+', x).group()))
    
    n = min(len(video_files), len(subtitle_files))
    for  i in range(len(video_files)):
        video_file = video_files[i]
        subtitle_file = subtitle_files[i]
        
        video_path = os.path.join(video_dir, video_file)
        srt_path = os.path.join(subtitle_dir, subtitle_file)
        ass_path = os.path.join(sas_subtitle_dir, subtitle_file.replace(".srt", ".ass"))
        print('ass_path',ass_path)
        first_ass_path=copy.deepcopy(ass_path)
        output_video = os.path.join(output_dir, f"{os.path.splitext(video_file)[0]}_subtitled.mp4")
        # print('11111',ass_path)
        ass_path=ass_path.replace("\\", "\\\\").replace("C:", "C\:")

        print('output_video',output_video)
        print('first_ass_path',first_ass_path)

        
        convert_srt_to_ass(srt_path, first_ass_path)        
        cmd = '''ffmpeg -i \"{}\" -vf \"ass=\'{}\'\" -c:a copy \"{}\" -y'''.format(video_path,ass_path,output_video)
        print('==CMD====',cmd)
        os.system(cmd)
        print(f"✅ 合成字幕：{output_video}")
def add_single_text_to_videos(single_video_dir,singlesas_font_dir,output_dir,video_name):# 指定文案和视频合成

    singlesas_font_dir=singlesas_font_dir.replace("\\", "\\\\").replace("C:", "C\:")
    output_video = os.path.join(output_dir, f"{video_name}_single.mp4")

    cmd = '''ffmpeg -i \"{}\" -vf \"ass=\'{}\'\" -c:a copy \"{}\" -y'''.format(single_video_dir,singlesas_font_dir,output_video)
    print('==CMD====',cmd)
    os.system(cmd)
    print(f"✅ 单独合成字幕：{output_video}")
    finally_video_url=os.path.join(os.getcwd(),'media','uploads',video_name, f"{video_name}_single.mp4")
    finally_video_url=os.path.normpath(finally_video_url)
    print(finally_video_url)
    return finally_video_url
def get_videos(request):
    '''返回视频列表'''
    media_url = "http://127.0.0.1:8090/media/uploads/"
    video_dir = os.path.join(settings.MEDIA_ROOT, "uploads")

    # 确保上传目录存在
    if not os.path.exists(video_dir):
        return JsonResponse({"videos": []})

    # 获取所有视频文件
    video_files = [f for f in os.listdir(video_dir) if f.endswith((".mp4", ".avi", ".mov", ".mkv"))]

    # 生成完整的视频 URL 列表
    video_list = [{"name": video, "url": f"{media_url}{video}"} for video in video_files]

    return JsonResponse({"videos": video_list})
def create_generate_speech(text,voice,speech_rate): #生成视频配音
    if not text:
        return JsonResponse({"error": "Text is required"}, status=400)

    # 生成文件名（防止特殊字符）
    safe_text = "".join(c for c in text if c.isalnum() or c in " _-").strip()
    file_path = os.path.join(AUDIO_SAVE_PATH, f"{safe_text}.mp3")
    # file_path = os.path.normpath(file_path)

    # 先删除旧文件
    # if os.path.exists(file_path):
    #     os.remove(file_path)

    # 生成新语音
    asyncio.run(synthesize_speech(text, voice, speech_rate, file_path))

    return JsonResponse({"audioUrl": f"http://127.0.0.1:8090/media/tts_audio/{safe_text}.mp3"})
def generate_subtitleVideo(request):
    '''根据文案和视频生成单个视频'''
    responseData=json.loads(request.body)
    print(responseData)
    text=responseData['text'] #句子
    video_url=responseData['videoUrl']
    # speechRate=responseData['speechRate']#语速
    # voice=responseData['role'] #角色

    from pathlib import Path
    backGroundMusic=responseData['backgroundMusic']
    print(backGroundMusic)
    # voice_file_name = Path(backGroundMusic)
    # print('voice_file_name',voice_file_name)

    

    backGroundMusic_path=os.path.join(os.getcwd(),'media','music',backGroundMusic)
    backGroundMusic_path=os.path.normpath(backGroundMusic_path)


    watermarkText=responseData['watermarkText'] #水印文字
    watermarkSize=responseData['watermarkSize'] #水印大小
    watermarkSpeed=responseData['watermarkSpeed'] #水印速度

    videoSplit=video_url.split('/')
    video_name=videoSplit[-1].split('.')[0]

    dir_path = os.path.join(os.getcwd(),'media','uploads',video_name)
    os.makedirs(dir_path, exist_ok=True) 

    # 把文本转换为字幕
    singleText_to_individual_srt(text,video_name)

    # # 合成语音
    voice_text="".join(c for c in text if c.isalnum() or c in " _-").strip()
    voice_path = os.path.join(os.getcwd(),AUDIO_SAVE_PATH, f"{voice_text}.mp3") #生成声音路径
    voice_path = os.path.normpath(voice_path)
    # print('====voice_path======',voice_path)

    # create_generate_speech(text,voice,speechRate)
    # print('=========语音合成已完成=============')

    # 字幕和视频合成
    sas_name='subtitle_'+video_name+'.ass'
    saa_file=os.path.join(os.getcwd(),'media','uploads',video_name,sas_name )
    video_file=os.path.join(os.getcwd(),'media','uploads',video_name+'.mp4' )
    output_dir=os.path.join(os.getcwd(),'media','uploads',video_name )
    finalVideoUrl=add_single_text_to_videos(video_file,saa_file,output_dir,video_name)
    print('=========字幕合成视频完成=============')

    # 合成水印并返回最终视频
    add_water_video=os.path.join(os.getcwd(),'media','uploads',video_name, f"{video_name}_addWater.mp4") #合成水印视频
    # add_water_video = add_water_video.replace("/", "\\")
    add_water_video=os.path.normpath(add_water_video)

    add_dynamic_watermark(finalVideoUrl,add_water_video,text=watermarkText,fontsize=watermarkSize)
    print('=========水印合成视频完成=============')

    #视频和语音合成并返回最终视频
    finalVideoUrl=merge_video_audio(add_water_video,backGroundMusic_path,video_name)
    print('=========合成最终视频完成=============')

    font_path=os.path.join(os.getcwd(),'media','font','NotoSerifSC-VariableFont_wght.ttf')

    # 第三步：合成字幕、水印和音频（使用 cmd 命令）
    video_file = os.path.join(os.getcwd(), 'media', 'uploads', f'{video_name}.mp4')
    output_video_path = os.path.join(os.getcwd(), 'media', 'uploads', video_name, f"{video_name}_finally.mp4")
    print(output_video_path)

    # 第四步：视频和背景音乐合成
    # merge_video_audio_backgroundMusic(output_video_path,backGroundMusic_path,video_name)


    # saa_file=saa_file.replace("\\", "\\\\").replace("C:", "C\:")

    # font_path="C\\:/Users/Administrator/Desktop/myVideo/myproject/media/font/NotoSerifSC-VariableFont_wght.ttf"

    # 构建 ffmpeg 命令字符串
    # ffmpeg_command =f'ffmpeg -i "{video_file}" -i "{voice_path}" ' \
    #             f'-i "{backGroundMusic_path}" ' \
    #              f'-filter_complex "[0:v]subtitles=\'{saa_file}\'[v1]; ' \
    #              f'[v1]drawtext=text=\'{watermarkText}\':fontfile=\'{font_path}\':fontcolor=white:fontsize={watermarkSize}:x=w*mod(t\,10)/10:y=h*mod(t\,10)/10[v2]" ' \
    #              f'-map "[v2]" -map 1:a -c:v libx264 -c:a aac -b:a 192k -strict experimental -shortest  -y "{output_video_path}"'
    # print('==ffmpeg_command===',ffmpeg_command)
    # # 使用 os.system 执行 ffmpeg 命令
    # os.system(ffmpeg_command)

    output_file_path=os.path.join("http://127.0.0.1:8090/",'media','uploads',video_name,video_name+'_finally.mp4')

    # return output_file_path



    return JsonResponse({"finalVideoUrl": output_file_path})

def merge_video_audio(video_path,audio_path,video_name):
    '''合成视频和语音'''
    finally_output_video=os.path.join(os.getcwd(),'media','uploads',video_name,video_name+'_finally.mp4')

    if os.path.exists(finally_output_video):  # 判断文件是否存在
        os.remove(finally_output_video)  # 删除文件
        print(f"{finally_output_video} 已删除")
    else:
        print(f"{finally_output_video} 不存在")
    # 使用 FFmpeg 合成视频和音频
    cmd = f'ffmpeg -i {video_path} -i {audio_path} -c:v libx264 -c:a aac -strict experimental {finally_output_video}'
    print("====语音合成视频=====",cmd)
    os.system(cmd)
def merge_video_audio_backgroundMusic(video_path, audio_path, video_name):
    '''合成视频并保留原声，同时加背景音乐并调整背景音乐音量'''
    # 输出合成后的视频文件路径
    finally_output_video = os.path.join(os.getcwd(), 'media', 'uploads', video_name, video_name + '_backgroundMusic.mp4')

    # 检查文件是否已存在，若存在则删除
    if os.path.exists(finally_output_video):  
        os.remove(finally_output_video)  # 删除已存在的文件
        print(f"{finally_output_video} 已删除")
    else:
        print(f"{finally_output_video} 不存在")

    # 使用 FFmpeg 合成视频和音频
    # 保留原音并添加背景音乐，背景音乐音量为原来的0.2倍（可以根据需要调整）
    cmd = f'ffmpeg -i "{video_path}" -i "{audio_path}" -filter_complex "[0:a][1:a]amix=inputs=2:duration=longest[a];[1:a]volume=[b];[a][b]amix=inputs=2:duration=longest" -c:v libx264 -c:a aac -strict experimental "{finally_output_video}"'

    # 打印出 FFmpeg 命令
    print("====视频合成命令=====", cmd)

    # 执行 FFmpeg 合成操作
    os.system(cmd)

    # import subprocess
    # cmd = [
    # 'ffmpeg', '-i', video_path, '-i', audio_path,
    # '-map', '0:v:0', '-map', '1:a:0',
    # '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental',
    # finally_output_video
    # ]
    # print("====语音合成视频=====", " ".join(cmd))
    # subprocess.run(cmd, check=True)

    


def downLoad_video(request):
    '''下载单个'''
def merge_videos(video_dir, output_video,file_dir): #视频合成
    """
    合并文件夹下所有视频
    """
    # 获取文件夹内所有视频文件
    video_files = [f for f in os.listdir(video_dir) if f.endswith(('.mp4', '.mkv', '.avi'))]  # 你可以根据需要添加视频格式
    print('======343434343434=',video_files)

    # 创建一个临时的 file_list.txt 文件
    file_list_path = os.path.join(file_dir, "file_list.txt")
    with open(file_list_path, 'w',encoding='utf-8') as file:
        for video in video_files:
            file.write(f"file '{os.path.join(video_dir, video)}'\n")
    # print(file_list_path)
    # input()

    # 使用 ffmpeg 合并视频
    # cmd = [
    #     "ffmpeg", "-f", "concat", "-safe", "0", "-i", file_list_path, "-c", "copy", output_video, "-y"
    # ]
    # subprocess.run(cmd, check=True)
    cmd='''ffmpeg -f \"concat\" -safe 0 -i \"{}\" -c copy \"{}\" -y'''.format(file_list_path,output_video)
    print(cmd)

    # cmd = '''ffmpeg -i \"{}\" -vf \"ass=\'{}\'\" -c:a copy \"{}\" -y'''.format(video_path,ass_path,output_video)
    os.system(cmd)
    print(f"✅ 合成最终视频: {output_video}")

    # 删除临时的 file_list.txt 文件
    # os.remove(file_list_path)
    print(f"🗑️ 已删除临时文件: {file_list_path}")
@csrf_exempt
def generate_video(request):
    if request.method == 'POST':
        videos = []
        texts = []
        upload_dir = 'media/uploads/'
        output_dir = 'media/generated/'
        text_dir = 'media/text/'
        os.makedirs(upload_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(text_dir, exist_ok=True)
        video_dir=os.getcwd()+'media/uploads/'
        text_dir_fina=os.getcwd()+'media/text/'
        print(video_dir)

        for key in request.FILES:
            if key.startswith("videos"):
                file = request.FILES[key]
                file_name = f"{uuid.uuid4()}_{file.name}"
                file_path = os.path.join(video_dir, file_name)
                # print(file_path)
                
                with default_storage.open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                
                videos.append(file_path)
                print(videos)
                text_key = key.replace("videos", "texts")
                text_content = request.POST.get(text_key, "")

                # 将文本内容保存到text_dir
                text_file_name = f"{uuid.uuid4()}_text.txt"
                text_file_path = os.path.join(text_dir_fina, text_file_name)
                with open(text_file_path, 'a+', encoding='utf-8') as text_file:
                    text_file.write(text_content.strip())
                
                texts.append(text_file_path)
                print(texts)

        # 合成带字幕的视频
        clips = []
        for video_path, text in zip(videos, texts):
            video = VideoFileClip(video_path)
            txt_clip = TextClip(text)
            txt_clip.set_text(text)
            txt_clip.set_style(
                background_color='white',
                size=(video.w, None),
                shadow=0,
                shadow_color='black',
                font_family='Arial',
                font_size=24
            )
            final_clip = CompositeVideoClip([video, txt_clip])
            clips.append(final_clip)
        print(clips)

        final_video = CompositeVideoClip(clips)
        generated_video_path = os.path.join(output_dir, "output.mp4")
        final_video.write_videofile(generated_video_path, codec='libx264', fps=24)
        print(final_video)
        print('全部处理完成')
        
    data = {
            "code": 200,
            "msg": '视频合成成功'
            }
    return JsonResponse(data, safe=False)
