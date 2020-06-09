# MakeMeGreen is a chat bot that educates people about reducing enviromental footprint, tracks their green activivities

MakeMeGreen is a chat bot built for Alexa that inspires and educates people to take personal actions against climate change, keeps track of their green actions over time and offers them completely customized service.

It offers the following features:
- Hundreds of green opportunities for reduction of plastic, paper and water consumption (more to come). Example: Prefer dishwashing over hand-washing saves ~ 24 gallons of water per wash and gives you 28 green points per week.
- The bot offers and keeps track of green points for each action taken that accrue over time. One green point is approximately equivalent of 0.012 grams of CO2E.
- The bot is smart enough to detect voice vs text-based invocations and offers 3 levels of personalization:
	- Completely anonymous: If the bot is invoked through Lex test UI, there is no user-identifying information sent to the bot. It still offes green opportunities but it can't track them over time.
	- Anonymous but personalized: If the bot is invoked through Slack or Alexa, it gets a unique user id for the user but has no contact information like email or phone number. It still keeps track of green actions and points over time.
	- Personalized: If the user is willing to give email address or phone number, it can track your green points and email you periodic progress and motivational reports should you choose.
- You can check your green profile at any time to find out how many green points you have accumulated over any time period and the green opportunities you have implemented.

- Gamification with Green challenges: You can organize a green challenge at Cvent (Example: Plastic-free August) and let the bot track people's green actions and points and give away awards.

- Green product ratings: You can ask the bot for product recommendations. For example, the bot would Seventh Generation cleaning products which have a significantly lesser impact on the environment over equivalent Dawn products.

We hope to release MakeMeGreen as a free Alexa skill for everyone in the US to use and benefit from.

MakeMeGreen is an open-source project whose source code is maintained at: https://github.com/sabarivasan/makemegreen

I hope you consider MakeMeGreen for the AWS awards and help offset some of the cloud costs we incur for hosting it on AWS.

AWS Tech used: Lex, Alexa, Lambda, DynamoDB

The following is a pictorial description of what we built for the hackathon and what we plan to build in the future:
https://github.com/sabarivasan/makemegreen/blob/master/Green%20companion%20chatbot.png


