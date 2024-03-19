from app.utils import logging
from app.utils import config
import assemblyai as aai
import json


logger = logging.get_logger()

def initialize_assemblyai():
    try:
        aai.settings.api_key = config.ASSEMBLYAI_API_KEY
        transcriber = aai.Transcriber()
        
        return transcriber
    except Exception as e:
        logger.error(f"Error initializing AssemblyAI: {e}")
      
        
def generate_transcript(mp3_file_path):
    logger.info("Generating transcript from audio file")
    
    transcriber = initialize_assemblyai()
    transcript = transcriber.transcribe(mp3_file_path)

    if transcript.status == aai.TranscriptStatus.error:
        logger.error("Error generating transcript")
    else:
        sentences = transcript.get_sentences() # Getting sentences from the transcript
        sentences_data = []
        for sentence in sentences:
            sentences_data.append(sentence.text)
            
        return sentences_data