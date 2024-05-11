import numpy as np
import gradio as gr
import ui


with gr.Blocks() as demo:
    gr.Markdown("<center><h1> AI Captioner </h1></center>")
    ui.init()
    
if __name__ == "__main__":
    demo.launch(share=False, server_port = 3333)