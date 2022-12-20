pipeline {
  agent any
  stages {
    stage('variables') {
      agent { docker 'openjdk:8' }
      steps {
        sh '''
            PROJECT_ID='wave46-mihaiadrian'
            IMAGE_URI="gcr.io/$PROJECT_ID/titanic:model"
        '''
      }
    }
    
    stage('build') {
      agent { docker 'openjdk:8' }
      steps {
        sh '''
          docker build ./ -t $IMAGE_URI
        '''
      }
    }
    
    stage('push') {
      agent { docker 'openjdk:8' }
      steps {
        sh '''
          docker push $IMAGE_URI
        '''
      }
    }
  }
}
