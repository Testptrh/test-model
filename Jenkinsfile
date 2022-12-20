pipeline {
  agent any
  stages {
    stage('test') {
      agent { docker 'openjdk:7' }
      steps {
        sh '''
          sh "java -version"
        '''
      }
    }
  }
}
