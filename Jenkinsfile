pipeline {
  agent any
  options {
    buildDiscarder(logRotator(numToKeepStr: '5'))
  }
  stages {
    stage('Scan') {
      steps {
        script {
          // Use 'mvnw.cmd' on Windows with the correct path
          bat '"./mvnw.cmd" clean sonar:sonar'
        }
      }
    }
  }
}

