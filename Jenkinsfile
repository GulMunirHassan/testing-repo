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
        script {
            def scannerHome = tool 'SonarQube'
            withSonarQubeEnv('testingSonarQube') {
                sh """
                    ${scannerHome}/bin/sonar-scanner \
                    -X \
                    -Dsonar.host.url=localhost:9000 \
                    -Dsonar.login=sqp_40be0bcd4d6ecf4945fc3c1fbe60cfc9cb952f4e
                """
            }
        }
    }
}


    }
}
