pipeline {
    agent any

    tools {
        git 'Default' // Specify the name of the Git tool configured in Jenkins
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
