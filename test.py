import os 
import gradio as gr
from huggingface_hub import snapshot_download
from huggingface_hub import HfApi
from glob import glob

TOKEN_HF = os.environ["TOKEN_HF"]
DATA_PATH = "data"

api = HfApi(endpoint="https://huggingface.co", # Can be a Private Hub endpoint.
    token=TOKEN_HF)
api.snapshot_download(repo_id="congdc/thumb-youtube", local_dir="data/", repo_type="dataset")
