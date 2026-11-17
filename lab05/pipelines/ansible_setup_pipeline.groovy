pipeline {
    agent {
        label 'ansible-agent'
    }

    parameters {
        string(name: 'GIT_URL', defaultValue: 'https://github.com/gausatereduard/automation.git', description: 'Repository that contains the Ansible playbooks')
        string(name: 'BRANCH', defaultValue: 'main', description: 'Branch to use')
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                dir('automation') {
                    deleteDir()
                    git branch: params.BRANCH, url: params.GIT_URL
                }
            }
        }

        stage('Check Ansible') {
            steps {
                sh '''
                    ansible --version
                    ansible-playbook --version
                '''
            }
        }

        stage('Configure Test Server') {
            steps {
                dir('automation/lab05') {
                    sh '''
                        set -e
                        ansible-playbook -i ansible/hosts.ini ansible/setup_test_server.yml
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Test server configured successfully.'
        }
        failure {
            echo 'Ansible playbook failed. Check the stage log above.'
        }
    }
}
