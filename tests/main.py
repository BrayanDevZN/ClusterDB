"Executa todos os testes de um tipo especifico"

from src.logs.log import logger
import sys 
import subprocess
from pathlib import Path
import os 

class ArgError(Exception):
    pass 

class ExecuteTests:

    def __init__(self)->None:

        self.BASE_DIR = Path(__file__).resolve().parent


    #remove o root path
    def _remove(self) -> None:

        ROOT = Path(__file__).resolve().parent.parent
        path = str(self.BASE_DIR)
        path = path.replace(str(ROOT), "")
        path = path.replace("/", "")
        self.BASE_DIR = Path(path)
        
        

    #Captrua o argumento e adiciona no caminho
    def _args(self) -> None:

        arg = sys.argv[1] if len(sys.argv) > 1 else None 
        if arg is None:
            raise ArgError("Expeted arg")
            
               
        args = ["functional", "integration", "unit"]

        if not arg in args:

            raise ArgError(f"Not expeted {arg}")

        self.arg = arg

        self.path = self.BASE_DIR / arg

    #Pega todos os arquivos do caminho
    def _get_paths(self) -> None:

        logger.info(f"Get files in {self.path}...")

        self.paths = os.listdir(self.path) if os.path.exists(self.path) else False

        if self.paths:

            logger.success(f"Files: {" ,".join(self.paths)}")

        else:

            logger.warning(f"Not exists files in {self.path}")

    #Executa comando por comando de cada arquivo
    def _execute(self) -> None:

        if self.paths:

            logger.info(f"Executing {self.arg} tests...")

            for path in self.paths:

                if path != "__pycache__":
                    BASE = ["python", "-m"]


                    module = str(self.path / path)
                    module = module.replace(".py", "")
                    module = module.replace("/", ".")

                    BASE.append(str(module))
                    logger.info(f"Executing command {" ".join(BASE)}...")

                    print(("=" *25) + module + ("=" *25)) 
                    print()
    
                    subprocess.run(BASE, check=True)

                logger.success(f"{self.arg} executed with success")

    #Executa todos os comandos
    def run(self) -> None:
        self._remove()
        self._args()
        self._get_paths()
        self._execute()



if __name__ == "__main__":
    instance = ExecuteTests()
    instance.run()



        

    



    

    



        