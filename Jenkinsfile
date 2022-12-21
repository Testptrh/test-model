pipeline {
  agent { dockerfile true }
  stages {
    stage('Test') {
      docker.image('user/image:version').inside("""-entrypoint=''""") {
        steps {
        sh '''
          PROJECT_ID='wave46-mihaiadrian'
          IMAGE_URI="gcr.io/$PROJECT_ID/titanic:model"
           '''
        }
        
        steps {
        sh '''
          docker build -t $IMAGE_URI
           '''
        }
        
        steps {
        sh '''
          gcloud auth configure-docker gcr.io
           '''
        }
        
        steps {
        sh '''
          docker push $IMAGE_URI
           '''
        }
      }
    }
  }
}
