const { REST, Routes, ActivityType, Events } = require('discord.js');
const logger = require('../utils/logger');
const config = require('../config');

module.exports = {
    name: Events.ClientReady,
    once: true,
    async execute(client) {
        logger.success(`Logged in as ${client.user.tag} (${client.user.id})`);

        // Register slash commands
        const commands = [];
        client.commands.forEach(cmd => {
            if (cmd.data) {
                commands.push(cmd.data.toJSON());
            }
        });

        const rest = new REST({ version: '10' }).setToken(config.token);

        try {
            logger.info(`Started refreshing ${commands.length} application (/) commands.`);

            const data = await rest.put(
                Routes.applicationCommands(client.user.id),
                { body: commands }
            );

            logger.success(`Successfully reloaded ${data.length} application (/) commands globally.`);
        } catch (error) {
            logger.error('Failed to reload application (/) commands:', error);
        }

        // Set rich activity presence
        const updatePresence = () => {
            const serverCount = client.guilds.cache.size;
            client.user.setPresence({
                activities: [{
                    name: `over ${serverCount} server${serverCount === 1 ? '' : 's'} | /help`,
                    type: ActivityType.Watching
                }],
                status: 'online'
            });
        };

        updatePresence();
        setInterval(updatePresence, 10 * 60 * 1000); // refresh every 10 mins
    }
};
