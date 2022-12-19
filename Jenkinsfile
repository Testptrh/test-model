pipeline {
  agent any
  stages {
    stage('version') {
      steps {
        cd trainer
        ls
      }
    }
    stage('hello') {
      steps {
        sh 'python3 test.py'
      }
    }
  }
}
