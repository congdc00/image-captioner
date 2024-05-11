import os 
import gradio as gr
from huggingface_hub import snapshot_download
from huggingface_hub import HfApi
from glob import glob

TOKEN_HF = os.environ["TOKEN_HF"]
DATA_PATH = "data"

def download (source_img):
    api = HfApi(endpoint="https://huggingface.co", # Can be a Private Hub endpoint.
        token=TOKEN_HF)
    api.snapshot_download(repo_id=source_img, local_dir="data/", repo_type="dataset")
    return gr.update(visible=True)

def upload(name_version, name_repo):
    api = HfApi(endpoint="https://huggingface.co", # Can be a Private Hub endpoint.
    token=TOKEN_HF)
    api.upload_file(
        path_or_fileobj="data/capitons.json",
        path_in_repo= f"captions/{name_version}.json",
        repo_id=name_repo,
        repo_type="dataset",
    
    )

def count_imgs(path):
    num_img = 0
    if "." in path:
        num_img = 1
    else: 
        subs_path = glob(path + "/*")
        for sub_path in subs_path:
            num_img += count_imgs(sub_path)
    return num_img

def analysis():
    num_imgs = count_imgs(f"{DATA_PATH}/imgs")
    info = f"Num imgs: {num_imgs}"
    return gr.update(value = info, visible=True)