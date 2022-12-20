pipeline {
  agent any
  stages {
    stage('variables') {
      steps {
        sh '''
                PROJECT_ID='wave46-mihaiadrian'
                IMAGE_URI="gcr.io/$PROJECT_ID/titanic:model"
           '''
      }
    } 
    stage('cleanup') {
      steps {
        sh 'docker system prune -a --volumes --force'
      }
    }
    stage('build image') {
      steps {
        sh 'docker build -t $IMAGE_URI .'
      }
    }
  }
}
