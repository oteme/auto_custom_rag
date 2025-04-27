
from manager import PipelineManager
from config_for_test import config

if __name__ == "__main__":
    manager = PipelineManager(config)
    manager.initialize_pipeline()
    manager.ingest()

    manager.query("Tell me about forests")
