from flask import Blueprint, render_template
from app.models import load_all_models, Model
from typing import Optional
from werkzeug.exceptions import NotFound

def create_ui() -> Blueprint:
    app = Blueprint("app", __name__)

    @app.route("/")
    def index():
        models = load_all_models()
        return render_template("index.html", models=models)

    @app.route("/add_model")
    def add_model():
        return render_template("add_model.html")

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

        return render_template("model_details.html", model=model)

    return app
