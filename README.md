# Gender differences in writing: Clustertools and E-grammar features

These tools were used for a computational text analysis, analyzing gender differences in writing: who uses emoticons, abbreviations, clippings, etc., the most? Covers feature extraction, text clustering by features, and plotting of results. 

This repository contains 

###[Clustertools](https://github.com/patrickschu/chapter2/blob/master/current/clustertools.py)
A Python module used for cluster analysis and inspection. Implements the methodology for general purpose computer-assisted clustering and conceptualization developed in [Grimmer & King](http://www.pnas.org/content/108/7/2643.short). It helps us produce output like [this](https://github.com/patrickschu/chapter2/blob/master/outputfiles/sample_clustering_output.MD).

###[Egrammartools](https://github.com/patrickschu/chapter2/blob/master/current/egrammartools.py)
A Python module used for extraction of e-grammar features. Implements search algorithms for features of e-grammar listed in Herring, ["Grammar and electronic communication"](http://info.ils.indiana.edu/~herring/e-grammar.pdf). For instance: extract emoticons, extract abbreviations, or extract non-Standard punctuation. 

###[R-scripts](https://github.com/patrickschu/chapter2/blob/master/rscripts/plot_egrammar_by_category_0102.R)
Visualize the study results: which group uses which feature?

---
![alt text](https://github.com/patrickschu/chapter2/blob/master/rscripts/overfeatures%20.png "Plot feature by category")
---
