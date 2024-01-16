pipeline{
  agent { label 'linux' }
  options{
    buildDiscarder(logRotator(numToKeepStr: '5'))
  }
Stages{
  Stage('Scan'){
    steps {
        withSonarQubeEnv(installationName: 'testingSonarQube'){
          sh.'./mvnw clean sonar:sonar'
        }
    }
  }
}
}
