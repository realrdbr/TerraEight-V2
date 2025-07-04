import requests
import zipfile
import os
import sys
from tqdm import tqdm # Import tqdm for progress bars


def download_and_extract_zip_with_choice_and_progress():
    # Download Links
    download_links = {
        "1": "https://github.com/realrdbr/TerraEight-V2/releases/download/v1.0.0-basic/TerraEight-V2.zip",
        "2": "https://github.com/realrdbr/TerraEight-V2/releases/download/v1.0.0-enhanced/TerraEightV2-Enhance.zip"
    }


    print("Bitte wählen Sie das gewünschte Modpack aus:")
    print("1: Basic Modpack")
    print("2: Enhanced Modpack")


    choice = ""
    while choice not in download_links:
        choice = input("Ihre Wahl (1 oder 2): ").strip()
        if choice not in download_links:
            print("Ungültige Eingabe. Bitte geben Sie '1' oder '2' ein.")


    zip_url = download_links[choice]
    print(f"Sie haben '{'Basic Modpack' if choice == '1' else 'Enhanced Modpack'}' gewählt.")
    print(f"Der Download-Link ist: {zip_url}")


    # Looks for the Documents folder based on the operating system
    if sys.platform == "win32":
        documents_path = os.path.join(os.environ["USERPROFILE"], "Documents")
    elif sys.platform == "darwin": # macOS
        documents_path = os.path.join(os.path.expanduser("~"), "Documents")
    else: # Linux/Unix
        documents_path = os.path.join(os.path.expanduser("~"), "Documents")


    target_directory = os.path.join(documents_path, "My Games", "Terraria", "tModLoader", "Mods", "ModPacks")


    # checks if the target directory exists, if not, it creates it
    if not os.path.exists(target_directory):
        print(f"Zielordner '{target_directory}' existiert nicht. Erstelle ihn...")
        try:
            os.makedirs(target_directory)
            print("Zielordner erfolgreich erstellt.")
        except OSError as e:
            print(f"Fehler beim Erstellen des Zielordners: {e}")
            return


    # temporary filename for the downloaded zip file
    zip_filename = os.path.join(target_directory, "downloaded_modpack.zip")


    try:
        print(f"Versuche, die ZIP-Datei von '{zip_url}' herunterzuladen...")
        response = requests.get(zip_url, stream=True)
        response.raise_for_status()


        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 8192


        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc="Download")
        with open(zip_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                progress_bar.update(len(chunk))
                f.write(chunk)
        progress_bar.close()
        print(f"ZIP-Datei erfolgreich nach '{zip_filename}' heruntergeladen.")

        # extract the downloaded zip file
        print(f"Entpacke die ZIP-Datei nach '{target_directory}'...")
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            # Progressbar for extraction
            file_list = zip_ref.namelist()
            total_files = len(file_list)
            for i, file_name in enumerate(file_list):
                zip_ref.extract(file_name, target_directory)
                # simple progress output
                sys.stdout.write(f"\rEntpacke Datei {i+1} von {total_files} ({file_name[:50]}...)")
                sys.stdout.flush()
            print("\nZIP-Datei erfolgreich entpackt.")


        # cleanup
        os.remove(zip_filename)
        print(f"Heruntergeladene ZIP-Datei '{zip_filename}' gelöscht.")
        print("Vorgang abgeschlossen.")


    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Herunterladen der Datei: {e}")
    except zipfile.BadZipFile:
        print("Die heruntergeladene Datei ist keine gültige ZIP-Datei oder ist beschädigt.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")


if __name__ == "__main__":
    download_and_extract_zip_with_choice_and_progress()

