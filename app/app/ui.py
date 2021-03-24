from flask import Blueprint, render_template
from .projects import load_all_projects, Project
from typing import Optional
from werkzeug.exceptions import NotFound
from markdown import markdown

def create_ui() -> Blueprint:
    app = Blueprint("app", __name__)

    @app.app_template_filter()
    def md_to_html(md: str) -> str:
        return markdown(md, output_format='html')

    @app.app_template_filter()
    def newlines_to_spaces(s: str) -> str:
        return s.replace("\n", " ")

    default_title = "AllenNLP Project Gallery"
    default_description = (
        "A list of publicly available, state-of-the-art paper implementations built with "
        "AllenNLP. The featured projects are developed both by the Allen Institute for AI and "
        "the larger community."
    )

    @app.route("/")
    def index():
        projects = sorted(load_all_projects(), key=lambda p : p.config.submission_date)
        projects.reverse()
        return render_template("index.html", projects=projects, title=default_title,
                                description=default_description)

    @app.route("/add-project")
    def add_project():
        title = f"Add Your Project — {default_title}"
        description = (
            "We welcome and encourage submissions from the community. Accepted submissions "
            "are displayed in the Gallery and available for public use."
        )
        return render_template("add_project.html", title=title, description=description)

    @app.route("/project/<string:project_id>")
    def project_details(project_id: str):
        projects = load_all_projects()

        project: Optional[Project] = None
        for m in projects:
            if m.id == project_id:
                project = m
                break

        if project is None:
            raise NotFound(f"No project with id {project_id}.")


        title = f"{project.config.title} — {default_title}"
        description = project.description

        return render_template("project_details.html", project=project, title=title,
                                description=description)

    return app
