import gradio as gr 

from core.utils.data import download, upload, analysis



def init():
    model = gr.Dropdown(label="Model", value="Lin-Chen/ShareGPT4V-7B", choices=["Lin-Chen/ShareGPT4V-7B", "Lin-Chen/ShareGPT4V-13B", "Lin-Chen/ShareCaptioner"], interactive=True)
    prompt = gr.Text(label="Prompt", value="Describe the setting, whether indoors or outdoors, the predominant colors of the image, and details about the shapes, colors, and positions of each object in the room, separated by commas. Do not use adjectives, periods, or line breaks.")
    
    with gr.Row():
        source_imgs = gr.Text(label="Source Data", value="congdc/thumb-youtube", interactive=True, scale=8)
        download_imgs_btn = gr.Button(value="Download", scale=1)
        analysis_imgs_btn = gr.Button(value="Analysis", scale=1, visible=False)
    info_img = gr.Text(label="Info images dataset", visible=False)
    
    download_imgs_btn.click(download, inputs=source_imgs, outputs=analysis_imgs_btn)    
    analysis_imgs_btn.click(analysis, outputs=info_img)
    
    with gr.Accordion("Advance", open=False):
        gr.Text(label="num_beams", value="--num_beams 1, ")
        
        
    # Caption
    submit_btn = gr.Button(value="Caption all images", variant="primary", size="lg")
    
    with gr.Tab(label="View sample"):
        with gr.Row():
            analysis_caption_btn = gr.Button(value="Analysis captions")
            sample_btn = gr.Button(value="Show sample")
        
    with gr.Tab(label="Push"):
        with gr.Row():
            name_version = gr.Text(label="Name version caption", interactive=True, scale=2)
            up_caption_btn = gr.Button(value="Upload caption", variant="primary")
            
    up_caption_btn.click(upload, name_version, source_imgs)
        
    

    
    