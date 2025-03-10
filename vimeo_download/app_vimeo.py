import base64
import os
import subprocess
import hashlib

import requests
from tqdm import tqdm


def generate_hash_filename(file_path, extension=".mp4"):
    """
    Gera um nome de arquivo curto baseado em hash a partir do conteúdo do arquivo.
    Utiliza MD5 pela sua velocidade e trunca para manter o nome do arquivo curto.
    """
    hash_object = hashlib.md5()
    with open(file_path, 'rb') as f:
        # Ler o arquivo em fragmentos para lidar com arquivos grandes de maneira eficiente
        for chunk in iter(lambda: f.read(4096), b''):
            hash_object.update(chunk)
    
    # Obter os primeiros 16 caracteres do hexdigest para um nome de arquivo mais curto
    short_hash = hash_object.hexdigest()[:16]
    return f"video_{short_hash}{extension}"


def download(what, to, base):
    print("saving", what["mime_type"], "to", to)
    with open(to, "wb") as file:
        init_segment = base64.b64decode(what["init_segment"])
        file.write(init_segment)
        for segment in tqdm(what["segments"]):
            segment_url = base + segment["url"]
            resp = requests.get(segment_url, stream=True)
            if resp.status_code != 200:
                print("not 200!")
                print(segment_url)
                break
            for chunk in resp:
                file.write(chunk)
    print("done")


def download_video(url, custom_filename=None):
    """
    Baixa um vídeo do Vimeo.
    
    Args:
        url (str): A URL do vídeo do Vimeo para baixar
        custom_filename (str, opcional): Nome de arquivo personalizado para usar em vez do gerado automaticamente
    """
    temp_output_file = "temp_output.mp4"
    
    if "master.json" in url:
        url = url[: url.find("?")] + "?query_string_ranges=1"
        url = url.replace("master.json", "master.mpd")
        print(url)
        subprocess.run(["youtube-dl", url, "-o", temp_output_file])
        
        final_filename = generate_hash_filename(temp_output_file)
        os.rename(temp_output_file, final_filename)
        return

    base_url = url[: url.rfind("/", 0, -26) + 1]
    content = requests.get(url).json()

    # Filtra para vídeos com altura de 720p
    video_720p = [d for d in content["video"] if d["height"] == 720]
    if not video_720p:
        print(f"Não foi encontrado vídeo em 720p para a URL {url}.")
        
    # Seleciona o vídeo com 720p
    video = video_720p[0]

    # Seleciona o áudio com a maior taxa de bits
    audio_quality = [(i, d["bitrate"]) for (i, d) in enumerate(content["audio"])]
    audio_idx, _ = max(audio_quality, key=lambda _h: _h[1])
    audio = content["audio"][audio_idx]

    base_url = base_url + content["base_url"]
    video_tmp_file = "video.mp4"
    audio_tmp_file = "audio.mp4"

    download(video, video_tmp_file, base_url + video["base_url"])
    download(audio, audio_tmp_file, base_url + audio["base_url"])

    command = [
        "ffmpeg",
        "-i",
        audio_tmp_file,
        "-i",
        video_tmp_file,
        "-c",
        "copy",
        temp_output_file,
    ]

    try:
        print("Juntando vídeo e áudio...")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(result.stdout)  # Mostra a saída do comando
        
        if custom_filename:
            # Usa o nome de arquivo personalizado mas mantém a extensão mp4
            filename = f"{custom_filename}.mp4"
            print(f"Usando nome de arquivo personalizado: {filename}")
        else:
            # Usa a lógica original de nome de arquivo gerado automaticamente
            filename = generate_hash_filename(temp_output_file)
        
        os.rename(temp_output_file, filename)
        print(f"Arquivo final salvo como: {filename}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Output error: {e.stderr}")

    os.remove(video_tmp_file)
    os.remove(audio_tmp_file)
    # Se houve um erro, temp_output_file pode ainda existir
    if os.path.exists(temp_output_file):
        os.remove(temp_output_file)