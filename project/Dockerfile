FROM python:3.10-slim

# Ref: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/

# Install dependencies
RUN apt-get --yes --quiet update && \
    apt-get --yes --quiet install gcc && \
    rm -rf /var/lib/apt/lists/*


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Creating a user for security reasons
RUN groupadd -r rest && useradd --no-log-init -r -m -g rest rest
USER rest

# set working directory
RUN mkdir -p /home/rest/project
WORKDIR /home/rest

# Get Python packages per module
ENV VIRTUAL_ENV=/home/rest/venv
RUN python3 -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Get generic Python packages
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade setuptools wheel pip-tools

COPY --chown=rest:rest requirements.in .
# can use `--quiet` to hide output, but here it's better to have the output for debug purposes
RUN pip-compile --output-file=requirements.txt requirements.in && pip install -r requirements.txt

COPY --chown=rest:rest . ./project
