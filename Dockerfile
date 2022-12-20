FROM gcr.io/deeplearning-platform-release/tf2-gpu.2-5
WORKDIR /
RUN pip install cloudml-hypertune
COPY trainer /trainer
ENTRYPOINT ["python", "-m", "trainer.task"]


# Commands to build the image
# PROJECT_ID='wave46-mihaiadrian'
# IMAGE_URI="gcr.io/$PROJECT_ID/titanic:model"
# gcloud auth configure-docker
# docker build ./ -t $IMAGE_URI
# docker push $IMAGE_URI
