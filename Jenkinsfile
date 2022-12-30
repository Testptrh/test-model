pipeline {
    agent any
    stages {
        stage('Build image') {
            steps {
                // Build the container image using the Dockerfile in the project's root directory
                sh 'docker build ./ -t gcr.io/wave46-mihaiadrian/titanic:cicd'
            }
        }
        stage('Push image') {
            steps {
                sh 'docker push gcr.io/wave46-mihaiadrian/titanic:cicd'
            } 
        }
        stage('Deploy on port') {
            steps {
                sh 'kubectl expose deployment titanic-app --name=titanic-service-cicd --type=LoadBalancer --port 80 --target-port 8000'
            }
        }
        
    }
}
