pipeline {
  agent any
  stages {
    stage('variables') {
      steps {
        sh '''
          PROJECT_ID='wave46-mihaiadrian'
          IMAGE_URI="gcr.io/$PROJECT_ID/titanic:model"
        '''
      }
    }
    
    stage('build') {
      steps {
        sh '''
          docker build ./ -t $IMAGE_URI
        '''
      }
    }
    
    stage('push') {
      steps {
        sh '''
          docker push $IMAGE_URI
        '''
      }
    }
  }
}
