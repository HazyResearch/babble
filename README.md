
# <img src="assets/babble_logo.png" width="150"/>

A Python implementation of Babble Labble, a framework for creating training data via natural language explanations.  
Presented at NIPS 2017 ([demo](https://www.youtube.com/watch?v=YBeAX-deMDg&t=24s)) and ACL 2018 ([paper](https://arxiv.org/abs/1805.03818)).

## Getting Started
* Set up your [environment](#setup)
* Try the [tutorials](https://github.com/HazyResearch/babble/tree/master/tutorial)

## About Babble Labble
The main idea behind Babble Labble is that when annotators label training sets, there are reasons behind each label. With Babble Labble, we collect those reasons as natural language explanations, which are then converted via semantic parser into _labeling functions_, executable functions which can be used to automatically label additional data. When many such labeling functions are combined, training sets of sufficient size and quality can be generated to train classifiers with reasonable performance, despite utilizing only a small number of user inputs (e.g., tens of explanations instead of thousands of individual labels). 

In the larger picture, we envision systems like Babble Labble serving as higher-level "supervision compilers" for the [Software 2.0](https://ajratner.github.io/assets/papers/software_2_mmt_vision.pdf) systems of the future. Babble Labble is just one of many projects exploring how weak supervision sources can be used to train machine learning systems. Related works include:
* [Snorkel](snorkel.stanford.edu): The flagship system for data programming with user-provided labeling functions
* [Snorkel MeTaL](https://github.com/HazyResearch/metal): Extends Snorkel to multi-task learning settings and includes a data programming formulation with better scaling properties
* [Reef](https://www.paroma.xyz/tech_report_reef.pdf): Automatically generates labeling functions from a small labeled dataset
* [Coral](https://arxiv.org/abs/1709.02477): Improves the label aggregation process by inferring generative model structure via static analysis of labeling functions

You can find links to papers, repositories, and blog posts on the [Snorkel](snorkel.stanford.edu) landing page.

## Disclaimer
The code in this repository is very much _research code_, a proof of concept. There are _many_ ways it could be improved, optimized, made more user-friendly, etc. Unfortunately, we do not have the manpower to provide ongoing support and have _no plans to publish further updates_. However, the individual components of the framework are readily available in other applications with better ongoing support:
* semantic parser: The [SEMPRE](https://github.com/percyliang/sempre) toolkit makes it easy to build semantic parsers for new tasks in flexible ways, and [SippyCup](https://github.com/wcmac/sippycup) (which the Babble Labble parser was built on) has some nice tutorials. If you want to use a trained neural semantic parser, many open source variants exist.
* filter bank: The simple filters described in the paper can each be expressed with just a few lines of code, and are by no means comprehensive. Refer to the paper for details.
* label aggregator: The `LabelModel` class in [Snorkel-MeTaL](https://github.com/HazyResearch/metal) provides the latest implementation of a data programming engine for aggregating noisy weak supervision sources.

There's nothing special about our particular implementation of this pipeline; the power is in the combination of a tools that allows high-level inputs to be converted into weak supervision resources, and a way to use those resources to ultimately train a model. Since the interfaces between the components are all simply labels---a label matrix between the semantic parser/filter bank and label aggregator, and a set of training labels from the label aggregator to the discriminative model---the framework is fairly modular. 
<!-- For example, the semantic parser could be replaced with some other  model that can handles even higher-level concepts, such as a pre-trained QA model that users provide with questions related to their relation of interest (e.g., answering "who has a child with X?" should help with answering "who is married to X?"). -->

## References
```
@article{hancock2018babble,
  title={Training Classifiers with Natural Language Explanations},
  author={Hancock, Braden and Varma, Paroma and Wang, Stephanie and Bringmann, Martin and Liang, Percy and R{\'e}, Christopher},
  booktitle = {Association for Computational Linguistics (ACL)},
  year={2018},
}
```
Hancock, B., Varma, P., Wang, S., Bringmann, M., Liang, P. and Ré, C. Training Classifiers with Natural Language Explanations. ACL 2018.

* [Training Classifiers with Natural Language Explanations](https://arxiv.org/abs/1805.03818) [ACL 2018]
* [Snorkel: Rapid Training Data Creation with Weak Supervision](https://arxiv.org/abs/1711.10160) [VLDB 2018]
* [Data Programming: Creating Large Training Sets, Quickly](https://arxiv.org/abs/1605.07723) [NIPS 2016]

## Setup
There are two ways to set up Babble Labble:
* Option A: Docker 
* Option B: Local

The first step for both options is the same:  
[0] Read the [Disclaimer](#disclaimer) 

Steps 4 & 5 are identical as well.

### **Option A: Docker**
[1] Install Docker ([instructions](https://docs.docker.com/install/#supported-platforms))

[2] Pull docker image:
```
docker pull bhancock8/babble
```

[3] Run docker container
```
docker run --rm -i -p 8080:8080 -t bhancock8/babble /bin/bash
```

Skip to [Step 4](#options-a-and-b).

### **Option B: Local**

[1] Install Anaconda 3.6 ([instructions](https://www.anaconda.com/download/))

[2] Clone the repository:
```
git clone https://github.com/HazyResearch/babble.git
cd babble
```

[3] Set up environment:
```
conda env create -f environment.yml
source activate babble
source add_to_path.sh
```

Continue to [Step 4](#options-a-and-b).

### **Options A & B**
[4] Run unit tests:
```
nosetests
```
If the tests run successfully, you will see an "OK" printed at the end.  
If you chose Option B, the first time you run this may take extra time to install a language model for spaCy.

[5] Run the tutorial:

If you'd like to try out the tutorials, continue on to the [Tutorial README](https://github.com/HazyResearch/babble/tree/master/tutorial).
