FROM node:12.2.0-alpine


COPY . ./front_end

WORKDIR ./front_end

RUN npm install --silent
RUN npm install react-scripts@3.0.1 -g --silent

# add `/app/node_modules/.bin` to $PATH
ENV PATH /front_end/node_modules/.bin:$PATH

# start app
CMD ["npm", "start"]