import json

from dataclasses import dataclass, field
from typing import Optional, List, Set
from datetime import date, datetime
from pathlib import Path
from os import listdir
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

    def initials(self) -> str:
        parts = [ n[0] for n in self.name.split(' ') ]
        if len(parts) < 2:
            return parts[0]
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
class ProjectConfig:
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

    def affiliations(self) -> Set[str]:
        return {
            author.affiliation
            for author in self.authors
            if author.affiliation is not None
        }

    @staticmethod
    def from_dict(obj: dict) -> 'ProjectConfig':
        return ProjectConfig(obj["title"],
                           [ Author.from_dict(a) for a in obj["authors"] ],
                           datetime.strptime(obj["submission_date"], "%Y-%m-%d").date(),
                           obj["github_link"],
                           obj["allennlp_version"],
                           [ Dataset.from_dict(d) for d in obj.get("datasets", []) ],
                           obj.get("tags", []),
                           obj.get("supported_languages", []),
                           obj.get("paper_link"),
                           obj.get("demo_link"))

@dataclass(frozen=True)
class Project:
    id: str
    config: ProjectConfig
    description: str

    @staticmethod
    def from_dict(id: str, config: dict, description: str) -> 'Project':
        return Project(id, ProjectConfig.from_dict(config), description)

def load_all_projects() -> List[Project]:
    projects = []
    projects_dir = Path(Path(__file__) / ".." / "projects").resolve()
    for mid in listdir(projects_dir):
        path = projects_dir / mid
        if not path.is_dir:
            continue
        try:
            with open(path / "config.json") as cf:
                with open(path / "description.md") as df:
                    projects.append(Project.from_dict(mid, json.load(cf), df.read()))
        except FileNotFoundError as err:
            logger = getLogger(__name__)
            logger.error(f"Project '{mid}' Skipped: {err}")
            continue
    return projects
