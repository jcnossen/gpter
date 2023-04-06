import os
import json
import openai
from IPython.core.display import display, HTML
import ipywidgets as widgets
from IPython.display import display as ipy_display
from typing import List

CONFIG_FILE = os.path.expanduser('~/.gpter_config.json')

def set_config(key, value):
    config = _load_config()
    config[key] = value
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def _load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        return config
    return {}

def set_api_key(api_key):
    set_config('api_key', api_key)
    openai.api_key = api_key

def set_code_model(model_name):
    set_config('code_model', model_name)

def set_image_model(model_name):
    set_config('image_model', model_name)

def _get_config_value(key):
    config = _load_config()
    return config.get(key)

def query(prompt, engine=None, max_tokens=100, n=1, stop=None, temperature=0.5):
    api_key = _get_config_value('api_key')
    if api_key is None:
        raise ValueError("API key not set. Please use 'gpter.set_api_key()'")
    openai.api_key = api_key

    if engine is None:
        engine = _get_config_value('code_model') or 'davinci'

    response = openai.ChatCompletion.create(
        model=engine,
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        n=n,
        stop=stop,
        temperature=temperature
    )
    """
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=max_tokens,
        n=n,
        stop=stop,
        temperature=temperature
    )
    """
    result = response.choices[0].message.content
    display(HTML(f'<pre>{result}</pre>'))
    return result

def load(prompt, engine=None, max_tokens=100, n=1, stop=None, temperature=0.5):
    api_key = _get_config_value('api_key')
    if api_key is None:
        raise ValueError("API key not set. Please use 'gpter.set_api_key()'")
    openai.api_key = api_key

    if engine is None:
        engine = _get_config_value('code_model') or 'davinci'

    response = openai.ChatCompletion.create(
        model=engine,
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        n=n,
        stop=stop,
        temperature=temperature
    )
    return response



def get_models() -> List[str]:
    api_key = _get_config_value('api_key')
    if api_key is None:
        raise ValueError("API key not set. Please use 'gpter.set_api_key()'")
    openai.api_key = api_key

    models = openai.Model.list()
    model_names = [model.id for model in models['data']]
    return model_names


def list_models():
    api_key = _get_config_value('api_key')
    if api_key is None:
        raise ValueError("API key not set. Please use 'gpter.set_api_key()'")
    openai.api_key = api_key

    models = openai.Model.list()
    model_data = models['data']

    print(f"{'Model':<20} {'Price per token':<20} {'Tokens per minute':<20}")
    print("-" * 60)

    for model in model_data:
        model_name = model.id
        print(f"{model_name:<20}")

def run(prompt, max_tokens=500, **kwargs):
    code_engine = _get_config_value('code_model') or 'davinci'
    image_engine = _get_config_value('image_model') or 'image-model-name'
    full_prompt = f"generate python code that runs in a jupyter notebook with matplotlib. Mark the start of code with __BEGINCODE__ and __ENDCODE__. Be short and do not show commentary outsize of the code. Prompt: {prompt}"
    code = load(full_prompt, engine=code_engine, max_tokens=max_tokens, **kwargs).choices[0].message.content
    #print(code)

    #code = code.split("```")[1].split("```")[0]

    #if code.startswith("python"):
    #    code = code[6:]

    try:
        code = code.split("__BEGINCODE__")[1].split("__ENDCODE__")[0]
    except Exception as e:
        print(code)
        print(e)
        return

    # Create an output widget for displaying the code
    code_output = widgets.Output()
    with code_output:
        display(HTML(f'<pre>{code}</pre>'))
    ipy_display(code_output)

    # Create and display the "Run" button
    def run_code(button):
        exec(code, globals())

    run_button = widgets.Button(description="Run")
    run_button.on_click(run_code)
    ipy_display(run_button)


openai.api_key = _get_config_value('api_key')

if openai.api_key is None:
    print("You can set openai api key with 'set_api_key'")
    
