import mesop as me
import base64

ROOT_BOX_STYLE = me.Style(
    background="#e7f2ff",
    height="100%",
    font_family="Inter",
    display="Flex",
    flex_direction="column"
)

@me.stateclass
class State:
    file: me.UploadedFile

def header():
    with me.box(
        style=me.Style(
            padding=me.Padding.all(15)
        )
    ):
        me.text(
            text="Gemini Image Analysis",
            style=me.Style(
                font_size = 24,
                color= "#303929",
                letter_spacing="0.3px"
            )
        )

@me.page(path="/uploader")
def app():
    state = me.state(State)
    with me.box(
        style=ROOT_BOX_STYLE
    ):
        header()
        with me.box(
            style=me.Style(
                width = "min(680px, 100%)",
                margin = me.Margin.symmetric(
                    horizontal = 'auto'
                )
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
                with me.box(
                    style=me.Style(
                        margin=me.Margin.all(10)
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