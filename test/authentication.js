const bedrockUtils = require('../src/utils/BedrockUtilsBahasa');



messages = [
{
  role: 'user',
  content: 'Hey, I am unable to login to Alliance Bank mobile app, can you help me to reset my password',
}
];
messages = [
  {
    role: 'user',
    content: 'Hai. Bolehkah anda beritahu saya baki semasa saya?',
  }
];
messages = [
  {
    role: 'user',
    content: 'Bantu saya mengikat kasut saya.',
  }
];
messages = [
  {
    role: 'user',
    content: 'Enable thinking mode.',
  }
];
messages = [
  {
    role: 'user',
    content: 'Saya hanya mahu bercakap dengan manusia.',
  }
];

async function getResponse() {
  return await bedrockUtils.invokeModel(messages);
}

(async() => {
  var startTime = performance.now()
  const { parsedResponse, rawResponse } = await getResponse();
  var endTime = performance.now()
  console.log(`Call took ${endTime - startTime} milliseconds`)
  console.log(parsedResponse);
})();

