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
        sh 'python3 hello.py'
      }
    }
  }
}


sh 'python3 /var/lib/jenkins/workspace/cloud-pipeline/trainer/task.py'  