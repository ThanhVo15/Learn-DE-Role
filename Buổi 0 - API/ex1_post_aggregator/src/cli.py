import argparse
import sys
import asyncio
import pytest
from logging_utils import setup_root_logger, get_logger
from orchestrator import simulate_many_clients

logger = get_logger("CLI")

def main():
    setup_root_logger()
    parser = argparse.ArgumentParser(description="Post Aggregator Exercise 1")
    parser.add_argument("--run-tests", action="store_true", help="Run unit/integration tests first")
    parser.add_argument("--clients", type=int, default=3, help="Number of concurrent simulated clients")
    args = parser.parse_args()

    if args.run_tests:
        logger.info("Running tests before pipeline")
        # run pytest programmatically
        ret = pytest.main(["-q", "--disable-warnings", "tests"])
        if ret != 0:
            logger.error("Tests failed, aborting execution")
            sys.exit(ret)
        logger.info("All tests passed")

    # run pipeline
    results = asyncio.run(simulate_many_clients(args.clients))
    logger.info(f"Simulation results: {results}")

if __name__ == "__main__":
    main()
