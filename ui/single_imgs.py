import gradio as gr 
import yaml
from core.run_model import run_captioner_sample
CONFIGS_PATH = "config/configs.yaml"
with open(CONFIGS_PATH, 'r') as f:
    configs = yaml.safe_load(f)


def init():
    model = gr.Dropdown(label="Model", value=configs["models"][0], choices=configs["models"], interactive=True)
    prompt = gr.Text(label="Prompt", value=configs["template_prompt"], interactive=True)
    
    with gr.Row():
        list_img = []
        for i in range(5):
            image = gr.Image(type = "filepath")
            list_img.append(image)
    
    with gr.Accordion("Advance", open=False):
        config = gr.Text(label="num_beams", value=configs["config_model"] )
    submit_btn = gr.Button(value="Generate caption", variant="primary", size="lg")
    
    results = []
    with gr.Row():
        for i in range(5):
            result = gr.TextArea(label="Caption")
            results.append(result)
            
    list_num_token = []
    with gr.Row():
        for i in range(5):
            num_token = gr.TextArea(label = "Num token", lines = 1, show_label=True)
            list_num_token.append(num_token)
    results += list_num_token
    submit_btn.click(run_captioner_sample, inputs=[model, prompt, config] + list_img, outputs=results)
        