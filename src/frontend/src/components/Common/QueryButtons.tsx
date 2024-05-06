import { Box, Button, ButtonGroup} from "@chakra-ui/react";
import {useState} from "react";
import { MdExpandMore, MdExpandLess } from "react-icons/md"


const QueryButtons = () => {
    const [showingFilter, setShowingFilter] = useState(true);

    return <Box bg="ui.main">
        <ButtonGroup variant="solid" colorScheme="red">
            <Button>
                Clear Query
            </Button>
            <Button variant="solid" colorScheme="green">
                Query and Plot
            </Button>
            {/* <showFilterButton /> */}
            <Button variant="solid" colorScheme="gray" rightIcon={showingFilter?<MdExpandLess />:<MdExpandMore />}> 
                {showingFilter?"Hide Filters":"Show Filters"}
            </Button>
        </ButtonGroup>
    </Box>
}


export default QueryButtons