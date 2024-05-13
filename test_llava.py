from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration
import torch
from PIL import Image
import requests

class LLAVA:
    name_model = ""
    
    def init_model(name_model):
        LLAVA.name_model = name_model
        LLAVA.processor = LlavaNextProcessor.from_pretrained(name_model)
        LLAVA.model = LlavaNextForConditionalGeneration.from_pretrained(name_model) 
        LLAVA.model.to("cuda:0")
        
    def inference(img_path, configs):
        if configs["name_model"] != name_model:
            LLAVA.init_model(configs["name_model"])
        
        image = Image.open(img_path)
        prompt = configs["prompt"]
        inputs = LLAVA.processor(prompt, image, return_tensors="pt").to("cuda:0")
        
        output = LLAVA.model.generate(**inputs, max_new_tokens=configs["max_tokens"])

        return processor.decode(output[0], skip_special_tokens=True)

    
# from core.internlm.projects.ShareGPT4V.run_model import ShareGPT4v
# result = ShareGPT4v.inference(img_path, configs)