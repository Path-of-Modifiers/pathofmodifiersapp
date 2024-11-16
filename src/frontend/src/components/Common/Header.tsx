import {
  Flex,
  Text,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
} from "@chakra-ui/react";

import SettingsIcon from "../Icon/SettingsIcon";
import LogoutIcon from "../Icon/LogoutIcon";
import useAuth from "../../hooks/validation/useAuth";
import CustomLink from "./CustomLink";

// Header component for the application
const Header = () => {
  const { logout } = useAuth();
  const { user: currentUser } = useAuth();

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
          <CustomLink internalRoute="/settings">
            <MenuItem
              color="ui.white"
              bgColor="ui.secondary"
              icon={<SettingsIcon />}
              _hover={{ bgColor: "ui.lighterSecondary.100" }}
            >
              Settings
            </MenuItem>
          </CustomLink>
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
