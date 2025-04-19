def convertAudioFormat(inputPath, outputFormat):
    """
    Converts the audio file at inputPath to the specified outputFormat.
    
    Args:
        inputPath (str): Path to the input audio file.
        outputFormat (str): Desired output audio format (e.g., 'mp3', 'wav').
    
    Returns:
        str: Path to the converted audio file.
    """
    import os
    from pydub import AudioSegment

    # Load the audio file
    audio = AudioSegment.from_file(inputPath)

    # Define the output path
    base, _ = os.path.splitext(inputPath)
    outputPath = f"{base}.{outputFormat}"

    # Export the audio in the desired format
    audio.export(outputPath, format=outputFormat)

    return outputPath

def preprocessAudio(audioData):
    """
    Preprocesses the audio data for further analysis.
    
    Args:
        audioData (AudioSegment): The audio data to preprocess.
    
    Returns:
        AudioSegment: The preprocessed audio data.
    """
    # Example preprocessing: Normalize the audio
    normalized_audio = audioData.normalize()
    
    return normalized_audio