import { Box, Button, Container, Text } from "@chakra-ui/react";
import { Link } from "@tanstack/react-router";

// 404 page for the application
const NotFound = () => {
  return (
    <Box bg="ui.main">
      <Container
        h="100vh"
        alignItems="stretch"
        bg="ui.main"
        justifyContent="center"
        textColor="ui.white"
        textAlign="center"
        centerContent
      >
        <Text
          fontSize="8xl"
          color="ui.main"
          fontWeight="bold"
          textColor="ui.white"
          lineHeight="1"
          mb={4}
        >
          404
        </Text>
        <Text fontSize="md" textColor="ui.white">
          Oops!
        </Text>
        <Text fontSize="md" textColor="ui.white">
          Page not found.
        </Text>
        <Button
          as={Link}
          to="/"
          color="ui.main"
          textColor="ui.white"
          borderColor="ui.white"
          variant="outline"
          mt={4}
        >
          Return to Path of Modifiers main page
        </Button>
      </Container>
    </Box>
  );
};

export default NotFound;
