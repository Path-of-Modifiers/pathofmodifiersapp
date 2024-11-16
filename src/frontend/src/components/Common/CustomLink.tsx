import { LinkProps, Link } from "@chakra-ui/react";
import { Link as RouterLink } from "@tanstack/react-router";

interface CustomLinkProps extends LinkProps {
  internalRoute?: string;
  hrefRoute?: string;
  from?: string;
}

const CustomLink = ({
  children,
  hrefRoute,
  internalRoute,
  from,
  ...props
}: CustomLinkProps) => {
  return (
    <Link
      {...props}
      as={RouterLink}
      to={internalRoute ? internalRoute : hrefRoute}
      from={from}
    >
      {children}
    </Link>
  );
};

export default CustomLink;
