const { createReadStream } = require("node:fs");
const { join } = require("node:path");
const { pipeline } = require("node:stream/promises");

exports.handler = awslambda.streamifyResponse(async (event, responseStream, context) => {
  responseStream = awslambda.HttpResponseStream.from(responseStream, {
    statusCode: 200,
    headers: {
      "Content-Type": "text/html; charset=utf-8",
    },
  });

  await pipeline(
    createReadStream(join(__dirname, "chanchai.html")),
    responseStream,
  );
});
