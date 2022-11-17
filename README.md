## Dagster with celery workers with flower and minio

For first create `.env` from `template.env`

We need to create minio access keys and crate buckets. Run minio `docker compose up minio -d` and create buckets: `dagster`, `dagster-compute-logs`. Than create access key and secret key and save in .env file.


Run dagster: `docker compose up --build -d`


Paste in launchpad:
```
execution:
  config:
    broker: 
      env: CELERY_BROKER_URL
resources:
  io_manager:
    config:
      s3_bucket: dagster
      s3_prefix: dagster-celery
  s3:
    config:
      endpoint_url: 
        env: S3_BACKEND_URL
```