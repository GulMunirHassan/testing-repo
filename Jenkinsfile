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
                    sh 'pip install -r requirments.txt'
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
                        sh 'bash -c ". venv/bin/activate"'
                    } else {
                        bat 'venv\\Scripts\\activate.bat'
                    }
                    sh 'python3 manage.py migrate'
                }
            }
        }

        stage('Collect Static Files') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'bash -c ". venv/bin/activate"'
                    } else {
                        bat 'venv\\Scripts\\activate.bat'
                    }
                    sh 'python3 manage.py collectstatic --noinput'
                }
            }
        }

        stage('Run Django Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'bash -c ". venv/bin/activate"'
                    } else {
                        bat 'venv\\Scripts\\activate.bat'
                    }
                    sh 'python3 manage.py test'
                }
            }
        }

        stage('Build Docker Image') {
        steps {
            script {
                // Set the Docker image name
                def dockerImageName = 'gulmunir/test'
                def dockerTag = 'latest' // or use a specific tag like '${BUILD_NUMBER}'

                // Build the Docker image
                sh "docker build -t ${dockerImageName}:${dockerTag} ."
            }
        }
    }

    stage('Push to Docker Hub') {
        steps {
            script {
                // Set Docker Hub credentials
                def dockerHubCredentials = 'gulmunir'

                // Log in to Docker Hub
                withCredentials([usernamePassword(credentialsId: dockerHubCredentials, usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_PASSWORD')]) {
                    sh "echo $DOCKERHUB_PASSWORD | docker login -u $DOCKERHUB_USERNAME --password-stdin"
                }

                // Set the Docker image name
                def dockerImageName = 'gulmunir/test'
                def dockerTag = 'latest' // or use a specific tag like '${BUILD_NUMBER}'

                // Push the Docker image to Docker Hub
                sh "docker push ${dockerImageName}:${dockerTag}"
            }
        }
    }

    stage('Add SSH Key') {
            steps {
                script {
                    // Create the .ssh directory if it does not exist
                    sh "mkdir -p /var/lib/jenkins/.ssh"
                    // Set proper permissions
                    sh "chmod 700 /var/lib/jenkins/.ssh"
                    // Add the host key to the known_hosts file
                    sh "ssh-keyscan -t rsa 192.168.0.110 >> /var/lib/jenkins/.ssh/known_hosts"
                    // Set proper permissions for known_hosts file
                    sh "chmod 644 /var/lib/jenkins/.ssh/known_hosts"
                }
            }
        }

    stage('Run Ansible Playbook') {
        steps {
             environment {
                    ANSIBLE_HOST_KEY_CHECKING = "False"
                }
            script {
                // Using withCredentials to securely inject username and password
                    withCredentials([usernamePassword(credentialsId: 'ubuntu', usernameVariable: 'SSH_USER', passwordVariable: 'SSH_PASS')]) {
                        sh """
                            ansible-playbook -i /etc/ansible/hosts /etc/ansible/myplaybook.yml --user $SSH_USER --ask-pass
                        """
                // Assuming Ansible and required roles/collections are already installed on Jenkins server
                // Replace 'your_playbook.yml' with the path to your Ansible playbook
                // Replace 'your_inventory_file' with the path to your Ansible inventory or dynamically create it
                //sh 'ansible-playbook -i /etc/ansible/hosts /etc/ansible/myplaybook.yml'
            }
        }
    }
        
        // Add additional stages if necessary (like deployment)
    }
}
}
