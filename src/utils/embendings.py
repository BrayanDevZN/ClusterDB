"gera os embendings e salva"

import logging
import os

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

from sentence_transformers import SentenceTransformer, util
from transformers.utils import logging as transformers_logging
from huggingface_hub.utils import disable_progress_bars
from src.logs.log import logger
import numpy as np


transformers_logging.set_verbosity_error()
disable_progress_bars()

logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("httpx2").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)


class Embendings:

    def __init__(self) -> None:

        self.model = SentenceTransformer(
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )


    # Cria o emb
    async def encode(self, text: str | list) -> list:

        logger.info("Creating embendings...")

        embs = self.model.encode(
            text,
            show_progress_bar=False
        )

        logger.success("Embendings created with sucess")

        return embs


    # Compara embs
    async def cos(self, emb: list, check_emb: list) -> float:

        logger.info("Checking similarity from embendings...")

        emb = np.array(emb)
        check_emb = np.array(check_emb)

        check = util.cos_sim(emb, check_emb)

        logger.success("Embendings checked with success")

        return check.item()