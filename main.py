import os
import requests


def get_surah_names():
    url = "https://api.alquran.cloud/v1/meta"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            ref["number"]: ref["name"]
            for ref in data["data"]["surahs"]["references"]
        }
    else:
        print("Failed to fetch Surah names from the API.")
        return None


def download_surah_audio(range_start, range_end):
    base_url = (
        "https://cdn.islamic.network/quran/audio-surah/128/ar.abdulbasitmurattal/{}.mp3"
    )
    output_folder = "surah_audio"
    surah_names = get_surah_names()

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for surah_number in range(range_start, range_end + 1):
        url = base_url.format(surah_number)
        filename = os.path.join(output_folder, f"Surah_{surah_number}.mp3")

        print(f"Downloading Surah {surah_number}...")

        # Download the MP3 file
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)

            # Rename the file based on Surah name
            if surah_names and surah_number in surah_names:
                english_name = surah_names[surah_number]
                new_filename = os.path.join(output_folder, f"{english_name}.mp3")
                os.rename(filename, new_filename)
                print(
                    f"Surah {surah_number} downloaded successfully as {english_name}.mp3"
                )
            else:
                print(f"Surah {surah_number} downloaded successfully.")
        else:
            print(
                f"Failed to download Surah {surah_number}. Status code: {response.status_code}"
            )



download_surah_audio(114, 114)
