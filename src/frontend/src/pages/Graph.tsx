import React from 'react';

import { Container, Text } from '@chakra-ui/react';



const Dashboard: React.FC = () => {

    return (
        <>
            <Container maxW='full' pt={12}>
                <Text fontSize='2xl'>Hi, Sjukingen! 👋🏼</Text>
                <Text>Welcome back, nice to see you again!</Text>
            </Container>
        </>

    )
}

export default Dashboard;