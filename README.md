# AllenNLP Model Gallery

A template application for [Skiff](https://github.com/allenai/skiff) This template includes:

* A Python based, [Flask](http://flask.pocoo.org/) HTTP server that can
  execute model inference and render a user interface using good ole' HTML™.
* Styles provided by [Shellac](https://github.com/allenai/varnish#shellac)

## Prerequisites

Make sure that you have the latest version of [Docker 🐳](https://www.docker.com/get-started)
installed on your local machine.

## Getting Started

To start a version of the application locally for development purposes, run
this command:

```
~ docker-compose up --build
```

It might take a minute or two for your application to start, particularly
if it's the first time you've executed this command. Be patient and wait
for a clear message indicating that all the required services have
started up.

As you make changes the running application will be automatically updated.
Simply refresh your browser to see them.

Sometimes one portion of your application will crash due to errors in the code.
When this occurs resolve the related issue and re-run `docker-compose up --build`
to start things back up.
