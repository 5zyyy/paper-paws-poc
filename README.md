# Paper Paws (POC)
Version 1.0.0

### Project Set Up
```git clone https://github.com/5zyyy/paper-paws-poc.git```
<br>
```pip install -e .```

### Run app
```streamlit run .\src\app.py```

### Docker
Build docker image
<br>
```docker build -t paper-paws-poc:1.0.0 .```

Save docker image as .tar or download [here](https://drive.google.com/file/d/1y2VrQ6zLwjj_E1R-Rwrc3tzCGA9SKIfu/view?usp=sharing)
<br>
```docker save -o paper-paws-poc.tar paper-paws-poc:1.0.0```

Load docker image from .tar
<br>
```docker load -i paper-paws-poc.tar```

Run docker image
<br>
```docker run --name paper-paws-app -p 8501:8501 paper-paws-poc:1.0.0```