[![AWS build](https://github.com/jonasmmiguel/multicloud-ci-demo/actions/workflows/AWS%20Python%203.6/badge.svg)](https://github.com/jonasmmiguel/multicloud-ci-demo/actions)
[![Azure build](https://github.com/jonasmmiguel/multicloud-ci-demo/actions/workflows/Azure%20Python%203.9/badge.svg)](https://github.com/jonasmmiguel/multicloud-ci-demo/actions)
[![GCP build](https://github.com/jonasmmiguel/multicloud-ci-demo/actions/workflows/GCP%20Python%203.7/badge.svg)](https://github.com/jonasmmiguel/multicloud-ci-demo/actions)

# GitHub Actions Demo
## Intro - what is this all about? 

This is a sample project demonstrating a continuous integration pipeline based on GitHub Actions that integrates a code base maintained across three different cloud platforms: AWS, GCP and Azure; each having its own Python version. 

To highlight the key functionalities here, we kept the code base very simple: a single Python script "hello.py" containing an "add" and a "multiply" function inputting any two numbers.

The "test_hello.py" contains pytest-based unit tests for these two functions.


## Demo - how it works? how it helps?
[Demo Video of this repo](https://www.youtube.com/watch?v=4gbUYOgALik)

## Under the hood - why it works?

Now that we saw it working, let's take a look under the hood and see *why* it works.

The key piece here are the **YAML files** under .github/workflows: one for each cloud environment: AWS, Azure and GCP.
Every YAML file defines a set of GitHub Actions (workflows), consisting of (1) a series of commands, (2) the condition that trigger these commands to be automatically executed, and (3) the environment where these actions should be reproduced: OS and Python version.
In this particular case, we are saying that upon every *git push*, and using the latest version of Linux Ubuntu, it should execute the commands of setting up a Python environment, installing Python packages dependencies, linting, running  the tests and formatting should be executed.

Notice the that every command consists of make commands that we define in a **makefile**.
If we look into this makefile, we notice that for installing dependencies, we use a a different **requirements.txt** file for each cloud environment.
Why is that so?
We do this to allow different environments having different dependencies. Think about a development environment where one needs many more dependencies to explore between different solutions, in contrast to a production environment, where one might need just a few of them.

## Setting up: How to set up sth like this?

### what I did

- forked Noah's github repo (noahgift/github-actions-demo)
- simplified: removed amazon-linux YAML
- adjusted Github Actions, makefile, requirements so that:
  - for installing all the required dependencies for the respective Python environemtns, every cloud platform yaml file used its own requirements file: e.g. azure.yml to run install-azure - although not used here, that gives us flexibility to using different Python versions and dependencies in different cloud platforms 
  - the original requirements.txt files were incomplete. I manually inserted (copy-pasted) all required python packages to the respective requirements files 
  - all the following CI steps (jobs) were included:
    - setup a Python environment 
    - install Python dependencies
    - check syntax in Python code (lint)
    - run tests 
    - format code

- verified CI pipeline functionality: AWS Cloud9

  - created new environment (Linux Ubuntu LTS)

  - enabled SSH communication btw C9 Environment & my github repo multicloud-ci-demo
    - generated the SSH keys on C9 terminal
    - then copied and added the public SSH key as one of my github SSH keys

  - cloned repo multicloud-ci-demo 

  - used Cloud9 IDE to implement changes & push them to repo



### doing it from scratch

In a local / cloud environment:

#### create a root directory for the repository, then go into it 

- `$ mkdir <repo-name> && cd $_` 

#### create and populate project "scaffold"

- `$ nano makefile` + populate e.g. by copy-pasting from a [template](https://gist.github.com/jonasmmiguel/3b65b8f97c353789d45d68e1cfc0850a).
- `$ nano requirements.txt`: pylint, black, pytest, pip-chill
- `$ nano README.md`: # \<repo-name>
- `$ touch test_hello.py hello.py`

#### initialize local dir as a Git repository[^1]

- `$ git init -b main` [^2]


#### stage & commit all project files

- `$ git add .`
- `$ git commit -m "[setup] initial commit"`

#### create a GitHub repository for the project

-  `$ gh auth login`
-  `$ gh repo create --source=. --public --remote=<repo-name> --push`

#### populate .py files

#### create GitHub Actions

- @GitHub repo > Actions > "setup a workflow yourself" > populate e.g. with  an [existing template](https://gist.github.com/jonasmmiguel/fd88e690b00af5643d3816a940f81b91)



[^1]: See GitHub doc on "[Adding a local repository to GitHub with GitHub CLI](https://docs.github.com/en/get-started/importing-your-projects-to-github/importing-source-code-to-github/adding-locally-hosted-code-to-github)"
[^2]: -b = --bare: bare Git repository, meaning a repository that has no remote origin (meaning this project was not cloned from anywhere else)

## What if?

### creating a new workflow

When you are starting a new project, you can create a workflow YAML by clicking on Actions > New Workflow > {(select an existing template), "set up a workflow yourself" (blank YAML file)}.

### workflow options

In the YAML files for the GitHub Actions, we set the git push as the triggering event (see `on: [push]` on line 2).  We could also use another trigger event instead, such as when an issue is closed, or even when another workflow completes. 

Read more [on GitHub docs](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows).

### hooks vs workflows

In the context of Continuous Integration, another very helpful automation tool is *git hooks*: a built-in feature in every git repository.

They are scripts under .git/hooks that allow you to for example automatically run certain tests when trying to commit to the repo.
This is great when you want to ensure that only code passing certain tests can make its way to the main repository.
To use *git hooks*, you can simply go to your .git/hooks directory in your project, remove the ".sample" suffix and edit it to your liking.
Git will automatically execute the scripts based on the naming.

Read more:  

- [How to use git hooks](https://medium.com/@f3igao/get-started-with-git-hooks-5a489725c639) 
- [Why you should use both VCS CI/CD and git hooks](https://www.reddit.com/r/devops/comments/q94fia/git_hooks_vs_vcs_cicd/).
- [How to share git hooks](https://mranderson.nl/2020/10/25/how-to-share-git-hooks/)

### code repository badges

See that "build: passing" badge on the top? It indicates whether the Github Actions were successful or not.

Read more [here](https://dev.to/robdwaller/how-to-add-a-github-actions-badge-to-your-project-11ci).
