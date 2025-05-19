import random

from prefect import flow, get_run_logger, task
from prefect.deployments import run_deployment


@flow
def flow_sees_subflow(n: int = 5) -> int:
    logger = get_run_logger()
    logger.info(f"hello from flow_sees_subflow, n = {n}")
    for i in range(n):
        logger.info(f"iteration {i}")
        value = a_task()
        logger.info(f"got value from a_task = {value}")
    return random.randint(1, 100)


@flow
def flow_sees_flow() -> None:
    logger = get_run_logger()
    logger.info("hello from flow_sees_flow")
    logger.info("calling flow_sees_subflow/subflow")
    i = 1
    flow_run = run_deployment(name="flow_sees_subflow/subflow", parameters={"n": i})
    logger.info(f"flow_run = {flow_run}")
    logger.info("waiting for flow_sees_subflow/subflow to finish?")


@task
def a_task() -> int:
    logger = get_run_logger()
    value = random.randint(1, 100)
    logger.info(f"hello from a_task. got value = {value}")
    return value
