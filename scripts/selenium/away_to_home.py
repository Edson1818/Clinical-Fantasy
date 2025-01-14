import re

# Input and output file paths
input_file = "away_xga_auto.py"  # Original script
output_file = "home_xga_auto.py"  # New script with replacements

# Read the content of the original script
with open(input_file, "r") as file:
    content = file.read()

# Replace all case-insensitive occurrences of 'away' with 'home'
# The \b ensures only whole words are replaced
modified_content = re.sub(r'\baway\b', 'home', content, flags=re.IGNORECASE)

# Write the modified content to the new file
with open(output_file, "w") as file:
    file.write(modified_content)

print(f"New script created: {output_file} (all 'away' replaced with 'home').")