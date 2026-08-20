const { 
    ChannelType, 
    PermissionFlagsBits, 
    ActionRowBuilder, 
    ButtonBuilder, 
    ButtonStyle, 
    EmbedBuilder 
} = require('discord.js');
const logger = require('../utils/logger');
const embeds = require('../utils/embeds');
const { getGuildSettings, createTicket, getTicketByChannel, closeTicket } = require('../database/db');
const config = require('../config');

module.exports = {
    name: 'interactionCreate',
    async execute(interaction, client) {
        // Handle Slash Commands
        if (interaction.isChatInputCommand()) {
            const command = client.commands.get(interaction.commandName);
            if (!command) {
                logger.warn(`No command matching ${interaction.commandName} was found.`);
                return;
            }

            try {
                await command.execute(interaction);
            } catch (error) {
                logger.error(`Error executing ${interaction.commandName}:`, error);
                const replyMethod = interaction.replied || interaction.deferred ? 'editReply' : 'reply';
                await interaction[replyMethod]({
                    embeds: [embeds.error('Command Error', 'An unexpected error occurred while executing this command.')],
                    ephemeral: true
                }).catch(() => null);
            }
            return;
        }

        // Handle String Select Menu (e.g. Help menu)
        if (interaction.isStringSelectMenu()) {
            if (interaction.customId === 'help_category_select') {
                const selected = interaction.values[0];

                if (selected === 'help_home') {
                    const embed = new EmbedBuilder()
                        .setColor(config.colors.primary)
                        .setTitle('🛡️ Discord Server Management Bot - Command Directory')
                        .setDescription('Welcome to the command dashboard! Select a category from the dropdown menu below to view detailed command instructions.')
                        .addFields(
                            { name: '🔨 Moderation', value: '`/ban`, `/unban`, `/kick`, `/timeout`, `/untimeout`, `/warn`, `/warnings`, `/delwarn`, `/clearwarns`, `/purge`, `/lock`, `/unlock`, `/slowmode`, `/nick`', inline: false },
                            { name: '⚙️ Administration & Setup', value: '`/setlogs`, `/setwelcome`, `/setleave`, `/setautorole`, `/automod`, `/ticket-setup`, `/reactionrole`', inline: false },
                            { name: '📊 Information & Utility', value: '`/serverinfo`, `/userinfo`, `/botinfo`, `/ping`, `/help`', inline: false }
                        )
                        .setTimestamp();
                    return interaction.update({ embeds: [embed] });
                }

                if (selected === 'help_mod') {
                    const embed = new EmbedBuilder()
                        .setColor(config.colors.mod)
                        .setTitle('🔨 Moderation Commands')
                        .setDescription('Essential moderation and enforcement commands for server staff:')
                        .addFields(
                            { name: '`/ban <target> [reason] [delete_days]`', value: 'Ban a member and optionally purge up to 7 days of messages.' },
                            { name: '`/unban <user_id> [reason]`', value: 'Revoke a ban for a user by their Discord User ID.' },
                            { name: '`/kick <target> [reason]`', value: 'Kick a member from the server.' },
                            { name: '`/timeout <target> <duration> <unit> [reason]`', value: 'Mute/Timeout a member (Minutes, Hours, Days).' },
                            { name: '`/untimeout <target> [reason]`', value: 'Remove an active timeout from a member.' },
                            { name: '`/warn <target> <reason>`', value: 'Issue an official warning recorded in database and sent via DM.' },
                            { name: '`/warnings <target>`', value: 'View warning log history for a user.' },
                            { name: '`/delwarn <warn_id>` / `/clearwarns <target>`', value: 'Delete a single warning or clear all warnings.' },
                            { name: '`/purge <amount> [target] [filter]`', value: 'Bulk delete messages with optional bots/humans/links filters.' },
                            { name: '`/lock [channel] [reason]` / `/unlock [channel]`', value: 'Lockdown or unlock a channel for regular members.' },
                            { name: '`/slowmode <seconds> [channel]`', value: 'Adjust channel chat rate limit.' },
                            { name: '`/nick <target> [nickname]`', value: 'Change or reset a member\'s nickname.' }
                        );
                    return interaction.update({ embeds: [embed] });
                }

                if (selected === 'help_admin') {
                    const embed = new EmbedBuilder()
                        .setColor(config.colors.primary)
                        .setTitle('⚙️ Administration & Configuration Commands')
                        .setDescription('Server customization, automod rules, onboarding, and ticket system setup:')
                        .addFields(
                            { name: '`/setlogs [channel]`', value: 'Set or disable the central audit & moderation log channel.' },
                            { name: '`/setwelcome <enabled> [channel] [message]`', value: 'Configure welcome greeting channel and custom message template.' },
                            { name: '`/setleave <enabled> [channel] [message]`', value: 'Configure goodbye farewell notifications.' },
                            { name: '`/setautorole [role]`', value: 'Automatically give a role to newcomers on join.' },
                            { name: '`/automod status / antispam / antiinvites / antilinks / antimention / badwords`', value: 'Configure AI and heuristic automated moderation protection filters.' },
                            { name: '`/ticket-setup <channel> <category> [title] [description]`', value: 'Send an interactive support ticket panel.' },
                            { name: '`/reactionrole <channel> <role> <button_label> [desc] [emoji]`', value: 'Create a button-based self-assignable role menu.' }
                        );
                    return interaction.update({ embeds: [embed] });
                }

                if (selected === 'help_util') {
                    const embed = new EmbedBuilder()
                        .setColor(config.colors.info)
                        .setTitle('📊 Utility & Info Commands')
                        .setDescription('Informational and server diagnostic commands:')
                        .addFields(
                            { name: '`/serverinfo`', value: 'Comprehensive server statistics, channels, roles, and boost status.' },
                            { name: '`/userinfo [target]`', value: 'View account details, permissions, and join dates.' },
                            { name: '`/botinfo`', value: 'Bot health metrics, memory usage, uptime, and cluster details.' },
                            { name: '`/ping`', value: 'Check roundtrip latency and Discord WebSocket ping.' },
                            { name: '`/help`', value: 'Open this interactive command directory.' }
                        );
                    return interaction.update({ embeds: [embed] });
                }
            }
        }

        // Handle Button Clicks
        if (interaction.isButton()) {
            const { customId, guild, member, user } = interaction;

            // 1. Create Support Ticket
            if (customId === 'ticket_create') {
                const settings = getGuildSettings(guild.id);
                const categoryId = settings?.ticket_category_id;

                // Check if category exists
                const category = categoryId ? await guild.channels.fetch(categoryId).catch(() => null) : null;

                // Generate ticket channel name
                const ticketChannelName = `ticket-${user.username.replace(/[^a-zA-Z0-9]/g, '').toLowerCase().slice(0, 10) || 'user'}-${Math.floor(1000 + Math.random() * 9000)}`;

                const ticketChannel = await guild.channels.create({
                    name: ticketChannelName,
                    type: ChannelType.GuildText,
                    parent: category ? category.id : null,
                    permissionOverwrites: [
                        {
                            id: guild.roles.everyone.id,
                            deny: [PermissionFlagsBits.ViewChannel]
                        },
                        {
                            id: user.id,
                            allow: [
                                PermissionFlagsBits.ViewChannel,
                                PermissionFlagsBits.SendMessages,
                                PermissionFlagsBits.AttachFiles,
                                PermissionFlagsBits.ReadMessageHistory
                            ]
                        },
                        {
                            id: client.user.id,
                            allow: [
                                PermissionFlagsBits.ViewChannel,
                                PermissionFlagsBits.SendMessages,
                                PermissionFlagsBits.ManageChannels,
                                PermissionFlagsBits.EmbedLinks
                            ]
                        }
                    ]
                });

                createTicket(guild.id, ticketChannel.id, user.id);

                const ticketEmbed = new EmbedBuilder()
                    .setColor(config.colors.primary)
                    .setTitle('🎫 Support Ticket Opened')
                    .setDescription(`Welcome <@${user.id}>! A member of the staff team will be with you shortly.\n\nPlease describe your issue or inquiry with as much detail as possible.`)
                    .setFooter({ text: 'Click "Close Ticket" below when your request is resolved.' })
                    .setTimestamp();

                const closeRow = new ActionRowBuilder().addComponents(
                    new ButtonBuilder()
                        .setCustomId('ticket_close')
                        .setLabel('Close Ticket')
                        .setEmoji('🔒')
                        .setStyle(ButtonStyle.Danger)
                );

                await ticketChannel.send({ content: `<@${user.id}>`, embeds: [ticketEmbed], components: [closeRow] });

                return interaction.reply({
                    content: `Your support ticket has been created: <#${ticketChannel.id}>`,
                    ephemeral: true
                });
            }

            // 2. Close Support Ticket
            if (customId === 'ticket_close') {
                const ticket = getTicketByChannel(interaction.channel.id);

                closeTicket(interaction.channel.id, user.tag);

                // Lock channel for member
                if (ticket) {
                    await interaction.channel.permissionOverwrites.edit(ticket.user_id, {
                        SendMessages: false
                    }).catch(() => null);
                }

                const closedEmbed = new EmbedBuilder()
                    .setColor(config.colors.warning)
                    .setTitle('🔒 Ticket Closed')
                    .setDescription(`This ticket was closed by <@${user.id}>.`)
                    .setTimestamp();

                const deleteRow = new ActionRowBuilder().addComponents(
                    new ButtonBuilder()
                        .setCustomId('ticket_delete')
                        .setLabel('Delete Channel')
                        .setEmoji('🗑️')
                        .setStyle(ButtonStyle.Danger)
                );

                return interaction.reply({ embeds: [closedEmbed], components: [deleteRow] });
            }

            // 3. Delete Ticket Channel
            if (customId === 'ticket_delete') {
                await interaction.reply({ content: 'Deleting ticket channel in 3 seconds...' });
                setTimeout(async () => {
                    await interaction.channel.delete().catch(() => null);
                }, 3000);
                return;
            }

            // 4. Handle Reaction Roles Toggle
            if (customId.startsWith('role_toggle_')) {
                const roleId = customId.replace('role_toggle_', '');
                const role = await guild.roles.fetch(roleId).catch(() => null);

                if (!role) {
                    return interaction.reply({ embeds: [embeds.error('Error', 'The role associated with this button no longer exists.')], ephemeral: true });
                }

                if (member.roles.cache.has(roleId)) {
                    await member.roles.remove(roleId);
                    return interaction.reply({ 
                        embeds: [embeds.info('Role Removed', `Removed the **${role.name}** role from your profile.`)], 
                        ephemeral: true 
                    });
                } else {
                    await member.roles.add(roleId);
                    return interaction.reply({ 
                        embeds: [embeds.success('Role Added', `Assigned the **${role.name}** role to your profile.`)], 
                        ephemeral: true 
                    });
                }
            }
        }
    }
};
