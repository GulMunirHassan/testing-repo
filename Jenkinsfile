pipeline {
    agent any

    tools {
        git 'Git' // Specify the name of the Git tool configured in Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout code from GitHub
                git branch: 'main', url: 'https://github.com/GulMunirHassan/testing-repo.git'
            }
        }

        stage('Build and Analyze') {
            steps {
                // Set up Python virtual environment
                script {
                    // Your existing setup code
                }

                // Run SonarQube analysis
                script {
                    def scannerHome = tool 'SonarQube'
                    withSonarQubeEnv('testingSonarQube') {
                        sh "$scannerHome/bin/sonar-scanner"
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up
            script {
                // Your existing cleanup code
            }
        }
    }
}
