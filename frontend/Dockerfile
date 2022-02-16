# Pull latest official node image
FROM node:latest

# Expose ports
EXPOSE 3000

# Set working directory
WORKDIR /app

# Add /app/node_modules/.bin to environment variables
ENV PATH /app/node_modules/.bin:$PATH

# Copy package files and install app dependencies
COPY package.json /app/package.json
COPY yarn.lock /app/yarn.lock
RUN yarn install
RUN yarn add react-scripts
RUN yarn add react-multi-select-component
RUN yarn add @material-ui/core
RUN yarn add @material-ui/icons
RUN yarn add @material-ui/lab
RUN yarn add axios

# Add React app to working directory
ADD . /app

# Start the React app
CMD ["yarn", "start"]
