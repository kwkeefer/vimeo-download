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

### Instalação

Para instalar o Vimeo Downloader, você precisará dos seguintes componentes:

1. **Dependências do sistema:**
   - **FFmpeg** - Necessário para combinar arquivos de áudio e vídeo
     - [FFmpeg - Download](https://ffmpeg.org/download.html)
   - **youtube-dl** - Necessário para alguns formatos de URL do Vimeo
     - Instale via pip: `pip install youtube-dl`

2. **Instalação do Vimeo Downloader:**

   Recomendamos a instalação usando **uv**, um gerenciador de pacotes Python extremamente rápido:

   - Primeiro, instale o **uv** seguindo as instruções em [https://astral.sh/uv/install](https://astral.sh/uv/install)
   
   - Em seguida, instale o Vimeo Downloader diretamente do GitHub:
     ```bash
     uv tool install git+https://github.com/mangareira/vimeo-download.git
     ```

3. **Uso após a instalação:**
   
   Após a instalação, você pode usar o comando `vimeo-dl` diretamente no terminal:
   ```bash
   vimeo-dl -u "URL_DO_VIDEO"
   ```
   
   Ou para processar múltiplas URLs de um arquivo:
   ```bash
   vimeo-dl -f "caminho/para/arquivo_com_urls.txt"
   ```

### Como usar

1. Adicione as URLs dos vídeos no array `urls` dentro do código. Cada URL deve conter o caminho da playlist JSON ou do arquivo de vídeo desejado.
   
2. Execute o script:
   ```bash
   python app_vimeo.py
   ```

3. O script irá:
   - Iterar sobre as URLs fornecidas.
   - Baixar os segmentos de vídeo e áudio da URL fornecida.
   - Juntar o vídeo e áudio em um arquivo MP4.

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


### Possíveis Erros

- **Erro ao baixar segmentos**: Se o download de um segmento falhar (não retornar o código 200), o script interrompe o processo para evitar arquivos corrompidos.
- **Erro ao combinar áudio e vídeo**: Verifique se o **FFmpeg** está corretamente instalado e configurado no sistema.

### Licença

Este projeto está disponível sob a licença MIT.