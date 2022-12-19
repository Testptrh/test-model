pipeline {
  agent any
  stages {
    stage('version') {
      steps {
        cd trainer
      }
    }
    stage('ls') {
      steps {
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
