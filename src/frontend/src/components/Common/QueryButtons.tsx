import { Box, Button, ButtonGroup} from "@chakra-ui/react";
import { Dispatch } from "react";
import { MdExpandMore, MdExpandLess } from "react-icons/md"

interface QueryButtonProps {
    showingFilter: boolean;
    setShowingFilter: Dispatch<React.SetStateAction<boolean>>
  }


const QueryButtons = ({showingFilter, setShowingFilter}: QueryButtonProps) => {
    const handleShowingFilter = () => {
        setShowingFilter(!showingFilter);
    }
    return <Box bg="ui.main">
        <ButtonGroup variant="solid" colorScheme="red">
            <Button>
                Clear Query
            </Button>
            <Button variant="solid" colorScheme="green">
                Query and Plot
            </Button>
            <Button variant="solid" colorScheme="gray" rightIcon={showingFilter?<MdExpandLess />:<MdExpandMore />} onClick={handleShowingFilter}> 
                {showingFilter?"Hide Filters":"Show Filters"}
            </Button>
        </ButtonGroup>
    </Box>
}


export default QueryButtons