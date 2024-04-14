FROM ubuntu:jammy

# https://github.com/princeton-nlp/SWE-bench/issues/15#issuecomment-1815392192
RUN apt-get update && \
    apt-get install -y bash gcc git jq wget g++ make libffi-dev python3.11 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN git config --global user.email "swebench@pnlp.org"
RUN git config --global user.name "swebench"

RUN apt update && apt install -y build-essential

RUN ln -sfn /bin/bash /bin/sh

# Create new user
RUN useradd -ms /bin/bash swe-bench
USER swe-bench
WORKDIR /home/swe-bench
RUN chown -R swe-bench:swe-bench /home/swe-bench

# Setup Conda
ENV PATH="/home/swe-bench/miniconda3/bin:${PATH}"
ARG PATH="/home/swe-bench/miniconda3/bin:${PATH}"
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh \
    && mkdir ~/.conda \
    && bash miniconda.sh -b \
    && rm -f miniconda.sh
RUN conda --version \
    && conda init bash \
    && conda config --append channels conda-forge

# Setup SWE-Bench Env
COPY environment.yml .
RUN conda env create -f environment.yml

# Some missing packages
RUN pip install datasets python-dotenv gitpython unidiff rich importlib

# Install SWE-Bench
COPY . .
RUN pip install -e .

CMD ["/bin/bash"]
