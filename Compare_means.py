import pandas as pd
from scipy.stats import levene, ttest_ind
import pingouin as pg

# Load the Excel file
file_path = '/path/to/your/file/Demgraphics.xlsx'
xls = pd.ExcelFile(file_path)

# Iterate through each sheet in the Excel file
results = {}
for sheet_name in xls.sheet_names:
    data = pd.read_excel(xls, sheet_name=sheet_name)
    # Assume the first column is categorical and the second is continuous
    categorical, continuous = data.columns[0], data.columns[1]
    
    # Group data based on the categorical column
    grouped = data.groupby(categorical)[continuous]
    
    # Determine the number of unique categories
    unique_categories = data[categorical].nunique()

    # Perform different tests based on the number of unique categories
    if unique_categories == 2:
        # Perform Levene's test
        group1, group2 = [group for name, group in grouped]
        levene_test = levene(group1, group2)
        levene_fvalue = levene_test.statistic  # F-value from Levene's test

        # Conduct appropriate t-test based on Levene's test
        if levene_test.pvalue > 0.05:
            # Equal variances
            t_test = ttest_ind(group1, group2, equal_var=True)
            test_type = 'T-test'
        else:
            # Unequal variances
            t_test = ttest_ind(group1, group2, equal_var=False)
            test_type = 'Welch\'s T-test'
        
        # Store results
        results[sheet_name] = {
            'Levene\'s Test p-value': levene_test.pvalue,
            'Levene\'s Test F-value': levene_fvalue,
            'Test Type': test_type,
            'Test Result': t_test
        }
    elif unique_categories > 2:
        # Perform Levene's test for ANOVA
        levene_test = levene(*[group for name, group in grouped])
        levene_fvalue = levene_test.statistic  # F-value from Levene's test

        # Conduct ANOVA or Welch's ANOVA based on Levene's test
        if levene_test.pvalue > 0.05:
            # Equal variances, perform one-way ANOVA
            anova_result = pg.anova(dv=continuous, between=categorical, data=data, detailed=True)
            test_type = 'One-way ANOVA'
        else:
            # Unequal variances, perform Welch's ANOVA
            anova_result = pg.welch_anova(dv=continuous, between=categorical, data=data)
            test_type = 'Welch\'s ANOVA'
        
        # Check if we should perform post-hoc testing
        if anova_result['p-unc'].iloc[0] <= 0.05:
            posthoc_results = pg.pairwise_gameshowell(dv=continuous, between=categorical, data=data)
        else:
            posthoc_results = "ANOVA not significant; no post-hoc test performed."

        # Store results
        results[sheet_name] = {
            'Levene\'s Test p-value': levene_test.pvalue,
            'Levene\'s Test F-value': levene_fvalue,
            'Test Type': test_type,
            'Test Result': anova_result,
            'Post-Hoc Test': posthoc_results
        }

# Print the results
for sheet, result in results.items():
    print(f"Results for {sheet}:")
    print(f"Levene's Test p-value: {result['Levene\'s Test p-value']}")
    print(f"Levene's Test F-value: {result['Levene\'s Test F-value']}")
    print(f"{result['Test Type']} Result:\n{result['Test Result']}\n")
    if 'Post-Hoc Test' in result:
        print("Post-Hoc Test Result:\n", result['Post-Hoc Test'], "\n")
