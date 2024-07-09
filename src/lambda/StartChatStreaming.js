const { v4: uuidv4 } = require('uuid');
const { ConnectClient, StartContactStreamingCommand } = require("@aws-sdk/client-connect");

exports.handler = async (event) => {
    try {
        // Extract relevant information from the event object
        const contactData = event.Details.ContactData;
        //const StreamingEndpointArn = contactData.MediaStreams.Customer.Audio.StreamARN;
        const ContactId = contactData.ContactId;
        const InstanceARN = contactData.InstanceARN;
        const ClientToken = uuidv4(); // Generate a unique client token

        console.log("Starting chat streaming");
        console.log(event);
        console.log(contactData.MediaStreams);

        // Validate extracted data
        if (!ContactId || !InstanceARN) {
            console.log("Invalid input, missing fields");
            //if(!StreamingEndpointArn) console.log("Missing StreamingEndpointArn");
            if(!ContactId) console.log("Missing ContactID");
            if(!InstanceARN) console.log("Missing InstanceARN");
            return {
                statusCode: 400,
                body: JSON.stringify({ message: 'Missing required parameters in the event object' }),
            };
        }

        // Extract InstanceId from InstanceARN
        const InstanceId = InstanceARN.split('/').pop();

        const input = { // StartContactStreamingRequest
          InstanceId: InstanceId, // required
          ContactId: ContactId, // required
          ChatStreamingConfiguration: { // ChatStreamingConfiguration
            StreamingEndpointArn: 'arn:aws:sns:ap-southeast-2:855990150714:chat-sns-topic', // required
          },
          ClientToken: ClientToken, // required
        };

        console.log("Sending start streaming command");
        console.log(input);
        
        const command = new StartContactStreamingCommand(input);
        const client = new ConnectClient();
        const response = await client.send(command);

        console.log("Sent start streaming command");
        console.log(response);

        return {
            statusCode: 200,
            body: JSON.stringify(response),
        };
    } catch (error) {
        console.error('Error initiating chat stream:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ message: 'Failed to start contact streaming', error }),
        };
    }
};
