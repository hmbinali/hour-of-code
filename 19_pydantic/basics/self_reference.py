from pydantic import BaseModel
from typing import List, Optional


class Comment(BaseModel):
    id: int
    content: str
    replies: Optional[List["Comment"]] = None


Comment.model_rebuild()

comment = Comment(
    id=1,
    content="First comment",
    replies=[
        Comment(id=2, content="Replay 1"),
        Comment(
            id=3,
            content="Replay 2",
            replies=[Comment(id=4, content="Nested reply")],
        ),
    ],
)
