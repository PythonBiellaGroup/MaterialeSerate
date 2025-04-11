import io
from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
from loguru import logger
from PIL import Image


class BaseRAG(ABC):
    """
    Abstract base class for Retrieval-Augmented Generation (RAG) pipelines.
    Provides a common interface and shared helper methods.
    """

    def __init__(self):
        self.graph = None

    @abstractmethod
    def invoke(self, query: str) -> str:
        """
        Process the input query through the RAG pipeline and return the output.
        """
        pass

    def print_graph(self):
        """
        Render and display the pipeline's graph if available.
        """
        if self.graph:
            logger.info("Rendering graph visualization.")
            try:
                image_bytes = self.graph.get_graph(xray=True).draw_mermaid_png()
                image = Image.open(io.BytesIO(image_bytes))
                plt.imshow(image)
                plt.axis("off")
                plt.show()
            except Exception as e:
                logger.error(f"Failed to render graph: {e}")
                logger.info(self.graph.get_graph(xray=True).draw_mermaid())
        else:
            logger.info("No graph visualization available for this pipeline.")
