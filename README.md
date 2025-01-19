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
  - [Option 2: Direct Installation](#option-2-direct-installation)
  - [Option 3: Docker (Simple)](#option-3-docker-simple)
  - [Option 4: Docker (Advanced)](#option-4-docker-advanced)
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
2. In BitQuery dashboard, navigate to Account > API V1 > Api-Keys
3. Copy and paste your API key in the settings page of the app

## ⚡ Quick Start
1. Install and run the app using one of the installation options [below](#️-installation)
2. Navigate to `http://localhost:8501` in your browser
3. Create a database and add BitQuery API key in settings
4. Start paper trading!

## 🛠️ Installation
### Option 1: .exe installation (recommended)
*Add .exe installation steps here*

### Option 2: Direct Installation
1️⃣ Clone the repository: ```git clone https://github.com/5zyyy/paper-paws-poc.git```
<br>
2️⃣ Install dependencies: ```pip install -e .```
<br>
3️⃣ Run the app: ```streamlit run .\src\app.py```  

### Option 3: Docker (Simple)
1️⃣ Download .tar docker image [here](https://drive.google.com/file/d/1y2VrQ6zLwjj_E1R-Rwrc3tzCGA9SKIfu/view?usp=sharing)
<br>
2️⃣ Open command prompt in the directory where the .tar docker image is stored
<br>
3️⃣ Load docker image: ```docker load -i paper-paws-poc.tar```
<br>
4️⃣ Run docker image: ```docker run --name paper-paws-app -p 8501:8501 paper-paws-poc:1.0.0```

### Option 4: Docker (Advanced)
1️⃣ Clone the repository: ```git clone https://github.com/5zyyy/paper-paws-poc.git```
<br>
2️⃣ Build Docker image: ```docker build -t paper-paws-poc:1.0.0 .```
<br>
3️⃣ Run Docker image (create container): ```docker run --name paper-paws-app -p 8501:8501 paper-paws-poc:1.0.0```
<br>
**Optional:** Save Docker image as .tar: ```docker save -o paper-paws-poc.tar paper-paws-poc:1.0.0```

## 🛠️ Troubleshooting
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

1️⃣ Fork the repository
<br>
2️⃣ Create a new branch
<br>
3️⃣ Make your changes
<br>
4️⃣ Submit a pull request

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

## 📝 License
Modified MIT License with Repository and Commercial Restrictions

Copyright (c) 2025 Paper Paws

This project welcomes contributions to the original repository through pull requests. 
While you may fork and modify the code for personal use, publishing separate public 
repositories is not permitted. Commercial use is strictly prohibited.

See [LICENSE](LICENSE) for full terms.
