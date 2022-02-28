sf_crime_2022
============

*A project to understand SF crime data*

# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).
 
## [Unreleased] - yyyy-mm-dd
 
### To Be Added

- Excel spreadsheet with pivot tables. Possibly Power BI report if people can use that.

## [2.0.0] - 2022-02-28 12:29

### Added

- "incident reports JOIN da caseload JOIN prod1 JOIN prod2 BY YEAR.xlsx" and "Robberies BY YEAR.xlsx", which have a spreadsheet for 2018-2019 data and another for 2020-2021 data.
- "incident reports...BY YEAR.xlsx" has charts for visualizing the number of dismissals for each incident category, and also the average CJ and SP terms for each incident category.

## [1.0.0] - 2022-02-26 07:44

### Added

- Added data on street robberies, and ranked according to whether the case was dismissed and the defendant served time in county jail or state prison.

### Changed

- Now all of the "output files" are Excel workbooks.
- Removed unneeded columns from police report output data.

## [0.1.0] - 2022-02-25
 
### Added

- Initial commits. "input files" contains all the source data. All the data analysis is being done by "production 1+2.ipynb". You do not need to unzip the "police department incident reports.zip" file if you are using the Jupyter notebook; the notebook unzips it for you.


Contributing
------------

Be sure to read the [contribution guidelines]

(https://github.com/molsonkiko/sf_crime_2022/blob/main/CONTRIBUTING.md).