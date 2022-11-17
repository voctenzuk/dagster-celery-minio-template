from dagster import graph, op, repository, schedule
from dagster_aws.s3.io_manager import s3_pickle_io_manager
from dagster_aws.s3.resources import s3_resource
from dagster_celery import celery_executor


@op
def hello():
    return 1


@op
def goodbye(foo):
    if foo != 1:
        raise Exception("Bad io manager")
    return foo * 2


@graph
def my_graph():
    goodbye(hello())


my_job = my_graph.to_job(
    name="my_job",
    executor_def=celery_executor,
    resource_defs={
        "io_manager": s3_pickle_io_manager,
        "s3": s3_resource,
    },
)


@schedule(cron_schedule="* * * * *", job=my_job, execution_timezone="US/Central")
def my_schedule(_context):
    return {}


@repository
def celery_repository():
    return [my_job, my_schedule]
