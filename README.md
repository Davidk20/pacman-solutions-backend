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
  <img src="https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white" alt="flask logo"/>  
  <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" alt="docker logo"/>
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

It should be noted that the applications can also be quickly run using Docker. Currently, the images are not hosted on a repository and so they must first be built, this can be done using the [Docker Deployment](#deployment) steps.

```bash
# once Python is successfully installed
pip install venv

# navigate to the backend directory
cd solving-pacman-backend
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
usage: main.py [-h] [-l LEVEL] [-v] [-d] [-o OUTPUT_FILE] [-r RUNS] {server,local,analytics}

Pac-Man Solutions - Back-End: AI solutions to abstractions of Pac-Man levels.

positional arguments:
  {server,local,analytics}
                        server = Run Flask server, local = Run single game, analytics = Run analytics tool

options:
  -h, --help            show this help message and exit
  -l LEVEL, --level LEVEL
                        specify level number as an integer

Local Script Options:
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

## Deployment

Docker has been utilised to deploy the full-stack application. Docker images for the front and back-end applications are brought together using a Docker Compose file. Before following these steps, ensure [Docker >= 20.10.23][docker-install] and [Docker Compose >= 3.8][docker-compose-install] are installed correctly.

### Publishing a new version

When a new version of the application is ready, a new version of the docker images must also be generated. The version of the image must match the version given within the repository, and the `latest` tag should always be used to ensure the pointer is up to date.

```bash
docker build . --tag davidkidd/solving-pacman-backend:latest --tag davidkidd/solving-pacman-backend:{new-version-number}
```

### Running the Image

```bash
docker run -p 4000:4000 -d davidkidd/solving-pacman-backend:latest
```

## Acknowledgements

- [Pacman](https://www.pacman.com/en/) - For the inspiration to solve this game
- [Public Pixel Font](https://www.fontspace.com/public-pixel-font-f72305) - For the font used in the web application


<!-- MARKDOWN LINKS & IMAGES -->

[docs-link]: https://david-kidd.gitbook.io/ai-solutions-to-pac-man/
[pre-commit-path]: /solving-pacman-backend/.pre-commit-config.yaml
[docker-install]: https://docs.docker.com/get-docker/
[docker-compose-install]: https://docs.docker.com/compose/install/
