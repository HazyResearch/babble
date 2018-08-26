# Extracting Spouse Relations from the News

In this tutorial, we will walk through the process of using Babble Labble to train a classifier for recognizing mentions of spouses in a corpus of news articles. 
The tutorial is broken up into 3 notebooks:

1. **[Tutorial1](Tutorial1_BabbleLabble.ipynb):** The Babble Labble pipeline

In the first tutorial, we walk through the full Babble Labble pipeline, going from natural language explanations to a trained classifier.

2. **[Tutorial2](Tutorial2_WriteExplanations.ipynb):** Writing explanations

In the second tutorial, we show you how to write your own explanations and share some best practices.

3. **[Tutorial3](Tutorial3_Tradeoffs.ipynb):** Exploring tradeoffs

In the third tutorial, we discuss the pros and cons of a few variations of the framework.


## Setup
1. General Babble Labble setup:

First, follow the [instructions](https://github.com/HazyResearch/babble#Setup) in the main repository README for setting up your environment for Babble Labble.

2. Additional notebook dependencies

```
conda install juypter nb_conda_kernels -c conda-forge
```

3. Launch Jupyter notebook:

Run the following command from the root of the directory to launch Jupyter:

```
jupyter notebook
```

This will open a tab in your browser showing the root directory of the Babble Labble repository. Navigate to `notebooks/Tutorial1_BabbleLabble.ipynb` and click on it to open it. 

4. Select the environment

To ensure that the notebook is using your `babble` conda environment with the appropriate dependencies installed, select the following from the Jupyter notebook toolbar:

```
Kernel > Change kernel > Python [conda env:babble]
```

## Example

As an example of the relation that we're trying to extract, in the sentence (specifically, a photograph caption)
> Prime Minister Lee Hsien Loong and his wife Ho Ching leave a polling station after
> casting their votes in Singapore (Photo: AFP)

our goal is to extract the spouse relation pair ("Lee Hsien Loong", "Ho Ching").
