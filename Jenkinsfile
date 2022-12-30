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
                // Push the image to a Docker registry (e.g., Docker Hub or Google Container Registry)
                    sh 'docker push gcr.io/wave46-mihaiadrian/titanic:cicd'
                }
            }
        stage('Deploy to GKE') {
            steps {
                // Deploy the container image to the GKE cluster
                    kubernetesDeploy(
                    configs: '*.yaml',
                    deployTimeout: 15,
                    namespace: 'cicd1',
                    containerTemplate: 'ci-cd-model:v1',
                    quiet: true
                    )
                }
            }
        }
    }
