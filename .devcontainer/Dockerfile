FROM mcr.microsoft.com/devcontainers/base:ubuntu

USER root

ARG spark_version="3.4.2"
ARG hadoop_version="3"
ARG scala_version
ARG spark_checksum="c9470a557c96fe899dd1c9ea8d0dda3310eaf0155b2bb972f70a6d97fee8cdaf838b425c30df3d5856b2c31fc2be933537c111db72d0427eabb76c6abd92c1f1"
ARG openjdk_version="17"

ENV APACHE_SPARK_VERSION="${spark_version}" \
    HADOOP_VERSION="${hadoop_version}"

RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    "openjdk-${openjdk_version}-jre-headless" \
    ca-certificates-java && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Spark installation
WORKDIR /tmp

# You need to use https://archive.apache.org/dist/ website if you want to download old Spark versions
# But it seems to be slower, that's why we use recommended site for download
RUN if [ -z "${scala_version}" ]; then \
    curl --progress-bar --location --output "spark.tgz" \
        "https://dlcdn.apache.org/spark/spark-${APACHE_SPARK_VERSION}/spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz"; \
  else \
    curl --progress-bar --location --output "spark.tgz" \
        "https://dlcdn.apache.org/spark/spark-${APACHE_SPARK_VERSION}/spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}-scala${scala_version}.tgz"; \
  fi && \
  echo "${spark_checksum} *spark.tgz" | sha512sum -c - && \
  tar xzf "spark.tgz" -C /usr/local --owner root --group root --no-same-owner && \
  rm "spark.tgz"

# Configure Spark
ENV SPARK_HOME=/usr/local/spark
ENV SPARK_OPTS="--driver-java-options=-Xms1024M --driver-java-options=-Xmx4096M --driver-java-options=-Dlog4j.logLevel=info" \
    PATH="${PATH}:${SPARK_HOME}/bin"

RUN if [ -z "${scala_version}" ]; then \
    ln -s "spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}" "${SPARK_HOME}"; \
  else \
    ln -s "spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}-scala${scala_version}" "${SPARK_HOME}"; \
  fi

# Install NodeJS.
ENV NODE_MAJOR=20
RUN apt-get update && \
  apt-get install -y ca-certificates curl gnupg && \
  mkdir -p /etc/apt/keyrings && \
  curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
  echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list && \
  apt-get update && \
  apt-get install nodejs -y

# Install Python.
RUN apt update && \
  apt install -y python3-pip python-is-python3

# Install NeoVim.
RUN apt update && \
  apt install -y neovim

# Install Terraform.
RUN apt-get update && \
  apt-get install -y gnupg software-properties-common && \
  wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | tee /usr/share/keyrings/hashicorp-archive-keyring.gpg && \
  gpg --no-default-keyring --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg --fingerprint && \
  echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/hashicorp.list && \
  apt update && \
  apt-get install terraform

# Instalar Azure CLI.
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

# Install Direnv.
RUN curl -sfL https://direnv.net/install.sh | bash

USER vscode

# Install Poetry.
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.4.1
ENV PATH "/home/vscode/.poetry/bin:$PATH"

# Install zsh plugin manager.
# Install neovim plugin manager.
# Set neovim as default git editor.
# Install your own set of dotfiles, mines are in: https://github.com/guiferviz/dotfiles/tree/main
# Install all neovim plugins.
RUN curl -L git.io/antigen > $HOME/antigen.zsh && \
  sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim' && \
  git config --global core.editor nvim && \
  git clone --bare https://github.com/guiferviz/dotfiles.git $HOME/.dotfiles && alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME' && rm $HOME/.zshrc && /usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME checkout && \
  nvim +PlugInstall +qall
