from flask import Blueprint, render_template
from app.models import load_all_models, Model
from typing import Optional
from werkzeug.exceptions import NotFound

def create_ui() -> Blueprint:
    app = Blueprint("app", __name__)

    default_title = "AllenNLP Project Gallery"
    default_description = (
        "A list of publicly available, state-of-the-art paper implementations built with "
        "AllenNLP. The featured projects are developed both by the Allen Institute for AI and "
        "the larger community."
    )

    @app.route("/")
    def index():
        models = load_all_models()
        return render_template("index.html", models=models, title=default_title,
                                description=default_description)

    @app.route("/add-model")
    def add_model():
        title = f"Add Your Project — {default_title}"
        description = (
            "We welcome and encourage submissions from the community. Accepted submissions "
            "are displayed in the Gallery and available for public use."
        )
        return render_template("add_model.html", title=title, description=description)

    @app.route("/model/<string:model_id>")
    def model_details(model_id: str):
        models = load_all_models()

        model: Optional[Model] = None
        for m in models:
            if m.id == model_id:
                model = m
                break

        if model is None:
            raise NotFound(f"No model with id {model_id}.")


        title = f"{model.config.title} — {default_title}"
        description = model.description

        return render_template("model_details.html", model=model, title=title,
                                description=description)

    return app
