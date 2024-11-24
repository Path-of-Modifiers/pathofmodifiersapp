import { Flex, Text } from "@chakra-ui/react";
import CustomLink from "./CustomLink";
import DateDaysHoursSinceLaunchStats from "./DateDaysHoursSinceLaunchStats";

// Header component for the application
const Header = () => {
  return (
    <Flex as="header" align="center" justify="space-between" padding="1rem">
      <CustomLink internalRoute={"/"}>
        <Text
          color="ui.white"
          fontSize="30px"
          fontWeight="medium"
          _hover={{ color: "ui.inputChanged", textDecoration: "underline" }}
        >
          Path of Modifiers
        </Text>
      </CustomLink>

      <DateDaysHoursSinceLaunchStats
        style={{ transform: "translateY(5px)" }}
        textAlign="center"
        color="white"
      />
    </Flex>
  );
};

export default Header;
