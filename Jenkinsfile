pipeline{
    agent any
    options{
        buildDiscarder(logRotator(numToKeepStr:'5'))
    }
    stages{
        stage('Scan'){
            steps{
                withSonarQubeEnv(installationName: 'sonar'){
                    //bat 'mvnw clean org.sonarsource.scanner.maven:sonar-maven-plugin:3.9.0.2155:sonar'
                    bat(script: 'mvnw clean org.sonarsource.scanner.maven:sonar-maven-plugin:3.9.0.2155:sonar', returnStatus: true)
                }
            }
        }
    }
}
