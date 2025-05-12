import random

from prefect import flow, get_run_logger, task


@flow
def the_flow() -> None:
    logger = get_run_logger()
    logger.info("hello from the_flow")
    for i in range(5):
        logger.info(f"iteration {i}")
        value = a_task()
        logger.info(f"got value from a_task = {value}")


@task
def a_task() -> int:
    logger = get_run_logger()
    value = random.randint(1, 100)
    logger.info(f"hello from a_task. got value = {value}")
    return value


if __name__ == "__main__":
    the_flow.serve()
