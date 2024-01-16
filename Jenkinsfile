pipeline {
  agent { label 'linux' }
  options {
    buildDiscarder(logRotator(numToKeepStr: '5'))
  }
  stages {
    stage('Scan') {
      steps {
        withSonarQubeEnv(installationName: 'testingSonarQube') {
          sh './mvnw clean sonar:sonar' // Fix the typo here
        }
      }
    }
  }
}
