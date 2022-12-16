# ML-Climate-Project-Fall2022
<!-- 
Throughout the semester each student will work on an individual project, which you will summarize in a final technical paper. You will showcase and document your work through a private git repository following this template.

The organization of this repository is as follows:

```
abstract.md
journal.md
doc/
src/
etc/
```
- The file `abstract.md` simply contains an abstract of the project. At first, it is an aspirational abstract, one that describes the research program you want to complete. You will refine it through the semester.
- The file `journal.md` is a diary of your progress. It contains dated entries with a description of what you are doing, what you found, what you are thinking, and so on. It is mainly a resource for you, but I will glance at it too (at the end of the semester). Please update and commit it at least once per week.
- The `doc/` directory contains the LaTeX document that you are writing. We will provide a template for your final paper.
- The `src/` directory contains the code you are writing. The data you are analyzing should live here too.
- The `etc/` directory contains anything else — materials, notes, photos of whiteboards, and so on — that you want to keep track of.
There should be nothing else in the top level directory of your repository.

Commit often, at least every week. You are graded on the quality of the project and the path that you took to get there. -->
# Solar Panel Location Selection Using Power Generation Potential Prediction

This project is for my semester in ML and Climate at Columbia University during the Fall of 2022. 

I develop an approach to help identify promising locations to build solar panel arrays by leveraging  only GHI levels and ambient temperature readings from the National Renewable Energy Laboratory (NREL)'s satelitte data to approximate the historical potential Photovoltaic output that matches SOTA simulations. I explore machine learning models from Linear Regression to Random Forest approachs and document the results in notebooks viewable in this repository.

First, run requirements.txt:
```
$ pip install -r requirements.txt
```

Note: You will also need to install osgeo (GDAL) to process the raster files. A .whl file is included to install the version used in this project

### To walkthrough this project, view the following notebooks under the src/Notebooks folder in sequence:

- 1 Map Visualization and Data Selection
- 2 EDA on DATA
- 3 Data and Modeling

My process is documented in journal.md and my resources are listed in resources.md
