"Cria todo caminho se não existir"
from src.logs.log import logger
from pathlib import Path
import os

def get_paths() -> str:
        
    BASE_DIR = Path(__file__).resolve().parent.parent.parent / "data"
    BASE_DIR.mkdir(exist_ok=True)
    
    paths = ["clusters", "database"]

    for name in paths:

        path = BASE_DIR / name 
        

        if not os.path.exists(path):

            logger.info(f"Creating path {name}...")
            path.mkdir(exist_ok=True)

    envs = ["prod", "staging", "test", "develop"]
    for env in envs:
        path = BASE_DIR / "clusters" / env 

        if not os.path.exists(path):
            logger.info(f"Creating environment {env}...")
            path.mkdir(exist_ok=True)


    logger.success(f"Created paths in {BASE_DIR}/")
    
    return f"sqlite+aiosqlite:///{BASE_DIR}/database/users.db"

    

        


    

