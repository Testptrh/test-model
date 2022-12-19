pipeline {
  agent any
  stages {
    stage('version') {
      steps {
        sh 'cd trainer'
      }
    }
    stage('ls') {
      steps {
        sh 'ls'
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
