import os 
import gradio as gr
from huggingface_hub import snapshot_download
from huggingface_hub import HfApi
from glob import glob
import shutil
import json
import multiprocessing
from tqdm import tqdm
TOKEN_HF = os.environ["TOKEN_HF"]
DATA_PATH = "data"

old_repo = ""

def count_token(caption):
    return len(caption.split())

def download (source_img):
    
    global old_repo
    
    if source_img != old_repo and os.path.exists("data/"):
        shutil.rmtree("data/")
        old_repo = source_img
    os.makedirs("data/", exist_ok=True)
    
        
    api = HfApi(endpoint="https://huggingface.co", # Can be a Private Hub endpoint.
        token=TOKEN_HF)
    try:
        api.snapshot_download(repo_id=source_img, local_dir="data/", repo_type="dataset", force_download=True, max_workers= multiprocessing.cpu_count())
    except:
        gr.Warning(f"Not exit {source_img}")
    
    return gr.update(visible=True)

def upload(name_version, name_repo):
    json_path = "data/captions.json"
    api = HfApi(endpoint="https://huggingface.co", # Can be a Private Hub endpoint.
    token=TOKEN_HF)
    api.upload_file(
        path_or_fileobj=json_path,
        path_in_repo= f"captions/{name_version}.json",
        repo_id=name_repo,
        repo_type="dataset",
    
    )
    gr.Info(f"Upload to captions/{name_version}.json done")
    

def count_imgs(path):
    num_img = 0
    if "." in path:
        num_img = 1
    else: 
        subs_path = glob(path + "/*")
        for sub_path in subs_path:
            num_img += count_imgs(sub_path)
    return num_img

def analysis_imgs():
    num_imgs = count_imgs(f"{DATA_PATH}/imgs")
    info = f"Num image: {num_imgs}"
    return gr.update(value = info, visible=True)

def show_ex(name_img):
    
    # READ Caption info
    json_path = "data/captions.json"
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
    else:
        gr.Warning(f"Not exist {json_path}")
        return None, None
        
    
    # READ Image
    img_path = ""
    caption = ""
    for img in data['imgs']:
        if img['img_path'] == name_img:
            caption = img['caption']
            img_path = img['img_path']
            break
    if img_path == "":
        gr.Warning(f"Not exist image {name_img}")
        return None, None
    
    return (gr.update(value= img_path), gr.update(value = caption))

def analysis_captions(results):

    # Khởi tạo hai danh sách rỗng để chứa img_path và caption
    img_paths = []
    captions = []

    # Lặp qua danh sách các hình ảnh trong tệp JSON và thêm img_path và caption vào danh sách tương ứng
    min_len_token = 9999
    name_img_min_len_caption = ""
    
    max_len_token = 0
    name_img_max_len_caption = ""
    avg_len_token = 0
    for img in results['imgs']:
        img_paths.append(img['img_path'])
        captions.append(img['caption'])
        
        len_token = count_token(img['caption'])
        
        if min_len_token > len_token:
            min_len_token = len_token
            name_img_min_len_caption = img_paths[-1]
        
        if max_len_token < len_token:
            max_len_token = len_token
            name_img_max_len_caption = img_paths[-1]
            
        avg_len_token += len_token
    
    if len(results['imgs']) > 0:
        avg_len_token /= len(results['imgs'])
    result = f"Num captions: {len(captions)}\nAvg token:  {avg_len_token}\nMin token:  {min_len_token} ({name_img_min_len_caption})\nMax token:  {max_len_token} ({name_img_max_len_caption})"
    return gr.update(value = result, visible=True)

