pipeline {
  agent any
  stages {
    stage('version') {
      steps {
        sh 'python3 --version'
      }
    }
    stage('hello') {
      steps {
        cd trainer
        sh 'python3 test.py'
      }
    }
  }
}
