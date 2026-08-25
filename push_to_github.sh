#!/bin/bash
# Helper script to push the completed Lab 1 repository to GitHub

echo "======================================================="
echo "Pushing openapi-mock-server-generator to GitHub"
echo "Repository: https://github.com/Akshayarcot/openapi-mock-server-generator"
echo "======================================================="

# Verify git remote
git remote -v

echo ""
echo "Attempting git push to origin main..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "🔗 View your repo: https://github.com/Akshayarcot/openapi-mock-server-generator"
else
    echo ""
    echo "⚠️  Push failed. If you need authentication:"
    echo "Option 1 (GitHub PAT): Use your username 'Akshayarcot' and your GitHub Personal Access Token as password."
    echo "Option 2 (SSH): Run 'git remote set-url origin git@github.com:Akshayarcot/openapi-mock-server-generator.git' and then 'git push -u origin main'."
fi
