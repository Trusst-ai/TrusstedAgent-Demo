const dynamoUtils = require('../utils/DynamoUtils');
const bedrockUtils = require('../utils/BedrockUtils');
const { v4: uuidv4 } = require('uuid');
const uuid = require('uuid');

module.exports.processMessage = async (message) => {
    
    const parsedMessage = this.parseMessage(message);
    if( this.isMessageCustomerUtterance(parsedMessage) ) {
        var contactId = parsedMessage.ContactId;
        var transcriptionContext = {
            stopping: false, // Are we stopping?
            transcripts: [],
            metrics: {},
            messages: await dynamoUtils.getAllMessages(contactId),
            contactId: contactId,
        };
        await dynamoUtils.setNextMessage(contactId, 'Processing', 'I am currently processing customer input', 'Thanks I am processing');

        const transcriptItem = {
            contactId: contactId,
            transcriptId: uuid.v4(),
            channel: 'CHAT',
            content: parsedMessage.Content,
            participant: parsedMessage.ParticipantRole,
            startOffset: 0,
            endOffset: 0,
        };
        
        console.info(`Made transcript: ${JSON.stringify(transcriptItem, null, 2)}`);
        
        await dynamoUtils.createTranscriptItem(transcriptItem);
        
        transcriptionContext.messages.push({
            role: 'user',
            content: parsedMessage.Content,
        });
        
        const { parsedResponse, rawResponse } = await bedrockUtils.invokeModel(transcriptionContext.messages);
        const saveMessage = await this.handleModelResponse(contactId, parsedResponse);
        
        if (saveMessage)
        {
            await dynamoUtils.createMessage(contactId, 'user', parsedMessage.Content);
            await dynamoUtils.createMessage(contactId, 'assistant', rawResponse);
        }
        
        transcriptionContext.transcripts.push(transcriptItem);
        transcriptionContext.stopping = true;
    }
    else {
        console.log('Message is not a Customer Utterance, skipping');
    }
};

module.exports.handleModelResponse = async (contactId, parsedResponse) => {
  try
  {
    const tool = parsedResponse.Response?.Action.Tool;
    const thought = parsedResponse.Response?.Thought;
    const message = parsedResponse.Response?.Action.Argument;
    var saveMessage = true;

    switch (tool)
    {
      case 'ThinkingMode':
      case 'Angry':
      case 'Fallback':
      {
        saveMessage = false;
        break;
      }
    }

    await dynamoUtils.setNextMessage(contactId, tool, thought, message);

    return saveMessage;
  }
  catch (error)
  {
    console.error('Failed to handle model response', error);
    throw error;
  }
}

module.exports.parseMessage = (body) => {
    const noSlash = body.replace(/\\/g, "");
    const noQuoteBeforeBracket = noSlash.replace(/\"{/g,"{");
    const noQuoteAfterBracket = noQuoteBeforeBracket.replace(/}\"/g,"}");
    const parsedBody = JSON.parse(noQuoteAfterBracket);
    return parsedBody.Message;
}

module.exports.isMessageCustomerUtterance = (message) => {
    if( message.Type == "MESSAGE" && message.ParticipantRole == "CUSTOMER" ) {
        return true;
    }
    else {
        return false;
    }
}