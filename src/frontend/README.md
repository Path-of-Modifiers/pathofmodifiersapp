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

- Download the OpenAPI JSON file from [http://localhost/api/api_v1/openapi.json](http://localhost/api/api_v1/openapi.json) and copy it to a new file `openapi.json` at the root of the `frontend` directory.

- To simplify the names in the generated frontend client code, modify the `openapi.json` file by running the following script:

```bash
node modify-openapi-operationids.js
```

- To generate the frontend client, run:

```bash
npm run generate-client
```

- Commit the changes.

## Add hidden files

The frontend contains some hidden files that we do not want to share with the public. These hidden files are located in the src/frontend/hidden_content directory. Below are the commands to import the hidden files and develop or produce with them. Our project includes decoy files in place of the hidden ones, allowing the project to run, but with different behavior.

- Copy the hidden files to `src\frontend\hidden_content\` respective folders.

- Run the git commands below.

Add clean and smudge filters:

```bash
git config filter.replaceGraphing.clean "cp -a $PWD/src/frontend/hidden_content/graphing_hidden/* $PWD/src/frontend/src/hooks/graphing/"

git config filter.replaceGraphing.smudge "cp -a $PWD/src/frontend/hidden_content/graphing_decoy/* $PWD/src/frontend/src/hooks/graphing/"
```

Ignore changes to the hidden files:

```bash
git update-index --assume-unchanged src/frontend/src/hooks/graphing/utils.tsx
git update-index --assume-unchanged src/frontend/src/hooks/graphing/processPlottingData.tsx
```

## Code structure

The frontend code is structured as follows:

- `frontend/hidden_content` - Hidden files.
- `frontend/src` - The main frontend code.
- `frontend/src/assets` - Static assets.
- `frontend/src/client` - The generated OpenAPI client.
- `frontend/src/components` - The different components of the frontend.
- `frontend/src/hooks` - Custom hooks.
- `frontend/src/routes` - The different routes of the frontend which include the pages.
  theme.tsx - The Chakra UI custom theme.
- `frontend/src/schemas` - Custom schemas for objects.
- `frontend/src/store` - Zustand Global State management functions.
