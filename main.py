import random

from prefect import flow, get_run_logger, task
from prefect.deployments import run_deployment


@flow
def the_flow() -> None:
    logger = get_run_logger()
    logger.info("hello from the_flow")
    for i in range(5):
        logger.info(f"iteration {i}")
        value = a_task()
        logger.info(f"got value from a_task = {value}")


@flow
def the_another_flow(n: int = 5) -> None:
    logger = get_run_logger()
    logger.info(f"hello from the_another_flow, n = {n}")
    for i in range(n):
        logger.info(f"iteration {i}")
        value = a_task()
        logger.info(f"got value from a_task = {value}")


@flow
def flow_sees_flow() -> None:
    logger = get_run_logger()
    logger.info("hello from flow_sees_flow")
    logger.info("calling the-another-flow/second-flow")
    for i in range(4):
        logger.info(f"iteration {i} - calling the-another-flow/second-flow")
        flow_run = run_deployment(name="the-another-flow/second-flow")
    logger.info(f"flow_run = {flow_run}")
    logger.info("waiting for the-another-flow/second-flow to finish?")


@task
def a_task() -> int:
    logger = get_run_logger()
    value = random.randint(1, 100)
    logger.info(f"hello from a_task. got value = {value}")
    return value


if __name__ == "__main__":
    the_flow.serve()
