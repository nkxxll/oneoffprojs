from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from .logger import Logger
from .server.config import load_config


class RefineNote:
    _refine_prompt = ChatPromptTemplate.from_template("""
    SYSTEM: You are an expert editor. Your goal is to take messy, fragmented notes
    and transform them into a highly readable Markdown format.

    TASK:
    - Fix grammar and shorthand.
    - Use H2 and H3 headers for organization.
    - Add a "TL;DR" summary at the top.
    - Extract 3-5 keywords for tagging.

    ORIGINAL NOTE:
    {raw_note}

    REFINED NOTE:
    """)

    _config = load_config()
    _llm = ChatOllama(model=_config.model, temperature=0.2)
    _refine_chain = _refine_prompt | _llm | StrOutputParser()
    _logger = Logger(name="noteweaver.refine").get()

    @staticmethod
    def refine(str_path: str):
        path = Path(str_path)
        RefineNote._logger.info("Starting note refinement for %s", path)
        try:
            content = path.read_text()
            RefineNote._logger.info("Loaded note content from %s", path)
            refined_note = RefineNote._refine_chain.invoke({"raw_note": content})
            RefineNote._logger.info("Completed note refinement for %s", path)
            return refined_note
        except Exception:
            RefineNote._logger.exception("Failed to refine note for %s", path)
            raise
