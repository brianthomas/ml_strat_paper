# Analysis Code for "Determining Research Priorities Using Machine Learning" Paper 

## About
This is a project related to the paper "Determining Research Priorities Using Machine Learning" (Thomas etal. (2024), DOI:TBD) 

- [Installation](#installation)
- [Getting the data](#getting-the-data)
- [Running](#running)
- [Configuration](#configuration)


## Installation

You will need to create the virtual environment for running the software. Once this is installed you can use the provided utility or download the data manually from Zenodo.

### Software 
**Requirements**
- Python 3.10

Build the conda environment:
```bash
> conda env create -f env-strat-paper.yml
> conda activate strat-paper
```

### Data 

Data were produced using the [topic emergence package](https://github.com/abuonomo/topic-emergence-ADS).  Data are stored on Zenodo [DOI: TBD](https://zenodo.org/) and may be obtained using the provided utility as follows:

```bash
> python bin/download_data.py
``` 

## Use

Each of the notebooks illustrates part of the work from processing the outputs from the LDA modeling (data obtained above) to analysis and plotting of the results. 

Descriptions of notebooks:

| Name | Description |
| :--- | :---------- | 
| [Process\_Data](notebooks/Process_Data.ipynb) | Do (most of) the basic processing of LDA model output data into form used by other notebooks. Some light analysis of processing is also included. **Run this notebook first** to generate the files needed by other notebooks. There are various switches within the notebook to test various data generation/filtering choices. |  
| Bootstrap\_Estimation\_1998-2010\_RI.ipynb      | Estimate errors using bootstrap for Research Interest (RI) metric. |  
| Bootstrap\_Estimation\_1998-2010\_TCS.ipynb     | Estimate errors using bootstrap for Topic Contribution Score (TCS) metric. |  
| Bootstrap\_Estimation\_1998-2010\_TCS\_CAGR.ipynb| Estimate errors using bootstrap for TCS Compount Annual Growth Rate (TCS\_CAGR) metric. | 
| Bootstrap\_Estimation\_DS2010\_TCS.ipynb        | Estimate errors using bootstrap for the Decadal Survey 2010 (DS2010) corpus TCS (TCS_{DS2010}) metric. | 
| Bootstrap\_Estimation\_Decadal2010-Whitepapers\_TCS.ipynb | Estimate errors using bootstrap for the Decadal Survey 2010 submitted whitepapers TCS (TCS_{whitepaper}) metric. | 
| Journal\_Citation\_Modeling.ipynb | Modeling of citation rates for astronomy literature (1998 - 2019) with various functions. | 
| MLCR\_Analysis.ipynb | Analysis of TCS-based metrics compared to the Mean Lifetime Citation Rate (MLCR). | 
| Paper\_plots.ipynb | Generate most of the plots for the paper. |  
| Stable\_Topics.ipynb | Generate stable topic files from LDA model output data. You dont need to use this notebook unless you want to investigate other Lpt thresholds than the one used in the paper. |  


