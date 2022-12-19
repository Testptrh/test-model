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
        #!/bin/sh
        python /var/lib/jenkins/workspace/cloud-pipeline/trainer/task.py
      }
    }
  }
}
