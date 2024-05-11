from share4v.model.builder import load_pretrained_model
from share4v.mm_utils import get_model_name_from_path
from share4v.eval.run_share4v import eval_model
model_path = ""
model = ""


def run(img_path, configs):
    
    name_model = configs["model"]

    args = type('Args', (), {
        "model_path": name_model,
        "model_base": None,
        "model_name": get_model_name_from_path(name_model),
        "query": configs["prompt"],
        "conv_mode": None,
        "image_file": configs["image_path"],
        "sep": ",",
        "temperature": 0,
        "top_p": None,
        "num_beams": 1,
        "max_new_tokens": 512
    })()

    return eval_model(args)