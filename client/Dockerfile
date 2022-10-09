from yarnpkg/node-yarn as client
WORKDIR /app
COPY . .
RUN yarn install
EXPOSE 3000
CMD ["yarn", "start"]
