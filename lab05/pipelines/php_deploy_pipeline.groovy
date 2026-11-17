pipeline {
    agent {
        label 'ansible-agent'
    }

    parameters {
        string(name: 'GIT_URL', defaultValue: 'https://github.com/gausatereduard/automation.git', description: 'Repository that contains both the playbooks and the PHP project')
        string(name: 'BRANCH', defaultValue: 'main', description: 'Branch to deploy')
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

        stage('Deploy to Test Server') {
            steps {
                dir('automation/lab05') {
                    sh '''
                        set -e
                        ansible-playbook -i ansible/hosts.ini ansible/deploy_php_app.yml \
                            -e "project_dir=$WORKSPACE/automation/lab05/app"
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    set -e
                    curl -fsS http://test-server/ | grep -q 'Aurora Studio'
                    echo 'Test server responds and serves the deployed site.'
                '''
            }
        }
    }

    post {
        success {
            echo 'Deployment completed. Open http://localhost:8081/ in a browser.'
        }
        failure {
            echo 'Deployment failed. Check the stage log above.'
        }
    }
}
