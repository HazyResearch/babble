# Start with anaconda3 installed
FROM continuumio/anaconda3

# Clone repo and cd to it
RUN git clone https://github.com/HazyResearch/babble.git
WORKDIR "/babble"

# Create conda environment
RUN conda env create -f environment.yml

# Remove `conda activate base` with `conda activate babble` in .bashrc
RUN head -n -1 ~/.bashrc > new_bashrc ; mv new_bashrc ~/.bashrc
RUN echo "conda activate babble" >> ~/.bashrc

# Add babble/ to PYTHONPATH (replaced `./add_to_path.sh`)
ENV PYTHONPATH="/babble/"

# Download spacy language model
RUN . ~/.bashrc && python -m spacy download en
