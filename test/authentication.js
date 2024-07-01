const bedrockUtils = require('../src/utils/BedrockUtils');



messages = [
{
  role: 'user',
  content: 'Hey, I am unable to login to Alliance Bank mobile app, can you help me to reset my password',
}
];

async function getResponse() {
  return await bedrockUtils.invokeModel(messages);
}

(async() => {
  const { parsedResponse, rawResponse } = await getResponse();
  console.log(parsedResponse);
})();

