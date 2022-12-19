pipeline {
  agent any
  stages {
    stage('test') {
      steps {
        sh '''
             python '/var/lib/jenkins/workspace/cloud-pipeline/trainer/task.py'
        '''
      }
    }
  }
}
