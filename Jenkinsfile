pipeline {
    agent any

    environment {
        SONAR_QUBE_SCANNER_HOME = tool 'testingSonarQube'
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
                bat 'C:\\Users\\IntraPC\\AppData\\Local\\Programs\\Python\\Python312\\python -m venv venv'
                bat 'venv\\Scripts\\activate'

                // Install Python dependencies
                bat 'pip install -r requirements.txt'

                // Run SonarQube analysis
                script {
                    def scannerHome = tool 'testingSonarQube'
                    withSonarQubeEnv('testingSonarQube') {
                        bat 'C:\\Users\\IntraPC\\Downloads\\sonarqube\\bin\\windows-x86-64\\SonarScanner.MSBuild.exe begin /k:"testingSonarQube" /n:"testingSonarQube" /v:"1.0"'
                        bat 'MSBuild.exe /t:Rebuild'
                        bat 'C:\\Users\\IntraPC\\Downloads\\sonarqube\\bin\\windows-x86-64\\SonarScanner.MSBuild.exe end'
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up
            bat 'venv\\Scripts\\deactivate' // Deactivate Python virtual environment
            deleteDir()
        }
    }
}
