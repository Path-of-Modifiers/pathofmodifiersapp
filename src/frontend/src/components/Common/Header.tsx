import {
  Flex,
  Link,
  Text,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
} from "@chakra-ui/react";
import SettingsIcon from "../Icon/SettingsIcon";
import LogoutIcon from "../Icon/LogoutIcon";
import useAuth from "../../hooks/validation/useAuth";

// Header component for the application
const Header = () => {
  const { logout } = useAuth();
  const { user: currentUser } = useAuth();

  return (
    <Flex as="header" align="center" justify="space-between" padding="1rem">
      <Link href={"/"}>
        <Text
          color="ui.white"
          fontSize="30px"
          fontWeight="medium"
          _hover={{ color: "ui.inputChanged", textDecoration: "underline" }}
        >
          Path of Modifiers
        </Text>
      </Link>

      {/* Menu for user actions */}
      <Menu placement="bottom-end">
        <MenuButton
          color="ui.white"
          fontSize="20px"
          fontWeight="medium"
          _hover={{ color: "ui.inputChanged", textDecoration: "underline" }}
        >
          <Text>{currentUser?.username}</Text>
        </MenuButton>
        <MenuList bgColor="ui.secondary" border={0} p={2} minW="150px">
          <MenuItem
            color="ui.white"
            bgColor="ui.secondary"
            icon={<SettingsIcon />}
            onClick={() => (window.location.href = "/settings")}
            _hover={{ bgColor: "ui.lighterSecondary.100" }}
          >
            Settings
          </MenuItem>
          <MenuItem
            color="ui.white"
            bgColor="ui.secondary"
            icon={<LogoutIcon />}
            onClick={logout}
            _hover={{ bgColor: "ui.lighterSecondary.100" }}
          >
            Logout
          </MenuItem>
        </MenuList>
      </Menu>
    </Flex>
  );
};

export default Header;
