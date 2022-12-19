FROM gcr.io/deeplearning-platform-release/tf2-gpu.2-5
WORKDIR /
RUN pip install cloudml-hypertune
COPY trainer /trainer
ENTRYPOINT ["python", "-m", "trainer.task"]

# dsa
