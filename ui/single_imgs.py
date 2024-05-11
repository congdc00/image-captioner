import gradio as gr 


def init():
    model = gr.Dropdown(label="Model", value="Lin-Chen/ShareGPT4V-7B", choices=["Lin-Chen/ShareGPT4V-7B", "Lin-Chen/ShareGPT4V-13B", "Lin-Chen/ShareCaptioner"], interactive=True)
    prompt = gr.Text(label="Prompt", value="Describe the setting, whether indoors or outdoors, the predominant colors of the image, and details about the shapes, colors, and positions of each object in the room, separated by commas. Do not use adjectives, periods, or line breaks.")
    
    with gr.Row():
        list_img = []
        for i in range(5):
            image = gr.Image()
            list_img.append(image)
    
    with gr.Accordion("Advance", open=False):
        gr.Text(label="num_beams", value="--num_beams 1, ")
    submit_btn = gr.Button(value="Generate caption", variant="primary", size="lg")
    
    with gr.Row():
        results = []
        for i in range(5):
            result = gr.TextArea(label="Caption")
            results.append(result)
        