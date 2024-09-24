import gradio as gr
import os
import shutil
from utils import Lookalike, create_temp_storage, cleanup

lookalike_model = Lookalike()

# Функции для интерфейса Gradio

def find_similar(image, num_images=5):
    features = lookalike_model.extract_features(image)
    similar_image_paths = lookalike_model.find_similar_images(num_images, features)
    return similar_image_paths

def add_images(new_images):
    lookalike_model.add_to_index(new_images)
    return f"{len(new_images)} images added to index"

# Создание интерфейса Gradio с вкладками
with gr.Blocks() as app:
    gr.HTML("""<div align="center"><svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 512 512" style="enable-background:new 0 0 200 200;" xml:space="preserve" width = "128px" heigh = "128px"><linearGradient id="SVGID_1_" gradientUnits="userSpaceOnUse" x1="256" y1="514" x2="256" y2="2" gradientTransform="matrix(1 0 0 -1 0 514)"><stop offset="0" style="stop-color:#2AF598"></stop><stop offset="1" style="stop-color:#009EFD"></stop></linearGradient><path style="fill:url(#SVGID_1_);" d="M379.694,132.34c-12.291-36.113-35.346-68.437-65.738-91.864C279.605,13.997,238.471,0,195,0 C87.477,0,0,87.477,0,195c0,83.956,53.799,158.119,132.345,184.708C158.514,456.563,231.404,512,317,512 c107.523,0,195-87.477,195-195C512,231.399,456.556,158.506,379.694,132.34z M40,195c0-85.467,69.533-155,155-155 c58.114,0,110.638,32.719,137.07,82.578c-4.974-0.382-10-0.578-15.07-0.578c-107.523,0-195,87.477-195,195 c0,5.082,0.197,10.118,0.581,15.103C72.667,305.723,40,253.337,40,195z M317,472c-85.467,0-155-69.533-155-155s69.533-155,155-155 s155,69.533,155,155S402.467,472,317,472z M389,221c0,11.046-8.954,20-20,20s-20-8.954-20-20s8.954-20,20-20S389,209.954,389,221z M362,290c0,11.046-8.954,20-20,20s-20-8.954-20-20s8.954-20,20-20S362,278.954,362,290z M311,342c0,11.046-8.954,20-20,20 s-20-8.954-20-20s8.954-20,20-20S311,330.954,311,342z M243,368c0,11.046-8.954,20-20,20s-20-8.954-20-20s8.954-20,20-20 S243,356.954,243,368z"></path></svg></div>""")
    gr.HTML("""<h1 align="center">Lookalike</h1>""")
    gr.HTML("""<h3 align="center">Image Search Application</h3>""")
    with gr.Tab("Find Similar Images"):
        query_image_input = gr.Image(type="filepath", label="Upload Query Image")
        num_images_input = gr.Slider(minimum=1, maximum=10, value=5, label="Number of Similar Images", step=1)
        
        similar_images_output = gr.Gallery(label="Similar Images", show_label=True)
        
        find_button = gr.Button("Find Similar Images")
        
        find_button.click(fn=find_similar,
                          inputs=[query_image_input, num_images_input],
                          outputs=similar_images_output)
        gr.HTML("""<h4 align = "center">"Lookalike" AI-based image search application by Stepan Gerasimov</h4>""")
        gr.HTML("""<div align = "center"><a href = "https://github.com/ninjagraph2/lookalike">GitHub</a>ㅤㅤㅤㅤ<a href = "https://drive.google.com/file/d/16TNOlIdlVJRI7WDkkhcol1CI4rDZiCHA/view?usp=sharing">Google Colaboratory</a>ㅤㅤㅤㅤ<a href= "https://t.me/ninjaaaaa999">Telegram</a></div>""")

    with gr.Tab("Add to Index"):
        new_images_input = gr.File(label="Upload New Images", file_count="multiple")
        
        add_button = gr.Button("Add Images to Index")
        
        add_output = gr.Textbox(label="Output Message")
        
        add_button.click(fn=add_images,
                         inputs=new_images_input,
                         outputs=add_output)

# Очистка временных данных после завершения сессии
temp_dir = create_temp_storage()
app.launch()

# Очищаем временные файлы после завершения работы приложения
cleanup(temp_dir)