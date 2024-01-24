pipeline {
    agent any

    stages {
        stage('SCM') {
            steps {
                checkout scm
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                script {
                    // Create a virtual environment
                    sh 'python3 -m venv venv'
                    // Activate the virtual environment
                    if (isUnix()) {
                        sh 'bash -c ". venv/bin/activate"'
                    } else {
                        bat 'venv\\Scripts\\activate.bat'
                    }
                    // Install dependencies
                    sh 'pip3 install -r requirements.txt'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script{
                def scannerHome = tool 'SonarQube';
                withSonarQubeEnv() {
                    sh "${scannerHome}/bin/sonar-scanner"
                }
                }
            }
        }

        stage('OWASP Dependency-Check Vulnerabilities') {
            steps {
                script{
                dependencyCheck additionalArguments: ''' 
                    -o './'
                    -s './'
                    -f 'ALL' 
                    --prettyPrint''', odcInstallation: 'OWASP Dependency-Check Vulnerabilities'
                
                dependencyCheckPublisher pattern: 'dependency-check-report.xml'
                }
            }
        }

        stage('Run Django Migrations') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'source venv/bin/activate'
                    } else {
                        bat 'venv\\Scripts\\activate.bat'
                    }
                    sh 'python manage.py migrate'
                }
            }
        }

        stage('Collect Static Files') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'source venv/bin/activate'
                    } else {
                        bat 'venv\\Scripts\\activate.bat'
                    }
                    sh 'python manage.py collectstatic --noinput'
                }
            }
        }

        stage('Run Django Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'source venv/bin/activate'
                    } else {
                        bat 'venv\\Scripts\\activate.bat'
                    }
                    sh 'python manage.py test'
                }
            }
        }

        // Add additional stages if necessary (like deployment)
    }
}
