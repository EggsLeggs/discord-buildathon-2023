# Discord Buildathon 2023 Project
## Hiragana & Katakana Practice App

The application is a way to practice Hiragana and Katakana. If you haven't learnt them yet, you can use this [hiragana guide](https://www.tofugu.com/japanese/learn-hiragana/) or [katakana guide](https://www.tofugu.com/japanese/learn-katakana/) to learn them.

⚠️ There are still a couple features missing, you'll see them very soon though:
- a prettier end ui
- buttons with the options in them
- hosting! - This bot will be hosted on a server soon, so you can use it without having to run it yourself.

Please open issues if you find any bugs or have any suggestions!


### How to use
These steps assume you have the make command installed on your system. If you do not, you can still run the commands in the Makefile manually.
#### Development
Requirements:
- Node.js (for npx)
- Make (optional)

Steps:
1. Clone the repository
2. Copy the `.env.example` file to `.env` and fill in the values
2. Run `make setup` to install poetry and dependencies
3. Run `make dev` to start the development server
#### Production
This project uses Docker to build and run the production server. You can start an example server by running `make start` in the project directory.
Requirements:
- Docker
- Make (optional)

Steps:
1. Clone the repository
2. Copy the `.env.example` file to `.env` and fill in the values
3. Run `start` to build and start the production server
