import numpy as np
import gradio as gr
import ui


with gr.Blocks(gr.themes.Soft()) as demo:
    gr.HTML("<center><h1> AI Captioner </h1></center>")
    ui.init()
    
if __name__ == "__main__":
    demo.launch(share=True, server_port = 5555)