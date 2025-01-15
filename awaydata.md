# xGA and xG per game - away data

[This script](new_folder/awaydatascript.png) automates the process of extracting data from the "Away" tab on my data source. It performs the following tasks:

Navigates to the data source using Selenium.

Clicks the "Away" tab to display relevant statistics.

Extracts key data points such as team name, matches played, xG, xGA, and calculates xG per game and xGA per game.

Saves the processed data into a [CSV file](new_folder/awaydatatable.png) for further analysis.

This script is useful for analysing team performance in away matches, focusing on key metrics like xG and xGA.

Skills used:

Python Programming

Selenium Automation

Web Scraping

Data Processing

Pandas Data Manipulation - creating a DataFrame from extracted data, saving data to a CSV file for later use

Regular Expressions (Regex) - cleaning numeric data by removing unwanted characters

File Handling - storing processed data into an optimised and readable CSV format

Basic Debugging - printing logs to trace script execution steps (e.g., loading page, extracting rows)
