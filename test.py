import os 
import gradio as gr
from huggingface_hub import snapshot_download
from huggingface_hub import HfApi
from glob import glob

TOKEN_HF = os.environ["TOKEN_HF"]
DATA_PATH = "data"

api = HfApi(endpoint="https://huggingface.co", # Can be a Private Hub endpoint.
    token=TOKEN_HF)
api.upload_file(
    path_or_fileobj="data/caption.json",
    path_in_repo="captions/share_gpt_version1.json",
    repo_id="congdc/imgs-furniture",
    repo_type="dataset",
)