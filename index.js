const { Client, Intents } = require('discord.js');
const token = require('./token');
const client = new Client({ intents: [Intents.FLAGS.GUILDS] });

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

client.on('interactionCreate', async interaction => {
  if (!interaction.isCommand()) return;

  if (interaction.commandName === 'sena') {
    await interaction.reply('fat and gay');
  }
});

client.on('message', msg => {
  if (msg.content === 'sena') {
    msg.reply('fat and gay');
  }
});

client.login(token);