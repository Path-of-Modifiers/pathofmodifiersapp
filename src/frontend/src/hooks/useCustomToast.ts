import { useToast } from "@chakra-ui/react";
import { useCallback } from "react";

export interface Toast {
  (title: string, description: string, status: "success" | "error"): void;
}

const useCustomToast = () => {
  const toast = useToast();

  const showToast = useCallback(
    (title: string, description: string, status: "success" | "error") => {
      toast({
        title,
        description,
        status,
        isClosable: true,
        position: "bottom-right",
      });
    },
    [toast]
  );

  return showToast;
};

export default useCustomToast;
