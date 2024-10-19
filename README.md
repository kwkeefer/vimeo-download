# VIMEO DOWNLOADER

## Video Downloader and Merger

Este é um script Python que realiza o download de vídeos e áudios separadamente a partir de uma lista de URLs e, em seguida, combina os dois arquivos em um único arquivo MP4 utilizando o **FFmpeg**. O objetivo do script é baixar vídeos de fontes que utilizam **JSON** para organizar seus arquivos de mídia, além de ser capaz de manipular URLs com diferentes formatos de playlist.

### Funcionalidades

- Faz o download de vídeo e áudio em segmentos de uma URL baseada em JSON.
- Combina automaticamente o áudio e vídeo em um arquivo MP4.
- Filtra vídeos de 720p e áudios com a melhor qualidade.
- Utiliza **FFmpeg** para juntar vídeo e áudio em um único arquivo.
- Progresso do download exibido utilizando a biblioteca `tqdm` para uma melhor experiência do usuário.

### Pré-requisitos

Antes de rodar o script, certifique-se de ter o seguinte instalado no seu ambiente:

- **Python 3.x**
- **FFmpeg** (para combinar o vídeo e áudio)
- **youtube-dl** (opcional, dependendo da URL que está sendo utilizada)
- Dependências Python (instaláveis via `pip`):
  - `requests`
  - `tqdm`

### Instalação

1. Clone o repositório ou copie o código para um arquivo Python no seu projeto.
2. Instale as dependências necessárias com o seguinte comando:
   ```bash
   pip install requests tqdm
   ```

3. Instale o **FFmpeg** em seu sistema, se ainda não o tiver:
   - [FFmpeg - Download](https://ffmpeg.org/download.html)

4. Verifique se o **youtube-dl** está instalado:
   ```bash
   pip install youtube-dl
   ```

### Como usar

1. Adicione as URLs dos vídeos no array `urls` dentro do código. Cada URL deve conter o caminho da playlist JSON ou do arquivo de vídeo desejado.
   
2. Execute o script:
   ```bash
   python app_vimeo.py
   ```

3. O script irá:
   - Iterar sobre as URLs fornecidas.
   - Baixar os segmentos de vídeo (com 720p, se disponível ou maiores) e os segmentos de áudio com a melhor qualidade.
   - Juntar o vídeo e o áudio em um arquivo MP4.

4. O arquivo final será salvo com o nome `aula-X.mp4` (onde X é o índice da URL na lista).

### Estrutura do Script

- **download(what, to, base)**: Função que realiza o download dos segmentos de vídeo e áudio. Cada segmento é baixado sequencialmente e escrito no arquivo temporário.
- **subprocess.run**: Utilizado para rodar o comando FFmpeg que junta o vídeo e o áudio.
- **tqdm**: Utilizado para exibir uma barra de progresso durante o download de cada segmento.
- **youtube-dl**: O script tenta usar `youtube-dl` em URLs que contêm `master.json`, convertendo-as para um formato compatível com **MPEG-DASH**.

### Como pegar a url

- Abra o DevTools antes de iniciar o video
- depois fique na aba de network
- inicio o video e espere começa-lo
- Volte para o DevTools e va para aba de network
- Você vizualizara o json com inicio **playlist.json**
- Clique nela e aparecera a url completa
- A url tem tempo limitado, recomendo pegar dez no maximo

Segue a imagem como referencia

![referencia](https://github.com/mangareira/vimeo-download/blob/main/reference.png)


### Exemplo de Uso

Suponha que você tenha uma URL JSON de um vídeo:

```python
urls = [
    "https://vod-adaptive-ak.vimeocdn.com/exp=1724439491~acl=%2FRANDONUUID%2F%2A~hmac=..."
]
```

Quando você rodar o script, ele irá:

1. Baixar os segmentos de vídeo e áudio da URL fornecida.
2. Juntar o vídeo e áudio em um arquivo final com o nome `aula-x.mp4`.
3. Exibir o progresso do download de cada segmento.
4. Excluir os arquivos temporários após a combinação.

### Possíveis Erros

- **Erro ao baixar segmentos**: Se o download de um segmento falhar (não retornar o código 200), o script interrompe o processo para evitar arquivos corrompidos.
- **Erro ao combinar áudio e vídeo**: Verifique se o **FFmpeg** está corretamente instalado e configurado no sistema.

### Licença

Este projeto está disponível sob a licença MIT.