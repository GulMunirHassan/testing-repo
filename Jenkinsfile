pipeline {
    agent any

    environment {
        SONAR_QUBE_SCANNER_HOME = tool 'SonarQubeScanner'
        PYTHON_HOME = tool 'Python3'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout code from GitHub
                git 'https://github.com/GulMunirHassan/testing-repo.git'
            }
        }

        stage('Build and Analyze') {
            steps {
                // Set up Python virtual environment
                sh """
                    $C:\Users\IntraPC\AppData\Local\Programs\Python\Python312/python -m venv venv
                    source venv/bin/activate
                """

                // Install Python dependencies
                sh 'pip install -r requirements.txt'

                // Run SonarQube analysis
                script {
                    def scannerHome = tool 'SonarQubeScanner'
                    withSonarQubeEnv('testingSonarQube') {
                        sh "$C:\Users\IntraPC\Downloads\sonarqube\bin\windows-x86-64\SonarService"
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up
            sh 'deactivate' // Deactivate Python virtual environment
            deleteDir()
        }
    }
}
