# Chicago-business-prediction

Implement a machine learning pipeline to priorize the business licenses that are likely to die in 2 years in Chicago.

The full project report can be found [here](https://drive.google.com/a/uchicago.edu/file/d/1NLHlREFRioDvy4RXcORt5rwpzddIeetA/view?usp=sharing)

## Pipelines
* ```cofigs```: a folder contains the configure files of different combinations of features. We use them to pass all the parameters that we need into pipelines.   
* ```data```: contains an sh file to download the cleaned full data set.   
* ```data_collector```: a folder contains all the code we use to collect and clean data.   
* ```output```: a folder to save the results of our pipeline, including performance table, precision and recall curve plots and AUC-ROC curve plots.   
* ```pipeline```: contains the modules of imputation, evaluation, discretization, get dummies and scaling.   
* ```tests```: a set of test code for our piepline.   
* ```main.py```: the main function to run models and get results.   
* ```transformer.py```: the function to preprocess data set before modeling.   

## Getting Started

Get the full dataset
 
```
cd data
sh get_fullfiles.sh
```

### Prerequisites


All the packages' requirement is in the enviorment.yml

To clone the enviorment, simply run the following:

```
conda env create -f environment.yml
```

To activate the enviorment, simply run the following:

```
conda activate myenv
```

### Installing

```
python setup.py install
```

## Running the tests

```
py.test
```

## Running the pipeline

```
python main.py --config ./cofigs/acs_geo.yml
```
In the configs file, there are different combination of features that from ACS, reported 311, reported Crime, business license that you can choose.


## Getting results

The results of the pipeline is saved in the output folder. 

Under the performance foler, there would be csvs to keep all the performance of all models

Under the pr folder, there would be precison-recall graphs

Under the roc foler, there would be roc graphs

## Additional materials
* [temporal validation table](https://drive.google.com/a/uchicago.edu/file/d/1jQ9wZKCAliO6Ibg5McQ28BSvFOGrgiRN/view?usp=sharing)
* [feature list](https://docs.google.com/spreadsheets/d/1XEcMPa9SfWi0rUXY8ytfh5Jrqg-YI2ES4oPsTkODm1E/edit?usp=sharing)
* [feature importance of the best model](https://drive.google.com/a/uchicago.edu/file/d/1ipv4gyi4jyJ3FtJfF_snqXp2cpmJ1NAd/view?usp=sharing)
* [final list of the best model](https://drive.google.com/a/uchicago.edu/file/d/1SZ1MD0Vxceh2FCYSbM6cm2zVQc37uLEl/view?usp=sharing)
## Authors

* **Peng Wei**  [CV](https://pengwei715.github.io/)
* **Yuwei Zhang**  [Linkedin](https://www.linkedin.com/in/yuwei-zhang-b3b597102/)
* **Ta-yun Yang**  [Linkedin](https://www.linkedin.com/in/ta-yun-yang-9a3539171/)
* **Xuan Bu**  [Linkedin](https://www.linkedin.com/in/xuanbu/)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

This project is the final project of machine learning for public policy in University of Chicago.  

* Supervised by Professor [Rayid Ghani](https://github.com/dssg/MLforPublicPolicy) 
* Inspired by [Satej](https://github.com/satejsoman) 
