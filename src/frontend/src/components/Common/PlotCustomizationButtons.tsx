import { Button, Flex, FlexProps } from "@chakra-ui/react";
import { capitalizeFirstLetter } from "../../hooks/utils";
import { usePlotSettingsStore } from "../../store/PlotSettingsStore";
import { CurrencyVisuals } from "../Graph/GraphComponent";

interface PlotCustomizationButtonsProps {
  flexProps: FlexProps | undefined;
  mostCommonCurrencyUsed: string;
  chaosVisuals: CurrencyVisuals;
  secondaryVisuals: CurrencyVisuals;
}

const PlotCustomizationButtons = (props: PlotCustomizationButtonsProps) => {
  const mostCommonCurrencyUsed: string = props.mostCommonCurrencyUsed;
  const renderButtons = mostCommonCurrencyUsed !== "chaos";

  const { setShowChaos, setShowSecondary } = usePlotSettingsStore();

  const handleShowChaos = () => {
    setShowChaos();
  };
  const handleShowSecondary = () => {
    setShowSecondary();
  };

  return (
    renderButtons && (
      <Flex
        {...props.flexProps}
        direction={["column", "row"]} // Column for small screens, row for larger screens
        maxW="98vw"
        flexWrap="wrap"
      >
        <Button
          variant="solid"
          bg={props.chaosVisuals.buttonBackground}
          color={props.chaosVisuals.buttonColor}
          _hover={{ bg: "ui.lightInput" }}
          onClick={handleShowChaos}
          borderWidth={1}
          borderColor={props.chaosVisuals.buttonBorderColor}
          mb={[2, 0]}
        >
          Show price in Chaos
        </Button>
        <Button
          variant="solid"
          bg={props.secondaryVisuals.buttonBackground}
          color={props.secondaryVisuals.buttonColor}
          _hover={{ bg: "ui.lightInput" }}
          borderWidth={1}
          ml={[0, 2]}
          borderColor={props.secondaryVisuals.buttonBorderColor}
          onClick={handleShowSecondary}
        >
          Show price in {capitalizeFirstLetter(mostCommonCurrencyUsed)}
        </Button>
      </Flex>
    )
  );
};

export default PlotCustomizationButtons;
