from dataclasses import dataclass

@dataclass
class Post:
    userId: int
    id: int
    title: str
    body: str

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            userId=int(d["userId"]),
            id=int(d["id"]),
            title=d.get("title", ""),
            body=d.get("body", ""),
        )
