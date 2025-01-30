# My React Native App

## Description
This is a basic React Native app with authentication screens (Login and Signup) and CI/CD setup.

## Setup
1. Clone the repository:
   ```
   git clone <repository-url>
   cd my-react-native-app
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the app on Android:
   ```
   npm run android
   ```

4. Run the app on iOS:
   ```
   npm run ios
   ```

## CI/CD
The CI/CD pipeline is configured using GitHub Actions. It runs on every push to the `main` branch and on every pull request to the `main` branch. The pipeline includes steps for installing dependencies, running tests, and building the project.

## Features
- Login Screen
- Signup Screen
- Form validation
- State management using Redux
- Navigation using react-navigation
- CI/CD pipeline using GitHub Actions

## Best Practices
- Follow the component-based architecture for better maintainability.
- Use Redux for managing global state.
- Implement form validation to enhance user experience.
- Keep the code clean and well-documented.

## Documentation
For more information on how to use the application, refer to the individual component files and the CI/CD configuration file.