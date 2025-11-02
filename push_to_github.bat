@echo off
REM GitHub Push Script for LawBot360
REM Run this after creating the repository on GitHub

echo ============================================
echo  LawBot360 - GitHub Push Script
echo ============================================
echo.

REM Change to project directory
cd /d "D:\ML Projects\LawBot360"

echo Step 1: Please create the repository on GitHub first:
echo.
echo   1. Go to: https://github.com/new
echo   2. Repository name: LawBot360
echo   3. Choose Public or Private
echo   4. DO NOT initialize with README, .gitignore, or license
echo   5. Click "Create repository"
echo.
pause

echo.
echo Step 2: Enter your GitHub username:
set /p GITHUB_USERNAME="GitHub Username: "

echo.
echo Step 3: Adding remote and pushing...
git remote add origin https://github.com/%GITHUB_USERNAME%/LawBot360.git
git branch -M main
git push -u origin main

echo.
echo ============================================
echo  Done! Your repository is now on GitHub
echo ============================================
echo.
echo Repository URL: https://github.com/%GITHUB_USERNAME%/LawBot360
echo.
pause

