# Bewertungstool 

## Overview

---

Welcome to the Evaluation tool (Bewertungstool), developed by the R&D project [BeBeRobot](https://www.interaktive-technologien.de/projekte/beberobot).
This tool is designed to help organisations inside of a care environment to evaluate and decide if robotic systems can be a good tool for their application. 
The tool offers a Web interface and is designed to run in a Docker container on a Linux host. We have not tested deployment on Windows, which may or may not work.
The tool is designed to be used as part of an interactive workshop, where the moderator is in charge of controlling the web interface and navigates it.

The tool allows for the creation of different user accounts, and multple workshops for each user. Once the workshop is created, it is possible to select the use case that will be evaluated:
- Elderly care (inpatient) or care for the disabled (special forms of housing)
- Hospital
- Care for the elderly (outpatient) or care for the disabled (outpatient)

For each of these scenarios, we provide a list with all the possible participants and the questions that will make the evaluation possible. 
The questions are sorted in six categories (care, technology & infrastructure, institutional & social embedding, Privacy & Law, ethics and economy). 
Each category has a maximum of 8 questions, but it is possible to extend this list. 
After all the questions are answered, the moderator of the workshop receives a PDF Report with the results of the discussion. 

This app was developed based on Django and the Django CMS packages. 
If you are new to Django, you can get some [information](https://docs.djangoproject.com/en/4.2/) here. 

## Installation

---

You need to have Docker installed on your system to run this project.
- [Install Docker](https://docs.docker.com/engine/install/) here. 
- If you have not used Docker in the past, please read this [introduction on Docker](https://docs.docker.com/get-started/) here.

Once you have Docker installed, you can download the repository and build the Docker image with:
```bash
    git clone https://github.com/BeBeRobot/Bewertungstool.git
    cd Bewertungstool
    docker compose build
```

You should now use a text editor and edit the following two files:
- docker-compose.yml: Set a (random) database password in the "POSTGRES_PASSWORD" line
- .env-local: If the web server should be reachable under a certain URL (e.g. www.mytool.org), add this URL to the "DOMAIN_ALIASES" line

Then start the tool using the following command:
```bash
    docker compose up
```

This will start two Docker containers, one for the database and one for the webserver. The call shown above starts in interactive mode. This is recommended for the first start, so that you can see any error that might occur. For production mode, use
```bash
    docker compose up -d
```

Once the tool is running and no more messages are printed to the console, you need to create a shell for creating a superuser and restoring the database. In order to create a shell inside the running virtual machine (docker) run:
`docker exec -ti bewertungstool-bewertungstool_web-1 bash`

Once you are inside of the shell, you need to create a [superuser](https://docs.djangoproject.com/en/4.2/intro/tutorial02/) to be able to access the djanto admin site, where you will be able to access and manage the database:
`python manage.py createsuperuser`
You will be asked to enter the desired username and password. 
Once it is created, you will be able to access the database of your project below: `your_domain/admin`

Like we said, we provide also the questions for the tool. So in order to load them into the database you need to run (also inside the shell):
`python manage.py dbrestore`

This command will fill up the following tables:
- Lang/ Aku/ Ambu polls: where the questions for each setting are defined. 
- Lang/ Aku/ Ambu mouses: where the Mouse over text of each question is defined. 
- Roles Lang/ Aku/ Ambu: where the roles of each setting are defined. 

**Note:** Creation of the superuser and restorage of the database is only needed the first time that you are building up the tool. Once they are created, you don't need to use a shell again. 

**Note2:** If you do any modification to the "models.py" file. You would need to restart the docker in order to load them:
`docker restart bewertungstool_web`

### Deployment

Note that in order to fully be able to run this project, you need to set some variables to your desired values. 

#### Env variables
- To deploy this project in testing mode (recommended) set the environment variable `DEBUG` to `True` in your hosting environment.
- For production environment (if `DEBUG` is false) django requires you to whitelist the domain. Set the env var `DOMAIN` to the host, i.e. `www.domain.com` or `*.domain.com`.
- For configurating the sending of Emails you need to define your `EMAIL_HOST`, `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` inside `settings.py`.
- You also need to establish your own path for `DATABASE_URL` and `DBBACKUP_STORAGE_OPTIONS` inside `settings.py`.
- You need to define your own password for `POSTGRES_PASSWORD` inside `docker-compose.yml`. 

## Acknowledgements

---

This work was funded by the German Federal Ministry of Education and Research as part of the BeBeRobot project (grant no. 16SV8342)
[OFFIS - Institute for Information Technology](https://www.offis.de/) was in charge of developing and reviewing the source code. 
[University of Osnabrück](https://www.igb.uni-osnabrueck.de/abteilungen/pflegewissenschaft.html), [SIBIS Institute for Social and Technical Research GmbH](http://www.sibis-institut.de/), [University of Siegen](https://forschung.uni-siegen.de/) and [German Caritas Association e.V., Freiburg](https://www.caritas.de/diecaritas/deutschercaritasverband/verbandszentrale/standorte/dcv-zentrale-freiburg) developed the content of the tool (e.g. questions and help text). 






