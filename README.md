# 🐾 Paper Paws (POC)

A paper trading simulator for meme coins on the Solana blockchain. Practice trading without risking real assets.

📚 **[Visit our website](https://www.paperpaws.xyz/) for more details on the project!**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.13-green)
![Streamlit](https://img.shields.io/badge/streamlit-1.41.1-red)

## 📋 Table of Contents
- [Features](#-features)
- [API Key Setup](#-api-key-setup)
- [Quick Start](#-quick-start)
- [Installation](#️-installation)
  - [Option 1: .exe installation](#option-1-exe-installation-recommended)
  - [Option 3: Docker (Simple)](#option-2-docker-simple)
  - [Option 4: Docker (Advanced)](#option-3-docker-advanced)
- [Troubleshooting](#️-troubleshooting)
- [Bug Reports](#-bug-reports)
- [Contributing](#-contributing)
- [Dependencies](#-dependencies)
- [License](#-license)

## 🚀 Features
- Paper trade tokens with real-time data
- Real-time token price tracking
- Portfolio management with P/L tracking
- Trade history with CSV export
- Customizable trading fees
- Docker support

## 🔑 API Key Setup
1. Sign up at [BitQuery](https://bitquery.io/)
2. In BitQuery dashboard, navigate to Account > API V2 > Applications
3. Click on 'New Application'
4. Enter the any name for the application (e.g. 'Paper Paws') and select an access token lifespan (Recommended: 3 months)
5. Click on 'Manage'
6. Click on 'Generate New Token'
7. Copy and paste your 'Access token' in the settings page of the app

## ⚡ Quick Start
1. Install and run the app using one of the installation options [below](#️-installation)
2. Navigate to `http://localhost:8501` in your browser
3. Create a database and add BitQuery API key in settings
4. Start paper trading!

## 🛠️ Installation
### Option 1: .exe installation (recommended)
1. Download the .exe [here](https://drive.google.com/file/d/1zDS6xK3oOeq9rELP7JFryzbS0SPEPYco/view?usp=sharing)
2. Extract the .zip file
3. Run paperpaws.exe
4. **NOTE: Keep the .exe file in a folder as it creates settings and database files**  

### Option 2: Docker (Simple)
1. Open command prompt
2. Pull docker image: ```docker pull paperpaws/paper-paws-poc:1.0.0```
3. Run docker image: ```docker run --name paper-paws-app -p 8501:8501 paperpaws/paper-paws-poc:1.0.0```

### Option 3: Docker (Advanced)
1. Clone the repository: ```git clone https://github.com/5zyyy/paper-paws-poc.git```
2. Build Docker image: ```docker build -t paper-paws-poc:1.0.0 .```
3. Run Docker image (create container): ```docker run --name paper-paws-app -p 8501:8501 paper-paws-poc:1.0.0```
4. Save Docker image as .tar: ```docker save -o paper-paws-poc.tar paper-paws-poc:1.0.0``` (*optional*)

## 🔌 Project Set Up
1. Clone the repository: ```git clone https://github.com/5zyyy/paper-paws-poc.git```
2. Install dependencies: ```pip install -e .``` and ```pip install -r requirements.txt```
3. Run the app: ```streamlit run .\src\app.py```
4. Compile .exe: ```python build.py```

## ⚠️ Troubleshooting
Common issues and solutions:
- **Database Error**: Reset database in settings
- **Docker Port Error**: Make sure port 8501 is not in use
- **API Error**: Verify your BitQuery API key in settings

## 🐛 Bug Reports
Found a bug? Please report them in our telegram [here](https://t.me/paperpawsxyz) or open an issue with:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior

## 🤝 Contributing
We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

Please include a clear description with the pull request:
 - What problem does this solve?
 - What changes were made?
 - How to test these changes?
 - Screenshots (if applicable)

## 📦 Dependencies
- Python 3.13+
- Streamlit
- Pandas
- DuckDB
- PyYAML
- Streamlit Extras
- PyInstaller

## 📝 License
Modified MIT License with Repository and Commercial Restrictions

Copyright (c) 2025 Paper Paws

This project welcomes contributions to the original repository through pull requests. 
While you may fork and modify the code for personal use, publishing separate public 
repositories is not permitted. Commercial use is strictly prohibited.

See [LICENSE](LICENSE) for full terms.
