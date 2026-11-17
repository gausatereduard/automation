pipeline {
    agent {
        label 'php-agent'
    }

    parameters {
        string(name: 'GIT_URL', defaultValue: 'https://github.com/gausatereduard/automation.git', description: 'Repository that contains the PHP project')
        string(name: 'BRANCH', defaultValue: 'main', description: 'Branch to build')
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

        stage('Environment') {
            steps {
                sh '''
                    php -v
                    composer --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                dir('automation/lab05/app') {
                    sh '''
                        set -e
                        composer install --no-interaction --prefer-dist --no-progress
                    '''
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                dir('automation/lab05/app') {
                    sh '''
                        set -e
                        vendor/bin/phpunit --log-junit build/junit.xml
                    '''
                }
            }
        }

        stage('Archive Results') {
            steps {
                dir('automation/lab05/app') {
                    archiveArtifacts artifacts: 'build/junit.xml', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'automation/lab05/app/build/junit.xml'
        }
        success {
            echo 'Build and tests completed successfully.'
        }
        failure {
            echo 'Build or tests failed. Check the stage log above.'
        }
    }
}
