pipeline {
  agent any
  stages {
    stage('test') {
      steps {
        sh '''
          gcloud compute zones list
        '''
      }
    }
  }
}