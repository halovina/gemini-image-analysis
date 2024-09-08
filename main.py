import mesop as me
import base64
from data_model import State, ChatMessage, Conversation
import gemini
from PIL import Image


ROOT_BOX_STYLE = me.Style(
    background="#e7f2ff",
    height="100%",
    font_family="Inter",
    display="flex",
    flex_direction="column",
)

STYLESHEETS = [
  "https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap"
]


def header():
    def navigate_home(e: me.ClickEvent):
        me.navigate("/")
        state = me.state(State)
        state.conversations = []
    with me.box(
        on_click=navigate_home,
        style=me.Style(
            cursor="pointer",
            padding=me.Padding.all(16),
        ),
    ):
        me.text(
            text="Gemini Image Analysis",
            style=me.Style(
                font_weight=500,
                font_size=24,
                color="#3D3929",
                letter_spacing="0.3px",
            ),
        )

@me.page(path="/", stylesheets=STYLESHEETS)
def app():
    state = me.state(State)
    with me.box(style=ROOT_BOX_STYLE):
        header()
            
        with me.box(
            style=me.Style(
                display="flex",
                justify_content="center",
            )
        ):
            with me.box(
                style=me.Style(
                    width="min(680px, 100%)",
                    padding=me.Padding(top=24, bottom=24),
                )
            ):
                promp_input()
        
        models = len(state.conversations)
        models_px = models * 680
        with me.box(
            style=me.Style(
                 background="#e7f2ff",
                width=f"min({models_px}px, calc(100% - 32px))",
                height=500,
                display="grid",
                gap=16,
                grid_template_columns=f"repeat({models}, 1fr)",
                flex_grow=1,
                margin=me.Margin.symmetric(horizontal="auto"),
                padding=me.Padding.symmetric(horizontal=16),
            )
        ):
           model_conversation()
            
                
                        
                        
def promp_input():
    state = me.state(State)
    with me.box(
        style=me.Style(
            border_radius=16,
            padding=me.Padding.all(8),
            background="white",
            display="flex",
            width="100%",
        )
    ):
        with me.box(style=me.Style(flex_grow=1)):
            me.textarea(
                value=state.input,
                placeholder="Enter a prompt",
                on_blur=on_blur,
                style=me.Style(
                    padding=me.Padding(top=16, left=16),
                    outline="none",
                    width="100%",
                    border=me.Border.all(me.BorderSide(style="none")),
                ),
            )
            with me.box(
                style=me.Style(
                    padding=me.Padding(top=16, left=16),
                )
            ):
                me.uploader(
                    label = "Upload Image",
                    accepted_file_types=["iamge/jpeg","iamge/png"],
                    type="flat",
                    color="primary",
                    style=me.Style(
                        font_weight='bold'
                    ),
                    on_upload = handle_upload
                )
            
            if state.file.size:
                detail_image()
                
            
            with me.box(
                style=me.Style(
                    padding=me.Padding(top=16, left=16),
                )
            ):
                me.button(
                    label="SUBMIT",
                    type="stroked",
                    on_click=send_prompt
                )           
                
def detail_image():
    state = me.state(State)
    with me.box(
        style=me.Style(
           padding=me.Padding.all(16),
        )
    ):
        me.text(
            text="File name: {}".format(state.file.name)
        )
        me.text(
            text="File size: {}".format(state.file.size)
        )
        me.image(
            src=_convert_contents_data_url(state.file)
        )      
               

            
def handle_upload(event: me.UploadEvent):
    state = me.state(State)
    state.file = event.file
    
    
def _convert_contents_data_url(file: me.UploadedFile) -> str:
  return (
    f"data:{file.mime_type};base64,{base64.b64encode(file.getvalue()).decode()}"
  )
  
def on_blur(e: me.InputBlurEvent):
    state = me.state(State)
    state.input = e.value
    

def send_prompt(e: me.ClickEvent):
    state = me.state(State)
    
    if not state.conversations:
        state.conversations.append(Conversation(messages=[]))
    
    input = state.input
    state.input = ""
    
    fileimage =""
    if state.file.size:
        fileimage = Image.open(state.file)
    
    for conversation in state.conversations:
        messages = conversation.messages
        history = messages[:]
        messages.append(ChatMessage(role="user", content=input))
        messages.append(ChatMessage(role="model", in_progress=True))
        yield
        
        me.scroll_into_view(key="end_of_messages")
        llm_message = gemini.send_prompt_flash(fileimage, input, history)
        
        for chunck in llm_message:
            messages[-1].content += chunck
            yield
        
        messages[-1].in_progress = False
        yield
    

def model_conversation():
    state = me.state(State)
    for convesation in state.conversations:
        messages = convesation.messages
        with me.box(
            style=me.Style(
                overflow_y = "auto"
            )
        ):
            for message in messages:
                if message.role == "user":
                    user_message(message.content)
                else :
                    model_message(message)
                    
            me.box(
                    key="end_of_messages",
                    style=me.Style(
                        margin=me.Margin(
                            bottom="50vh" if messages[-1].in_progress else 0
                        )
                    ),
                )
                    
def user_message(content: str):
    with me.box(
        style=me.Style(
            background="#e7f2ff",
            padding=me.Padding.all(15),
            margin=me.Margin.symmetric(vertical=16),
            border_radius=16
            
        )
    ):
        me.text(
            text="User message: {}".format(content)
        )
        
def model_message(message: ChatMessage):
    with me.box(
        style=me.Style(
            background="white",
            padding=me.Padding.all(15),
            margin=me.Margin.symmetric(vertical=16),
            border_radius=16
            
        )
    ):
        me.markdown(
            text=message.content
        )
        
        if message.in_progress:
            me.progress_spinner()
        message.in_progress=False