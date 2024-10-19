import os
import base64
import requests
import subprocess
from tqdm import tqdm

# Array com os URLs
urls = [
"https://vod-adaptive-ak.vimeocdn.com/exp=1724439491~acl=%2FRANDONUUID%2F%2A~hmac=579ef000de001ca54b7badab9fb102183655ad98b118b5ff7f90e6d3f52d8958/RANDONUUID/v2/playlist/av/primary/playlist.json?omit=av1-hevc&pathsig=8c953e4f~Z2XL4HO6Z_Moeti5UwkjiXt5auVxmm2FOZnyKBQ9mX0&qsr=1&rh=2DCFWc"
]

# Loop para iterar sobre os URLs
for i, url in enumerate(urls):
    #nome do arquivo dos videos
    file_name = f"aula-{i + 80}"

    if 'master.json' in url:
        url = url[:url.find('?')] + '?query_string_ranges=1'
        url = url.replace('master.json', 'master.mpd')
        print(url)
        subprocess.run(['youtube-dl', url, '-o', file_name])
        continue

    def download(what, to, base):
        print('saving', what['mime_type'], 'to', to)
        with open(to, 'wb') as file:
            init_segment = base64.b64decode(what['init_segment'])
            file.write(init_segment)
            for segment in tqdm(what['segments']):
                segment_url = base + segment['url']
                resp = requests.get(segment_url, stream=True)
                if resp.status_code != 200:
                    print('not 200!')
                    print(segment_url)
                    break
                for chunk in resp:
                    file.write(chunk)
        print('done')

    file_name += '.mp4'
    base_url = url[:url.rfind('/', 0, -26) + 1]
    content = requests.get(url).json()

    # Filtra para vídeos com altura de 720p
    video_720p = [d for d in content['video'] if d['height'] == 720]
    if not video_720p:
        print(f"Não foi encontrado vídeo em 720p para a URL {url}.")
        continue

    # Seleciona o vídeo com 720p
    video = video_720p[0]

    # Seleciona o áudio com a maior taxa de bits
    audio_quality = [(i, d['bitrate']) for (i, d) in enumerate(content['audio'])]
    audio_idx, _ = max(audio_quality, key=lambda _h: _h[1])
    audio = content['audio'][audio_idx]
    
    base_url = base_url + content['base_url']
    video_tmp_file = 'video.mp4'
    audio_tmp_file = 'audio.mp4'

    download(video, video_tmp_file, base_url + video['base_url'])
    download(audio, audio_tmp_file, base_url + audio['base_url'])

    command = ["ffmpeg", "-i", audio_tmp_file, "-i", video_tmp_file, "-c", "copy", file_name]

    try:
        print("Joining video and audio...")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(result.stdout)  # Exibe a saída do comando
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Output error: {e.stderr}")

    os.remove(video_tmp_file)
    os.remove(audio_tmp_file)
