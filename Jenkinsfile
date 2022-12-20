pipeline {
  agent any
  stages {
    stage('test') {
      agent { docker 'openjdk:8' }
      steps {
        sh '''
            PROJECT_ID='wave46-mihaiadrian'
            IMAGE_URI="gcr.io/$PROJECT_ID/titanic:model"
        '''
      }
    }
    
    stage('test') {
      agent { docker 'openjdk:8' }
      steps {
        sh '''
          docker build ./ -t $IMAGE_URI
        '''
      }
    }
    
    stage('test') {
      agent { docker 'openjdk:8' }
      steps {
        sh '''
          docker push $IMAGE_URI
        '''
      }
    }
  }
}
