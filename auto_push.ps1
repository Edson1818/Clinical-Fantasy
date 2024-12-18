# Navigate to project folder
Set-Location -Path "C:\Users\Edi Okwok\Documents\clinical_fantasy"

# Add all changes to the staging area
git add .

# Commit changes with current date and time
git commit -m "Auto-commit: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"

# Push changes to the remote repository
git push origin main

# Success message
Write-Output "✅ Changes have been successfully pushed to GitHub!"