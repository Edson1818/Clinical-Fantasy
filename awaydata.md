# xGA and xG per game - away data

[This script](new_folder/awaydatascript.png) automates the process of extracting data from the "Away" tab on my data source. It performs the following tasks:

Navigates to the data source using Selenium.

Clicks the "Away" tab to display relevant statistics.

Extracts key data points such as team name, matches played, xG, xGA, and calculates xG per game and xGA per game.

Saves the processed data into a [CSV file](new_folder/awaydatatable.png) for further analysis.

This script is useful for analysing team performance in away matches, focusing on key metrics like xG and xGA.

Skills used:

Python Programming - writing structured and functional Python code, handling exceptions and implementing error-handling mechanisms. 

Selenium Automation - navigating web pages using Selenium WebDriver, interacting with web elements via XPath and Selenium function, waiting for elements to be clickable using explicit waits.

Web Scraping - extracting table rows and cells from a web page, parsing text data from HTML elements.

Data Processing - cleaning and validating numeric data (xG and xGA values), calculating derived metrics like xG per game and xGA per game.

Pandas Data Manipulation - creating a DataFrame from extracted data, saving data to a CSV file for later use.

Regular Expressions (Regex) - cleaning numeric data by removing unwanted characters.

File Handling - storing processed data into an optimised and readable CSV format.

Basic Debugging - printing logs to trace script execution steps (e.g., loading page, extracting rows).
