import { Box, CloseButton, Flex, Stack } from "@chakra-ui/react";
import { GroupedModifierByEffect, GroupedModifier } from "../../../client";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
  HandleChangeEventFunction,
} from "../StandardLayoutInput/SelectBoxInput";
import { AddICheckText } from "../../Icon/AddICheckText";
import { useExpandedComponentStore } from "../../../store/ExpandedComponentStore";
import { useEffect, useState } from "react";
import AddIconCheckbox from "../../Icon/AddIconCheckbox";
import { useGraphInputStore } from "../../../store/GraphInputStore";
// For debugging purposes
// import { useOutsideClick } from "../../../hooks/useOutsideClick";
import { FancySelectedModifier } from "./FancySelectedModifier";
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
  // The modifier options need to be formatted in a certain way
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

  const { addModifierSpec, removeModifierSpec, updateSelectedModifierSpec } =
    useGraphInputStore();

  // NOTE: Tthe index, which is the selected modifier's position in
  //`selectedModifiers` is used as a unique identifier both internally
  // in `ModifierInput` but also for `WantedModifierSpecs` which allows
  // multiple of the same modifier to be present in `WantedModifier`
  // by extension.
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

    newlySelectedModifier.isSelected = true;
    // Removes the current modifier and replaces it with the new
    if (overrideIndex !== undefined) {
      newlySelectedModifier.index = overrideIndex;

      setSelectedModifiers((prevSelectedModifiers) => [
        ...prevSelectedModifiers.slice(0, overrideIndex),
        newlySelectedModifier,
        ...prevSelectedModifiers.slice(overrideIndex + 1),
      ]);

      removeModifierSpec(overrideIndex);
      newlySelectedModifier.groupedModifier.modifierId.map((modifierId) => {
        addModifierSpec({ modifierId: modifierId }, overrideIndex);
      });
    } else {
      newlySelectedModifier.index = selectedModifiers.length;
      setSelectedModifiers((prevSelectedModifiers) => [
        ...prevSelectedModifiers,
        newlySelectedModifier,
      ]);
      newlySelectedModifier.groupedModifier.modifierId.map((modifierId) => {
        addModifierSpec({ modifierId: modifierId }, selectedModifiers.length);
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

  const handleCheckboxChange = (
    selectedModifier: ModifierOption,
    index_to_handle: number
  ) => {
    updateSelectedModifierSpec(index_to_handle, !selectedModifier.isSelected);
    selectedModifier.isSelected = !selectedModifier.isSelected;
    // Removes the modifier if not selected, and adds it
    // if it is selected.
    // if (selectedModifier.isSelected) {
    //   selectedModifier.groupedModifier.modifierId.map((modifierId) => {
    //     addModifierSpec({ modifierId: modifierId }, index_to_handle);
    //   });
    // } else {
    //   removeModifierSpec(index_to_handle);
    // }
  };

  // Removes the modifier
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
    }
  };

  const { clearClicked, setClearClicked } = useGraphInputStore();

  // removes all selected modifiers
  useEffect(() => {
    if (clearClicked) {
      setSelectedModifiers([]);
      setClearClicked();
    }
  }, [clearClicked, setClearClicked]);

  // For debugging
  // const { wantedModifierSpecs } = useGraphInputStore();
  // useEffect(() => {
  //   console.log(wantedModifierSpecs);
  // }, [wantedModifierSpecs]);

  const selectedModifierSelectBoxes = selectedModifiers.map(
    (selectedModifier, index) => (
      <Flex
        key={index}
        bgColor={"ui.secondary"}
        flexDirection={"row"}
        // height={10}
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
              handleCheckboxChange(selectedModifier, index);
            }
          }}
        />
        <FancySelectedModifier
          selectedModifier={selectedModifier}
          index={index}
          isDimmed={!selectedModifier.isSelected}
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
