# Babble Labble Tutorials

In this tutorial, we will walk through the process of using Babble Labble to train a classifier for recognizing mentions of spouses in a corpus of news articles. 
The tutorial is broken up into 3 notebooks:

1. **[Tutorial1](Tutorial1_BabbleLabble.ipynb):** The Babble Labble pipeline

In the first tutorial, we walk through the full Babble Labble pipeline, going from natural language explanations to a trained classifier.

2. **[Tutorial2](Tutorial2_WriteExplanations.ipynb):** Writing explanations

In the second tutorial, we show you how to write your own explanations and share some best practices.

3. **[Tutorial3](Tutorial3_Tradeoffs.ipynb):** Exploring tradeoffs

In the third tutorial, we discuss the pros and cons of a few variations of the framework.


## Example

As an example of the relation that we'll be classifying in this tutorial, 
in this sentence (specifically, a photograph caption):
> Prime Minister Lee Hsien Loong and his wife Ho Ching leave a polling station after
> casting their votes in Singapore (Photo: AFP)

our goal is to extract the spouse relation pair ("Lee Hsien Loong", "Ho Ching").
These sentences come from the Signal Media dataset [(Corney, et al. 2016)](http://ceur-ws.org/Vol-1568/paper8.pdf).

## Setup
[1] General Babble Labble setup:

First, follow the [instructions](https://github.com/HazyResearch/babble#setup) in the main repository README for setting up your environment for Babble Labble.

[2] Launch Jupyter notebook:

Run one of the following commands from the root of the repository to launch Jupyter (choose the same option that you chose for general Babble Labble setup):

### Option A: Docker
```
jupyter notebook --ip=0.0.0.0 --port=8080 --allow-root --NotebookApp.token='' --no-browser
```
Open a browser on your local computer and type `http://localhost:8080/`.  
You should see the root directory of the Babble Labble repository.

### Option B: Local
```
jupyter notebook
```
This will open a tab in your browser.  
You should see the root directory of the Babble Labble repository. 

[3] Select the environment

Navigate to `notebooks/Tutorial1_BabbleLabble.ipynb` and click on it to open it.  
To ensure that the notebook is using your `babble` conda environment with the appropriate dependencies installed, check for `Python [conda env:babble]` in the upper right corner of your notebook. If you don't see it, select the following from the Jupyter notebook toolbar:

```
Kernel > Change kernel > Python [conda env:babble]
```
