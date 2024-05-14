# Path of Modifiers - Frontend

The frontend is built with [Vite](https://vitejs.dev/), [React](https://react.dev/), [TypeScript](https://www.typescriptlang.org/), [TanStack Query](https://tanstack.com/query/latest), [TanStack Router](https://tanstack.com/router/latest), [Zustand](https://github.com/pmndrs/zustand) and [Chakra UI](https://v2.chakra-ui.com/).

## Frontend development

Before you begin, ensure that you have the Node Version Manager (nvm) installed on your system.

- You can install it using the [official nvm guide](https://github.com/nvm-sh/nvm#installing-and-updating).

- After installing nvm, proceed to the `frontend` directory:

```bash
cd frontend
```

- If the Node.js version specified in the .nvmrc file isn't installed on your system, you can install it using the appropriate command:

```bash
npm install
```

- Once the installation is complete, switch to the installed version:

```bash
nvm use
```

- Within the `frontend` directory, install the necessary NPM packages:

```bash
npm install
```

- And start the live server with the following `npm` script:

```bash
npm run dev
```

- Then open your browser at [http://localhost:5173/](http://localhost:5173/).

Notice that this live server is not running inside Docker, it's for local development, and that is the recommended workflow. Once you are happy with your frontend, you can build the frontend Docker image and start it, to test it in a production-like environment. But building the image at every change will not be as productive as running the local development server with live reload.

## Generate Client

- Start the Docker Compose stack.

- Download the OpenAPI JSON file from [http://localhost/api/v1/openapi.json](http://localhost/api/api_v1/openapi.json) and copy it to a new file `openapi.json` at the root of the `frontend` directory.

- To simplify the names in the generated frontend client code, modify the `openapi.json` file by running the following script:

```bash
node modify-openapi-operationids.js
```

- To generate the frontend client, run:

```bash
npm run generate-client
```

- Commit the changes.

## Code structure

The frontend code is structured as follows:

- `frontend/src` - The main frontend code.
- `frontend/src/assets` - Static assets.
- `frontend/src/client` - The generated OpenAPI client.
- `frontend/src/components` - The different components of the frontend.
- `frontend/src/hooks` - Custom hooks.
- `frontend/src/routes` - The different routes of the frontend which include the pages.
  theme.tsx - The Chakra UI custom theme.
- `frontend/store` - Zustand Global State management functions.
