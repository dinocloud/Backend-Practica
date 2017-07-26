node {

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
            sh 'docker tag backend-practica dinocloud/backend-practica:$(echo ${BRANCH_NAME}   | sed -e "s|origin/||g") -${BUILD_NUMBER}="devops_file"'
            sh 'docker push dinocloud/backend-practica:$(echo ${BRANCH_NAME}   | sed -e "s|origin/||g") -${BUILD_NUMBER}="devops_file"'
        }

     stage ('Clean local memory')
        {
            sh 'docker rmi dinocloud/backend-practica:$(echo ${BRANCH_NAME}'
        }


    }


}

