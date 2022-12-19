pipeline {
  agent any
  stages {
    stage('test') {
      steps {
        sh '''
             PROJECT_ID='wave46-mihaiadrian'
             IMAGE_URI="gcr.io/$PROJECT_ID/titanic:model"
             docker build ./ -t $IMAGE_URI
             docker push $IMAGE_URI
        '''
      }
    }
  }
}
