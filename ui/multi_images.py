import gradio as gr 

from core.utils.data import download, upload, analysis_imgs, show_ex
from core.run_model import run_captioner
import yaml

CONFIGS_PATH = "config/configs.yaml"
with open(CONFIGS_PATH, 'r') as f:
    configs = yaml.safe_load(f)

def reset_config():
    return gr.update(value=configs["config_model"])
def enable(mode_caption):
    if mode_caption == "Custom":
        return gr.update(visible=True, interactive= True), gr.update(visible=True, interactive= True)
    else:
        return gr.update(value = "", visible=False), gr.update(value = "captions/caption.json", visible=False)

def init():
    
    with gr.Row():
        with gr.Column(scale=8):
            source_imgs = gr.Text(label="Source Data", placeholder="put name model here", interactive=True)
            info_img = gr.Text(label="Info images dataset", visible=False, container=False)
        download_imgs_btn = gr.Button(value="Download", variant="primary", scale=1)
        analysis_imgs_btn = gr.Button(value="Analysis", scale=1)
        
    
    
    download_imgs_btn.click(download, inputs=source_imgs, outputs=analysis_imgs_btn)    
    analysis_imgs_btn.click(analysis_imgs, outputs=info_img)
    
    
    model = gr.Dropdown(label="Model", value=configs["models"][0], choices=configs["models"], interactive=True)
    prompt = gr.Text(label="Prompt", value=configs["template_prompt"], interactive=True)
    
    

    with gr.Accordion("Advance", open=False):
        with gr.Row():
            config = gr.Text(label="Configs", value=configs["config_model"], interactive=True, scale=5)
            reset_btn = gr.Button(value="Reset")
        
    reset_btn.click(reset_config, outputs=config)
        
        
    # Caption
    mode_caption = gr.Dropdown(choices=["All", "Custom"], label="Num image caption", value = "All", interactive=True)
    default_caption_path = gr.Text(value="captions/caption.json", visible=False, label="Read from caption")
    list_img_caption = gr.Text(value="", placeholder = "imgs/<type_img>/<name_img>", visible=False, label="List images")
    mode_caption.change(enable,inputs = mode_caption, outputs = [list_img_caption, default_caption_path])
    
    submit_btn = gr.Button(value="Generate caption", variant="primary", size="lg")
    info_captioner = gr.TextArea(label= "Info captioner", visible=False)
    submit_btn.click(run_captioner, inputs = [model, prompt, config,default_caption_path, list_img_caption], outputs=info_captioner)
    
    # View sample
    with gr.Tab(label="Samples"):
        with gr.Row():
            name_img = gr.Text(label="Name img")
            sample_btn = gr.Button(value="Show sample")
        with gr.Row():
            img_result = gr.Image(label="Image sample", scale=4)
            caption_result = gr.TextArea(label="Caption", scale=1)
    sample_btn.click(show_ex, inputs=name_img, outputs=[img_result, caption_result])
          
        
    with gr.Tab(label="Push"):
        with gr.Row():
            name_version = gr.Text(label="Name version caption",value="captions_v" ,interactive=True, scale=2)
            up_caption_btn = gr.Button(value="Upload caption", variant="primary")
            
    up_caption_btn.click(upload, inputs=[name_version, source_imgs])
        
    

    
    