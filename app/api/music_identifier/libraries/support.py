import requests
from pydub import AudioSegment
from app.utils import logging
import json
from app.utils import config

logger = logging.get_logger()

import os

AUDD_API_KEY = config.AUDD_API_KEY

def find_musics_in_the_audio(mp3_file_path):
    results = []
    endpoint = 'https://api.audd.io/recognize'
    data = {
        'api_token': AUDD_API_KEY
    }
    # Open the file and pass it to the 'files' parameter
    with open(mp3_file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(endpoint, data=data, files=files)

    if response.status_code == 200:
        return response.json()
    else:
        # Corrected status code comparison to integer
        if response.status_code == 902:
            logger.error(f"Request failed with status code {response.status_code}: The limit was Reached")
        else:
            logger.error({'error': f'Request failed with status code {response.status_code}.'})
