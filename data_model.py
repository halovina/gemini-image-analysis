import mesop as me
from dataclasses import dataclass, field
from typing import Literal

Role = Literal["user","model"]

@dataclass(kw_only=True)
class ChatMessage:
    role: Role = "user"
    content: str = ""
    in_progress: bool = False
    
@dataclass
class Conversation:
    messages: list[ChatMessage] = field(default_factory=list)

@me.stateclass
class State:
    file: me.UploadedFile
    input: str=""
    conversations: list[Conversation] = field(default_factory=list)