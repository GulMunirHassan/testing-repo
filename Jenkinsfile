pipeline {
  agent any
  options {
    buildDiscarder(logRotator(numToKeepStr: '5'))
  }
  stages {
    stage('Scan') {
      steps {
        script {
          // Use 'mvnw.cmd' on Windows
          bat './mvnw.cmd clean sonar:sonar'
        }
      }
    }
  }
}
