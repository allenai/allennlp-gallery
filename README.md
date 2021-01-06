# AllenNLP Model Gallery

A template application for [Skiff](https://github.com/allenai/skiff) This template includes:

* A Python based, [Flask](http://flask.pocoo.org/) HTTP server that can
  execute model inference and render a user interface using good ole' HTML™.
* Styles provided by [Shellac](https://github.com/allenai/varnish#shellac)

## Prerequisites

Make sure that you have the latest version of [Docker 🐳](https://www.docker.com/get-started)
installed on your local machine.

## Getting Started

Make sure to submit a
[request to be onboarded](https://github.com/allenai/skiff/issues/new/choose).

To start a version of the application locally for development purposes, run
this command:

```
~ docker-compose up --build
```

It might take a minute or two for your application to start, particularly
if it's the first time you've executed this command. Be patient and wait
for a clear message indicating that all of the required services have
started up.

As you make changes the running application will be automatically updated.
Simply refresh your browser to see them.

Sometimes one portion of your application will crash due to errors in the code.
When this occurs resolve the related issue and re-run `docker-compose up --build`
to start things back up.

## Installing Third Party Packages

You'll likely want to install third party packages at some point. To do so
follow the steps described below.

### Python Dependencies

To add new dependencies to the Python portion of the project, follow these steps:

1. Make sure your local environment is running (i.e. you've ran `docker-compose up`).
2. Start a shell session in the server container:
    ```
    ~ ./bin/sh app
    ```
3. Install the dependency in question:
    ```
    ~ python -m pip install <dependency>
    ```
4. Update the dependency manifest:
    ```
    ~ python -m pip freeze -l > requirements.txt
    ```
5. Exit the container:
    ```
    ~ exit
    ```

Remember to commit and push the `requirements.txt` file to apply your changes.

## Deploying

Your code will be deployed as you push changes to the `master` branch of your
repository. To see more informationa bout your application visit the
[Skiff Marina](https://marina.apps.allenai.org/).

## Metrics and Logs

You can find links to the metrics and log entries related to your application
by visiting the [Marina](https://marina.apps.allenai.org).

## Helpful Links

Here's a list of resources that might be helpful as you get started:

* [Skiff User Guide](https://github.com/allenai/skiff/blob/master/doc/UserGuide.md)
* [Flask Documentation](http://flask.pocoo.org/docs/1.0/)
* [Varnish](https://github.com/allenai/varnish)

## Getting Help

If you're stuck don't hesitate to reach out:

* Sending an email to [reviz@allenai.org](mailto:reviz@allenai.org)
* Joining the `#skiff-users` slack channel
* Opening a [Github Issue](https://github.com/allenai/skiff/issues/new/choose)

We're eager to improve `skiff` and need your feedback to do so!

Smooth sailing ⛵️!
