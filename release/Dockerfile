# Submission Reproducibility Dockerfile
FROM python:3.11-slim

LABEL maintainer="Causal History Recovery Contributors"
LABEL description="Matched-State Causal-History Evaluation of Robot Policy Recovery"
LABEL version="1.0.0-rc1"

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/workspace/src

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libosmesa6-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY release/requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /workspace/src/
COPY models/ /workspace/models/
COPY configs/ /workspace/configs/
COPY results/ /workspace/results/
COPY tests/ /workspace/tests/
COPY scripts/ /workspace/scripts/

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import causal_history_recovery; import torch; import gymnasium" || exit 1

ENTRYPOINT ["python"]
CMD ["scripts/run_smoke_test.py"]
