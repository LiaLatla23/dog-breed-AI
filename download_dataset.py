import requests

url = "http://vision.stanford.edu/aditya86/ImageNetDogs/images.tar"
output = "images.tar"

print("Iniciando descarga...")

response = requests.get(url, stream=True, timeout=30)
response.raise_for_status()

total = int(response.headers.get("content-length", 0))
downloaded = 0

with open(output, "wb") as file:
    for chunk in response.iter_content(chunk_size=1024 * 1024):
        if chunk:
            file.write(chunk)
            downloaded += len(chunk)

            if total:
                percentage = downloaded / total * 100
                print(f"\rDescargado: {percentage:.1f}%", end="")

print("\nDescarga terminada.")