from core.utils.data import analysis_captions, count_token
from glob import glob
import gradio as gr
import os
import json
from tqdm import tqdm
import time

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
    new_list_img = []
    for img_path in list_img:
        new_img_path = "data/" + img_path
        new_list_img.append(new_img_path)
    list_img = new_list_img
    return list_img

def generative_caption(img_path, configs):
    
    
    try:
        
        # PUT CODE HERE
        result = ""
        
    except:
        result = ""
        gr.Warning("Out of memory")
        

    return result

def run_captioner(model, prompt, configs, read_json_path, list_img): #progress=gr.Progress(track_tqdm = True)):
   
    start_time = time.time()
    
    configs = get_config(configs)
    configs["model_path"] = model
    configs["prompt"] = prompt
    
    # progress(0, desc="Starting...", unit="images")
    
    # Remove old captions
    read_json_path = "data/" + read_json_path
    json_path = "data/captions.json"
    if read_json_path != json_path:
        if os.path.exists(json_path):
            os.remove(json_path)
    
    # New json path
    if list_img == "":
        list_img = get_imgs(IMGS_PATH)
        results = {"imgs": []}
        
        for img_path in tqdm(list_img):
            result = {}
            result["caption"] = generative_caption(img_path, configs)
            result["img_path"] = img_path
            results["imgs"].append(result)
    
    # Overite json path
    else:
        
        if os.path.exists(read_json_path):
            with open(read_json_path, 'r') as f:
                results = json.load(f)
            
            if "imgs" in results and isinstance(results["imgs"], list):
                list_img = get_list_img(list_img)
                
                # Revert caption
                for i, result in enumerate(results["imgs"]):
                    if result["img_path"] in list_img:
                        results["imgs"][i]["caption"] = generative_caption(result["img_path"], configs)
                        index = list_img.index(result["img_path"])  # Tìm vị trí đầu tiên của giá trị
                        list_img.pop(index)
                
                for img_path in tqdm(list_img):
                    if os.path.exists(img_path):
                        result = {}
                        result["caption"] = generative_caption(img_path, configs)
                        result["img_path"] = img_path
                        results["imgs"].append(result)
                    else:
                        gr.Warning(f'Not exist {img_path}')
            else:
                gr.Warning(f'Content {read_json_path} is not valid')
                
        else:
            
            # solution 3
            results = {"imgs": []}
            gr.Warning(f'Not exist {read_json_path}')
        
        
        
    with open(json_path, 'w') as f:
        json.dump(results, f)
    
    gr.Info("Caption done")
    
    end_time = time.time()
    delta_time = end_time - start_time
    return analysis_captions(results, delta_time)



def run_captioner_sample(model, prompt, configs, img1, img2, img3, img4, img5, progress=gr.Progress(track_tqdm = True)):
    configs = get_config(configs)
    configs["model_path"] = model
    configs["prompt"] = prompt
    
    progress(0, desc="Starting...", unit="images")

    results = []
    list_num_token = []
    list_img_path  = [img1, img2, img3, img4, img5]
    for img_path in progress.tqdm(list_img_path):
        if img_path != None:
            caption = generative_caption(img_path, configs)
            list_num_token.append(count_token(caption))
            results.append(gr.update(value = caption))
        else:
            list_num_token.append(0)
            results.append(None)
    results += list_num_token
    return tuple(results)