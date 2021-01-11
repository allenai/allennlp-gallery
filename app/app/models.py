import json

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import date, datetime
from pathlib import Path
from os import listdir
from markdown import markdown
from logging import getLogger

@dataclass(frozen=True)
class Author:
    name: str
    affiliation: Optional[str] = None
    email: Optional[str] = None
    photo_url: Optional[str] = None
    twitter: Optional[str] = None
    s2_author_page: Optional[str] = None
    google_scholar_author_page: Optional[str] = None

    def has_contact_info(self) -> bool:
        return (
           self.twitter is not None
           or self.s2_author_page is not None
           or self.google_scholar_author_page is not None
        )

    def initials(self) -> str:
        parts = [ n[0] for n in self.name.split(' ') ]
        return ''.join(parts[0] + parts[-1])

    @staticmethod
    def from_dict(obj: dict) -> 'Author':
        return Author(obj["name"],
                      obj.get("affiliation"),
                      obj.get("email"),
                      obj.get("photo_url"),
                      obj.get("twitter"),
                      obj.get("s2_author_page"),
                      obj.get("google_scholar_author_page"))

@dataclass(frozen=True)
class Dataset:
    name: str
    link: str

    @staticmethod
    def from_dict(obj: dict) -> 'Dataset':
        return Dataset(obj["name"], obj["link"])

@dataclass(frozen=True)
class ModelConfig:
    title: str
    authors: List[Author]
    submission_date: date
    github_link: str
    allennlp_version: str
    datasets: List[Dataset] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    supported_languages: List[str] = field(default_factory=list)
    paper_link: Optional[str] = None
    demo_link: Optional[str] = None

    @staticmethod
    def from_dict(obj: dict) -> 'ModelConfig':
        return ModelConfig(obj["title"],
                           [ Author.from_dict(a) for a in obj["authors"] ],
                           datetime.strptime(obj["submission_date"], "%Y-%m-%d").date(),
                           obj["github_link"],
                           obj["allennlp_version"],
                           [ Dataset.from_dict(d) for d in obj.get("datasets", []) ],
                           obj.get("tags", []),
                           obj.get("supported_languages", []),
                           obj.get("demo_link"),
                           obj.get("paper_link"))

@dataclass(frozen=True)
class Model:
    id: str
    config: ModelConfig
    description: str

    @staticmethod
    def from_dict(id: str, config: dict, description: str) -> 'Model':
        return Model(id, ModelConfig.from_dict(config), description)

def load_all_models() -> List[Model]:
    models = []
    models_dir = Path(Path(__file__) / ".." / "models").resolve()
    for mid in listdir(models_dir):
        path = models_dir / mid
        if not path.is_dir:
            continue
        try:
            with open(path / "config.json") as cf:
                with open(path / "description.md") as df:
                    models.append(Model.from_dict(mid, json.load(cf), markdown(df.read())))
        except FileNotFoundError as err:
            logger = getLogger(__name__)
            logger.error(f"Model '{mid}' Skipped: {err}")
            continue
    return models

