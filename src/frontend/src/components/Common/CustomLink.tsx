import { LinkProps, Link } from "@chakra-ui/react";
import { Link as RouterLink } from "@tanstack/react-router";

interface CustomLinkProps extends LinkProps {
  internalRoute?: string;
  hrefRoute?: string;
}

const CustomLink = ({
  children,
  hrefRoute,
  internalRoute,
  ...props
}: CustomLinkProps) => {
  return (
    <Link
      {...props}
      as={RouterLink}
      to={internalRoute ? internalRoute : hrefRoute}
    >
      {children}
    </Link>
  );
};

export default CustomLink;
