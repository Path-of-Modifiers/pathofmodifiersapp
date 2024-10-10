import { Box, CloseButton, Flex, Stack } from "@chakra-ui/react";
import { GroupedModifierByEffect, GroupedModifier } from "../../../client";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
  HandleChangeEventFunction,
} from "../StandardLayoutInput/SelectBoxInput";
// import {
//   MinMaxNumberProps,
//   MinMaxNumberInput,
// } from "../StandardLayoutInput/MinMaxNumberInput_v2";
import { AddICheckText } from "../../Icon/AddICheckText";
import { useExpandedComponentStore } from "../../../store/ExpandedComponentStore";
import { useEffect, useState } from "react";
import AddIconCheckbox from "../../Icon/AddIconCheckbox";
import { useGraphInputStore } from "../../../store/GraphInputStore";
// For debugging purposes
// import { useOutsideClick } from "../../../hooks/useOutsideClick";
import { MixedInput } from "./MixedInput";
interface ModifierInputProps {
  prefetchedmodifiers: GroupedModifierByEffect[];
}

export interface ModifierOption extends SelectBoxOptionValue {
  isSelected?: boolean;
  index?: number;
  static?: boolean;
  relatedUniques: string;
  groupedModifier: GroupedModifier;
}

export const ModifierInput = (props: ModifierInputProps) => {
  const modifierPreFetched: ModifierOption[] = props.prefetchedmodifiers.map(
    (prefetchedModifier) => ({
      value: prefetchedModifier.effect,
      label: prefetchedModifier.effect,
      regex: prefetchedModifier.regex,
      static: prefetchedModifier.static ?? undefined,
      relatedUniques: prefetchedModifier.relatedUniques,
      groupedModifier: prefetchedModifier.groupedModifier,
    })
  );
  // For debugging purposes
  // const ref = useOutsideClick(() => {
  //   const store = useGraphInputStore.getState();
  // console.log("STORE", store);
  // console.log("LOCALSTORESELECTEDMODIFIERS", selectedModifiers);
  // });

  const [selectedModifiers, setSelectedModifiers] = useState<ModifierOption[]>(
    []
  );

  const {
    addModifierSpec,
    removeModifierSpec,
    nPossibleInputs,
    updateNPossibleInputs,
  } = useGraphInputStore();

  const handleModifierSelect: HandleChangeEventFunction = (
    newValue,
    overrideIndex?: number
  ) => {
    const newlySelectedModifier = modifierPreFetched.find(
      (modifier) => modifier.label === newValue?.label
    );
    if (!newlySelectedModifier) {
      return;
    }

    const nInputs = newlySelectedModifier.groupedModifier.modifierId.length;

    newlySelectedModifier.isSelected = true;
    if (overrideIndex !== undefined) {
      newlySelectedModifier.index = overrideIndex;

      setSelectedModifiers((prevSelectedModifiers) => [
        ...prevSelectedModifiers.slice(0, overrideIndex),
        newlySelectedModifier,
        ...prevSelectedModifiers.slice(overrideIndex + 1),
      ]);

      newlySelectedModifier.groupedModifier.modifierId.map((modifierId) => {
        removeModifierSpec(modifierId);
        addModifierSpec({ modifierId: modifierId }, overrideIndex, nInputs);
      });
    } else {
      newlySelectedModifier.index = selectedModifiers.length;
      setSelectedModifiers((prevSelectedModifiers) => [
        ...prevSelectedModifiers,
        newlySelectedModifier,
      ]);
      newlySelectedModifier.groupedModifier.modifierId.map((modifierId) => {
        addModifierSpec(
          { modifierId: modifierId },
          selectedModifiers.length,
          nInputs
        );
      });
    }
  };

  const { setExpandedModifiers } = useExpandedComponentStore();
  const expandedModifiers = useExpandedComponentStore(
    (state) => state.expandedModifiers
  );
  const handleExpanded = () => {
    setExpandedModifiers(!expandedModifiers);
  };

  const handleCheckboxChange = (selectedModifier: ModifierOption) => {
    console.log(selectedModifier);
    selectedModifier.isSelected = !selectedModifier.isSelected;
  };

  const handleRemoveModifier = (index_to_remove: number) => {
    const modifierToRemove = selectedModifiers.find(
      (modifier) => modifier.index === index_to_remove
    );
    if (modifierToRemove) {
      setSelectedModifiers((prevSelectedModifiers) =>
        prevSelectedModifiers.filter(
          (modifier) => modifier.index !== index_to_remove
        )
      );
      setSelectedModifiers((prevSelectedModifiers) =>
        prevSelectedModifiers.map((selectedModifier, index) => ({
          ...selectedModifier,
          index: index,
        }))
      );
      removeModifierSpec(index_to_remove);
      updateNPossibleInputs();
    }
  };

  const { clearClicked, wantedModifierSpecs, setClearClicked } =
    useGraphInputStore();

  useEffect(() => {
    if (clearClicked) {
      setSelectedModifiers([]);
      setClearClicked();
    }
  }, [clearClicked, setClearClicked]);

  useEffect(() => {
    console.log(wantedModifierSpecs);
  }, [wantedModifierSpecs]);

  const selectedModifierSelectBoxes = selectedModifiers.map(
    (selectedModifier, index) => (
      <Flex
        key={index}
        bgColor={"ui.secondary"}
        flexDirection={"row"}
        height={10}
        // maxHeight={10}
        maxWidth="95vw"
        alignItems={"center"}
        gap={2}
      >
        <AddIconCheckbox
          isChecked={selectedModifier.isSelected}
          key={index}
          onChange={() => {
            if (selectedModifier.groupedModifier.modifierId[0] !== null) {
              handleCheckboxChange(selectedModifier);
            }
          }}
        />
        <SelectBoxInput
          handleChange={handleModifierSelect}
          optionsList={modifierPreFetched}
          defaultText={selectedModifier.label}
          multipleValues={true}
          id={`modifierInput-${index}`}
          isDimmed={!selectedModifier.isSelected}
          presetIndex={index}
          flexProps={{
            w: `${80 - nPossibleInputs * 10}%`,
            minW: `${80 - nPossibleInputs * 10}%`,
            // mr: "auto",
          }}
        />
        <MixedInput
          selectedModifier={selectedModifier}
          index={index}
          isDimmed={!selectedModifier.isSelected}
          nPossibleInputs={nPossibleInputs}
          ml="auto"
        />
        <CloseButton
          _hover={{ background: "gray.100", cursor: "pointer" }}
          onClick={() => {
            handleRemoveModifier(index);
          }}
        />
      </Flex>
    )
  );

  return (
    <Flex direction="column" color="ui.dark" width={"inputSizes.ultraBox"}>
      <Box mb={2}>
        <AddICheckText
          text="Modifiers"
          isChecked={expandedModifiers}
          onChange={handleExpanded}
        />
      </Box>
      {expandedModifiers && (
        <Box>
          <Stack color={"ui.white"} width="100%" mb={2}>
            {selectedModifierSelectBoxes}
          </Stack>

          {/* mx here needs to be same length as checkboxes in selectedModifiersList */}
          <Box
            mx="40px"
            // For debugging purposes
            // ref={ref}
          >
            <SelectBoxInput
              handleChange={handleModifierSelect}
              optionsList={modifierPreFetched}
              defaultText="+ Add Modifier"
              multipleValues={true}
              id={`modifierInput-${selectedModifiers.length}`}
              flexProps={{
                width: "100%",
              }}
            />
          </Box>
        </Box>
      )}
    </Flex>
  );
};
