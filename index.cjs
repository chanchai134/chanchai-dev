const { readFile } = require("node:fs/promises");
const { join } = require("node:path");

exports.handler = async () => {
  const body = await readFile(join(__dirname, "chanchai.html"), "utf8");

  return {
    statusCode: 200,
    headers: {
      "Content-Type": "text/html; charset=utf-8",
    },
    body,
  };
};
