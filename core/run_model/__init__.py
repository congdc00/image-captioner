from core.utils.data import analysis_captions, count_token
import time
from glob import glob
import gradio as gr
import os
import shutil
import json

IMGS_PATH = "data/imgs"

def get_config(configs):
    
    list_config = configs.split(",")
    results = {}
    for config in list_config:
        config = config.replace(" --", "--")
        key, value = config.split(" ")
        key = key.replace("--", "")
        if value.isdigit():
            value = int(value)
        elif "." in value:
            value = float(value)
        elif value == "None":
            value = None
        results[key] = value
    return results

def get_imgs(path):
    imgs = []
    if "." in path:
        imgs.append(path)
    else: 
        subs_path = glob(path + "/*")
        for sub_path in subs_path:
            imgs += get_imgs(sub_path)
    return imgs

def get_list_img(list_img):
    list_img = list_img.split("\n")
    return list_img

def generative_caption(img_path, configs):
    
    # PUT CODE HERE
    
    return ""

def run_captioner(model, prompt, configs, list_img, progress=gr.Progress()):
    
    configs = get_config(configs)
    configs["model"] = model
    configs["prompt"] = prompt
    json_path  = "data/captions.json"
    progress(0, desc="Starting...")
    
    if list_img == "":
        if os.path.exists(json_path):
            os.remove(json_path)
        list_img = get_imgs(IMGS_PATH)
        results = {"imgs": []}
        
        for img_path in progress.tqdm(list_img):
            result = {}
            result["caption"] = generative_caption(img_path, configs)
            result["img_path"] = img_path
            results["imgs"].append(result)
    else:
        list_img = get_list_img(list_img)
        with open(json_path, 'r') as f:
            results = json.load(f)
        
        for i, result in enumerate(results["imgs"]):
            if result["img_path"] in list_img:
                results["imgs"][i]["caption"] = generative_caption(result["img_path"], configs)
        
    with open(json_path, 'w') as f:
        json.dump(results, f)
        
    
    return analysis_captions(results)



def run_captioner_sample(model, prompt, configs, img1, img2, img3, img4, img5, progress=gr.Progress()):
    configs = get_config(configs)
    configs["model"] = model
    configs["prompt"] = prompt
    
    progress(0, desc="Starting...")

    results = []
    list_num_token = []
    list_img_path  = [img1, img2, img3, img4, img5]
    for img_path in list_img_path:
        if img_path != None:
            caption = generative_caption(img_path, configs)
            list_num_token.append(count_token(caption))
            results.append(gr.update(value = caption))
        else:
            list_num_token.append(0)
            results.append(None)
    results += list_num_token
    return tuple(results)