import argparse
import sys
from pathlib import Path

from vimeo_download.app_vimeo import download_video


def parse_args():
    """Analisa os argumentos de linha de comando para o baixador de vimeo."""
    parser = argparse.ArgumentParser(
        description="Download videos from Vimeo with automatic content-based naming."
    )

    # Cria um grupo mutuamente exclusivo para os métodos de entrada de URL
    input_group = parser.add_mutually_exclusive_group(required=True)

    input_group.add_argument("-u", "--url", help="Single URL to download", type=str)

    input_group.add_argument(
        "-f", "--file", help="Path to a file containing URLs (one per line)", type=str
    )
    
    # Add a new argument for custom filename
    parser.add_argument(
        "-n", "--name", 
        help="Custom filename for download (only works with -u/--url option)", 
        type=str
    )

    return parser.parse_args()


def process_urls(urls, custom_filename=None):
    """Processa uma lista de URLs baixando cada uma."""
    for i, url in enumerate(urls, 1):
        url = url.strip()
        if not url or url.startswith("#"):  # Omitir linhas vazias e comentários
            continue

        print(f"\n[{i}] Processing URL: {url}")
        try:
            # Pass the custom filename only for the first URL when specified
            filename = custom_filename if i == 1 and custom_filename else None
            download_video(url, filename)
        except Exception as e:
            print(f"Error processing URL {url}: {e}")


def main():
    """Ponto de entrada principal para a interface de linha de comandos."""
    args = parse_args()

    # Check if name is provided with file option
    if args.name and args.file:
        print("Warning: Custom filename (-n/--name) only works with single URL (-u/--url) option.")
        print("The custom filename will be ignored for batch downloads.")

    if args.url:
        # Process a single URL with optional custom filename
        process_urls([args.url], args.name)
    elif args.file:
        # Process URLs from a file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File '{args.file}' not found.")
            sys.exit(1)

        try:
            with open(file_path, "r") as f:
                urls = f.readlines()

            if not urls:
                print(f"Error: File '{args.file}' is empty.")
                sys.exit(1)

            print(f"Found {len(urls)} URLs in '{args.file}'")
            process_urls(urls)

        except Exception as e:
            print(f"Error reading file '{args.file}': {e}")
            sys.exit(1)
