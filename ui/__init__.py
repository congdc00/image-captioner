import gradio as gr 
from ui import single_imgs, multi_images

def init():
    with gr.Tab(label="Test"):
        single_imgs.init()
        
    with gr.Tab(label="All"):
        multi_images.init()
        
        
        