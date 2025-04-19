import os


def downloadModel(modelName):
    """
    Downloads a model from Hugging Face or Whisper and saves it to the local directory.
    """

def loadModel(modelName):
    """
    Loads a model from the local directory.
    """

def isModelAvailable(modelName) -> bool:
    """
    Checks if a model is available in the local directory.
    """
    # Check if the model is available in the local directory
    return os.path.exists(f"models/{modelName}")

def getAvailableModels() -> list:
    """
    Returns a list of available models in the local directory.
    """
    # Get a list of available models in the local directory
    return os.listdir("models")