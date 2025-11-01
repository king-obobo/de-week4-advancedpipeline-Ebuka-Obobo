from pipeline.pipeline import Pipeline
from pipeline.logging_config import setup_logger

logger = setup_logger(__name__)


if __name__ == "__main__":
    try:
        my_pipeline = Pipeline()
        my_pipeline.run()
    except Exception as e:
        print(f"An error occured: {e}")
