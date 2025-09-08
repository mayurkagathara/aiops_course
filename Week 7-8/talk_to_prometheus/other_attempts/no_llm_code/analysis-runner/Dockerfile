FROM python:3.11-slim
WORKDIR /runner
RUN pip install --no-cache-dir pandas numpy
COPY job.py /runner/job.py
ENTRYPOINT ["python", "/runner/job.py"]
