# T-tests-and-One-way-ANOVAs
This Python script automates statistical analysis on grouped data contained within multiple sheets of an Excel file. It intelligently determines whether to apply a t-test or one-way ANOVA based on the number of subgroups within a categorical variable. Furthermore, it assesses variance equality using Levene's test to decide on the appropriate versions of these tests (standard or Welch's) and performs a Games-Howell post-hoc test if needed. This tool is designed to streamline the statistical analysis process in research settings where data comparisons across groups are necessary.

## Features
- **Dynamic Test Selection:** Automatically chooses between a t-test and one-way ANOVA based on subgroup count.
- **Levene's Test for Equality of Variances:** Assesses variances to determine the suitable statistical test.
- **Robust Statistical Testing:** Executes standard or Welch’s t-test and ANOVA depending on variance equality.
- **Post-Hoc Analysis with Games-Howell:** Conducts post-hoc testing when significant differences are found in ANOVA.
- **Comprehensive Results Output:** Outputs include p-values, F-values, and test results, formatted for ease of interpretation.

## How to Use
1. Ensure that your Excel file is formatted correctly with each sheet having two columns: the first for the categorical variable and the second for the continuous variable.
2. Update the `file_path` variable in the script to the location of your Excel file.
3. Run the script in a Python environment where `pandas`, `numpy`, `scipy.stats`, and `pingouin` are installed.

## Excel File Structure
Each sheet in the Excel file should be structured as follows:
- The **first column** contains the categorical variable.
- The **second column** contains the continuous variable.

## Installation
Install all dependencies using pip:
```bash
pip install pandas scipy.stats pingouin
Compare_means.py
