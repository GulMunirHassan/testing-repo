node {
  stage('SCM') {
    checkout scm
  }
  stage('SonarQube Analysis') {
    def scannerHome = tool 'SonarQube';
    withSonarQubeEnv() {
      sh "${scannerHome}/bin/sonar-scanner"
    }
  }
  stage('OWASP Dependency-Check Vulnerabilities') {
        dependencyCheck additionalArguments: ''' 
                    -o './'
                    -s './'
                    -f 'ALL' 
                    --prettyPrint''', odcInstallation: 'OWASP Dependency-Check Vulnerabilities'
        
        dependencyCheckPublisher pattern: 'dependency-check-report.xml'
    }
  stage('Run Selenium Tests') {
    // Assuming your tests can be run with a simple command
    // You might need to activate a virtual environment or set other environment variables
    sh 'python -m pytest tests/' // Replace with your test command
    //sh 'mvn test'

    // If you're generating JUnit XML reports with pytest, you can archive them like this:
    junit '**/test-reports/*.xml'
  }
}
