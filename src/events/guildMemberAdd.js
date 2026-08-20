const { EmbedBuilder } = require('discord.js');
const { getGuildSettings } = require('../database/db');
const logger = require('../utils/logger');
const embeds = require('../utils/embeds');
const { logModAction } = require('../utils/modLogger');
const config = require('../config');

module.exports = {
    name: 'guildMemberAdd',
    async execute(member) {
        const { guild } = member;
        const settings = getGuildSettings(guild.id);
        if (!settings) return;

        // 1. Send Welcome Message
        if (settings.welcome_enabled && settings.welcome_channel) {
            const channel = await guild.channels.fetch(settings.welcome_channel).catch(() => null);
            if (channel && channel.isTextBased()) {
                const rawTemplate = settings.welcome_message || 'Welcome to {server}, {user}!';
                const formattedMsg = rawTemplate
                    .replace(/\{user\}/g, `<@${member.id}>`)
                    .replace(/\{username\}/g, member.user.username)
                    .replace(/\{server\}/g, guild.name)
                    .replace(/\{memberCount\}/g, guild.memberCount.toString());

                const welcomeEmbed = new EmbedBuilder()
                    .setColor(config.colors.success)
                    .setTitle(`👋 Welcome to ${guild.name}!`)
                    .setDescription(formattedMsg)
                    .setThumbnail(member.user.displayAvatarURL({ dynamic: true, size: 256 }))
                    .setFooter({ text: `Member #${guild.memberCount}` })
                    .setTimestamp();

                await channel.send({ embeds: [welcomeEmbed] }).catch(err => {
                    logger.error('Failed to send welcome message:', err);
                });
            }
        }

        // 2. Assign Auto-Role
        if (settings.autorole_id) {
            const role = await guild.roles.fetch(settings.autorole_id).catch(() => null);
            if (role) {
                await member.roles.add(role).catch(err => {
                    logger.error(`Failed to assign auto-role ${settings.autorole_id} to ${member.user.tag}:`, err);
                });
            }
        }

        // 3. Log to Mod Channel
        const accountCreatedTimestamp = Math.floor(member.user.createdTimestamp / 1000);
        const modEmbed = embeds.modAction({
            action: 'Member Joined',
            target: member.user,
            moderator: 'Gateway Event',
            reason: 'User joined the server',
            extra: {
                'Account Created': `<t:${accountCreatedTimestamp}:R>`,
                'Total Members': guild.memberCount
            }
        });

        await logModAction(guild, modEmbed);
    }
};
