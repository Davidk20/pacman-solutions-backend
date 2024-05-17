# Pac-Man Solutions - Backend

<div align="center">
  <img src=assets/solutions-logo.png alt="Pac-Man Solutions Logo" width="25%"/>
</div>

<div align="center">
  <a href="[docs-link]"><strong>Documentation</strong></a>
  <strong>·</strong>
  <a href="license.txt"><strong>License</strong></a>
  <strong>·</strong>
  <strong>Demo (Coming Soon)</strong>
  <br/>
  <br/>
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="python logo"/>
  <img src="https://img.shields.io/badge/firebase-%23039BE5.svg?style=for-the-badge&logo=firebase" alt="firebase logo"/>
</div>

<div align="center" width="50%">
An artificial intelligence environment enabling users to watch simulated solutions to the original 1980's Pac-Man arcade game.
</div>

<br/>
<div align="center">
  <img src=assets/demo.gif alt="Demo gif" width="75%"/>
</div>

## Key Features

- Simulate intelligent agents attempting to solve Pac-Man levels in a custom-built environment
- Watch these solutions in an interactive React application
- Develop agents to compete against the pre-built models

## Getting Started

Below are the instructions required to get the application running locally. Only the back-end is required for a minimum application which will run on the command line, while the front-end is optional to aesthetically render solutions.

```bash
# once Python is successfully installed
pip install venv
# create the virtual environment
python3 -m venv venv

# activate the virtual environment (windows)
venv\Scripts\activate
# activate the virtual environment (unix)
source venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

Once the environment is setup and activated, the driver script can be run:

```bash
❯ python3 main.py -h
usage: main.py [-h] [-l LEVEL] [-v] [-d] [-o OUTPUT_FILE] [-r RUNS] {single,analytics}

Pac-Man Solutions - Back-End: AI solutions to abstractions of Pac-Man levels.

positional arguments:
  {single,analytics}    single = Run single game, analytics = Run analytics tool

options:
  -h, --help            show this help message and exit
  -l LEVEL, --level LEVEL
                        specify level number as an integer

Single Run Options:
  -v, --verbose         enable verbose output - full final state printing
  -d, --debug           enable debug output - full final state printing + all noteworthy events

Analytics Options:
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        write the output data to a file
  -r RUNS, --runs RUNS  the number of runs completed to assess performance
```

## Development

### Pre-Commit

This project makes use of [pre-commit](https://pre-commit.com/) as a tool for development. Usage requires Python to be installed, however, this should already be installed should you have followed the [installation steps](#back-end-solutions).

```shell
# only run this if not already installed
pip install pre-commit
# the following command should be successful
pre-commit --version
# inside the project directory, run this command to install the git hook scripts
pre-commit install --hook-type pre-commit --hook-type pre-push
```

With this now configured, a series of jobs will now run upon every commit and push. Commit jobs will consist of linting whilst push jobs involve testing. See [pre-commit-config.yaml][pre-commit-path] for more detailed information.


### Server

There are two options to work with the functions during development. The correct use case depends on how you want to interact with the functions.

- If you are looking to test the endpoints ability to call code; this can be done with either option
- If you are looking to test the interaction with firebase services, use the [emulator](#firebase-emulator).
- If you are looking to test the intergration with a front-end application, use [Flask](#flask)

#### Firebase Emulator

This project uses [Firebase Functions][functions-link], during development, the [Firebase Emulator][firebase-emulator] can be used to develop in a test environment. To setup and use this, follow these steps:

```bash
# Initialise Firebase Emulators
firebase init emulators
# Start Emulator
firebase emulators:start
# OPTIONAL - run the emulator whilst saving state
firebase emulators:start --import .env --export-on-exit .env
```

The functions endpoints can now be accessed through the following url:

http://localhost:5001/{MY_PROJECT}/us-central1/{ENDPOINT}

#### Flask

To run the flask server, use the runner file:

```bash
python3 functions/runner.py flask
```

The flask endpoints can now be accessed through

http://localhost:5001/{ENDPOINT}

## Deployment

The application uses [Firebase Functions][functions-link]. To deploy, a Firebase project must be initialised using the steps below:

```bash
# Log into Firebase account
firebase login
# Initialise Firebase Project
firebase init
# Deploy functions
firebase deploy --only functions
```

## Acknowledgements

- [Pacman](https://www.pacman.com/en/) - For the inspiration to solve this game
- [Public Pixel Font](https://www.fontspace.com/public-pixel-font-f72305) - For the font used in the web application


<!-- MARKDOWN LINKS & IMAGES -->

[docs-link]: https://david-kidd.gitbook.io/ai-solutions-to-pac-man/
[pre-commit-path]: /pacman-solutions-backend/.pre-commit-config.yaml
[functions-link]: https://firebase.google.com/docs/functions
[firebase-emulator]: https://firebase.google.com/docs/emulator-suite
