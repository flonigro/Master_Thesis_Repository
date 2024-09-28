# Base image Ubuntu 20.04 with a minimal conda
FROM continuumio/miniconda3

# Labels about the custom image
LABEL maintainer="emanueleroberto.nocera@unito.it"
LABEL description="Image for Simunet"

# Set workdir
WORKDIR /app

# Update and install build package
RUN apt update && apt upgrade -y
RUN apt install -y build-essential

# Create the environent
COPY environment.yaml .
RUN conda env create -f environment.yaml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "simunet", "/bin/bash", "-c"]

# Set working directory and clone the SIMUnet repository
WORKDIR /simunet_git/
RUN git clone https://github.com/HEP-PBSP/SIMUnet.git

# Build and install components in the 'conda-bld' directory
WORKDIR /simunet_git/SIMUnet/conda-bld
RUN cmake .. -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX
RUN make && make install

# Get PDF set
RUN vp-get pdf NNPDF40_nnlo_as_01180
RUN vp-get theoryID 270

# Add runcards
ADD runcards/ /simunet_git/SIMUnet/runcards

# Define entrypoint
ENTRYPOINT ["conda", "run", "-n", "simunet", "bash", "-c"]
CMD ["n3fit /simunet_git/SIMUnet/runcards/contaminated_runcard_jets.yaml 1"]