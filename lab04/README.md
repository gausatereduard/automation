Goal
Learn how to configure Jenkins for DevOps task automation, including creating and managing CI/CD pipelines.

Preparation
Create a lab04 folder in your GitHub repository to store all files related to this lab work. You should have Docker and Docker Compose installed to complete the assignment.

Assignment
Create a docker-compose.yml file and define the following services in it:

Jenkins Controller
SSH Agent
Setting up Jenkins Controller
Add the Jenkins Controller service configuration to the docker-compose.yml file:

services:
  jenkins-controller:
    image: jenkins/jenkins:lts
    container_name: jenkins-controller
    ports:
      - "8080:8080"
      - "50000:50000"
    volumes:
      - jenkins_home:/var/jenkins_home
    networks:
      - jenkins-network

volumes:
  jenkins_home:
  jenkins_agent_volume:

networks:
  jenkins-network:
    driver: bridge
Start the Jenkins Controller container using Docker Compose and configure it following the on-screen instructions.

TODO: img src1.png, src2.png

Setting up SSH Agent
Create a secrets folder in the root of your project and add SSH keys necessary for connecting to remote servers.

mkdir secrets
cd secrets
ssh-keygen -f jenkins_agent_ssh_key
Create a Dockerfile for the SSH agent with the following content:

FROM jenkins/ssh-agent

# install PHP-CLI
RUN apt-get update && apt-get install -y php-cli
Add the SSH Agent service configuration to the docker-compose.yml file:

  ssh-agent:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ssh-agent
    environment:
      - JENKINS_AGENT_SSH_PUBKEY=${JENKINS_AGENT_SSH_PUBKEY}
    volumes:
      - jenkins_agent_volume:/home/jenkins/agent
    depends_on:
      - jenkins-controller
    networks:
      - jenkins-network
Create a .env file in the root of your project and add the JENKINS_AGENT_SSH_PUBKEY environment variable.

Restart the Docker Compose project to apply the changes.

Connecting SSH Agent to Jenkins
Check that the "SSH Agents Plugin" is installed in Jenkins. If not, install it via Manage Jenkins > Manage Plugins.

Register SSH keys in Jenkins:

Log into the Jenkins web interface at http://localhost:8080.
Go to Manage Jenkins > Manage Credentials.
Add a new SSH key, setting the username to jenkins and selecting the corresponding private key from the secrets folder.
Add a new Jenkins agent node:

Go to Manage Jenkins > Manage Nodes and Clouds > New Node.
Name the node ssh-agent1, select type Permanent Agent
Add the label php-agent for the node.
Configure the node by specifying:
Remote root directory: /home/jenkins/agent
Launch method: Launch agents via SSH
Host: ssh-agent
Credentials: select the previously added SSH key

TODO: scr4.png

Creating Jenkins Pipeline for DevOps Task Automation
Choose a repository with a PHP project on GitHub (for example, from the "PHP Programming" or "Virtualization and Containerization" course). The project should contain unit tests. Create a new Jenkins pipeline using the following Jenkinsfile:

pipeline {
    agent {
        label 'php-agent'
    }
    
    stages {        
        stage('Install Dependencies') {
            steps {
                // Project preparation (install dependencies if needed)
                echo 'Preparing project...'
                // Add project-specific commands here
            }
        }
        
        stage('Test') {
            steps {
                // Running tests
                echo 'Running tests...'
                // Add commands to run your tests here
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed.'
        }
        success {
            echo 'All stages completed successfully!'
        }
        failure {
            echo 'Errors detected in the pipeline.'
        }
    }
}
Verify that the pipeline executes successfully and unit tests pass.

error I got:

The SSH agent container is fine — it was rejecting connections before authentication because Jenkins refused the agent's SSH host key.

The node is configured with:

```
<sshHostKeyVerificationStrategy class="hudson.plugins.sshslaves.verifiers.KnownHostsFileKeyVerificationStrategy"/>
```
but /var/jenkins_home/.ssh/known_hosts did not exist. Jenkins closed the connection during key exchange, which is exactly what the agent logged as:

```
Connection closed by 172.18.0.2 port ... [preauth]
```
This also explains the repeated attempts every ~15 seconds and the SSH Launch ... failed in 165,334 ms messages. The SSH keys themselves are correct — .env and secrets/jenkins_agent_ssh_key.pub match, and the agent later accepted the key.

What I did
Generated the host keys file inside the Jenkins container and restarted Jenkins:

```
docker exec jenkins-controller sh -c "mkdir -p /var/jenkins_home/.ssh && ssh-keyscan -H ssh-agent > /var/jenkins_home/.ssh/known_hosts && chown -R jenkins:jenkins /var/jenkins_home/.ssh && chmod 700 /var/jenkins_home/.ssh"
docker restart jenkins-controller
```

## Final pipeline overview

TODO: img scr6.png

Report Preparation
Create a readme.md file in the lab04 folder of your GitHub repository. In the report, describe the following points:

Project description.
Steps for setting up Jenkins Controller
Steps for setting up SSH agent
Steps for creating and configuring Jenkins pipeline
Answer the questions:
What are the advantages of using Jenkins for DevOps task automation?
What other types of Jenkins agents exist?
What problems did you encounter when setting up Jenkins and how did you solve them?
Submission
Upload the scripts to your GitHub repository and provide a link to it.
