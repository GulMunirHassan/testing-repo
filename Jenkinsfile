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

        // stage('OWASP Dependency-Check Vulnerabilities') {
        //     steps {
        //         script{
        //         dependencyCheck additionalArguments: ''' 
        //             -o './'
        //             -s './'
        //             -f 'ALL' 
        //             --prettyPrint''', odcInstallation: 'OWASP Dependency-Check Vulnerabilities'
                
        //         dependencyCheckPublisher pattern: 'dependency-check-report.xml'
        //         }
        //     }
        // }

    //     stage('Run Django Migrations') {
    //         steps {
    //             script {
    //                 if (isUnix()) {
    //                     sh 'bash -c ". venv/bin/activate"'
    //                 } else {
    //                     bat 'venv\\Scripts\\activate.bat'
    //                 }
    //                 sh 'python3 manage.py migrate'
    //             }
    //         }
    //     }

    //     stage('Collect Static Files') {
    //         steps {
    //             script {
    //                 if (isUnix()) {
    //                     sh 'bash -c ". venv/bin/activate"'
    //                 } else {
    //                     bat 'venv\\Scripts\\activate.bat'
    //                 }
    //                 sh 'python3 manage.py collectstatic --noinput'
    //             }
    //         }
    //     }

    //     stage('Run Django Tests') {
    //         steps {
    //             script {
    //                 if (isUnix()) {
    //                     sh 'bash -c ". venv/bin/activate"'
    //                 } else {
    //                     bat 'venv\\Scripts\\activate.bat'
    //                 }
    //                 sh 'python3 manage.py test'
    //             }
    //         }
    //     }

    //     stage('Build Docker Image') {
    //     steps {
    //         script {
    //             // Set the Docker image name
    //             def dockerImageName = 'gulmunir/test'
    //             def dockerTag = 'latest' // or use a specific tag like '${BUILD_NUMBER}'

    //             // Build the Docker image
    //             sh "docker build -t ${dockerImageName}:${dockerTag} ."
    //         }
    //     }
    // }

    // stage('Push to Docker Hub') {
    //     steps {
    //         script {
    //             // Set Docker Hub credentials
    //             def dockerHubCredentials = 'gulmunir'

    //             // Log in to Docker Hub
    //             withCredentials([usernamePassword(credentialsId: dockerHubCredentials, usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_PASSWORD')]) {
    //                 sh "echo $DOCKERHUB_PASSWORD | docker login -u $DOCKERHUB_USERNAME --password-stdin"
    //             }

    //             // Set the Docker image name
    //             def dockerImageName = 'gulmunir/test'
    //             def dockerTag = 'latest' // or use a specific tag like '${BUILD_NUMBER}'

    //             // Push the Docker image to Docker Hub
    //             sh "docker push ${dockerImageName}:${dockerTag}"
    //         }
    //     }
    // }

       stage('Run Ansible Playbook') {
            steps {
                script {
            withCredentials([sshUserPrivateKey(credentialsId: 'ansible', keyFileVariable: 'SSH_KEY')]) {
                sh """
                   export ANSIBLE_HOST_KEY_CHECKING=False
                   ansible-playbook /etc/ansible/myplaybook.yml --private-key=$SSH_KEY
                """
                    }
                }
            }
        }
    }
}
