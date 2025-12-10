import axios from "axios";
import {faker}  from "@faker-js/faker";

async function loadSwagger() {
  const url = "https://petstore.swagger.io/v2/swagger.json";
  const res = await axios.get(url);
  return res.data;
}

// Gera valores baseados nos tipos do Swagger
function generateValue(schema) {
  if (!schema) return faker.lorem.word();

  switch (schema.type) {
    case "string":
      return faker.lorem.words();
    case "integer":
      return faker.datatype.number({ min: 1, max: 9999 });
    case "number":
      return faker.datatype.float();
    case "boolean":
      return faker.datatype.boolean();
    case "array":
      return [generateValue(schema.items)];
    case "object":
      const obj = {};
      if (schema.properties) {
        for (let p in schema.properties) {
          obj[p] = generateValue(schema.properties[p]);
        }
      }
      return obj;
    default:
      return faker.lorem.word();
  }
}

async function fuzzEndpoint(method, url, parameters) {
  const baseUrl = "https://petstore.swagger.io/v2" + url;

  let query = {};
  let body = {};

  if (parameters) {
    parameters.forEach((param) => {
      if (param.in === "query") {
        query[param.name] = generateValue(param.schema || param);
      } else if (param.in === "body" || param.in === "formData") {
        body = generateValue(param.schema);
      } else if (param.in === "path") {
        // substitui parâmetro no path
        url = url.replace(`{${param.name}}`, generateValue(param.schema));
      }
    });
  }

  const fullUrl = baseUrl.replace(url, url);

  try {
    const res = await axios({
      method,
      url: fullUrl,
      params: query,
      data: Object.keys(body).length ? body : undefined,
    });

    console.log(`✔️ [${method.toUpperCase()}] ${fullUrl} -> ${res.status}`);
  } catch (err) {
    console.error(
      `❌ [${method.toUpperCase()}] ${fullUrl} -> ERROR: ${
        err.response?.status || err.message
      }`
    );
  }
}

async function main() {
  const swagger = await loadSwagger();
  const paths = swagger.paths;

  console.log("Iniciando Fuzzing na Petstore...");

  for (let path in paths) {
    const methods = paths[path];

    for (let method in methods) {
      const endpoint = methods[method];
      const parameters = endpoint.parameters || [];

      await fuzzEndpoint(method, path, parameters);
    }
  }

  console.log("✔️ Fuzzing concluído.");
}

main();
