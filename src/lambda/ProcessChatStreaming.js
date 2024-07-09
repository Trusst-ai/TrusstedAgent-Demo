const chatService = require('../utils/ChatService');

exports.handler = async (event) => {
    console.log(event)
    for (const record of event.Records) {
        try {
            console.log(record.body);
            await chatService.processMessage(record.body);
        } catch(error) {
            console.log(error);
            console.error("Failed to process event");
        }
    }

    return {
        statusCode: 200,
        body: JSON.stringify('Messages processed successfully!')
    };
};
