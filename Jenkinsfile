pipeline {
    agent { dockerfile true }
    stages {
        stage('Test') {
            steps {
                sh '''
                        PROJECT_ID='wave46-mihaiadrian'
                        IMAGE_URI="gcr.io/$PROJECT_ID/titanic:model"
                   '''
            }
        }
        
    stage('build') {
            steps {
                sh 'docker build -t $IMAGE_URI'
            }
        }
        
    stage('login') {
            steps {
                sh 'gcloud auth configure-docker gcr.io'
            }
        }
    
    stage('push') {
            steps {
                sh 'docker push $IMAGE_URI'
            }
        }
    }
}
