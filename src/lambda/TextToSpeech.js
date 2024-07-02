module.exports.handler = async (event) => {
  const url = event.URL;
  const text = event.Text;

  await callEc2TextToSpeech(url, text);
}

const callEc2TextToSpeech = async (url, text) => {
  try {
    console.log(`Calling URL ${url} for text ${text}`);

    const res = await fetch(url, {
      body: JSON.stringify({ text: text }),
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    console.log('Status Code:', res.status);
  } catch (err) {
    console.error(err);
  }
}
