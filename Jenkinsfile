String dockerTag = null

node {

    dockerTag = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"

    stage('Checkout')
    {
        checkout scm
    }

    stage('Build image')
    /*In this stage, docker builds the image in the path stablished.*/
    {
        sh "/usr/bin/docker build -t backend-practica  . "
    }

    stage('Test image') {
         //app.inside {
        //    sh 'echo "Tests passed"'
        //}
    }

    stage('Push image')
    {
        /* Finally, we'll push the image with two tags:
         * First, the incremental build number from Jenkins
         * Second, the 'latest' tag.
         * Pushing multiple tags is cheap, as all the layers are reused. */

        withCredentials([usernamePassword(credentialsId: '48253a45-d82c-43c8-b39e-031c511bc475', passwordVariable: 'DOCKER_REGISTRY_PASS', usernameVariable: 'DOCKER_REGISTRY_USER')]) {
            sh "docker login --username=${DOCKER_REGISTRY_USER} --password=${DOCKER_REGISTRY_PASS} "
             if (${env.BRANCH_NAME}=='master')
             {
                dockerTag = latest
             }
            sh "docker tag backend-practica dinocloud/backend-practica:${dockerTag}"
            sh "docker push dinocloud/backend-practica:${dockerTag}"
    }

     stage ('Clean local memory')
        {
            sh "docker rmi -f \$(docker images -f \"reference=dinocloud/backend-practica:${dockerTag}\" -q)"
        }
    }


}

