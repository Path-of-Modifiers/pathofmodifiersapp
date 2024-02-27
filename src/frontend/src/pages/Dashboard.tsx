import React from 'react';

import { Container, Text } from '@chakra-ui/react';
import { Image } from '@chakra-ui/react';



const Dashboard: React.FC = () => {

    return (
        <>
            <Container maxW='full' pt={12}>
                <Text fontSize='2xl'>Hi, Sjukingen! 👋🏼</Text>
                <Text>Welcome back, nice to see you again!</Text>
                <Image src="./images/POM_logo.jpg" alt="POM logo"/>
            </Container>
        </>

    )
}

export default Dashboard;