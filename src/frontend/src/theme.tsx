import { extendTheme } from "@chakra-ui/react";

const theme = extendTheme({
  colors: {
    ui: {
      main: "#1B1B1B",
      secondary: "#282828",
      success: "#215918",
      danger: "#FF1D1D",
      white: "#FFFFFF",
      grey: "#B3B3B3",
      dark: "#1A202C",
      input: "#2d3333",
      darkSlate: "#252D3D",
    },
  },
  fonts: {
    body: "Josefin-Sans, Georgia, serif",
    heading: "Josefin-Sans, Georgia, serif",
    sidebar: "Inter, serif",
  },
  fontWeights: {
    hairline: 100,
    thin: 200,
    light: 300,
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
    extrabold: 800,
    black: 900,
  },
  fontSizes: {
    defaultRead: "1rem",
    input: "1.2rem",
    menu: "1.325rem",
  },
  lineHeights: {
    normal: "normal",
    none: 1,
    shorter: 1.25,
    short: 1.375,
    base: 1.5,
    tall: 1.625,
    taller: "2",
    "3": ".75rem",
    "4": "1rem",
    "5": "1.25rem",
    "6": "1.5rem",
    "7": "1.75rem",
    "8": "2rem",
    "9": "2.25rem",
    "10": "2.5rem",
  },
  letterSpacings: {
    tighter: "-0.05em",
    tight: "-0.025em",
    normal: "0",
    wide: "0.025em",
    wider: "0.05em",
    widest: "0.1em",
  },
  sizes: {
    inputSizes: {
      defaultBox: "11rem",
      defaultDescriptionText: "11rem",
      mdBox: "15rem",
      lgBox: "20rem",
    },
  },
});

export default theme;