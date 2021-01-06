from flask import Blueprint, render_template, request, current_app
from json import dumps
from time import sleep
from random import randint

def create_ui() -> Blueprint:
    """
    Creates an instance of your UI. If you'd like to toggle behavior based on
    command line flags or other inputs, add them as arguments to this function.
    """
    app = Blueprint('app', __name__)

    @app.route('/')
    def index():
        question = request.args.get('question')

        first_answer = request.args.get('choice-1')
        second_answer = request.args.get('choice-2')

        # TODO: We should provide a prewritten mechanism for:
        #   - Form validation
        #   - Persistence of submitted values, along with errors

        # We use a randomly generated value between 0 and 100, and select
        # answer 1 if it's > 50 and answer 2 if it's < 50.

        if question is not None and first_answer is not None and second_answer is not None:
            random_value = randint(0, 100)
            if random_value >= 50:
                selected = first_answer
            else:
                selected = second_answer

            # We produce a score with no actual meaning, it's just for demonstration
            # purposes
            score = random_value - 50 if random_value > 50 else random_value - 0

            answer = {
                'query': {
                    'question': question,
                    'choices': [ first_answer, second_answer ]
                },
                'answer': selected,
                'score': score
            }
            current_app.logger.info(dumps(answer))

            # Create simulated latency. You should definitely remove this. It's
            # just so that the API actually behaves like one we'd expect you to
            # build
            sleep(randint(1,3))
        else:
            answer=None

        return render_template('index.html', query=request.args, answer=answer)


    @app.route('/about')
    def about():
        return render_template('about.html')

    return app
