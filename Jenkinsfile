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
 stage('Setup Virtual Environment') {
            
                // Using ShiningPanda plugin to create a virtual environment
                sh 'python3 -m venv venv'
                script {
                    // Activating virtual environment
                    if (isUnix()) {
                        sh '. venv/bin/activate'
                    } else {
                        bat 'venv\\Scripts\\activate'
                    }

                    // Install dependencies
                    sh 'pip install -r requirements.txt'
                }
        }

        stage('Run Selenium Tests') {
          
                script {
                    // Activating virtual environment
                    if (isUnix()) {
                        sh '. venv/bin/activate'
                    } else {
                        bat 'venv\\Scripts\\activate'
                    }
                    // Run your Selenium tests
                    sh 'python -m pytest tests/' // Replace with your test command
                
            }
        }
        

  stage('Creating Test Report'){
    // If you're generating JUnit XML reports with pytest, you can archive them like this:
    junit '**/test-reports/*.xml'
  }
}
