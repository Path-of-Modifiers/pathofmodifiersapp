import React from 'react';
import ReactDOM from 'react-dom/client';

import { ChakraProvider } from '@chakra-ui/provider';
import { createStandaloneToast } from '@chakra-ui/toast';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';

import Dashboard from './pages/Dashboard';

// import { OpenAPI } from './client';
import theme from './theme';


// OpenAPI.BASE = import.meta.env.VITE_API_URL;
// OpenAPI.TOKEN = async () => {
//   return localStorage.getItem('access_token') || '';
// }

const router = createBrowserRouter([
  {
    path: '/',
    // element: <Root />,
    // errorElement: <ErrorPage />,
    children: [
      { path: '/', element: <Dashboard /> },
    ],
  },
]);

const { ToastContainer } = createStandaloneToast();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <RouterProvider router={router} />
      <ToastContainer />
    </ChakraProvider>
  </React.StrictMode>,
)