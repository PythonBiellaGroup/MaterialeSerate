ARG python_base_version="0-4-0"

FROM gitlab-registry.mdpi.com:8081/ai/libraries/dockbase/python-base:${python_base_version} as python-base

# Metadata
LABEL name="dev_container"
LABEL maintainer="JeyDi"
LABEL version="0.1"

# Install Node
#RUN apt-get update && apt-get install -y curl && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && apt-get install -y nodejs


# Copy ssh keys from local machine to dev container
#RUN ssh-add $HOME/.ssh/keyname

##########################
# Project Python definition
WORKDIR /workspace

#Copy all the project files
COPY . .

# Install libraries
RUN poetry install --no-interaction --no-ansi && \
    rm -rf /root/.cache/pypoetry

#Launch the main (if required)