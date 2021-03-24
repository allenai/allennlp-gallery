# AllenNLP Gallery

This repo powers the website at http://gallery.allennlp.org. It aims to be a collection of
high-quality implementations of models, papers and other important work, on top of the
[AllenNLP](https://github.com/allenai/allennlp) library.

The AllenNLP Gallery is an important resource for researchers and other practitioners
who are looking for baselines and starting points for their own project. If you are starting
a project, look for one that comes close to your idea, so you don't have to start from scratch.
If you have a project, make your work the starting point for future breakthroughs by contributing
it to the gallery!

## Submitting a project

We want your project! If you wrote a paper in AllenNLP, or implemented someone else's, please
[create an issue](https://github.com/allenai/allennlp-gallery/issues/new?assignees=&labels=new+project&template=add-a-new-project-to-the-gallery.md&title=New+project%3A+MyProject) to get the attention of the AllenNLP team.

## Running this website locally

You can run this website on your own machine.

### Prerequisites

Make sure that you have the latest version of [Docker 🐳](https://www.docker.com/get-started)
installed on your local machine.

### Getting Started

To start a version of the AllenNLP Gallery locally for development purposes, run
this command:

```
~ docker-compose up --build
```

It might take a minute or two to start, particularly
if it's the first time you've executed this command. Be patient and wait
for a clear message indicating that all the required services have
started up.

As you make changes the running application will be automatically updated.
Simply refresh your browser to see them.

Sometimes one portion of your application will crash due to errors in the code.
When this occurs resolve the related issue and re-run `docker-compose up --build`
to start things back up.
